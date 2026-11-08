#!/usr/bin/env python3
"""self-hosted-last.py -- refuse a list that puts a self-hosted record above a hosted one, or recommends it.

The failure this prevents: the client has no hardware and wants a hosted service, free, trial or paid.
A record whose offer is software the user installs, runs and maintains (`self_hosted: true`) is the last
resort. A list that ranks it first, or a row that stars it, sends the reader to the one option they cannot
use while a hosted one exists. The operator's rule of 2026-10-29: a self-hosted record is always at the
bottom of a list, and never starred, highlighted, ranked first or recommended.

Four things are checked.

1. Lists: every Markdown table and list in docs/ and in the root documents, generated blocks included.
   A row is tied to records by a record path (dossier/<topic>/<slug>.json), or else by a backticked slug
   of the document's topic (docs/<topic>/...) or a backticked <topic>/<slug> together with the provider
   name in its first cell (a list item's leading bold, link or code text), matched against every record's
   provider and slug, in the document's topic when the name has records there. A first cell that names
   several providers ("A, B and C") ties the row to each when every name is known. A cell cut short
   ("... as free bulk...") or giving the leading words of a long provider name ties to the one provider
   name of the topic it begins; a provider name with more words after it ("Defguard server") ties to that
   provider, but a part of a provider name does not. A name shared by hosted and self-hosted records ties
   to the records whose whole provider it is ("radicle", not "radicle (+ public seed nodes)"), and to
   nothing when those are mixed too. A row whose every record is self-hosted, or whose first cell (a list
   item's text up to its colon) says (self-hosted), is a self-hosted row, even when it ties to no record; a
   hosted provider's row that mentions a self-hosted tool in backticks is a hosted row. A self-hosted row
   above a hosted row of the same list is a defect; so is a self-hosted row that carries a recommendation
   (a star, "recommended", "best", "top pick", "start with", "first choice", "winner") or that does not say
   it is self-hosted or self-run (the convention: its first cell says (self-hosted)).
2. Prose: a sentence that names a self-hosted record (a record path, a backticked slug, a bold or linked
   name, or the provider name of a self-hosted record as written: four or more characters with a capital
   or a digit, standing for self-hosted records alone, and not the start of a longer hosted name) says in
   that sentence that it is self-hosted, self-run or the last resort, when it is a sentence of a paragraph
   that carries a star or opens "The answer", or when it carries a recommendation word itself.
3. Needs: every need of scripts/fshy/rules/needs.json, in the order `fr need` gives it, over the public
   store (.tmp/fshy/public.db, which the gate's projection check builds just before this one; it is built
   here only when it is missing or older than an input). A self-hosted row above a hosted row is a defect,
   and so is a store whose self_hosted column disagrees with the records. This guards fr.need_rows, the
   ordering every need goes through; the public Worker's order has its own test there.
4. Records: a record whose category says self-hosted or self-hostable, or whose tooling is exactly
   "self-hosted binaries", carries a self_hosted value: true, or false for a reviewed hosted lane (a
   public relay, a managed tier). No wording exempts it, and an unmarked one would sort among the hosted
   rows unreviewed. A record marked true carries a reason a reader can check: its own text says the user
   installs, runs or supplies what it offers, or the ledger entry that set the marker cites a capture or
   a source other than an inherited corpus card.

It reads the documents once, every dossier record, and one store. Exit codes: 0 clean, 1 a list, a need
or a record breaks the rule, 2 usage.

  python scripts/self-hosted-last.py --root .
  python scripts/self-hosted-last.py --selftest
"""
import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {"sources", "fixtures", ".tmp", ".git", "node_modules", "target", "dist"}
REF = re.compile(r"dossier/([a-z0-9-]+)/([a-z0-9][a-z0-9-]*)\.json")
SPEC = re.compile(r"<!-- generated:start([^>]*)-->")
ITEM = re.compile(r"\s*(?:\||[-*+] |\d+[.)] )")
RECOMMEND = re.compile(r"★|⭐|\brecommend(?:s|ed|ation)?\b|\bbest\b(?!-effort| per\b)|\btop pick\b|"
                       r"\bstart with\b|\bfirst choice\b|\bwinner\b", re.I)
SLUG = re.compile(r"`(?:([a-z0-9-]+)/)?([a-z0-9][a-z0-9-]*)`")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
LABEL = re.compile(r"\((?:self[- ]hosted|self[- ]run)[^)]*\)", re.I)
LEAD = re.compile(r"\s*(?:[-*+]|\d+[.)])\s+(?:\*\*([^*]+)\*\*|\[([^\]]+)\]\([^)]*\)|`([^`]+)`)")
SEP = re.compile(r"\s*\|[\s:|-]+\|?\s*$")
SH_TEXT = re.compile(r"self[- ]host", re.I)
SAYS = re.compile(r"\bself[- ](?:hosted|run)\b", re.I)
LAST = re.compile(r"\bself[- ](?:hosted|run)\b|\blast resort\b", re.I)
STAR = re.compile(r"[★⭐]")
ANSWER = re.compile(r"\W*the answer\b", re.I)
# an evidence line that only says the record came from an inherited catalogue card, not from the vendor
CARD = re.compile(r"corpus card|the card is the source", re.I)
# a record's own words that the user installs, runs or supplies what it offers
STATES = re.compile(r"self[- ]?host|self[- ]run|user[- ]run|on[- ]prem|\binstall|\blicen[cs]e\b|"
                    r"\b(?:user|client|customer|reader|operator)['’]s own\b|\byour own\b|\bthe (?:user|client) runs\b|"
                    r"\bown (?:hardware|machines?|computers?|cluster|gpus?|aws|cloud account)\b|"
                    r"\bruns? locally\b|\blocal (?:process|server|daemon|node|machine|runtime|app|engine)|\b(?:desktop|windows|mobile) app|"
                    r"\ban app\b|\bclient (?:software|librar|app|tool)|\bbring the computers\b|"
                    r"\bcontribut\w* (?:hardware|compute|gpus?)\b|\bseed(?:ing|er|s)?\b|\bpeer-to-peer\b|\bp2p\b|"
                    r"\bnode operator\b", re.I)


# ------------------------------------------------------------------ documents --

def documents(root):
    out = []
    docs = os.path.join(root, "docs")
    for dirpath, dirnames, files in os.walk(docs):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP)
        out += [os.path.join(dirpath, f) for f in sorted(files) if f.endswith(".md")]
    if os.path.isdir(root):
        out += [os.path.join(root, f) for f in sorted(os.listdir(root))
                if f.endswith(".md") and os.path.isfile(os.path.join(root, f))]
    return out


def lists(text):
    """[(first line number, [(line number, line, topic of its generated block or None)])]: runs of table rows
    and list items. An indented line continues the item above it; any other line ends the run. Fenced code
    is not a list."""
    runs, cur, fence, topic = [], [], None, None
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if fence:
            if s.startswith(fence):
                fence = None
            continue
        if s.startswith(("```", "~~~")):
            fence = s[:3]
            if cur:
                runs.append(cur)
                cur = []
            continue
        m = SPEC.search(line)
        if m:
            topic = dict(t.split("=", 1) for t in m.group(1).split() if "=" in t).get("topic")
        if "<!-- generated:end" in line:
            topic = None
        if ITEM.match(line):
            cur.append((n, line, topic))
        elif cur and s and line[:1] in " \t" and not line.lstrip().startswith("|"):
            n0, prev, t0 = cur[-1]
            cur[-1] = (n0, prev + " " + s, t0)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def norm(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    return " ".join(re.sub(r"[^\w.+]+|_", " ", s).replace(". ", " ").split()).strip(" .")


def name_keys(rec, slug):
    """The names a document may give a record: its provider, the provider's parts, and its slug."""
    prov = rec.get("provider") if isinstance(rec.get("provider"), str) else ""
    keys = {norm(slug.replace("-", " ")), norm(prov), norm(prov.split("(")[0])}
    for part in re.split(r"\s+(?:/|—|–|\+)\s+|\s*\(", prov):
        keys.add(norm(part.rstrip(")")))
    return {k for k in keys if len(k) >= 2}


class Records:
    """Every dossier record: its self_hosted flag, and the names and slugs a document may use for it."""

    def __init__(self, root):
        self.flag, self.recs, self.names, self.slugs = {}, {}, {}, {}
        self._plain = self._plain_by = None
        self._full = {}  # topic or None -> {normalised whole provider name: {rid}}, for a cut-short cell
        self.main = set()  # the whole names (provider, provider before its parenthesis, slug), not their parts
        base = os.path.join(root, "dossier")
        for topic in sorted(os.listdir(base)) if os.path.isdir(base) else []:
            d = os.path.join(base, topic)
            if not os.path.isdir(d):
                continue
            for f in sorted(os.listdir(d)):
                if not f.endswith(".json") or f.endswith(".generated.json"):
                    continue
                rid, slug = "%s/%s" % (topic, f[:-5]), f[:-5]
                try:
                    with open(os.path.join(d, f), encoding="utf-8") as fh:
                        rec = json.load(fh)
                except (OSError, ValueError):
                    continue
                if not isinstance(rec, dict):
                    continue
                self.recs[rid] = rec
                self.flag[rid] = rec.get("self_hosted") is True
                self.slugs.setdefault(topic, set()).add(slug)
                for k in name_keys(rec, slug):
                    self.names.setdefault(k, set()).add(rid)
                prov = rec.get("provider") if isinstance(rec.get("provider"), str) else ""
                self.main.update(k for k in (norm(prov), norm(prov.split("(")[0]), norm(slug.replace("-", " "))) if k)

    def is_self_hosted(self, rid):
        return self.flag.get(rid)  # None for a dangling path: the links check's defect, not this one's

    def by_name(self, cell, topic):
        """The records a provider cell names, in the document's topic when the name has records there; [] when
        the name is unknown or its records are hosted and self-hosted both."""
        text = LABEL.sub("", LINK.sub(r"\1", cell)).replace("**", "").replace("`", "").strip(" *_★⭐")
        for cand in (text, text.split("(")[0], re.split(r"\s+[—–:]\s+", text)[0]):
            got = self.one_name(cand, topic)
            if got is not None:
                return got
        # a cell that names several providers ("A, B and C as ...") ties the row to every one, but only when each
        # name is known and stands for hosted or self-hosted records alone
        head = re.split(r"\s+[—–:]\s+|:\s", text)[0]
        parts = [p.strip() for p in re.split(r",\s+(?:and\s+|or\s+)?|\s+(?:and|or)\s+", head) if p.strip()]
        rids = []
        for p in parts if len(parts) > 1 else ():
            got = self.one_name(p, topic)
            if got is None and " " in p:
                got = self.one_name(p.split(" ")[0], topic)
            if not got:
                rids = []
                break
            rids += [r for r in got if r not in rids]
        if rids:
            return rids
        # a long provider name cut short ("hyperswarm / hyperdht blind relay as free bulk...") or given by its leading
        # words ("JuiceFS community edition"), then a provider name with more words after it ("Defguard server")
        return self.prefix_of(text, topic) or self.word_prefix(text, topic)

    def full_names(self, topic):
        """{normalised whole provider name: {rid}} of the topic's records (of every record when topic is None)."""
        if topic not in self._full:
            by = {}
            for rid, rec in self.recs.items():
                prov = rec.get("provider") if isinstance(rec.get("provider"), str) else ""
                if prov and (topic is None or rid.split("/")[0] == topic):
                    by.setdefault(norm(prov), set()).add(rid)
            self._full[topic] = by
        return self._full[topic]

    def prefix_of(self, text, topic):
        """The records of the one provider name in the topic that the cell, less a trailing '...' or '…', begins: a
        name cut short. Two words and eight characters at least, ending on a word of the name; [] when no name or
        more than one fits, or its records are hosted and self-hosted both."""
        c = norm(re.sub(r"\s*(?:\.\.\.|…)\s*$", "", text))
        if len(c) < 8 or " " not in c:
            return []
        names = self.full_names(topic if topic in self.slugs else None)
        fit = [k for k in names if k.startswith(c) and (len(k) == len(c) or k[len(c)] == " ")]
        if len(fit) != 1:
            return []
        rids = sorted(names[fit[0]])
        return rids if len({self.flag[r] for r in rids}) == 1 else []

    def word_prefix(self, text, topic):
        """A provider name with more words after it ("Defguard server"): the longest leading run of words, five
        characters at least, that is a known name. Not for a cell that lists several names."""
        if re.search(r",|\s(?:and|or|/|\+|&)\s", text):
            return []
        words = norm(text.split("(")[0]).split()
        for i in range(len(words) - 1, 0, -1):
            cand = " ".join(words[:i])
            if len(cand) < 5:
                break
            if cand not in self.main:
                continue  # a part of a provider name ("WebDAV" of "DVC remotes (S3 / WebDAV / ...)") is not one
            got = self.one_name(cand, topic)
            if got is not None:
                return got
        return []

    def plain_names(self, s, topic):
        """The self-hosted records whose provider name s carries as written, in the document's topic when the name
        has records there. Only a name of four or more characters with a capital or a digit, that stands for
        self-hosted records alone, is looked for: a common word is not a provider. A longer hosted provider name
        that starts with it wins ("Windmill Cloud" is not "Windmill")."""
        if self._plain_by is None:
            by, hosted = {}, set()
            for rid, rec in self.recs.items():
                prov = rec.get("provider") if isinstance(rec.get("provider"), str) else ""
                if not prov:
                    continue
                main = prov.split("(")[0].strip()  # a parenthesis names what it runs over, not the provider
                names = {main} | {p.strip() for p in re.split(r"\s+(?:/|—|–|\+)\s+", main)}
                for name in names:
                    if len(name) < 4 or not re.search(r"[A-Z0-9]", name):
                        continue
                    got = self.one_name(name, None)
                    if not got:
                        continue
                    if all(self.flag[r] for r in got):
                        if self.flag[rid]:
                            by.setdefault(name, set()).add(rid)
                    elif not any(self.flag[r] for r in got):
                        hosted.add(name)
            self._plain_by = by
            alt = "|".join(sorted(map(re.escape, set(by) | (hosted - set(by))), key=len, reverse=True))
            self._plain = re.compile(r"(?<![\w-])(%s)(?![\w-])" % alt) if alt else None
        out = []
        for m in self._plain.finditer(s) if self._plain else ():
            if m.group(1) not in self._plain_by:
                continue  # a hosted provider's name
            rids = sorted(self._plain_by[m.group(1)])
            out += [r for r in rids if r.split("/")[0] == topic] or rids
        return out

    def one_name(self, cand, topic):
        """The records one name stands for, in the document's topic when it has records there; None when the name is
        unknown. A name shared by hosted and self-hosted records stands for the records whose whole provider it is
        ("radicle", not "radicle (+ public seed nodes)"), and for nothing when those are mixed too."""
        key = norm(cand)
        rids = self.names.get(key)
        if not rids:
            return None
        here = {r for r in rids if r.split("/")[0] == topic}
        rids = sorted(here or rids)
        if len({self.flag[r] for r in rids}) == 1:
            return rids
        whole = [r for r in rids if norm(self.recs[r].get("provider") if isinstance(self.recs[r].get("provider"), str)
                                          else "") == key]
        return whole if whole and len({self.flag[r] for r in whole}) == 1 else []


def first_cell(line):
    """The cell that names the provider: a table row's first cell that is not a number or a rank, or a list
    item's leading bold, link or code text. None when the row has no such cell."""
    if line.lstrip().startswith("|"):
        for c in [c.strip() for c in line.strip().strip("|").split("|")]:
            if c and not re.fullmatch(r"[#\d.:)\s-]*", c):
                return c
        return None
    m = LEAD.match(line)
    return next((g for g in m.groups() if g), None) if m else None


def rids_of(line, topic, recs=None, doc_topic=None):
    """The records one row names: record paths; a generated shortlist's last-cell slug (its block's topic);
    else backticked slugs of the document's topic, or backticked <topic>/<slug>, together with the provider
    name of its first cell. A hosted provider's row that mentions a self-hosted tool in backticks is tied to
    both, so it is not a self-hosted row."""
    rids = ["%s/%s" % m for m in REF.findall(line)]
    if not rids and topic and line.lstrip().startswith("|"):
        # a generated shortlist names its record by slug in the last cell
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        m = re.fullmatch(r"`([a-z0-9][a-z0-9-]*)`", cells[-1]) if cells else None
        if m:
            rids = ["%s/%s" % (topic, m.group(1))]
    if rids or recs is None:
        return rids
    for t, slug in SLUG.findall(line):
        t = t or doc_topic
        if t and slug in recs.slugs.get(t, ()) and "%s/%s" % (t, slug) not in rids:
            rids.append("%s/%s" % (t, slug))
    if not SEP.match(line):
        cell = first_cell(line)
        # a first cell that is itself a backticked slug already named its record: its words are not a name too
        lead = re.fullmatch(r"`?(?:[a-z0-9-]+/)?([a-z0-9][a-z0-9-]*)`?", (cell or "").strip())
        if cell and not (lead and any(r.endswith("/" + lead.group(1)) for r in rids)):
            rids += [r for r in recs.by_name(cell, doc_topic) if r not in rids]
    return rids


def head_of(line):
    """Where a row says what it is: a table row's first cell, or a list item's text up to its first colon or dash
    ("- `openlist` (self-hosted): ...")."""
    if line.lstrip().startswith("|"):
        return first_cell(line) or ""
    return re.split(r":\s|\s[—–]\s", line, maxsplit=1)[0]


def check_list(rows, is_self_hosted):
    """rows: [(line number, line, [rid, ...])] of one list. -> [(line number, why, line)]."""
    hits, first_sh, ordered = [], None, True
    for n, line, rids in rows:
        if rids is None:
            continue  # a table's header row
        # a row its first cell labels (self-hosted) is a self-hosted row, whatever else it names, and even when
        # it ties to no record: the label is the document's own word
        labelled = bool(LABEL.search(head_of(line)))
        if not rids and not labelled:
            continue
        flags = [is_self_hosted(r) for r in rids]
        if None in flags:
            continue
        if labelled or all(flags):
            if first_sh is None:
                first_sh = n
            m = RECOMMEND.search(line)
            if m:
                hits.append((n, "a self-hosted row recommends it (%r)" % m.group(0), line))
            elif not SAYS.search(line):
                hits.append((n, "a self-hosted row does not say so: label its first cell (self-hosted)", line))
        elif first_sh is not None and ordered:
            hits.append((n, "a hosted row below the self-hosted row of line %d" % first_sh, line))
            ordered = False  # one order defect per list: the first hosted row below a self-hosted one
    return hits


def check_documents(root, recs=None):
    recs = recs or Records(root)
    hits, nlists, named = [], 0, set()
    for path in documents(root):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        rel = os.path.relpath(path, root).replace("\\", "/")
        parts = rel.split("/")
        doc_topic = parts[1] if len(parts) > 2 and parts[0] == "docs" and parts[1] in recs.slugs else None
        for run in lists(text):
            # a table's header row (the row above its |---| row) names columns, not records
            head = {i - 1 for i, (_, line, _) in enumerate(run) if i and SEP.match(line)}
            rows = [(n, line, None if i in head else rids_of(line, topic, recs, doc_topic))
                    for i, (n, line, topic) in enumerate(run)]
            if not any(r or (r is not None and LABEL.search(head_of(line))) for _, line, r in rows):
                continue
            nlists += 1
            named.update(r for _, _, rr in rows for r in rr or () if recs.is_self_hosted(r))
            for n, why, line in check_list(rows, recs.is_self_hosted):
                hits.append({"file": rel, "line": n, "why": why, "text": line.strip()[:150]})
        for n, why, s in check_prose(text, recs, doc_topic):
            hits.append({"file": rel, "line": n, "why": why, "text": s.strip()[:150]})
    return hits, nlists, len(named)


def paragraphs(text):
    """[(first line number, text)]: the prose blocks of a page. A list, a table, a heading, an HTML comment and
    fenced code are not prose, and neither is a line that continues a list item."""
    out, cur, mode, fence = [], [], None, None

    def flush():
        if cur:
            out.append((cur[0][0], " ".join(s for _, s in cur)))
            cur.clear()
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if fence:
            if s.startswith(fence):
                fence = None
            continue
        if s.startswith(("```", "~~~")):
            flush()
            fence, mode = s[:3], None
            continue
        if not s:
            flush()
            mode = None
        elif ITEM.match(line) or s.startswith(("#", "<!--")) or (mode != "prose" and line[:1] in " \t"):
            flush()
            mode = "list" if ITEM.match(line) else None
        elif mode != "list":
            mode = "prose"
            cur.append((n, s[1:].strip() if s.startswith(">") else s))
    flush()
    return out


def sentences(para):
    """The sentences of one paragraph. A bold claim that ends in a full stop inside its ** is one sentence."""
    t = re.sub(r"\b(?:e\.g|i\.e|vs|etc|approx)\.", lambda m: m.group(0).replace(".", "\x00"), para)
    return [p.replace("\x00", ".") for p in re.split(r"(?<=[.!?]\*\*)\s+|(?<=[.!?])\s+(?=[^\s*])", t) if p.strip()]


def prose_rids(s, recs, doc_topic):
    """The records one sentence names: record paths, backticked slugs of the document's topic or backticked
    <topic>/<slug>, and the bold or linked provider names it carries."""
    rids = ["%s/%s" % m for m in REF.findall(s)]
    for t, slug in SLUG.findall(s):
        t = t or doc_topic
        if t and slug in recs.slugs.get(t, ()) and "%s/%s" % (t, slug) not in rids:
            rids.append("%s/%s" % (t, slug))
    for m in re.finditer(r"\*\*([^*]+)\*\*|\[([^\]]+)\]\([^)]*\)", s):
        rids += [r for r in recs.one_name(LABEL.sub("", m.group(1) or m.group(2)), doc_topic) or () if r not in rids]
    for rid in recs.plain_names(s, doc_topic):
        if rid not in rids:
            rids.append(rid)
    return rids


def check_prose(text, recs, doc_topic):
    """A sentence that names a self-hosted record must say in that sentence that it is self-hosted (self-hosted,
    self-run or last resort) when it is a sentence of a starred paragraph (a star anywhere in it), of a paragraph
    that opens "The answer", or when it carries a recommendation word ("best", "recommended", "start with",
    "first choice" and the like) itself: a star, an answer or a recommendation never presents one as the pick.
    -> [(line number, why, sentence)]."""
    hits = []
    for n, para in paragraphs(text):
        kind = "an answer" if ANSWER.match(para) else "a starred" if STAR.search(para) else None
        for s in sentences(para):
            word = None if kind else RECOMMEND.search(s)
            if not kind and not word:
                continue
            sh = [r for r in prose_rids(s, recs, doc_topic) if recs.is_self_hosted(r)]
            if sh and not LAST.search(s):
                where = ("of %s paragraph" % kind) if kind else "that recommends (%r)" % word.group(0)
                hits.append((n, "a sentence %s names self-hosted %s and does not say it is self-hosted or the last "
                             "resort" % (where, sh[0]), s))
    return hits


def check_records(recs):
    """Records whose own category or tooling says self-hosted and that carry no self_hosted marker. A record that
    names a hosted lane says self_hosted: false, the reviewed-hosted marker; no wording exempts it."""
    hits = []
    for rid, rec in sorted(recs.recs.items()):
        if "self_hosted" in rec:
            continue  # marked, or reviewed and kept hosted (false)
        cat = rec.get("category") if isinstance(rec.get("category"), str) else ""
        tooling = rec.get("tooling") if isinstance(rec.get("tooling"), str) else ""
        if not (SH_TEXT.search(cat) or tooling.strip().rstrip(".") == "self-hosted binaries"):
            continue
        hits.append({"file": "dossier/%s.json" % rid, "line": 0,
                     "why": "its category or tooling says self-hosted, and it has no self_hosted marker (true, or "
                            "false for a reviewed hosted lane)",
                     "text": (cat or tooling)[:150]})
    return hits


def last_marks(root):
    """{rid: the last ledger entry that set $.self_hosted} from history/ledger.jsonl."""
    out = {}
    try:
        with open(os.path.join(root, "history", "ledger.jsonl"), encoding="utf-8") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if isinstance(e, dict) and e.get("path") == "$.self_hosted":
                    out[e.get("rid")] = e
    except OSError:
        pass
    return out


def record_text(rec):
    """The prose of a record a reader sees: what it is, what is free, its limits and notes."""
    parts = [rec.get(k) for k in ("category", "tooling", "chaining", "binding_note", "interface_detail",
                                  "limits_note", "confidence_note", "reliability_note", "notes")]
    ft = rec.get("free_tier") if isinstance(rec.get("free_tier"), dict) else {}
    parts += [ft.get("stated"), ft.get("notes")]
    parts += [lim.get("value") for lim in rec.get("limits") or () if isinstance(lim, dict)]
    return " ".join(p for p in parts if isinstance(p, str))


def check_marks(recs, root):
    """A self_hosted: true marker carries its reason: the record's own text says the user runs it (STATES), or the
    ledger entry that set it cites a source of its own, a capture or a page other than an inherited corpus card. A
    marker set on a card line alone, with nothing in the record to say why, is a guess a reader cannot check."""
    marks, hits = last_marks(root), []
    for rid, rec in sorted(recs.recs.items()):
        if rec.get("self_hosted") is not True:
            continue
        ev = (marks.get(rid) or {}).get("evidence") or {}
        if ev.get("capture") or (rid in marks and not CARD.search(ev.get("proved") or "")):
            continue
        if STATES.search(record_text(rec)):
            continue
        hits.append({"file": "dossier/%s.json" % rid, "line": 0,
                     "why": "self_hosted is true with no reason a reader can check: the record does not say the user "
                            "runs it, and the marker's ledger entry cites only %s" %
                            ("an inherited corpus card" if rid in marks else "nothing"),
                     "text": (ev.get("url") or rec.get("category") or "")[:150]})
    return hits


# ---------------------------------------------------------------------- needs --

def check_order(names, flags):
    """names and self_hosted flags of one list, in list order -> the first name of a hosted row that follows a
    self-hosted one, or None."""
    seen = None
    for name, sh in zip(names, flags):
        if sh and seen is None:
            seen = name
        elif not sh and seen is not None:
            return name, seen
    return None


def fresh_store(root, path, fr):
    """The public store at path, built when it is missing, older than an input, or without the column."""
    why = None
    if not os.path.exists(path):
        why = "missing"
    elif fr.newest_input(root)[0] > os.stat(path).st_mtime:
        why = "older than an input"
    else:
        try:
            db = sqlite3.connect("file:%s?mode=ro" % path.replace("\\", "/"), uri=True)
            cols = {r[1] for r in db.execute("SELECT * FROM pragma_table_info('record')")}
            db.close()
            if "self_hosted" not in cols:
                why = "without record.self_hosted"
        except sqlite3.Error as e:
            why = "unreadable (%s)" % e
    if why:
        import build  # noqa: E402  (imported late: only a rebuild needs it)
        devnull, old = open(os.devnull, "w"), sys.stdout
        sys.stdout = devnull
        try:
            build.build(root, path, "public", None)
        finally:
            sys.stdout = old
            devnull.close()
    return why


def check_needs(root, store):
    sys.path.insert(0, os.path.join(HERE, "fshy"))
    import fr  # noqa: E402
    path = store or os.path.join(root, ".tmp", "fshy", "public.db")
    built = fresh_store(root, path, fr)
    st = fr.Store(path, root)
    hits = []
    try:
        bad = st.q("SELECT rid, self_hosted, json_extract(doc, '$.self_hosted') FROM record WHERE doc IS NOT NULL "
                   "AND self_hosted <> (CASE json_extract(doc, '$.self_hosted') WHEN 1 THEN 1 ELSE 0 END)")
        for rid, col, doc in bad[:20]:
            hits.append({"file": "store", "line": 0, "why": "record.self_hosted %s, the record says %s" % (col, doc),
                         "text": rid})
        sh = fr.CARD_COLS.index("self_hosted") + 1
        needs = fr.load_needs()
        for n in needs:
            rows = fr.need_rows(st, n)
            got = check_order([r[1] for r in rows], [r[sh] == "yes" for r in rows])
            if got:
                hits.append({"file": "need", "line": 0, "why": "hosted %s below self-hosted %s" % got,
                             "text": n["id"]})
        n_sh = st.one("SELECT count(*) FROM record WHERE self_hosted = 1")
    finally:
        st.close()
    return hits, len(needs), n_sh, built


# -------------------------------------------------------------------- selftest --

def selftest():
    fails = []

    def say(ok, name):
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails.append(name)

    tmp = tempfile.mkdtemp(prefix="self-hosted-last.")
    try:
        os.makedirs(os.path.join(tmp, "dossier", "egress"))
        os.makedirs(os.path.join(tmp, "docs"))
        os.makedirs(os.path.join(tmp, "docs", "egress"))
        for slug, sh, prov in (("hosted-a", False, None), ("hosted-b", False, None), ("tool-c", True, None),
                               ("acme-cloud", False, "Acme Cloud"), ("toolbox-oss", True, "Toolbox (open source)"),
                               ("dual-hosted", False, "Dual"), ("dual-self", True, "Dual"),
                               ("long-relay", True, "Longname relay as a free bulk infrastructure"),
                               ("shared", True, "Shared"), ("shared-plus", False, "Shared (+ public nodes)"),
                               ("remotes", True, "Remotes (S3 / Gizmo / SSH)"), ("toolbox-cloud", False, "Toolbox Cloud")):
            rec = {"topic": "egress", "slug": slug, "provider": prov or slug, "verdict": "qualifies"}
            if sh:
                rec["self_hosted"] = True
            with open(os.path.join(tmp, "dossier", "egress", slug + ".json"), "w", encoding="utf-8") as fh:
                json.dump(rec, fh)
        say(len(os.listdir(os.path.join(tmp, "dossier", "egress"))) == 12, "the fixture records landed")
        row = lambda s, extra="": "| %s | `dossier/egress/%s.json` |%s" % (s, s, extra)

        def run(body, rel=("docs", "a.md"), labels=False, head="| provider | record |\n| --- | --- |\n"):
            """The hits of one page. Unless labels, a missing (self-hosted) label is left out, so the order and
            recommendation cases read alone."""
            for f in (("docs", "a.md"), ("docs", "egress", "b.md")):
                if os.path.exists(os.path.join(tmp, *f)):
                    os.remove(os.path.join(tmp, *f))
            with open(os.path.join(tmp, *rel), "w", encoding="utf-8", newline="\n") as fh:
                fh.write("# a page\n\n" + head + body + "\ntail\n")
            hits, n, named = check_documents(tmp)
            return [h for h in hits if labels or "does not say so" not in h["why"]], n, named

        def run_t(body, **kw):  # a page of the egress topic
            return run(body, ("docs", "egress", "b.md"), **kw)

        def prose(body, **kw):  # a page of prose, no table
            return run_t(body, head="", labels=True, **kw)[0]

        hits, n, _ = run("\n".join([row("hosted-a"), row("hosted-b"), row("tool-c")]))
        say(n == 1 and not hits, "a list with the self-hosted row last passes")
        hits, _, _ = run("\n".join([row("tool-c"), row("hosted-a"), row("hosted-b")]))
        say(len(hits) == 1 and hits[0]["line"] == 6 and "below the self-hosted" in hits[0]["why"],
            "a self-hosted row above a hosted row is refused, on the first hosted row")
        hits, _, _ = run("\n".join([row("hosted-a"), row("tool-c", " best free tunnel |")]))
        say(len(hits) == 1 and "recommends" in hits[0]["why"], "a self-hosted row that says best is refused")
        hits, _, _ = run("\n".join([row("hosted-a", " ★ qualifies |"), row("tool-c")]))
        say(not hits, "a star on a hosted row is not this check's business")
        hits, _, _ = run("- [c](dossier/egress/tool-c.json)\n  continues the item\n- [a](dossier/egress/hosted-a.json)")
        say(len(hits) == 1, "a list item with a continuation line is one item, and its order is checked")
        hits, _, _ = run("```text\n" + row("tool-c") + "\n" + row("hosted-a") + "\n```")
        say(not hits, "a fenced code sample is not a list")
        hits, _, _ = run(row("tool-c") + "\n\nsome prose\n\n" + row("hosted-a"))
        say(not hits, "two lists split by prose are checked apart")
        hits, _, _ = run("<!-- generated:start topic=egress kind=shortlist -->\n| 1 | C | `tool-c` |\n"
                         "| 2 | A | `hosted-a` |\n<!-- generated:end -->")
        say(len(hits) == 1, "a generated shortlist row is resolved by its block's topic and checked")
        hits, _, _ = run(row("tool-c") + "\n| x | `dossier/egress/missing.json` |\n" + row("hosted-a"))
        say(len(hits) == 1, "a dangling record path is skipped, not counted as hosted or self-hosted")
        say(check_order(["a", "b", "c"], [False, False, True]) is None and
            check_order(["c", "a"], [True, False]) == ("a", "c"), "the need order check")
        # rows tied to records by name or by a backticked slug, with no record path
        hits, _, _ = run("| Toolbox | x |\n| Acme Cloud | y |")
        say(len(hits) == 1 and hits[0]["line"] == 6, "a row is tied to its record by the provider name of its first cell")
        hits, _, _ = run("| Acme Cloud | y |\n| Toolbox (self-hosted) | x |")
        say(not hits and rids_of("| Toolbox (self-hosted) | x |", None, Records(tmp), None) == ["egress/toolbox-oss"],
            "a provider name with the (self-hosted) label still resolves, and last is fine")
        hits, _, _ = run("| 1 | **[Toolbox](https://example.org)** | x |\n| 2 | Acme Cloud | y |")
        say(len(hits) == 1, "a rank cell is skipped, and a bold link names the provider")
        hits, _, _ = run("| Dual | x |\n| Acme Cloud | y |")
        say(not hits, "a name whose records are hosted and self-hosted both ties the row to nothing")
        hits, _, _ = run("| Nobody Inc | x |\n| Toolbox | y |\n| Acme Cloud | z |")
        say(len(hits) == 1 and hits[0]["line"] == 7, "an unknown name is skipped and the rest is checked")
        hits, _, _ = run_t("| x | `tool-c` |\n| y | `hosted-a` |")
        say(len(hits) == 1, "a backticked slug of the document's topic ties a hand-written row")
        hits, _, _ = run("| x | `tool-c` |\n| y | `hosted-a` |")
        say(not hits, "a bare backticked slug outside a topic's documents ties nothing")
        hits, _, _ = run("| x | `egress/tool-c` |\n| y | `egress/hosted-a` |")
        say(len(hits) == 1, "a backticked <topic>/<slug> ties a row anywhere")
        with open(os.path.join(tmp, "docs", "a.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# a page\n\n| Toolbox | Dual |\n| --- | --- |\n| Acme Cloud | y |\n")
        hits, _, _ = check_documents(tmp)
        say(not hits, "a table's header row names columns, not records")
        hits, _, _ = run("- **Toolbox**: x\n- **Acme Cloud**: y")
        say(len(hits) == 1, "a list item is tied to its record by its leading bold text")
        hits, _, _ = run("| Acme Cloud | y |\n| Toolbox | a best-effort relay, best per need |")
        say(not hits, "best-effort and best per are not recommendations")
        hits, _, _ = run("| Acme Cloud | y |\n| Toolbox | the best relay |")
        say(len(hits) == 1 and "recommends" in hits[0]["why"], "a self-hosted row tied by name that says best is refused")
        # labels: a self-hosted row says so
        hits, _, _ = run("| Acme Cloud | y |\n| Toolbox | x |", labels=True)
        say(len(hits) == 1 and "does not say so" in hits[0]["why"] and hits[0]["line"] == 6,
            "a self-hosted row with no (self-hosted) label is refused")
        hits, _, _ = run("| Acme Cloud | y |\n| Toolbox (self-hosted) | x |\n| x | `egress/tool-c`, a self-run relay |",
                         labels=True)
        say(not hits, "a row that says (self-hosted) or self-run passes")
        hits, _, _ = run_t("| Acme Cloud | via `tool-c` |\n| Toolbox (self-hosted) | x |", labels=True)
        say(not hits, "a hosted provider's row that mentions a self-hosted tool in backticks is a hosted row")
        hits, _, _ = run_t("| Toolbox (self-hosted) | x |\n| Acme Cloud | via `tool-c` |", labels=True)
        say(len(hits) == 1 and "below the self-hosted" in hits[0]["why"], "and it may not sit below a self-hosted row")
        hits, _, _ = run("| Acme Cloud (self-hosted) | x |\n| `dossier/egress/hosted-a.json` | y |", labels=True)
        say(len(hits) == 1 and "below the self-hosted" in hits[0]["why"],
            "a first cell labelled (self-hosted) makes the row self-hosted, whatever it names")
        recs = Records(tmp)
        say(recs.by_name("Acme Cloud and Toolbox", "egress") == ["egress/acme-cloud", "egress/toolbox-oss"] and
            recs.by_name("Toolbox, Acme Cloud and Nobody", "egress") == [] and
            recs.by_name("Toolbox, Hosted A", "egress") == ["egress/toolbox-oss", "egress/hosted-a"],
            "a cell that names several providers ties the row to each, and to nothing when one name is unknown")
        # prose: a starred or answer sentence that names a self-hosted record says so
        hits = prose("⭐ **Use Toolbox.** It is free.")
        say(len(hits) == 1 and "starred" in hits[0]["why"] and hits[0]["line"] == 3,
            "a starred sentence that names a self-hosted provider is refused")
        hits = prose("⭐ **Use Acme Cloud.** Toolbox is free and runs anywhere.")
        say(len(hits) == 1, "every sentence of a starred paragraph is read, not the starred one alone")
        hits = prose("⭐ **Use Acme Cloud.** Toolbox (self-hosted) is the last resort.\n\nToolbox is free.")
        say(not hits, "a sentence that says self-hosted passes, and a plain paragraph is not read")
        hits = prose("The answer, in one paragraph. `tool-c` relays it for free.")
        say(len(hits) == 1 and "answer" in hits[0]["why"], "an answer paragraph that names a self-hosted slug is refused")
        hits = prose("The answer: the self-run `tool-c` is the last resort, after `hosted-a`.")
        say(not hits, "an answer sentence that calls the self-hosted record the last resort passes")
        hits = prose("- ⭐ **Toolbox (self-hosted)**: x\n- **Acme Cloud**: y\n\n```\n⭐ Toolbox\n```")
        say(not [h for h in hits if "sentence" in h["why"]], "a list item and fenced code are not prose")
        hits = prose("⭐ toolbox, tooling and a toolbox-oss build are words, not the provider.")
        say(not hits, "a provider name is matched as written, so a common word is not a provider")
        # a name cut short, a shared name, a name with more words, and a labelled row that ties to nothing
        hits, _, _ = run("| Longname relay as a free bulk... | x |\n| Acme Cloud | y |")
        say(len(hits) == 1 and "below the self-hosted" in hits[0]["why"],
            "a cell cut short with '...' ties to the one provider name it begins")
        hits, _, _ = run("| Longname relay as a free | x |\n| Acme Cloud | y |")
        say(len(hits) == 1, "a cell that is the leading words of one provider name ties to it")
        hits, _, _ = run("| Longname | x |\n| Acme Cloud | y |")
        say(not hits, "a single word that only begins a provider name ties to nothing")
        hits, _, _ = run("| Shared | x |\n| Acme Cloud | y |")
        say(len(hits) == 1 and Records(tmp).by_name("Shared", "egress") == ["egress/shared"],
            "a name shared by a hosted and a self-hosted record ties to the record whose whole provider it is")
        hits, _, _ = run("| Toolbox server | x |\n| Acme Cloud | y |")
        say(len(hits) == 1, "a provider name with more words after it ties to the provider")
        hits, _, _ = run("| Gizmo is advertised on the free tier | x |\n| Acme Cloud | y |")
        say(not hits, "a part of a provider name with more words after it ties to nothing")
        hits, _, _ = run("| Acme Cloud | y |\n| Nobody, recommended (self-hosted) | x |")
        say(len(hits) == 1 and "recommends" in hits[0]["why"],
            "a row labelled (self-hosted) that ties to no record is still read for a recommendation")
        hits, _, _ = run("| Nobody (self-hosted) | x |\n| Acme Cloud | y |")
        say(len(hits) == 1 and "below the self-hosted" in hits[0]["why"],
            "a row labelled (self-hosted) that ties to no record still sorts after every hosted row")
        hits, _, _ = run("- `shared-plus` (self-hosted): x\n- **Acme Cloud**: y", labels=True)
        say(len(hits) == 1 and "below the self-hosted" in hits[0]["why"],
            "a list item labelled (self-hosted) after its lead is a self-hosted row")
        hits, _, _ = run_t("- `tool-c` (self-hosted): x\n- `shared` (self-hosted): y", labels=True)
        say(not hits, "a lead that is a backticked slug names its record, and its words are not read as a name too")
        hits = prose("Use **Toolbox** first: it is the best plan here.")
        say(len(hits) == 1 and "recommends" in hits[0]["why"],
            "a plain sentence that recommends a self-hosted record is refused")
        hits = prose("Toolbox (self-hosted) is the best of the last resorts. **Acme Cloud** is the best plan.")
        say(not hits, "a recommending sentence that says self-hosted passes, and a hosted pick passes")
        hits = prose("Toolbox Cloud is the best plan here, and **Acme Cloud** the next.")
        say(not hits, "a longer hosted provider name is not read as the self-hosted name it begins")
        # marks: a self_hosted marker carries a reason a reader can check
        os.makedirs(os.path.join(tmp, "history"))
        card = {"url": "https://example.org", "date": "2026-10-02",
                "proved": "listed in the peli-cloud corpus card at commit f6a71ab0; the card is the source, not the vendor page"}
        own = {"url": "https://example.org/pricing", "date": "2026-10-29", "proved": "the pricing page says it installs"}
        cap = dict(card, capture="sha256:" + "0" * 64, quote="x")
        with open(os.path.join(tmp, "history", "ledger.jsonl"), "w", encoding="utf-8", newline="\n") as fh:
            for rid, ev in (("egress/m-card", card), ("egress/m-text", card), ("egress/m-own", own),
                            ("egress/m-cap", cap)):
                fh.write(json.dumps({"rid": rid, "path": "$.self_hosted", "old": None, "new": True,
                                     "evidence": ev}) + "\n")
        mr = Records(tmp)
        for slug, text in (("m-card", "a platform host"), ("m-text", "the engine runs locally"), ("m-own", "a host"),
                           ("m-cap", "a host"), ("m-none", "a host"), ("m-hosted", "a host")):
            mr.recs["egress/" + slug] = {"category": text, "self_hosted": slug != "m-hosted"}
        got = sorted(h["file"] for h in check_marks(mr, tmp) if h["file"].startswith("dossier/egress/m-"))
        say(got == ["dossier/egress/m-card.json", "dossier/egress/m-none.json"],
            "a self_hosted marker set on an inherited card line, or on nothing, with no reason in the record is "
            "refused; a statement in the record, a source of its own or a capture passes (%s)" % got)
        # records: a category or tooling that says self-hosted needs a value, true or false
        for slug, rec in (("cat-sh", {"category": "tunnel software (self-hosted)"}),
                          ("tool-sh", {"category": "tunnel", "tooling": "self-hosted binaries"}),
                          ("relay", {"category": "tunnel software with a public relay", "tooling": "self-hosted binaries"}),
                          ("reviewed", {"category": "video platform, self-hosted instance", "self_hosted": False}),
                          ("marked", {"category": "tunnel software (self-hosted)", "self_hosted": True}),
                          ("lane", {"category": "tunnel (self-hostable)", "free_tier": {"stated": "a community relay"}})):
            recs.recs["egress/" + slug] = rec
        got = sorted(h["file"] for h in check_records(recs))
        say(got == ["dossier/egress/cat-sh.json", "dossier/egress/lane.json", "dossier/egress/relay.json",
                    "dossier/egress/tool-sh.json"],
            "a record whose category or tooling says self-hosted needs a self_hosted value; naming a hosted lane in "
            "words does not exempt it, false does (%s)" % got)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\nself-hosted-last selftest: %s" % ("0 failed" if not fails else "%d failed" % len(fails)))
    return 0 if not fails else 1


# ------------------------------------------------------------------------ main --

def main():
    ap = argparse.ArgumentParser(description="refuse a list that puts a self-hosted record above a hosted one")
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    ap.add_argument("--store", default=None, help="the store to read the needs from (default: .tmp/fshy/public.db)")
    ap.add_argument("--no-needs", action="store_true", help="check the documents only")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true", help="plant each defect and require it to be refused")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    if not os.path.isdir(os.path.join(root, "dossier")):
        print("self-hosted-last: no dossier/ under %s" % root, file=sys.stderr)
        return 2
    recs = Records(root)
    hits, nlists, n_named = check_documents(root, recs)
    hits += check_records(recs)
    hits += check_marks(recs, root)
    nneeds, n_sh, built = 0, None, None
    if not args.no_needs:
        h2, nneeds, n_sh, built = check_needs(root, args.store)
        hits += h2
    summary = ("%d list(s) or need(s) put a self-hosted record above a hosted one or recommend it, or record(s) lack "
               "the marker; checked %d lists that name records (%d self-hosted named), %d records and %d needs%s"
               % (len(hits), nlists, n_named, len(recs.recs), nneeds,
                  "" if n_sh is None else " over %d self-hosted records%s" % (n_sh, " (store built: %s)" % built
                                                                              if built else "")))
    if args.json:
        print(json.dumps({"hits": hits, "lists": nlists, "needs": nneeds, "self_hosted": n_sh}, indent=2))
    else:
        for h in hits:
            print("%s:%d  %s: %s" % (h["file"], h["line"], h["why"], h["text"]))
        print(summary)
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
