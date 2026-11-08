"""rq check: contradiction and invariant rules over dossier/, with a per-rule baseline (ratchet).

Errors fail the gate only when a violation is new against scripts/research/baseline.tsv; warnings are
counted and filed as policy issues; info is reported. Every rule here was measured on this corpus before it
was written (precision and runtime), and four rules that failed measurement were left out on purpose.
Rules gate on provenance: a defaulted placeholder is not a claim, so it never makes a contradiction.
"""
import collections
import glob
import hashlib
import json
import os
import re
from urllib.parse import urlsplit

from common import REPO, SETTINGS, core_name, domain_of, norm_url, other_tier, quote_found, read_capture

CUTOVER = SETTINGS["capture_cutover"]  # evidence dated on or after this day must carry a verified capture and quote
PROBE_CUTOVER = SETTINGS.get("probe_capture_cutover", "9999-12-31")  # the same for a probe: row (a stored probe record)
QUAL = ("qualifies", "qualifies-with-caveat")
ISO = re.compile(r"\b(?:USD|EUR|GBP|CNY|JPY|KRW|RUB|INR|CAD|AUD|CHF|PLN|SEK|NOK|DKK|CZK|HUF|TRY|BRL|MXN|IDR|THB|VND|PHP|MYR|SGD|HKD|TWD|NZD|ZAR|AED|UAH|KZT|RON|BGN|ILS|SAR|ARS|CLP|NGN|EGP|PKR|BDT|KES)\b")
NOFREE = re.compile(r"^\s*(no free (tier|plan|trial|allowance|test)|none\b|not offered|there is no free)", re.I)
DEFAULTED = re.compile(r"defaulted|assumed value|flagged, not evidence|not recorded in the|^unverified|not read:|not stated in the source", re.I)
SEEDDATE = re.compile(r"undated in the seed|dated to the seed pass")

# A severity is a word, or a map from topic to word with "*" for every other topic. The operator decided C01, C03
# and C18 on 2026-10-28 (issues #10, #11 and #12; history/2026-10-28T135534Z/operator-rulings-of-2026-10-28.md).
RULES = {
    "C01": ("error", "qualifies-no-free-tier", "a qualifying verdict while the record's own free tier says there is none"),
    "C03": ({"storage": "error", "netdisk-pan": "error", "*": "warn"}, "qualifies-no-probe",
            "verdict qualifies with no probe evidence; an error in storage and netdisk-pan, where the read path is the claim"),
    "C04": ("warn", "duplicate-disagreement", "same topic, domain and name disagree on verdict or a stated identity"),
    "C07": ("error", "unit-system", "free_tier.unit names one unit system while the stated text uses only the other"),
    "C09": ("error", "binding-not-in-limits", "binding names a constraint kind that no limits[] row has"),
    "C10": ("error", "evidence-after-verified", "an evidence row is dated after verified_at"),
    "C14": ("warn", "source-not-in-evidence", "free_tier.source_url is not among the evidence URLs"),
    "C15": ("error", "price-no-iso-currency", "a price with a number and no ISO 4217 currency code"),
    "C16": ("info", "provenance-flags", "evidence with a synthetic date or a placeholder probe"),
    "C17": ("warn", "fails-egress-not-assessed", "verdict fails-egress while egress was never assessed"),
    "C18": ("error", "qualifies-gated-identity",
            "verdict qualifies behind institution, national ID or a country phone (qualifies-with-caveat at best)"),
    "C19": ("error", "measured-no-probe", "confidence measured with no probe object and no probe: evidence"),
    "C20": ("error", "narrative-in-field", "process narrative or personal wording inside a record field"),
    "C21": ("error", "evidence-needs-capture", "an http evidence row dated %s or later, or a probe: row dated %s or later, "
            "without a capture whose text holds the quote" % (CUTOVER, PROBE_CUTOVER)),
}
POLICY = ()  # warn rules that wait for a methodology decision; C01, C03 and C18 were decided on 2026-10-28


def severity(rule, key=""):
    """error, warn or info for one violation: a rule's severity can depend on the topic its key starts with."""
    s = RULES[rule][0]
    if isinstance(s, dict):
        return s.get(key.split("/")[0], s["*"])
    return s


def is_error(rule, key=""):
    return severity(rule, key) == "error"


def severity_label(rule):
    s = RULES[rule][0]
    if isinstance(s, dict):
        return "/".join(sorted(set(s.values())))
    return s


def load_records(repo=REPO, view=None):
    """Every record of dossier/: from the working tree, or from a commit (view) read into memory with no file written
    (`scripts/rq check --rev REV`)."""
    if view is not None:
        out = []
        for topic, (mode, _) in sorted((view.listdir("dossier") or {}).items()):
            if mode != "40000":
                continue
            for name, (m2, oid) in sorted((view.listdir("dossier/" + topic) or {}).items()):
                if m2 == "40000" or not name.endswith(".json") or name.endswith(".generated.json"):
                    continue
                rec = json.loads(view.blob(oid).decode("utf-8"))
                rec["_rid"] = "%s/%s" % (topic, name[:-5])
                out.append(rec)
        return out
    out = []
    for p in sorted(glob.glob(os.path.join(repo, "dossier", "*", "*.json"))):
        if p.endswith(".generated.json"):
            continue
        with open(p, "rb") as f:
            rec = json.loads(f.read().decode("utf-8"))
        rec["_rid"] = "%s/%s" % (os.path.basename(os.path.dirname(p)), os.path.basename(p)[:-5])
        out.append(rec)
    return out


BINDING_RUNGS = ("measured", "documented")
BINDING_HINT = ("a record at rung measured or documented names `binding` (a kind that one of its limits[] rows has, "
                "or `none`) and a `binding_note`; the gate's binding check fails it otherwise")


def binding_missing(rec):
    """The gate's binding check (scripts/gate.sh check_binding) for one record: rung measured or documented and no
    `binding`. The schema keeps the field optional; the gate makes it required at those rungs, so the lint, the
    integrator and land apply the same predicate and a run never lands what CI then fails (W4-01)."""
    return isinstance(rec, dict) and rec.get("confidence") in BINDING_RUNGS and not rec.get("binding")


SELF_HOSTED_HINT = ("a record whose offer is software the user installs and runs sets `self_hosted: true` and says in "
                    "`tooling` what the user installs and runs; a hosted lane of such software (a public relay, a managed tier) "
                    "sets `self_hosted: false`. The gate's selfhosted check fails it otherwise, and an unmarked "
                    "self-hosted record sorts among the hosted ones")
_SHL = {}


def _self_hosted_last():
    """scripts/self-hosted-last.py of the checkout, loaded once, or None in a tree without it."""
    if "m" not in _SHL:
        _SHL["m"] = None
        p = os.path.join(REPO, "scripts", "self-hosted-last.py")
        if os.path.exists(p):
            import importlib.util
            spec = importlib.util.spec_from_file_location("self_hosted_last", p)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                _SHL["m"] = mod if hasattr(mod, "check_records") and hasattr(mod, "check_marks") else None
            except Exception:
                _SHL["m"] = None
    return _SHL["m"]


def self_hosted_problems(rec, rid, root=None):
    """The gate's record checks of scripts/self-hosted-last.py for one record: a category or tooling that says
    self-hosted needs a self_hosted marker, and a marker that is true needs a reason in the record's own text (or in
    root's history/ledger.jsonl; a draft has none). The lint of a draft and of a set, and land, apply them, so a run
    never lands a record the selfhosted check of CI then fails (W5-03). -> list of reasons."""
    mod = _self_hosted_last()
    if mod is None or not isinstance(rec, dict):
        return []
    import types
    ns = types.SimpleNamespace(recs={rid: rec})
    out = [h["why"] for h in mod.check_records(ns)]
    out += [h["why"] for h in mod.check_marks(ns, root or os.path.join(REPO, ".tmp", "rq", "no-ledger"))]
    return out


UNREACHABLE = re.compile(r'"status":\s*(?:null|0|[13-9]\d\d)\b')


def unreachable_row(e):
    """A probe: evidence row whose quote is a status other than 2xx: the page did not answer, so nothing of the record
    was checked and verified_at does not move (C10 skips it). A lane records `unverified: unreachable on DATE` with it
    and needs no confirm, which would re-date the record (W5-06)."""
    return isinstance(e, dict) and (e.get("url") or "").startswith("probe:") and bool(UNREACHABLE.search(e.get("quote") or ""))


def has_probe(r):
    return bool(r.get("probe")) or any((e.get("url") or "").startswith("probe:") for e in r.get("evidence") or [])


def h8(v):
    return hashlib.sha1(json.dumps(v, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:8]


def record_violations(r, repo=REPO, narrative=True, lane=None, view=None):
    """-> list of (rule, key, detail) for one record. C21 reads a capture from the lane, then from the commit a caller
    reads (view), then from the working tree and the live run branches."""
    rid = r.get("_rid") or "%s/%s" % (r.get("topic"), r.get("slug"))
    v = []
    ft = r.get("free_tier") or {}
    st = ft.get("stated") or ""
    unit = ft.get("unit")
    dec = re.search(r"\d\s?(?:kb|mb|gb|tb|pb)\b", st, re.I)
    binr = re.search(r"\d\s?(?:kib|mib|gib|tib|pib)\b", st, re.I)
    if (unit in ("GiB", "TiB") and dec and not binr) or (unit in ("GB", "TB", "MB") and binr and not dec):
        v.append(("C07", rid, "unit %s vs stated %r" % (unit, st[:60])))
    b = r.get("binding")
    if b not in (None, "none") and b not in {(l or {}).get("kind") for l in r.get("limits") or []}:
        v.append(("C09", rid, "binding %s" % b))
    va = (r.get("verified_at") or "")[:10]
    for e in r.get("evidence") or []:
        if va and (e.get("date") or "") > va and not unreachable_row(e):
            v.append(("C10", "%s|%s" % (rid, e.get("date")), "evidence %s after verified_at %s" % (e.get("date"), va)))
            break
    p = r.get("price_per_tb_month")
    if isinstance(p, str) and re.search(r"\d", p) and not ISO.search(p):
        v.append(("C15", rid, "price %r" % p[:60]))
    if r.get("confidence") == "measured" and not has_probe(r):
        v.append(("C19", rid, "measured without a probe"))
    verdict = r.get("verdict")
    ic = r.get("identity_cost") or {}
    if (verdict in QUAL and NOFREE.search(st)) or (verdict == "qualifies" and unit == "none"):
        v.append(("C01", rid, "verdict %s, free tier %r" % (verdict, st[:60])))
    if verdict == "qualifies" and not has_probe(r):
        v.append(("C03", rid, "qualifies, no probe"))
    if verdict == "fails-egress" and re.search(r"not assessed|rejected before its egress", (r.get("egress") or {}).get("terms") or "", re.I):
        v.append(("C17", rid, "fails-egress, egress not assessed"))
    if verdict == "qualifies" and ic.get("kind") in ("institution", "national-id", "country-phone"):
        v.append(("C18", rid, "verdict %s behind %s" % (verdict, ic.get("kind"))))
    su = ft.get("source_url")
    if su and su.startswith("http"):
        ev = {norm_url(e.get("url")).split("?")[0] for e in r.get("evidence") or [] if (e.get("url") or "").startswith("http")}
        if norm_url(su).split("?")[0] not in ev:
            v.append(("C14", rid, "source %s" % su[:60]))
    flags = sum(1 for e in r.get("evidence") or [] if SEEDDATE.search(e.get("proved") or "") or e.get("url") == "probe:unspecified")
    if flags:
        v.append(("C16", rid, "%d evidence row(s) with a synthetic date or placeholder probe" % flags))
    for e in r.get("evidence") or []:
        u, d = e.get("url") or "", e.get("date") or ""
        if (u.startswith("http") and d >= CUTOVER) or (u.startswith("probe:") and d >= PROBE_CUTOVER):
            cap, q = e.get("capture") or "", e.get("quote") or ""
            ok = False
            if cap and q:
                text = read_capture(cap, repo, lane, view)
                ok = text is not None and quote_found(q, text)[0] != "miss"
            if not ok:
                v.append(("C21", "%s|%s|%s" % (rid, e.get("url"), e.get("date")), "evidence %s %s" % (e.get("date"), (e.get("url") or "")[:50])))
    if narrative:
        import units
        for k in ("free_tier", "per_object_cap", "retention", "egress", "identity_cost", "limits", "limits_note",
                  "binding_note", "reliability_note", "notes", "chaining", "tooling", "interface_detail", "confidence_note"):
            val = r.get(k)
            if val in (None, "", [], {}):
                continue
            for path, leaf, rule, before in units.narrative_leaves(val, "$." + k, repo):
                v.append(("C20", "%s|%s|%s" % (rid, path, h8(leaf)), "%s %s: %s" % (path, rule, before[:90])))
    return v


UNCITED_HINT = ("drop a row only where another row cites the same page, or replace it in the same unit: drop_evidence "
                "and then append_evidence (or the set or confirm whose evidence it is) with a row that cites that page")


def source_urls(rec):
    """The http URLs that a field of the record names as its source: free_tier.source_url, the source_url of every
    other object, and the source of each limits[] row. The evidence list itself is not a field's source."""
    out = []

    def walk(v, key=None):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x, k)
        elif isinstance(v, list):
            for x in v:
                walk(x, key)
        elif isinstance(v, str) and key in ("source_url", "source") and v.startswith("http"):
            out.append(v)
    for k, v in (rec or {}).items():
        if k != "evidence":
            walk(v, k)
    return out


def uncited_sources(before, after):
    """The source URLs of after's fields that an evidence row of before cites and no row of after cites: what a dropped
    evidence row would leave unsupported. A source that no row cited before is C14's (a warning), not the drop's."""
    def key(u):
        return norm_url(u).split("?")[0]

    def cited(rec):
        return {key(e.get("url")) for e in (rec or {}).get("evidence") or []
                if isinstance(e, dict) and (e.get("url") or "").startswith("http")}
    was, now = cited(before), cited(after)
    return sorted({u for u in source_urls(after) if key(u) in was and key(u) not in now})


def cross_violations(recs):
    """C04: records of one topic, registrable domain and core name that disagree, both sides stated. Two records whose
    tiers differ are two offers of one provider, never a disagreement."""
    groups = collections.defaultdict(list)
    for r in recs:
        u = r.get("url") or ""
        d = domain_of(u) if u.startswith("http") else None
        if not d:
            continue
        groups[(r["topic"], d, core_name(r.get("provider")))].append(r)
    out = []
    for (t, d, n), rs in groups.items():
        if len(rs) < 2 or not n:
            continue
        rs.sort(key=lambda x: x["_rid"])
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                dup = (a.get("extras") or {}).get("duplicate_of") or (b.get("extras") or {}).get("duplicate_of")
                if dup or other_tier(a.get("tier"), b.get("tier")):
                    # two tiers of one provider are two offers (the schema's `tier`): they may well disagree
                    continue
                fields = []
                if a.get("verdict") != b.get("verdict"):
                    fields.append("verdict %s/%s" % (a.get("verdict"), b.get("verdict")))
                ia, ib = a.get("identity_cost") or {}, b.get("identity_cost") or {}
                if ia.get("kind") != ib.get("kind") and not DEFAULTED.search(ia.get("detail") or "") \
                        and not DEFAULTED.search(ib.get("detail") or ""):
                    fields.append("identity %s/%s" % (ia.get("kind"), ib.get("kind")))
                if fields:
                    out.append(("C04", "%s|%s" % (a["_rid"], b["_rid"]), "; ".join(fields)))
    return out


def baseline_path(repo=REPO):
    return os.path.join(repo, "scripts", "research", "baseline.tsv")


def load_baseline(repo=REPO):
    p = baseline_path(repo)
    if not os.path.exists(p):
        return collections.defaultdict(set)
    with open(p, encoding="utf-8") as f:
        return parse_baseline(f.read())


def parse_baseline(text):
    out = collections.defaultdict(set)
    for ln in (text or "").splitlines():
        if ln.startswith("#") or not ln.strip():
            continue
        rule, key = ln.rstrip("\r").split("\t", 1)
        out[rule].add(key)
    return out


def baseline_of(view=None, repo=REPO):
    """The baseline of a commit (a run branch), or of the working tree when view is None."""
    if view is None:
        return load_baseline(repo)
    b = view.read("scripts/research/baseline.tsv")
    return parse_baseline(b.decode("utf-8") if b else "")


def baseline_text(viol):
    rows = sorted({(r, k) for r, k, _ in viol if is_error(r, k)})
    out = ["# rule\tkey: error violations that existed when the rule was adopted; the gate fails only on new ones.",
           "# Fixing a record removes its row on the next `scripts/rq check --prune`; never add rows by hand."]
    out += ["%s\t%s" % (r, k) for r, k in rows]
    return "\n".join(out) + "\n", len(rows)


def write_baseline(viol, repo=REPO):
    text, n = baseline_text(viol)
    with open(baseline_path(repo), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return n


def run_all(repo=REPO, narrative=True, view=None):
    recs = load_records(repo, view)
    viol = []
    for r in recs:
        viol += record_violations(r, repo, narrative, view=view)
    viol += cross_violations(recs)
    return recs, viol


def new_errors(viol, repo=REPO, view=None):
    base = baseline_of(view, repo)
    return [(r, k, d) for r, k, d in viol if is_error(r, k) and k not in base.get(r, set())]


def summary(viol, repo=REPO, view=None):
    base = baseline_of(view, repo)
    c = collections.Counter(r for r, _, _ in viol)
    lines = []
    for rule, (_, name, desc) in sorted(RULES.items()):
        sev = severity_label(rule)
        n = c.get(rule, 0)
        nb = len(base.get(rule, ())) if "error" in sev else None
        new = sum(1 for r, k, _ in viol if r == rule and is_error(r, k) and k not in base.get(rule, set()))
        lines.append("%s %-10s %-27s %6d%s%s" % (rule, sev, name, n, ("  baseline %d" % nb) if nb is not None else "",
                                               ("  NEW %d" % new) if new else ""))
    return lines
