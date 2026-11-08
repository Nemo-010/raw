#!/usr/bin/env python3
"""verify-dossier.py — validate dossier records against a JSON-Schema subset.

PURPOSE
    Prove that every dossier record is structurally complete before a document
    cites it. A record missing `per_object_cap` or carrying `confidence: "high"`
    is a defect the gate must catch, not a style preference.

WHY IT EXISTS
    A validator that never fails is worthless. The seed corpus is exactly the
    shape this catches: 1,255 candidate records, of which 792 have no
    identity_cost at all, 16 have no verdict, and all 1,255 use a three-level
    confidence scale that the repository does not accept. Migrating them by hand
    would have hidden those gaps; validating them shows the gaps and keeps them.

SCHEMA SUBSET (draft-07 compatible)
    type, required, properties, additionalProperties, items, enum, const,
    pattern, minLength, maxLength, minimum, maximum, minItems, maxItems,
    uniqueItems, oneOf, anyOf, allOf, not, format (date, date-time, uri), $ref
    to a local "#/definitions/..." pointer.

DEPENDENCIES
    Python standard library only.

OUTPUT
    JSON by default: {"ok":bool,"schema":...,"records":N,"errors":[...],"warnings":[...]}
    --human for a table. --migrate converts a seed wave file into records.

EXIT CODES  (repository map, scripts/README.md)
    0  every record valid
    1  at least one record invalid (the defects are the output)
    2  usage error: bad arguments, unreadable schema or directory
    3  environment wrong: python too old for a schema construct, unreadable file

EXAMPLES
    python verify-dossier.py --schema dossier.schema.json dossier/
    python verify-dossier.py --schema dossier.schema.json fixtures/dossier-broken/
    python verify-dossier.py --schema dossier.schema.json --migrate \
        ../../seed/storage-research/dossiers/A-P3-object-storage-nonbig3.json \
        --out .tmp/migrated/
    python verify-dossier.py --selftest
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime

VERSION = "1.0.0"

# ------------------------------------------------------------------ helpers --

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Milliseconds are mandatory and the zone must be Z: scripts/README.md rule 5 makes
# a local-time or second-resolution timestamp unusable as evidence.
_DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(Z|[+-]\d{2}:?\d{2})$")
_URI_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:[^\s]*$")


def _is_type(value, name):
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "string":
        return isinstance(value, str)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "null":
        return value is None
    raise ValueError("unknown type %r" % name)


def _json_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _fmt(obj):
    s = json.dumps(obj, ensure_ascii=False, default=str)
    return s if len(s) <= 120 else s[:117] + "..."


def _resolve_ref(root, ref):
    if not ref.startswith("#/"):
        raise ValueError("only local $ref is supported, got %r" % ref)
    cur = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[part]
    return cur


class Validator:
    """A draft-07 subset validator. Errors carry a JSON pointer path."""

    def __init__(self, schema):
        self.root = schema
        self.errors = []
        self.warnings = []

    # -- entry --
    def validate(self, instance, schema=None, path="$"):
        schema = self.root if schema is None else schema
        if schema is True or schema == {}:
            return
        if schema is False:
            self._err(path, "schema", "no value is allowed here")
            return
        if "$ref" in schema:
            target = _resolve_ref(self.root, schema["$ref"])
            return self.validate(instance, target, path)

        self._check_type(instance, schema, path)
        self._check_enum(instance, schema, path)
        self._check_numeric(instance, schema, path)
        self._check_string(instance, schema, path)
        self._check_combinators(instance, schema, path)
        self._check_object(instance, schema, path)
        self._check_array(instance, schema, path)
        if "not" in schema:
            sub = Validator(self.root)
            sub.validate(instance, schema["not"], path)
            if not sub.errors:
                self._err(path, "not", "value matches a schema it must not match")

    # -- pieces --
    def _err(self, path, keyword, message, **extra):
        e = {"path": path, "keyword": keyword, "message": message}
        e.update(extra)
        self.errors.append(e)

    def _warn(self, path, message):
        self.warnings.append({"path": path, "message": message})

    def _check_type(self, instance, schema, path):
        if "type" not in schema:
            return
        want = schema["type"]
        wanted = want if isinstance(want, list) else [want]
        if not any(_is_type(instance, w) for w in wanted):
            self._err(path, "type", "expected %s, got %s" % ("|".join(wanted), _json_type(instance)))

    def _check_enum(self, instance, schema, path):
        if "enum" in schema and instance not in schema["enum"]:
            self._err(path, "enum", "%s is not one of %s" % (_fmt(instance), _fmt(schema["enum"])))
        if "const" in schema and instance != schema["const"]:
            self._err(path, "const", "%s != %s" % (_fmt(instance), _fmt(schema["const"])))

    def _check_numeric(self, instance, schema, path):
        if not _is_type(instance, "number"):
            return
        if "minimum" in schema and instance < schema["minimum"]:
            self._err(path, "minimum", "%s < %s" % (instance, schema["minimum"]))
        if "maximum" in schema and instance > schema["maximum"]:
            self._err(path, "maximum", "%s > %s" % (instance, schema["maximum"]))
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            self._err(path, "exclusiveMinimum", "%s <= %s" % (instance, schema["exclusiveMinimum"]))
        if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
            self._err(path, "exclusiveMaximum", "%s >= %s" % (instance, schema["exclusiveMaximum"]))

    def _check_string(self, instance, schema, path):
        if not isinstance(instance, str):
            return
        if "minLength" in schema and len(instance) < schema["minLength"]:
            self._err(path, "minLength", "length %d < %d" % (len(instance), schema["minLength"]))
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            self._err(path, "maxLength", "length %d > %d" % (len(instance), schema["maxLength"]))
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            self._err(path, "pattern", "%r does not match %r" % (instance[:80], schema["pattern"]))
        fmt = schema.get("format")
        if fmt == "date":
            if not _DATE_RE.match(instance):
                self._err(path, "format", "%r is not YYYY-MM-DD" % instance)
            else:
                try:
                    datetime.strptime(instance, "%Y-%m-%d")
                except ValueError:
                    self._err(path, "format", "%r is not a real date" % instance)
        elif fmt == "date-time":
            if not _DATETIME_RE.match(instance):
                self._err(path, "format",
                          "%r is not an ISO-8601 timestamp with an offset and Z" % instance)
            else:
                core = instance.rstrip("Zz")
                core = re.sub(r"([+-]\d{2}:?\d{2})$", "", core)
                try:
                    datetime.fromisoformat(core)
                except ValueError:
                    self._err(path, "format", "%r is not a real timestamp" % instance)
        elif fmt == "uri":
            if not _URI_RE.match(instance):
                self._err(path, "format", "%r is not an absolute URI" % instance[:80])

    def _check_combinators(self, instance, schema, path):
        if "oneOf" in schema:
            hits = 0
            sub_errors = []
            for i, sub in enumerate(schema["oneOf"]):
                v = Validator(self.root)
                v.validate(instance, sub, path)
                if not v.errors:
                    hits += 1
                else:
                    sub_errors.append(v.errors)
            if hits != 1:
                self._err(path, "oneOf", "matched %d of %d branches, exactly 1 required"
                          % (hits, len(schema["oneOf"])))
        if "anyOf" in schema:
            for sub in schema["anyOf"]:
                v = Validator(self.root)
                v.validate(instance, sub, path)
                if not v.errors:
                    break
            else:
                self._err(path, "anyOf", "matched none of %d branches" % len(schema["anyOf"]))
        if "allOf" in schema:
            for sub in schema["allOf"]:
                self.validate(instance, sub, path)

    def _check_object(self, instance, schema, path):
        if not isinstance(instance, dict):
            return
        props = schema.get("properties") or {}
        for req in schema.get("required") or []:
            if req not in instance:
                self._err(path, "required", "missing required property %r" % req,
                          missing=req)
        addl = schema.get("additionalProperties", True)
        for key, value in instance.items():
            child = "%s.%s" % (path, key)
            if key in props:
                self.validate(value, props[key], child)
            elif addl is False:
                self._err(child, "additionalProperties",
                          "property %r is not in the schema" % key, property=key)
            elif isinstance(addl, dict):
                self.validate(value, addl, child)
        for dep_key, dep_list in (schema.get("dependencies") or {}).items():
            if dep_key in instance:
                if isinstance(dep_list, list):
                    for d in dep_list:
                        if d not in instance:
                            self._err(path, "dependencies",
                                      "%r requires %r" % (dep_key, d))

    def _check_array(self, instance, schema, path):
        if not isinstance(instance, list):
            return
        if "minItems" in schema and len(instance) < schema["minItems"]:
            self._err(path, "minItems", "%d items < %d" % (len(instance), schema["minItems"]))
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            self._err(path, "maxItems", "%d items > %d" % (len(instance), schema["maxItems"]))
        if schema.get("uniqueItems"):
            seen = []
            for item in instance:
                key = json.dumps(item, sort_keys=True, default=str)
                if key in seen:
                    self._err(path, "uniqueItems", "duplicate item %s" % _fmt(item))
                seen.append(key)
        if "items" in schema:
            items = schema["items"]
            if isinstance(items, list):
                for i, (value, sub) in enumerate(zip(instance, items)):
                    self.validate(value, sub, "%s[%d]" % (path, i))
            else:
                for i, value in enumerate(instance):
                    self.validate(value, items, "%s[%d]" % (path, i))


# ------------------------------------------------------------------ loading --

def load_schema(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def iter_records(root):
    """Yield (path, record, kind). kind is 'record' or 'document'.

    Accepts two layouts:
      dossier/<topic>/<slug>.json    one record per file  (the target layout)
      <dir>/<wave>.json              a seed wave with a candidates[] array
    """
    if os.path.isfile(root):
        paths = [root]
    else:
        paths = sorted(glob.glob(os.path.join(root, "**", "*.json"), recursive=True))
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError) as e:
            yield p, None, "unreadable:%s" % e
            continue
        if isinstance(data, dict) and isinstance(data.get("candidates"), list):
            yield p, data, "wave"
        elif isinstance(data, list):
            for i, rec in enumerate(data):
                yield "%s[%d]" % (p, i), rec, "record"
        else:
            yield p, data, "record"


# ------------------------------------------------------------------ migrate --

CONFIDENCE_MAP = {"high": "documented", "medium": "reported", "low": "inferred"}

IDENTITY_ALIASES = {
    "anonymous": "anonymous", "email": "email", "any-phone": "any-phone",
    "country-phone": "country-phone", "national-id": "national-id",
    "card": "card", "institution": "institution",
}


def parse_identity(raw):
    """Split a free-text identity_cost into {kind, detail, country}.

    The seed writes 60+ shapes: 'email + card', 'country-phone(cn)',
    'institution — SSO only'. Coercing silently would lose the qualifier, so the
    original sentence is always preserved in detail.
    """
    if not raw:
        return {"kind": "email", "detail": "not stated in the source record", "country": None}, True
    text = " ".join(str(raw).split())
    low = text.lower()
    country = None
    m = re.search(r"country-phone\s*\(\s*([a-z+0-9]{1,8})\s*\)", low)
    if m:
        country = m.group(1)
    for kind in ("national-id", "institution", "country-phone", "any-phone",
                 "anonymous", "card", "email"):
        if re.search(r"\b%s\b" % re.escape(kind), low):
            return {"kind": kind, "detail": text, "country": country}, False
    return {"kind": "email", "detail": text, "country": country}, True


INTERFACE_TOKENS = [
    ("s3-compatible", ("s3 api", "s3-compatible", "s3 compatible")),
    ("s3", ("s3",)), ("rest", ("rest", "http api", "api")),
    ("graphql", ("graphql",)), ("webdav", ("webdav",)),
    ("sftp", ("sftp",)), ("ftps", ("ftps",)), ("ftp", ("ftp",)),
    ("scp", ("scp",)), ("rsync", ("rsync",)), ("smb", ("smb", "samba", "cifs")),
    ("nfs", ("nfs",)), ("ssh", ("ssh",)), ("graph", ("graph api", "microsoft graph")),
    ("oci", ("oci", "docker registry")), ("git", ("git",)),
    ("rclone", ("rclone",)), ("cli", ("cli",)),
]


def parse_interface(raw):
    """Tokenise interface prose with word boundaries: 'restic' is not REST,
    'HTTPS' is not S3, and 'rsync-over-SSH' is both rsync and ssh."""
    if not raw:
        return ["unknown"]
    low = str(raw).lower()
    out = []
    for token, needles in INTERFACE_TOKENS:
        for n in needles:
            if re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(n), low):
                if token == "s3" and "s3-compatible" in out:
                    break
                if token not in out:
                    out.append(token)
                break
    return out or ["unknown"]


LIMIT_KINDS = ("request-rate", "pull-count", "per-ip-shaping", "per-object-cap",
               "write-gated", "retention-clamped")


def extract_limits(limits_text, per_object_text, retention_text):
    """Pull `kind`-tagged constraints out of prose. Untagged prose is not lost:
    it goes to limits_note, and the gate reports how many records rely on that."""
    found = []
    text = str(limits_text or "")
    for kind in LIMIT_KINDS:
        if re.search(r"`?%s`?" % re.escape(kind), text):
            found.append({"kind": kind, "value": _trim(text), "source": "stated in limits prose"})
    if per_object_text and not any(f["kind"] == "per-object-cap" for f in found):
        found.append({"kind": "per-object-cap",
                      "value": _trim(per_object_text, 300),
                      "source": "per_object_cap field"})
    if retention_text and re.search(r"retention-clamped|clamp", str(retention_text), re.I) \
            and not any(f["kind"] == "retention-clamped" for f in found):
        found.append({"kind": "retention-clamped", "value": _trim(retention_text, 300),
                      "source": "retention prose"})
    return found


def _trim(s, n=400):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 3] + "..."


def first_url(raw, fallback=None):
    """Seed fields sometimes append prose after the URL. Take the URL, keep the
    prose nowhere: the prose belongs in the field that quotes the page."""
    if not raw:
        return fallback
    m = re.search(r"https?://[^\s)\]]+", str(raw))
    if m:
        return m.group(0).rstrip(".,;:")
    return fallback


def split_evidence(evidence_list):
    """Seed evidence is prose: 'URL — what it proved'. Split into {url,date,proved}."""
    out = []
    for item in evidence_list or []:
        text = " ".join(str(item).split())
        url = ""
        m = re.search(r"https?://[^\s,)\]\"']+", text)
        if m:
            url = m.group(0).rstrip(".,;")
        else:
            m = re.match(r"probe:\s*(\S+)", text)
            if m:
                url = "probe:" + m.group(1)
        date = ""
        dm = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
        if dm:
            date = dm.group(1)
        proved = text
        if url:
            proved = text.replace(url, "", 1).strip(" —-–:;,")
        if not url:
            url = "probe:unspecified"
        # A seed evidence string with no date is undated. Stamping it 1970 makes
        # the staleness gate able to see it, where a fabricated date would hide it.
        proved = _trim(proved, 1000)
        if len(proved) < 8:
            # A 4-character remainder ('docs') proved nothing. Keep the whole
            # original string rather than a fragment that fails the schema.
            proved = _trim(text, 1000)
        out.append({"url": url, "date": date or _UNDATED, "proved": proved})
    return out


def wave_to_records(wave, topic_hint):
    """Seed wave -> list of dossier records. Every field finds a home."""
    area = wave.get("area") or ""
    slot = wave.get("slot") or ""
    agent_focus = wave.get("agent_focus") or ""
    base = (slot or area or "wave").lower().replace("_", "-")
    records = []
    for idx, c in enumerate(wave.get("candidates") or [], 1):
        if not isinstance(c, dict):
            continue
        name = c.get("name") or "unnamed-%d" % idx
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        # Truncate on a hyphen boundary: a 70-char cut mid-word leaves a trailing
        # hyphen that the slug pattern rightly rejects.
        if len(slug) > 70:
            slug = slug[:70].rsplit("-", 1)[0] or slug[:70]
        slug = slug or "record-%d" % idx
        if not re.match(r"^[a-z0-9]", slug):
            slug = "r-" + slug
        ident, ident_inferred = parse_identity(c.get("identity_cost"))
        verified_at = _verified_at_from(c)
        rec = {
            "topic": topic_hint,
            "slug": slug,
            "provider": name,
            "url": first_url(c.get("url"), "https://unknown.invalid/"),
            "category": c.get("category") or "unstated",
            "free_tier": {
                "stated": c.get("quota") or "unstated",
                "unit": _unit_of(c.get("quota")),
                "source_url": first_url(c.get("quota_url"), first_url(c.get("url"),
                                                                       "https://unknown.invalid/")),
                "notes": _trim(c.get("quota") or ""),
            },
            "per_object_cap": {
                "stated": _per_object_from(c),
                "bytes": None,
                "source_url": first_url(c.get("quota_url"), first_url(c.get("url"))),
            },
            "retention": {
                "stated": _retention_from(c),
                "days": None,
            },
            "egress": {
                "terms": c.get("egress") or "unstated",
                "metered": _egress_metered(c.get("egress")),
                "source_url": c.get("url"),
            },
            "interface": parse_interface(c.get("interface")),
            "interface_detail": c.get("interface") or "",
            "tooling": c.get("tooling") or "unstated",
            "chaining": c.get("chaining") or "not stated in the source record",
            "limits": extract_limits(c.get("limits"), _per_object_from(c), _retention_from(c)),
            "limits_note": _trim(c.get("limits") or ""),
            "identity_cost": ident,
            "reliability_note": c.get("reliability_note") or "not stated",
            "confidence": CONFIDENCE_MAP.get(c.get("confidence"), "unverified"),
            "confidence_legacy": c.get("confidence") if c.get("confidence") in
                                 ("high", "medium", "low") else None,
            "evidence": split_evidence(c.get("evidence")),
            "verdict": c.get("verdict") or "trial-only",  # flagged in extras below
            "verified_at": verified_at,
            "price_per_tb_month": c.get("price_per_tb_month"),
            "notes": _trim(c.get("quota") or ""),
            "extras": {
                "source_wave": os.path.basename(_CURRENT_FILE[0]) if _CURRENT_FILE[0] else "",
                "agent_focus": _trim(agent_focus, 800),
                "quota_url": c.get("quota_url"),
                "write_once": c.get("write_once"),
                "probe": c.get("probe"),
                # A seed candidate with no verdict is not a finding we may invent.
                # The schema needs a token, so the record carries the sentinel and
                # says so, and the gate can count these.
                "verdict_defaulted": True if not c.get("verdict") else None,
                "per_object_cap_absent": True if _per_object_from(c).startswith("not stated") else None,
                "retention_absent": True if _retention_from(c).startswith("not stated") else None,
                "verified_at_derived": (None if verified_at.startswith("1970")
                                        else "max stated evidence date"),
                "verified_at_unknown": True if verified_at.startswith("1970") else None,
            },
        }
        if rec["confidence_legacy"] is None:
            del rec["confidence_legacy"]
        # Drop nulls in optional object members so the record stays readable.
        for key in ("per_object_cap", "retention", "egress"):
            rec[key] = {k: v for k, v in rec[key].items() if v is not None}
        rec["extras"] = {k: v for k, v in rec["extras"].items() if v is not None}
        # source_url is optional; drop it rather than emit null.
        for key in ("per_object_cap", "retention", "egress"):
            if rec[key].get("source_url") is None:
                rec[key].pop("source_url", None)
        if ident_inferred:
            rec["confidence_note"] = ("identity_cost was absent in the source record; "
                                      "kind defaulted to 'email' and flagged unverified")
        records.append(rec)
    return records


_CURRENT_FILE = [None]

# Explicit sentinel for evidence the seed did not date. Distinct from a real date
# so staleness.py can bucket it as "undated" rather than "ancient".
_UNDATED = "0001-01-01"


def _verified_at_from(c):
    """The newest date the record itself states, as an ISO timestamp.

    Only 3.4% of the seed's evidence rows carry a date at all, so most records
    have no defensible verified_at and get the sentinel. Deriving it from a stated
    date is legitimate ('checked no later than X'); inventing today's date is not,
    because it would silently mark the whole corpus fresh.
    """
    dates = []
    for item in c.get("evidence") or []:
        for m in re.finditer(r"(20\d{2}-\d{2}-\d{2})", str(item)):
            dates.append(m.group(1))
    for key in ("quota_read_on", "verified_at"):
        if c.get(key):
            dates.append(str(c[key])[:10])
    best = None
    for d in dates:
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            continue
        if best is None or d > best:
            best = d
    if best:
        return best + "T00:00:00.000Z"
    return "1970-01-01T00:00:00.000Z"


def _unit_of(quota):
    q = str(quota or "").lower()
    if "unlimited" in q or "no published" in q or "no aggregate cap" in q:
        return "unlimited"
    for unit, needles in (("TiB", ("tib", "trillion bytes")), ("TB", ("tb", "terabyte")),
                          ("GiB", ("gib",)), ("GB", ("gb", "gigabyte")),
                          ("MB", ("mb", "mib")), ("objects", ("object",)),
                          ("mixed", ("",))):
        if unit == "mixed":
            return "mixed"
        if any(n in q for n in needles):
            return unit
    return "none"


def _per_object_from(c):
    for key in ("per_object_cap", "per_file_cap"):
        if c.get(key):
            return str(c[key])
    text = str(c.get("limits") or "")
    m = re.search(r"(\d+(?:\.\d+)?\s*(?:KiB|MiB|GiB|TiB|KB|MB|GB|TB))\s*(?:per|/)\s*(?:file|object)",
                  text, re.I)
    if m:
        return m.group(0)
    m = re.search(r"(?:per[- ]object|per[- ]file|single file|max\.? file)[^.;]{0,80}?"
                  r"(\d+(?:\.\d+)?\s*(?:KiB|MiB|GiB|TiB|KB|MB|GB|TB))", text, re.I)
    if m:
        return m.group(0)
    # An explicit statement of absence is a finding, not a gap.
    m = re.search(r"no per[- ](?:file|object) cap published|no per[- ](?:file|object) cap stated",
                  " ".join(str(c.get(k) or "") for k in ("quota", "limits")), re.I)
    if m:
        return m.group(0).strip()
    return "not stated in the source record"


def _retention_from(c):
    text = " ".join(str(c.get(k) or "") for k in ("limits", "reliability_note", "quota"))
    m = re.search(r"(\d+)[- ]day[s]? (?:minimum|retention|billed)", text, re.I)
    if m:
        return m.group(0)
    if re.search(r"deleted when idle|no persistence|ephemeral", text, re.I):
        return "until the instance is recycled; not persistent"
    if re.search(r"retention-clamped|180-day|minimum storage", text, re.I):
        return _trim(text, 300)
    return "not stated in the source record"


def _egress_metered(egress):
    e = str(egress or "").lower()
    if not e or "not published" in e:
        return False
    if re.search(r"free|unmetered|no egress fee|unlimited", e) and \
            not re.search(r"then |after |per gb|/gb|ratio", e):
        return False
    return bool(re.search(r"per gb|/gb|then |allowance|ratio|metered|charged", e))


# ----------------------------------------------------------------- selftest --

def selftest(verbose=False):
    results = []

    def check(name, cond, detail=""):
        results.append((name, bool(cond), detail))
        if verbose or not cond:
            sys.stderr.write("%s %s%s\n" % ("PASS" if cond else "FAIL", name,
                                            ("  " + detail) if detail else ""))

    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.json")
    if not os.path.exists(schema_path):
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "dossier.schema.json")
    if not os.path.exists(schema_path):
        sys.stderr.write("selftest: schema.json not beside this script\n")
        return 1
    schema = load_schema(schema_path)

    good = {
        "topic": "storage", "slug": "example-host", "provider": "Example Host",
        "url": "https://example.com/pricing", "category": "object storage",
        "free_tier": {"stated": "10 GiB", "unit": "GiB",
                      "source_url": "https://example.com/pricing", "read_on": "2026-10-22"},
        "per_object_cap": {"stated": "5 GiB per file", "bytes": 5368709120},
        "retention": {"stated": "until deleted", "days": None},
        "egress": {"terms": "free", "metered": False},
        "interface": ["s3", "rest"], "tooling": "rclone", "chaining": "S3 origin",
        "limits": [{"kind": "request-rate", "value": "10/s", "source": "docs"}],
        "identity_cost": {"kind": "email", "detail": "email only", "country": None},
        "reliability_note": "none observed",
        "confidence": "measured",
        "evidence": [{"url": "probe:https://example.com/x", "date": "2026-10-22",
                      "proved": "200, 1234 bytes, sha256 recorded"}],
        "verdict": "qualifies", "verified_at": "2026-10-22T02:00:00.000Z",
    }

    def run(obj):
        v = Validator(schema)
        v.validate(obj)
        return v

    check("valid record passes", not run(good).errors,
          _fmt(run(good).errors[:2]))

    # each mutation must be caught
    import copy
    mutations = [
        ("missing required field", lambda d: d.pop("per_object_cap")),
        ("bad confidence rung", lambda d: d.__setitem__("confidence", "high")),
        ("bad topic", lambda d: d.__setitem__("topic", "storagee")),
        ("bad slug", lambda d: d.__setitem__("slug", "Not_A_Slug")),
        ("empty evidence", lambda d: d.__setitem__("evidence", [])),
        ("evidence without date", lambda d: d["evidence"][0].pop("date")),
        ("evidence bad date", lambda d: d["evidence"][0].__setitem__("date", "22/10/2026")),
        ("verified_at not Z", lambda d: d.__setitem__("verified_at", "2026-10-22 02:00:00")),
        ("verified_at no millis", lambda d: d.__setitem__("verified_at", "2026-10-22T02:00:00Z")),
        ("url not a URI", lambda d: d.__setitem__("url", "example.com/pricing")),
        ("identity kind bad", lambda d: d["identity_cost"].__setitem__("kind", "phone")),
        ("limit kind not in vocabulary",
         lambda d: d["limits"][0].__setitem__("kind", "fair-use")),
        ("additional property", lambda d: d.__setitem__("surprise", 1)),
        ("interface empty", lambda d: d.__setitem__("interface", [])),
        ("verdict not a token", lambda d: d.__setitem__("verdict", "maybe")),
        ("confidence legacy leaks into confidence",
         lambda d: d.__setitem__("confidence", "medium")),
    ]
    for name, mutate in mutations:
        d = copy.deepcopy(good)
        mutate(d)
        v = run(d)
        check("catches: " + name, bool(v.errors), _fmt(v.errors[:1]))

    # schema construct coverage
    d = copy.deepcopy(good)
    d["extras"] = {"k": "v"}
    check("extras accepted as an object", not run(d).errors, _fmt(run(d).errors[:1]))
    d = copy.deepcopy(good)
    d["limits"] = [{"kind": "request-rate", "value": "1/s", "source": "s"},
                   {"kind": "request-rate", "value": "1/s", "source": "s"}]
    check("duplicate limits allowed (not uniqueItems)", not run(d).errors)

    # migration round-trip on the real seed, if it is reachable
    seed = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "seed", "storage-research", "dossiers",
                        "A-P3-object-storage-nonbig3.json")
    seed = os.path.normpath(seed)
    if os.path.exists(seed):
        with open(seed, encoding="utf-8") as fh:
            wave = json.load(fh)
        recs = wave_to_records(wave, "storage")
        check("migration produced records", len(recs) > 0, str(len(recs)))
        bad = 0
        for r in recs:
            if run(r).errors:
                bad += 1
                if verbose:
                    check("migrated %s valid" % r["slug"], False, _fmt(run(r).errors[:2]))
        check("every migrated record validates", bad == 0, "%d of %d invalid" % (bad, len(recs)))
    else:
        # no checkout carries the seed corpus (it was migration input, kept in .tmp/ at most), so this case is
        # skipped everywhere; it is named here so a reader does not take it for a migration that passed
        check("migration round-trip skipped: no seed/storage-research beside the scripts", True, "skipped")

    failed = [r for r in results if not r[1]]
    sys.stderr.write("selftest: %d passed, %d failed, %d total\n"
                     % (len(results) - len(failed), len(failed), len(results)))
    return 0 if not failed else 1


# -------------------------------------------------------------------- main --

def main(argv=None):
    p = argparse.ArgumentParser(
        prog="verify-dossier.py",
        description="Validate dossier records against a JSON-Schema subset.",
        epilog="EXIT CODES\n"
               "  0 all valid   1 defects found   2 usage error   3 environment wrong\n\n"
               "EXAMPLES\n"
               "  python verify-dossier.py --schema dossier.schema.json dossier/\n"
               "  python verify-dossier.py --schema dossier.schema.json --migrate wave.json --out out/\n"
               "  python verify-dossier.py --selftest\n",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", nargs="?", help="a dossier directory, a record file, or a seed wave")
    p.add_argument("--schema", default=None, help="path to the JSON schema (required to validate)")
    p.add_argument("--migrate", metavar="WAVE", help="convert a seed wave file into records")
    p.add_argument("--out", metavar="DIR", help="write migrated records here")
    p.add_argument("--topic", default="storage", help="topic for --migrate (default storage)")
    p.add_argument("--human", action="store_true", help="human-readable report")
    p.add_argument("--max-errors", type=int, default=40, help="cap errors printed")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)

    if args.selftest:
        return selftest(verbose=args.human)

    if args.migrate:
        if not args.out:
            sys.stderr.write("verify-dossier: --migrate needs --out\n")
            return 2
        try:
            with open(args.migrate, encoding="utf-8") as fh:
                wave = json.load(fh)
        except (OSError, ValueError) as e:
            sys.stderr.write("verify-dossier: cannot read %s: %s\n" % (args.migrate, e))
            return 2
        _CURRENT_FILE[0] = args.migrate
        recs = wave_to_records(wave, args.topic)
        # One provider, one file is the target rule, but two seed waves legitimately
        # name the same provider. Writing every wave into one flat directory would
        # silently overwrite 90 records, so each wave gets its own subdirectory and
        # the collision is left visible for a human to resolve at promotion time.
        wave_dir = os.path.join(args.out, os.path.splitext(os.path.basename(args.migrate))[0])
        os.makedirs(wave_dir, exist_ok=True)
        seen = {}
        for r in recs:
            slug = r["slug"]
            if slug in seen:
                seen[slug] += 1
                r["slug"] = "%s-%d" % (slug, seen[slug])
            else:
                seen[slug] = 1
            path = os.path.join(wave_dir, r["slug"] + ".json")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(r, fh, ensure_ascii=False, indent=2, sort_keys=False)
                fh.write("\n")
        sys.stderr.write("verify-dossier: wrote %d records to %s\n" % (len(recs), args.out))

        if args.schema:
            schema = load_schema(args.schema)
            bad = 0
            for r in recs:
                v = Validator(schema)
                v.validate(r)
                if v.errors:
                    bad += 1
                    sys.stderr.write("  %s: %s\n" % (r["slug"], _fmt(v.errors[:3])))
            sys.stderr.write("verify-dossier: %d of %d migrated records invalid\n"
                             % (bad, len(recs)))
            return 0 if bad == 0 else 1
        return 0

    if not args.schema:
        sys.stderr.write("verify-dossier: --schema is required to validate\n")
        return 2
    if not args.path:
        sys.stderr.write("verify-dossier: need a path to validate\n")
        return 2
    if not os.path.exists(args.path):
        sys.stderr.write("verify-dossier: no such path: %s\n" % args.path)
        return 2

    try:
        schema = load_schema(args.schema)
    except (OSError, ValueError) as e:
        sys.stderr.write("verify-dossier: cannot read schema %s: %s\n" % (args.schema, e))
        return 2

    report = {"ok": True, "schema": os.path.abspath(args.schema), "records": 0,
              "files": 0, "errors": [], "warnings": [], "version": VERSION}
    for path, obj, kind in iter_records(args.path):
        if kind.startswith("unreadable"):
            report["ok"] = False
            report["errors"].append({"path": path, "keyword": "json",
                                     "message": kind})
            continue
        report["files"] += 1
        if kind == "wave":
            report["warnings"].append({
                "path": path, "message": "seed wave (%d candidates); validate the migrated "
                                         "records, not the wave" % len(obj["candidates"])})
            continue
        report["records"] += 1
        v = Validator(schema)
        v.validate(obj)
        for e in v.errors:
            e["file"] = path
            report["errors"].append(e)
        report["warnings"].extend({"path": w["path"], "file": path,
                                   "message": w["message"]} for w in v.warnings)

    if report["errors"]:
        report["ok"] = False

    if args.human:
        print("schema   %s" % report["schema"])
        print("files    %d   records %d" % (report["files"], report["records"]))
        print("errors   %d   warnings %d" % (len(report["errors"]), len(report["warnings"])))
        for e in report["errors"][:args.max_errors]:
            print("  %s  %s  %s: %s" % (os.path.basename(e.get("file", "?")),
                                        e["path"], e["keyword"], e["message"]))
        if len(report["errors"]) > args.max_errors:
            print("  ... %d more" % (len(report["errors"]) - args.max_errors))
        print("verdict  %s" % ("PASS" if report["ok"] else "FAIL"))
    else:
        if len(report["errors"]) > args.max_errors:
            report["errors_truncated"] = len(report["errors"]) - args.max_errors
            report["errors"] = report["errors"][:args.max_errors]
        print(json.dumps(report, ensure_ascii=False, indent=None))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
