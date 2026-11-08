#!/usr/bin/env python3
"""render.py -- make every generated table in docs/ a view of the dossiers.

The failure this prevents: a document states a count, a quota or a verdict, the
record it restates changes, and the two disagree silently. `conventions/README.md`
makes a table that restates a record a *generated* table, owned by this script,
between `<!-- generated:start -->` and `<!-- generated:end -->`. A hand-edited
generated table is the defect; a document with no generated table at all is the
reason two of `BRIEF.md`'s columns have been empty since it was written.

Two modes, and the second is the one the gate uses:

  render.py            write every block from the dossiers
  render.py --check    exit 1 if any block on disk disagrees with the dossiers,
                       and print the diff. Never writes.

A block names its own query in a header line so a reader can see what the table
is a view of:

  <!-- generated:start topic=storage kind=provider-table filter=verdict:qualifies sort=slug limit=40 -->

Kinds:
  topics       one row per dossier topic: counts, verdict mix, confidence mix
  provider     one row per matching record: the comparison table a reader scans
  totals       a bare key/value block for a count a document quotes in prose
  uncited      the `measured` and `documented` records of a topic that no other
               text of docs/ names: the gate's `links` check counts them cited
               here, so a run that adds a verified record lands with no hand
               edit of prose, and a reader still sees the record

The `--check` mode is deliberately independent of the writer: it renders the
expected text and compares it byte for byte, so a hand edit and a stale render
are the same defect and produce the same message.

A third mode reads a commit and writes nothing, for the research harness and CI:

  render.py --tree REV --json [--topics T1,T2]   print {path: text} for every file whose blocks change
  render.py --check --tree REV                   the --check of a commit, read from git objects

`render_tree(source, topics)` is the same render as a function: `scripts/rq land` reads this file from the commit
it writes, executes it from memory and calls it with that commit as the source, so a run renders with the
render.py of the tree it lands on. In the research checkout (`git config rq.researchCheckout` is `true`) the write
mode refuses: a run's tables are rendered by `scripts/rq land` (AGENTS.md section 2 rule 14).

Every list puts a self-hosted record (`self_hosted: true`) after every hosted
one, whatever the sort, and a limit cuts the self-hosted rows first. A
self-hosted row says so in its provider cell. `scripts/self-hosted-last.py`
refuses a list in docs/ that does otherwise.

Exit codes: 0 in agreement (or written), 1 a block disagrees, 2 usage, 3 no tree.
"""
import argparse
import json
import os
import re
import sys
import tempfile

BEGIN = "<!-- generated:start"
END = "<!-- generated:end -->"
BLOCK_RE = re.compile(
    r"<!-- generated:start(?P<args>[^>]*)-->(?P<body>.*?)<!-- generated:end -->",
    re.S)

KINDS = ("topics", "provider", "totals", "breakdown", "shortlist", "uncited")
# docs/ as the gate's `links` check reads it, set by main() and the selftest
CONTEXT = {"docs_dir": None, "cited": None}
TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DEFAULT_DOCS = "docs"
DEFAULT_DOSSIER = "dossier"

CONF_ORDER = ("measured", "documented", "reported", "inferred", "unverified")
VERDICT_ORDER = ("qualifies", "qualifies-with-caveat", "trial-only",
                 "paid-only", "fails-quota", "fails-egress", "fails-identity",
                 "dead")
IDENTITY_ORDER = ("anonymous", "email", "any-phone", "country-phone",
                  "national-id", "card", "institution")


# ------------------------------------------------------------------ records --

class Record(dict):
    """One dossier file, with the accessors a template needs."""

    @property
    def topic(self):
        return self.get("topic") or ""

    @property
    def slug(self):
        return self.get("slug") or ""

    @property
    def confidence(self):
        return self.get("confidence") or "unverified"

    @property
    def verdict(self):
        return self.get("verdict") or ""

    @property
    def self_hosted(self):
        """True when the user installs, runs and maintains it: the last resort, listed last."""
        return self.get("self_hosted") is True

    @property
    def identity(self):
        ic = self.get("identity_cost") or {}
        if isinstance(ic, dict):
            return ic.get("kind") or "-"
        return "-"

    @property
    def cap(self):
        """The per-object cap as stated, shortened. Never a number we made up."""
        poc = self.get("per_object_cap") or {}
        if not isinstance(poc, dict):
            return "-" if not poc else cell(str(poc), 34)
        stated = poc.get("stated")
        if stated:
            return cell(str(stated), 34)
        b = poc.get("bytes")
        if isinstance(b, int):
            return human_bytes(b)
        return "-"

    @property
    def retention(self):
        r = self.get("retention") or {}
        if not isinstance(r, dict):
            return "-"
        days = r.get("days")
        if isinstance(days, (int, float)) and days:
            return "%d d" % days
        stated = r.get("stated")
        return cell(str(stated), 24) if stated else "-"

    @property
    def free_tier(self):
        ft = self.get("free_tier") or {}
        if isinstance(ft, dict):
            return cell(str(ft.get("stated") or "-"), 46)
        return cell(str(ft), 46)


def human_bytes(n):
    for unit, size in (("TiB", 1 << 40), ("GiB", 1 << 30),
                       ("MiB", 1 << 20), ("KiB", 1 << 10)):
        if n >= size:
            return "%g %s" % (round(n / size, 2), unit)
    return "%d B" % n


def cell(text, width):
    """One table cell: no pipe, no newline, folded to a bounded width."""
    text = " ".join(str(text).split())
    text = text.replace("|", "/")
    if len(text) > width:
        text = text[: width - 3].rstrip() + "..."
    return text


def load_records(dossier_dir):
    records, bad = [], []
    for topic in sorted(os.listdir(dossier_dir)):
        tdir = os.path.join(dossier_dir, topic)
        if not os.path.isdir(tdir):
            continue
        for name in sorted(os.listdir(tdir)):
            if not name.endswith(".json") or name.endswith(".generated.json"):
                continue
            path = os.path.join(tdir, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    rec = json.load(fh)
            except (OSError, ValueError) as exc:
                bad.append((path, str(exc)))
                continue
            if not isinstance(rec, dict):
                bad.append((path, "not a JSON object"))
                continue
            rec.setdefault("topic", topic)
            rec.setdefault("slug", name[:-5])
            records.append(Record(rec))
    return records, bad


# ------------------------------------------------------------------- blocks --

def parse_args(spec):
    """`topic=storage kind=provider sort=slug limit=10` -> dict. No shell quoting."""
    out = {}
    for token in spec.split():
        if "=" not in token:
            out["kind"] = token
            continue
        key, _, value = token.partition("=")
        out[key] = value
    return out


def select(records, opts):
    topic = opts.get("topic")
    if topic and topic != "*":
        records = [r for r in records if r.topic == topic]

    for key in ("verdict", "confidence", "identity"):
        want = opts.get(key)
        if not want or want == "*":
            continue
        allowed = set(want.split(","))
        records = [r for r in records if getattr(r, key) in allowed]

    if opts.get("qualifies") == "1":
        records = [r for r in records
                   if r.verdict in ("qualifies", "qualifies-with-caveat")]

    sort_key = opts.get("sort", "slug")
    if sort_key == "verdict":
        order = {v: i for i, v in enumerate(VERDICT_ORDER)}
        records = sorted(records, key=lambda r: (order.get(r.verdict, 99), r.slug))
    elif sort_key == "confidence":
        order = {c: i for i, c in enumerate(CONF_ORDER)}
        records = sorted(records, key=lambda r: (order.get(r.confidence, 99), r.slug))
    elif sort_key == "identity":
        order = {i: n for n, i in enumerate(IDENTITY_ORDER)}
        records = sorted(records, key=lambda r: (order.get(r.identity, 99), r.slug))
    else:
        records = sorted(records, key=lambda r: r.slug)
    records = hosted_first(records)

    limit = opts.get("limit")
    if limit and limit.isdigit():
        records = records[: int(limit)]
    return records


def hosted_first(records):
    """Every hosted record, then every self-hosted one, each part in the order it had (a stable sort)."""
    return sorted(records, key=lambda r: r.self_hosted)


def provider_cell(r, width):
    name = cell(r.get("provider") or r.slug, width)
    return name + " (self-hosted)" if r.self_hosted else name


def render_topics(records, opts, doc_counts=None):
    link = opts.get("link") == "1"
    head = "| topic | records | qualifies | trial or paid | fails | dead | measured or documented |"
    rule = "| --- | --- | --- | --- | --- | --- | --- |"
    if link:
        head = "| topic | records | qualifies | trial or paid | fails | dead | measured or documented | documents |"
        rule = "| --- | --- | --- | --- | --- | --- | --- | --- |"
    lines = [head, rule]
    topics = sorted({r.topic for r in records})
    tot = [0] * 6
    for topic in topics:
        rs = [r for r in records if r.topic == topic]
        q = sum(1 for r in rs if r.verdict in ("qualifies", "qualifies-with-caveat"))
        tp = sum(1 for r in rs if r.verdict in ("trial-only", "paid-only"))
        fa = sum(1 for r in rs
                 if r.verdict in ("fails-quota", "fails-egress", "fails-identity"))
        dead = sum(1 for r in rs if r.verdict == "dead")
        vf = sum(1 for r in rs if r.confidence in ("measured", "documented"))
        row = [len(rs), q, tp, fa, dead, vf]
        tot = [a + b for a, b in zip(tot, row)]
        if link:
            n = (doc_counts or {}).get(topic)
            lines.append("| [`%s`](docs/%s/README.md) | %s | %s |"
                         % (topic, topic, " | ".join(str(n) for n in row),
                            "-" if n is None else n))
        else:
            lines.append("| %s | %s |" % (topic, " | ".join(str(n) for n in row)))
    if opts.get("total") != "0":
        if link:
            docs_total = sum((doc_counts or {}).get(t, 0) for t in topics)
            lines.append("| **all** | %s | %d |"
                         % (" | ".join(str(n) for n in tot), docs_total))
        else:
            lines.append("| **all** | %s |" % " | ".join(str(n) for n in tot))
    return "\n".join(lines)


def render_provider(records, opts, doc_counts=None):
    lines = ["| provider | offer | verdict | confidence | per-object cap | retention | identity | record |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in records:
        lines.append("| %s | %s | %s | %s | %s | %s | %s | `%s` |" % (
            provider_cell(r, 28),
            r.free_tier, r.verdict, r.confidence, r.cap, r.retention,
            r.identity, "dossier/%s/%s.json" % (r.topic, r.slug)))
    return "\n".join(lines)


def render_totals(records, opts, doc_counts=None):
    """A key/value block for the counts a document quotes in prose.

    `fields=a,b,c` prints one line per key, so a paragraph that quotes four
    counts regenerates all four together and cannot drift on one of them. A
    single `field=` still works and prints one line.
    """
    wanted = opts.get("fields") or opts.get("field") or "records"
    labels = (opts.get("labels") or "").split(",") if opts.get("labels") else []
    parts = []
    for i, key in enumerate(k.strip() for k in wanted.split(",") if k.strip()):
        label = labels[i] if i < len(labels) and labels[i] else opts.get("label")
        parts.append("%s %d" % (label or key, count_one(records, key)))
    # One line, because this block exists to sit inside a prose paragraph and
    # restate the counts that paragraph quotes. A per-line form turns a sentence
    # into a list and a reader stops treating it as one.
    return "; ".join(parts)


def count_one(records, key):
    """One count, by key. An unknown key raises: a silent zero is a defect."""
    if key == "records":
        return len(records)
    if key == "measured":
        return sum(1 for r in records if r.confidence == "measured")
    if key == "documented":
        return sum(1 for r in records if r.confidence == "documented")
    if key == "reported":
        return sum(1 for r in records if r.confidence == "reported")
    if key == "unverified":
        return sum(1 for r in records if r.confidence == "unverified")
    if key == "verified":
        return sum(1 for r in records
                   if r.confidence in ("measured", "documented"))
    if key == "qualifies":
        return sum(1 for r in records
                   if r.verdict in ("qualifies", "qualifies-with-caveat"))
    if key == "dead":
        return sum(1 for r in records if r.verdict == "dead")
    if key == "providers":
        # Distinct provider *names*, not slugs. The gap between this and
        # `records` is the slug families the conventions allow, and a document
        # that reports one must not be read as reporting the other.
        return len({(r.get("provider") or r.slug) for r in records})
    if key == "recurring-credit":
        return sum(1 for r in records
                   if (r.get("extras") or {}).get("free_tier_kind")
                   == "recurring-credit")
    if key.startswith("has:"):
        return count_field(records, key[4:])
    raise ValueError("unknown totals field %r" % key)


def _field(rec, path):
    """`extras.free_tier_kind` -> the value, or None. Dotted, no code exec."""
    cur = rec
    for part in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def count_field(records, path):
    """How many records carry a non-empty value at a dotted field path."""
    def present(v):
        if v is None or v == "" or v == [] or v == {}:
            return False
        return not (v == "unknown" or v == ["unknown"])
    return sum(1 for r in records if present(_field(r, path)))


def render_breakdown(records, opts, doc_counts=None):
    """A two-column table of one field's value counts, largest first.

    This is the generated form of every census in the topic. The failure it
    prevents: the README and `measurement.md` published two different rung
    distributions for the same 405 records, and `free-tier-census.md` published
    a third for the verdicts. A count that is rendered cannot disagree with the
    records it counts.

    `field=` names the dotted path. `sort=value` keeps the author's ordering,
    which is what a reader wants for an ordered vocabulary such as the rungs; the
    default sorts by count and breaks ties by the value.
    """
    path = opts.get("field")
    if not path:
        raise ValueError("a breakdown block needs field=<dotted.path>")
    counts = {}
    for r in records:
        value = _field(r, path)
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value) if value else "-"
        if value is None or value == "":
            value = "-"
        counts[str(value)] = counts.get(str(value), 0) + 1

    label = opts.get("label") or path.split(".")[-1].replace("_", " ")
    head = "| %s | Records |" % label
    rule = "| --- | --- |"
    if opts.get("sort") == "value":
        order = opts.get("order")
        if order:
            rank = {v: i for i, v in enumerate(order.split(","))}
            items = sorted(counts.items(), key=lambda kv: (rank.get(kv[0], 99), kv[0]))
        else:
            items = sorted(counts.items())
    else:
        items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    lines = [head, rule]
    for value, n in items:
        lines.append("| `%s` | %d |" % (cell(value, 40), n))
    if opts.get("total") != "0":
        lines.append("| **all** | %d |" % sum(counts.values()))
    return "\n".join(lines)


def render_shortlist(records, opts, doc_counts=None):
    """The buying table: what a row costs, and whether the cart agrees.

    The failure this prevents is the one that cost this corpus its credibility
    on compute. A page advertises a plan at one price; its "Order now" button
    lands on a cart that prices a *different* plan, or prices nothing, and
    nothing on either page says so. RackNerd's specials cart prices all five
    plans exactly as advertised. DediRock's Black Friday page advertises USD
    9.88/yr and its cart sells USD 5.99/**month** for another shape. Both pages
    return HTTP 200 and look current. The only way a reader can tell is if the
    two prices sit in separate columns, so they do.

    `band=free|micro|paid` selects by the monthly figure, `sort=beef` orders by
    what the machine can do rather than by what it costs, and every cell falls
    back to a dash. A dash means nobody has checked, which is a finding; an
    empty cell is an oversight.
    """
    def num(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def shape_of(r):
        s = r.get("extras", {}).get("shape") or {}
        parts = []
        if s.get("vcpu"):
            parts.append("%g vCPU" % s["vcpu"])
        if s.get("ram_gib"):
            parts.append("%g GiB" % s["ram_gib"])
        if s.get("disk_gib"):
            parts.append("%g GB" % s["disk_gib"])
        return " / ".join(parts) if parts else "-"

    band = opts.get("band")
    if band == "free":
        rows = [r for r in records if num(r.get("extras", {}).get("m24h_usd")) == 0.0]
    elif band == "micro":
        rows = [r for r in records
                if (num(r.get("extras", {}).get("m24h_usd")) or 0) > 0
                and (num(r.get("extras", {}).get("m24h_usd")) or 99) <= 1.0]
    elif band == "paid":
        rows = [r for r in records
                if (num(r.get("extras", {}).get("m24h_usd")) or 0) > 1.0
                and (num(r.get("extras", {}).get("m24h_usd")) or 99) <= 5.0]
    else:
        rows = list(records)

    if opts.get("sort") == "beef":
        rows.sort(key=lambda r: (-(num(r.get("extras", {}).get("shape", {}).get("ram_gib")) or 0),
                                 num(r.get("extras", {}).get("m24h_usd")) or 99,
                                 r.slug))
    elif opts.get("sort") == "price":
        rows.sort(key=lambda r: (num(r.get("extras", {}).get("m24h_usd")) or 99, r.slug))
    rows = hosted_first(rows)

    limit = opts.get("limit")
    if limit and limit.isdigit():
        rows = rows[: int(limit)]

    head = ("| # | provider | plan | shape | USD/mo | term | page price | "
            "cart price | cart works | buy or sign up | record |")
    rule = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    lines = [head, rule]
    for i, r in enumerate(rows, 1):
        ex = r.get("extras", {}) or {}
        m = num(ex.get("m24h_usd"))
        url = ex.get("cart_url") or ex.get("signup_url") or r.get("url") or ""
        works = ex.get("cart_works") or "-"
        lines.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | `%s` |" % (
            i,
            provider_cell(r, 22),
            cell(r.get("tier") or "-", 26),
            shape_of(r),
            "-" if m is None else ("%.2f" % m if m else "0"),
            cell(str(ex.get("term") or "-"), 10),
            cell(str(ex.get("price_on_page") or "-"), 18),
            cell(str(ex.get("price_in_cart") or "-"), 18),
            works,
            ("[link](%s)" % url) if url else "-",
            r.slug))
    if not rows:
        lines.append("| - | no record in this band | - | - | - | - | - | - | - | - | - |")
    return "\n".join(lines)


def cited_tokens(docs_dir):
    """The slug tokens of every document of docs/, as the gate's `links` check reads them, without the bodies
    of the `uncited` blocks: a record that only such a block names is not cited elsewhere."""
    parts = []
    for path in docs_files(docs_dir):
        text = scan(path)
        for m, args, _body in find_blocks(text):
            if parse_args(args.strip()).get("kind") == "uncited":
                start, end = m.span("body")
                text = text[:start] + " " * (end - start) + text[end:]
        parts.append(text)
    return set(TOKEN_RE.findall("\n".join(parts).lower()))


def render_uncited(records, opts, doc_counts=None):
    """The topic's `measured` and `documented` records that no other text of docs/ names, one row each."""
    if CONTEXT["cited"] is None:
        CONTEXT["cited"] = cited_tokens(CONTEXT["docs_dir"] or DEFAULT_DOCS)
    rows = hosted_first([r for r in records if r.confidence in ("measured", "documented") and r.slug not in CONTEXT["cited"]])
    if not rows:
        return "Every `measured` or `documented` record of this topic is named by a document."
    lines = ["| record | provider | verdict | confidence |", "| --- | --- | --- | --- |"]
    for r in rows:
        lines.append("| `%s` | %s | %s | %s |" % (r.slug, provider_cell(r, 40), r.verdict, r.confidence))
    return "\n".join(lines)


RENDERERS = {"topics": render_topics, "provider": render_provider,
             "totals": render_totals, "breakdown": render_breakdown,
             "shortlist": render_shortlist, "uncited": render_uncited}


def render_block(records, spec, doc_counts=None):
    opts = parse_args(spec)
    kind = opts.get("kind") or "provider"
    if kind not in RENDERERS:
        raise ValueError("unknown block kind %r (known: %s)"
                         % (kind, ", ".join(KINDS)))
    return RENDERERS[kind](select(records, opts), opts, doc_counts)


def expected_block(records, spec, doc_counts=None):
    """The exact bytes the block should contain between its markers."""
    return "\n" + render_block(records, spec, doc_counts) + "\n"


# --------------------------------------------------------------------- file --

def doc_counts_by_topic(docs_dir):
    """How many .md documents each topic directory holds, as a table cell."""
    counts = {}
    for topic in sorted(os.listdir(docs_dir)):
        tdir = os.path.join(docs_dir, topic)
        if not os.path.isdir(tdir):
            continue
        n = 0
        for dirpath, _, files in os.walk(tdir):
            n += sum(1 for f in files if f.endswith(".md"))
        counts[topic] = n
    return counts


def docs_files(docs_dir, root=None):
    """Every document that may hold a generated block.

    `docs/` is the main corpus, but `BRIEF.md` quotes the record counts in its
    coverage table and has been blocked on this script since it was written. So
    the root documents are scanned too, if they carry a marker.
    """
    out = []
    for dirpath, _, files in os.walk(docs_dir):
        for name in sorted(files):
            if name.endswith(".md"):
                out.append(os.path.join(dirpath, name))
    if root:
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name)
            if not (os.path.isfile(path) and name.endswith(".md")):
                continue
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    if BEGIN in fh.read():
                        out.append(path)
            except OSError:
                pass
    return sorted(set(out))


def scan(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def mask_code(text):
    """Blank out fenced and inline code, preserving length and newlines.

    A document that *documents* the marker convention — `conventions/README.md`
    does, inside inline backticks — would otherwise be read as holding an empty
    block, and the renderer would report the convention's own definition as a
    defect. Masking keeps offsets aligned so the real body is still sliced from
    the original text.
    """
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        if text.startswith("```", i) or text.startswith("~~~", i):
            fence = text[i:i + 3]
            j = text.find(fence, i + 3)
            j = n if j == -1 else j + 3
            for k in range(i, j):
                if out[k] not in "\r\n":
                    out[k] = " "
            i = j
            continue
        if text[i] == "`":
            j = i + 1
            while j < n and text[j] == "`":
                j += 1
            ticks = text[i:j]
            close = text.find(ticks, j)
            if close == -1:
                i = j
                continue
            for k in range(i, close + len(ticks)):
                if out[k] not in "\r\n":
                    out[k] = " "
            i = close + len(ticks)
            continue
        i += 1
    return "".join(out)


def find_blocks(text):
    """Yield (match, opening_args, body) for real blocks, not code samples."""
    masked = mask_code(text)
    for m in BLOCK_RE.finditer(masked):
        start, end = m.span("body")
        yield m, m.group("args"), text[start:end]


def check_file(path, text, records, doc_counts=None):
    """Return (mismatches, empty_blocks, unknown) for one document."""
    mismatches, empty, unknown = [], [], []
    for _m, args, body in find_blocks(text):
        spec = args.strip()
        if not spec:
            unknown.append((path, "", "a generated block with no query"))
            continue
        try:
            want = expected_block(records, spec, doc_counts)
        except ValueError as exc:
            unknown.append((path, spec, str(exc)))
            continue
        if body.strip() == "":
            empty.append((path, spec))
            continue
        if body.replace("\r\n", "\n") != want:
            mismatches.append((path, spec, body, want))
    return mismatches, empty, unknown


def rewrite_file(path, text, records, doc_counts=None, topics=None):
    """Replace every block body with its render. Returns (new_text, changed).

    Offsets come from the masked copy, so an inline example of the marker in a
    document is left byte-identical: only real blocks are rewritten. With
    `topics`, a block that names another topic is kept as it is; a block that
    names no topic (counts across topics) is always rendered.
    """
    changed = False
    out, last = [], 0
    for m, args, body in find_blocks(text):
        spec = args.strip()
        start, end = m.span("body")
        out.append(text[last:start])
        named = parse_args(spec).get("topic") if spec else None
        if not spec or (topics is not None and named not in (None, "*") and named not in topics):
            out.append(body)
            last = end
            continue
        try:
            want = expected_block(records, spec, doc_counts)
        except ValueError:
            out.append(body)
            last = end
            continue
        if body.replace("\r\n", "\n") != want:
            changed = True
        out.append(want)
        last = end
    out.append(text[last:])
    return "".join(out), changed


# ------------------------------------------------------------------ sources --
# A source is what the render reads: ls(rel) -> [(name, is_dir)] and text(rel) -> str or None, with paths
# relative to the repository root and "/" as the separator. DiskSource reads a working tree; GitSource and the
# harness's TreeView read a commit from git objects and write nothing.

class DiskSource:
    def __init__(self, root):
        self.root = root

    def ls(self, rel):
        d = os.path.join(self.root, *[p for p in rel.split("/") if p])
        try:
            names = sorted(os.listdir(d))
        except OSError:
            return []
        return [(n, os.path.isdir(os.path.join(d, n))) for n in names]

    def text(self, rel):
        p = os.path.join(self.root, *rel.split("/"))
        if not os.path.isfile(p):
            return None
        return scan(p)


class GitSource:
    """A commit, read through one `git cat-file --batch` process on binary pipes (a text-mode pipe on Windows turns
    \\n into \\r\\n). Standard library only."""

    def __init__(self, root, rev):
        import subprocess
        self.root, self.rev = root, rev
        fmt = subprocess.run(["git", "-C", root, "rev-parse", "--show-object-format"], capture_output=True, text=True)
        self.rawlen = 32 if fmt.stdout.strip() == "sha256" else 20
        self.p = subprocess.Popen(["git", "-C", root, "cat-file", "--batch"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def _get(self, spec):
        self.p.stdin.write(spec.encode("utf-8") + b"\n")
        self.p.stdin.flush()
        head = self.p.stdout.readline().split()
        if len(head) < 3 or head[-1] == b"missing":
            return None, None
        data = self.p.stdout.read(int(head[2]))
        self.p.stdout.read(1)
        return head[1].decode(), data

    def ls(self, rel):
        kind, data = self._get("%s:%s" % (self.rev, rel.strip("/")))
        if kind != "tree":
            return []
        out, i = [], 0
        while i < len(data):
            sp = data.index(b" ", i)
            nul = data.index(b"\0", sp)
            out.append((data[sp + 1:nul].decode("utf-8", "surrogateescape"), data[i:sp] == b"40000"))
            i = nul + 1 + self.rawlen
        return sorted(out)

    def text(self, rel):
        kind, data = self._get("%s:%s" % (self.rev, rel))
        return data.decode("utf-8") if kind == "blob" else None

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=10)
        except Exception:
            pass


def records_from(source):
    records = []
    for topic, is_dir in source.ls(DEFAULT_DOSSIER):
        if not is_dir:
            continue
        for name, sub in source.ls("%s/%s" % (DEFAULT_DOSSIER, topic)):
            if sub or not name.endswith(".json") or name.endswith(".generated.json"):
                continue
            try:
                rec = json.loads(source.text("%s/%s/%s" % (DEFAULT_DOSSIER, topic, name)))
            except ValueError:
                continue
            if isinstance(rec, dict):
                rec.setdefault("topic", topic)
                rec.setdefault("slug", name[:-5])
                records.append(Record(rec))
    return records


def doc_paths_from(source):
    """The documents of docs/ and the root documents that carry a marker, as relative paths."""
    out = []

    def walk(rel):
        for name, is_dir in source.ls(rel):
            p = "%s/%s" % (rel, name)
            if is_dir:
                walk(p)
            elif name.endswith(".md"):
                out.append(p)
    walk(DEFAULT_DOCS)
    for name, is_dir in source.ls(""):
        if not is_dir and name.endswith(".md") and BEGIN in (source.text(name) or ""):
            out.append(name)
    return sorted(set(out))


def render_tree(source, topics=None):
    """The generated blocks of a tree, rendered from that tree's records. -> {relative path: new text} for every
    document whose text changes. With `topics` (an iterable), only the blocks of those topics and the blocks that name
    no topic are computed; an `uncited` block is a topic's block. Every record is still loaded, because the counts
    across topics need them. Nothing is written."""
    records = records_from(source)
    paths = doc_paths_from(source)
    docs = [p for p in paths if p.startswith(DEFAULT_DOCS + "/")]
    counts = {t: 0 for t, is_dir in source.ls(DEFAULT_DOCS) if is_dir}
    for p in docs:
        parts = p.split("/")
        if len(parts) > 2 and parts[1] in counts:
            counts[parts[1]] += 1
    texts = {p: source.text(p) for p in paths}
    parts = []
    for p in docs:
        t = texts.get(p) or ""
        for m, args, _body in find_blocks(t):
            if parse_args(args.strip()).get("kind") == "uncited":
                start, end = m.span("body")
                t = t[:start] + " " * (end - start) + t[end:]
        parts.append(t)
    CONTEXT.update(docs_dir=None, cited=set(TOKEN_RE.findall("\n".join(parts).lower())))
    want = None if topics is None else set(topics)
    out = {}
    for p, text in sorted(texts.items()):
        if text is None or BEGIN not in text:
            continue
        new, changed = rewrite_file(p, text, records, counts, want)
        if new != text:
            out[p] = new
    return out


def research_checkout(root):
    import subprocess
    try:
        r = subprocess.run(["git", "-C", root, "config", "--get", "rq.researchCheckout"], capture_output=True, text=True)
    except OSError:
        return False
    return r.stdout.strip().lower() == "true"


# -------------------------------------------------------------------- proof --

def selftest():
    """Every case states its expected verdict. A check that cannot fail is off."""
    import shutil

    fails = 0

    def say(ok, name):
        nonlocal fails
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1

    tmp = tempfile.mkdtemp(prefix="render-selftest.")
    try:
        docs = os.path.join(tmp, "docs")
        dossier = os.path.join(tmp, "dossier", "storage")
        os.makedirs(docs)
        os.makedirs(dossier)
        recs = [
            {"topic": "storage", "slug": "alpha", "provider": "Alpha",
             "free_tier": {"stated": "10 GiB"}, "confidence": "documented",
             "verdict": "qualifies", "per_object_cap": {"bytes": 1 << 30},
             "retention": {"days": 30}, "identity_cost": {"kind": "email"}},
            {"topic": "storage", "slug": "beta", "provider": "Beta",
             "free_tier": {"stated": "none"}, "confidence": "reported",
             "verdict": "dead", "per_object_cap": {"stated": "4 GB"},
             "retention": {"stated": "n/a"}, "identity_cost": {"kind": "card"}},
        ]
        for r in recs:
            with open(os.path.join(dossier, r["slug"] + ".json"), "w",
                      encoding="utf-8") as fh:
                json.dump(r, fh)
        loaded, bad = load_records(os.path.join(tmp, "dossier"))
        say(len(loaded) == 2 and not bad, "loads every record")

        doc = os.path.join(docs, "a.md")
        spec = " topic=storage kind=provider sort=slug"
        body = expected_block(loaded, spec.strip())
        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\n<!-- generated:start%s-->%s%s\n\ntail\n"
                     % (spec, body, END))
        mism, empty, unknown = check_file(doc, scan(doc), loaded)
        say(not mism and not empty and not unknown, "a correct block agrees")

        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\n<!-- generated:start%s-->\n| hand | edited |\n|---|"
                     "---|\n| wrong | wrong |\n%s\n" % (spec, END))
        mism, _, _ = check_file(doc, scan(doc), loaded)
        say(len(mism) == 1, "a hand-edited block is refused")

        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\n<!-- generated:start%s-->\n%s\n" % (spec, END))
        _, empty, _ = check_file(doc, scan(doc), loaded)
        say(len(empty) == 1, "an empty block is refused, not passed as agreement")

        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\n<!-- generated:start kind=nonsense-->\n%s\n" % END)
        _, _, unknown = check_file(doc, scan(doc), loaded)
        say(len(unknown) == 1, "an unknown block kind is refused")

        # The render must be idempotent, or --check can never be green.
        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\n<!-- generated:start%s-->\nstale\n%s\n" % (spec, END))
        text = scan(doc)
        once, changed1 = rewrite_file(doc, text, loaded)
        twice, changed2 = rewrite_file(doc, once, loaded)
        say(changed1 and not changed2 and once == twice,
            "render is idempotent and reports the change once")

        # A document that DOCUMENTS the marker convention must not be read as
        # holding a block. conventions/README.md does exactly this.
        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\nthe markers are `<!-- generated:start -->` and "
                     "`<!-- generated:end -->`.\n")
        m, e, u = check_file(doc, scan(doc), loaded)
        say(not m and not e and not u,
            "an inline code sample of the marker is not a block")

        # An uncited block lists a verified record that no other document names, and only that one.
        CONTEXT.update(docs_dir=docs, cited=None)
        uspec = " topic=storage kind=uncited"
        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# doc\n\n<!-- generated:start%s-->\nstale\n%s\n" % (uspec, END))
        once, _ = rewrite_file(doc, scan(doc), loaded)
        say("| `alpha` |" in once and "`beta`" not in once,
            "an uncited block lists the documented record and not the reported one")
        with open(doc, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(once)
        CONTEXT.update(cited=None)
        m, e, u = check_file(doc, scan(doc), loaded)
        say(not m and not e and not u, "an uncited block does not cite its own rows")
        with open(os.path.join(docs, "b.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# other\n\nAlpha is `alpha`.\n")
        CONTEXT.update(cited=None)
        once, _ = rewrite_file(doc, scan(doc), loaded)
        say("`alpha`" not in once and "named by a document" in once,
            "a record that another document names leaves the uncited block")
        os.remove(os.path.join(docs, "b.md"))
        CONTEXT.update(docs_dir=None, cited=None)

        # A record whose provider carries a pipe must not break the table.
        loaded[0]["provider"] = "Al|pha"
        row = render_provider(select(loaded, {"topic": "storage"}), {})
        widths = {line.count("|") for line in row.splitlines()}
        say(len(widths) == 1, "a pipe in a record does not add a table column")

        # A self-hosted record is the last resort: last under every sort, cut first by a limit, and labelled.
        sh = Record({"topic": "storage", "slug": "aaa", "provider": "Aaa", "verdict": "qualifies",
                     "confidence": "measured", "self_hosted": True, "identity_cost": {"kind": "anonymous"},
                     "extras": {"m24h_usd": 0}})
        mixed = [sh] + loaded
        orders = [[r.slug for r in select(mixed, {"sort": s})] for s in ("slug", "verdict", "confidence", "identity")]
        say(all(o[-1] == "aaa" for o in orders), "a self-hosted record sorts after every hosted one, under every sort")
        say([r.slug for r in select(mixed, {"limit": "2"})] == ["alpha", "beta"],
            "a limit cuts the self-hosted record before a hosted one")
        table = render_provider(select(mixed, {}), {}).splitlines()
        say("Aaa (self-hosted)" in table[-1] and "(self-hosted)" not in "".join(table[:-1]),
            "a self-hosted row says so in its provider cell")
        short = render_shortlist(mixed, {"sort": "price"}).splitlines()
        say("Aaa (self-hosted)" in short[-1], "the shortlist puts a self-hosted record last")
        CONTEXT.update(cited=set())
        uncited = render_uncited(mixed, {}).splitlines()
        CONTEXT.update(cited=None)
        say("Aaa (self-hosted)" in uncited[-1] and "(self-hosted)" not in "".join(uncited[:-1]),
            "an uncited block puts a self-hosted record last and labels it")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nrender selftest: %s" % ("0 failed" if not fails else "%d failed" % fails))
    return 0 if not fails else 1


# --------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser(
        description="render the generated tables in docs/ from dossier/, "
                    "or check that they still agree")
    ap.add_argument("root", nargs="?", default=".",
                    help="repository root (default: .)")
    ap.add_argument("--root", dest="root_opt", default=None,
                    help="repository root; the same thing as the positional form")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any block disagrees; write nothing")
    ap.add_argument("--docs", default=None, help="docs directory (default: <root>/docs)")
    ap.add_argument("--dossier", default=None,
                    help="dossier directory (default: <root>/dossier)")
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the checker catches a bad block and accepts a good one")
    ap.add_argument("--tree", default=None, metavar="REV",
                    help="read a commit from git objects instead of the working tree; writes nothing")
    ap.add_argument("--topics", default=None, help="with --tree: render only these topics' blocks (T1,T2) and the "
                                                   "blocks that name no topic")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    root = os.path.abspath(args.root_opt or args.root)
    if not os.path.isdir(root):
        print("render: --root is not a directory: %s" % root, file=sys.stderr)
        return 2
    if args.tree:
        src = GitSource(root, args.tree)
        try:
            topics = [t for t in (args.topics or "").split(",") if t] or None
            changed = render_tree(src, topics)
        finally:
            src.close()
        if args.check:
            for p in sorted(changed):
                print("MISMATCH %s" % p)
            print("render: %s at %s" % ("%d document(s) disagree with dossier/" % len(changed) if changed
                                        else "every generated block agrees with dossier/", args.tree))
            return 1 if changed else 0
        print(json.dumps(changed, ensure_ascii=False, indent=1) if args.json else
              "\n".join("would write %s" % p for p in sorted(changed)) or "render: nothing to write")
        return 0
    if not args.check and not args.json and research_checkout(root):
        print("render: the research checkout changes records only through a run: scripts/rq open amend TOPIC "
              "\"RID: what is wrong\" (AGENTS.md section 2 rule 14), and scripts/rq land renders the run's tables. A hand "
              "change belongs to a session that the operator starts in its own clone. --check and --tree REV read only.",
              file=sys.stderr)
        return 2
    docs_dir = args.docs or os.path.join(root, DEFAULT_DOCS)
    dossier_dir = args.dossier or os.path.join(root, DEFAULT_DOSSIER)
    if not os.path.isdir(docs_dir):
        print("render: no docs/ directory at %s" % docs_dir, file=sys.stderr)
        return 3
    if not os.path.isdir(dossier_dir):
        print("render: no dossier/ directory at %s" % dossier_dir, file=sys.stderr)
        return 3

    records, bad = load_records(dossier_dir)
    doc_counts = doc_counts_by_topic(docs_dir)
    CONTEXT.update(docs_dir=docs_dir, cited=None)

    mismatches, empties, unknowns = [], [], []
    files = docs_files(docs_dir, root)
    for path in files:
        m, e, u = check_file(path, scan(path), records, doc_counts)
        mismatches += m
        empties += e
        unknowns += u

    if args.json:
        print(json.dumps({
            "docs": len(files),
            "records": len(records),
            "unreadable": [{"file": p, "error": e} for p, e in bad],
            "mismatched": [{"file": p, "query": s} for p, s, _, _ in mismatches],
            "empty": [{"file": p, "query": s} for p, s in empties],
            "unknown": [{"file": p, "query": s, "why": w} for p, s, w in unknowns],
            "checked": len(mismatches) + len(empties) + len(unknowns),
        }, indent=2))
        return 1 if (mismatches or empties or unknowns) else 0

    if args.check:
        for path, spec, have, want in mismatches:
            rel = os.path.relpath(path, root).replace("\\", "/")
            print("MISMATCH %s  [%s]" % (rel, spec.strip()))
            for line in _first_difference(have, want):
                print("    %s" % line)
        for path, spec in empties:
            rel = os.path.relpath(path, root).replace("\\", "/")
            print("EMPTY    %s  [%s]  block has markers and no body"
                  % (rel, spec.strip()))
        for path, spec, why in unknowns:
            rel = os.path.relpath(path, root).replace("\\", "/")
            print("UNKNOWN  %s  [%s]  %s" % (rel, spec.strip(), why))
        for path, err in bad:
            print("UNREADABLE %s  %s" % (path, err))

        n = len(mismatches) + len(empties) + len(unknowns) + len(bad)
        if n:
            print("\nrender: %d block(s) disagree with dossier/ over %d document(s)"
                  % (n, len(files)))
            return 1
        print("render: %d generated block(s) agree with %d record(s) over %d document(s)"
              % (_count_blocks(files), len(records), len(files)))
        return 0

    written = 0
    for path in files:
        text = scan(path)
        if BEGIN not in text:
            continue
        new, changed = rewrite_file(path, text, records, doc_counts)
        if changed:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            written += 1
            print("wrote %s" % os.path.relpath(path, root).replace("\\", "/"))
    print("render: %d block(s) over %d document(s); %d file(s) rewritten"
          % (_count_blocks(files), len(files), written))
    return 0


def _count_blocks(files):
    n = 0
    for path in files:
        try:
            n += len(list(find_blocks(scan(path))))
        except OSError:
            pass
    return n


def _first_difference(have, want, context=3):
    """The first disagreeing lines, so a reader can see the drift."""
    h = have.replace("\r\n", "\n").splitlines()
    w = want.replace("\r\n", "\n").splitlines()
    out = []
    for i in range(max(len(h), len(w))):
        hv = h[i] if i < len(h) else "<end of block>"
        wv = w[i] if i < len(w) else "<end of block>"
        if hv != wv:
            out.append("line %d" % (i + 1))
            out.append("  on disk: %s" % hv[:160])
            out.append("  record : %s" % wv[:160])
            break
    return out or ["byte-identical lines but different length"]


if __name__ == "__main__":
    sys.exit(main())
