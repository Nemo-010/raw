"""Public projection of dossier records: drop process keys, rewrite operator URLs, map
boilerplate to unknown classes, and strip narrative, personal and legal clauses.

Every source leaf receives exactly one disposition: kept, modified, withheld or excluded.
Every change is logged as (rid, path, rule, before) so the local store can show it.
Standard library only.
"""
import collections
import fnmatch
import hashlib
import json
import re

DISPOSITIONS = ("kept", "modified", "withheld", "excluded")
URL_KEYS = {"url", "source_url", "source"}
TOP_SKIP = {"topic", "slug", "verdict", "confidence", "binding", "verified_at", "category", "tier", "provider"}
SPLIT = re.compile(r"(?<=[.;!?])\s+(?=[A-Z0-9\"'(\[`])|(?<=;)\s+")
CODE = re.compile(r"`[^`]*`")
WORDS = re.compile(r"[^\W_]+")
DEF = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")
# A clause that follows a withheld clause and only points back at it: an enumerated reading "(b) ...", a verdict
# word that answers a withheld question, or a demonstrative that refers to the withheld text. Kept alone it reads
# as a sentence with no antecedent, so it goes with the clause it depends on.
FOLLOWER = re.compile(r"^(?:\((?:[a-h]|[1-9]|i{1,3}|iv|v)\)\s|(?i:refuted|unresolved|not settled|settled|unsettled|confirmed|supported|"
                      r"weakened|excluded|rejected|holds|stands)\b|(?:[Tt]his|[Tt]hat|[Tt]hese|[Tt]hose|[Bb]oth|[Nn]either|[Ss]uch|[Nn]or)\b)")
# Quoted third-party text: a single quote that opens after a non-letter and closes before one (an apostrophe
# inside a word, as in "don't", does not close it), a double-quoted span, and the curly forms. A rule with
# skip_quoted reads the clause with these spans blanked, so a vendor's "we" or "I" inside quotes is kept.
QUOTED = re.compile("(?<![A-Za-z0-9])'(?:[^'\\n]|'(?=[A-Za-z]))*'(?![A-Za-z0-9])|\"[^\"\\n]*\"|"
                    "\u201c[^\u201d\\n]*\u201d|\u2018[^\u2019\\n]*\u2019")


def expand(pattern, defs):
    """A clause rule may name the parts its patterns share in "defs" ({"LIC": "CC0|ODbL"}): {LIC} in its "re" (a
    string, or a list of alternatives joined with |) and in its neutralisers stands for that part, and a part may name
    another. A name is upper case, so a quantifier such as {0,60} is never read as one; a rule with no defs is
    compiled as written."""
    if not defs:
        return pattern
    for _ in range(len(defs) + 1):
        n = DEF.sub(lambda m: defs.get(m.group(1), m.group(0)), pattern)
        if n == pattern:
            return n
        pattern = n
    raise ValueError("projection.json: the defs of a clause rule name each other in a circle")


def blank_quoted(s):
    return QUOTED.sub(lambda m: " " * len(m.group(0)), s)


def clauses(s):
    """Split into clauses at SPLIT, but never inside quoted text: a quoted vendor sentence stays one piece."""
    spans = [m.span() for m in QUOTED.finditer(s)]
    out, start = [], 0
    for m in SPLIT.finditer(s):
        if any(a < m.start() < b for a, b in spans):
            continue
        out.append(s[start:m.start()])
        start = m.end()
    out.append(s[start:])
    return out


def tidy(res, orig):
    """The text left after clauses were withheld: no bracket without its partner, no empty brackets, no space
    before a comma, and a capital letter at the start when the original value began with one."""
    if not res:
        return res
    out, opens = [], []
    pairs = {")": "(", "]": "["}
    for ch in res:
        if ch in "([":
            opens.append(len(out))
            out.append(ch)
        elif ch in ")]":
            if opens and out[opens[-1]] == pairs[ch]:
                opens.pop()
                out.append(ch)
            # a closing bracket whose opening one was in a withheld clause is dropped
        else:
            out.append(ch)
    for i in reversed(opens):
        out[i] = ""
    t = "".join(out)
    t = re.sub(r"\(\s*\)|\[\s*\]", "", t)
    # a space before a full stop goes only at the end of a sentence, so a name such as ".mu" keeps its space
    t = re.sub(r"\s+([,;:]|\.(?=\s|$))", r"\1", re.sub(r"[ \t]{2,}", " ", t)).strip(" ;,")
    if t and orig[:1].isupper() and t[:1].islower():
        t = t[:1].upper() + t[1:]
    # a sentence whose last clause was withheld keeps the full stop the original ended with
    if t and orig.rstrip().endswith(".") and t[-1] not in ".!?":
        t += "."
    return t


def leaves(v, p=()):
    """Yield (path tuple, value) for every leaf; an empty dict or list is a leaf."""
    if isinstance(v, dict):
        if not v:
            yield p, v
        for k, x in v.items():
            yield from leaves(x, p + (k,))
    elif isinstance(v, list):
        if not v:
            yield p, v
        for i, x in enumerate(v):
            yield from leaves(x, p + (i,))
    else:
        yield p, v


def count_leaves(v):
    return sum(1 for _ in leaves(v))


def folded(p):
    """Array-folded dotted path for rule matching: limits[].value."""
    out = ""
    for k in p:
        if isinstance(k, int):
            out += "[]"
        else:
            out += ("." if out else "") + k
    return out


def jpath(p):
    """SQLite JSON path that keeps dynamic keys exactly: $.extras."NAT Start".price."""
    out = "$"
    for k in p:
        if isinstance(k, int):
            out += "[%d]" % k
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k):
            out += "." + k
        else:
            out += '."' + k.replace('"', '\\"') + '"'
    return out


class Projector:
    def __init__(self, rules, records):
        self.rules = rules
        ex = rules["exclude_records"]
        self.exclude_rids = set(ex["rids"])
        self.exclude_re = re.compile(ex["re"], re.I)
        self.drops = []
        for r in rules["drop_paths"]:
            rx = re.compile(fnmatch.translate(r["glob"]))
            self.drops.append((r["id"], rx, set(r.get("except", []))))
        self._drop_cache = {}
        self.url_rw = [(r["id"], re.compile(r["re"]), r["to"], r.get("strip_dash_in_group"))
                       for r in rules["url_rewrite"]]
        self.url_drop = [(r["id"], re.compile(r["re"])) for r in rules["url_drop"]]
        self.qty = re.compile(rules["quantity_re"], re.I)
        # a neutraliser is a pattern to delete, or a [pattern, replacement] pair
        self.neutralise = [(re.compile(x, re.I), "") if isinstance(x, str) else (re.compile(x[0], re.I), x[1])
                           for x in rules["narrative_neutralise"]]
        self.clauses = []
        for r in rules["clause_rules"]:
            fl = re.I if "i" in r.get("flags", "") else 0
            pat = r["re"] if isinstance(r["re"], str) else "|".join(r["re"])
            self.clauses.append({
                "id": r["id"], "class": r["class"], "action": r.get("action", r["class"]),
                "re": re.compile(expand(pat, r.get("defs")), fl), "to": r.get("to", ""),
                "skip": re.compile(r["skip_re"], re.I) if r.get("skip_re") else None,
                "skip_paths": tuple(r.get("skip_paths_prefix", [])),
                "keep_if_quantity": bool(r.get("keep_if_quantity")),
                "skip_quoted": bool(r.get("skip_quoted")),
                "local": [(re.compile(expand(a, r.get("defs")), re.I), b) for a, b in r.get("neutralise", [])],
                "triggers": [t.lower() for t in r["triggers"]],
            })
        trig = sorted({t for c in self.clauses for t in c["triggers"]}, key=len, reverse=True)
        self.trig_rx = re.compile("|".join(re.escape(t) for t in trig))
        self.legal_neut = [(re.compile(a, re.I), b) for a, b in rules["legal_neutralise"]]
        self.pre = [(r["id"], re.compile(r["re"], re.I), r["to"]) for r in rules.get("pre_rewrite", [])]
        # a path of a record in this repository (dossier/<topic>/<slug>.json) becomes the record id when that record
        # is published; the path of an excluded or missing record stays, and a clause rule withholds its clause
        rp = rules.get("record_path_rewrite")
        self.record_path = re.compile(rp["re"]) if rp else None
        self.public_rids = {"%s/%s" % (r.get("topic"), r.get("slug")) for r in records
                            if not self.excluded(r, "%s/%s" % (r.get("topic"), r.get("slug")))}
        # a key that is a research label (wave2, lane4_leading_asns) is published under a neutral name
        self.rename = {r["path"]: r["to"] for r in rules.get("rename_keys", [])}
        # a whole value that is a template written around no finding, at one field, is withheld
        self.boiler = [(r["id"], re.compile(r["re"]), set(r["paths"])) for r in rules.get("boilerplate_values", [])]
        # a value cut at a fixed length by a migration ends at its last whole word and is marked as cut
        tr = rules.get("truncated") or {}
        self.trunc_len = tr.get("length")
        self.trunc_mark = tr.get("mark", "\u2026")
        self.trunc_end = tuple(tr.get("complete_endings", [".", ")", '"', "'", "]", "!", "?"]))
        self.trunc_marked = set(tr.get("marked_lengths", []))
        # a title field (provider, tier, category) keeps the vendor and the product and loses a research note
        tr = rules.get("title_rule") or {}
        self.title_id = tr.get("id")
        self.title_paths = set(tr.get("paths", []))
        self.title_process = re.compile(tr["process_re"], re.I) if tr.get("process_re") else None
        self.title_ranking = re.compile(tr["ranking_re"], re.I) if tr.get("ranking_re") else None
        self._prose_cache = {}
        self._build_templates(records)

    # ------------------------------------------------------------------ templates
    def _build_templates(self, records):
        t = self.rules["templates"]
        skip = tuple(t["skip_paths_prefix"])
        classes = [(c, re.compile(rx, re.I)) for c, rx in t["classes"]]
        counts = collections.Counter()
        for rec in records:
            for p, v in leaves(rec):
                if isinstance(v, str) and len(v) >= 25 and not v.startswith("http"):
                    fp = folded(p)
                    if not fp.startswith(skip):
                        counts[(fp, v)] += 1
        self.templates = {}
        for (fp, v), n in sorted(counts.items()):
            if n < t["min_count"]:
                continue
            cls = next((c for c, rx in classes if rx.search(v)), t["default_class"])
            tid = "T" + hashlib.sha1((fp + "\0" + v).encode("utf-8")).hexdigest()[:8]
            self.templates[(fp, v)] = (tid, cls, n)
        self.template_text = t["public_text"]

    # ------------------------------------------------------------------ helpers
    def excluded(self, rec, rid):
        if rid in self.exclude_rids:
            return True
        hay = " ".join(str(rec.get(k) or "") for k in ("slug", "provider"))
        return bool(self.exclude_re.search(hay))

    def drop_rule(self, fp):
        if fp in self._drop_cache:
            return self._drop_cache[fp]
        res = None
        for rid_, rx, exc in self.drops:
            if fp in exc:
                continue
            if rx.match(fp):
                res = rid_
                break
        self._drop_cache[fp] = res
        return res

    def rewrite_url(self, u):
        """-> (new url or None, rule id or None)."""
        for rid_, rx, to, sd in self.url_rw:
            m = rx.match(u)
            if m:
                out = to
                for gi in range(1, (m.lastindex or 0) + 1):
                    g = m.group(gi)
                    if sd == gi:
                        g = g.replace("-", "")
                    out = out.replace("\\%d" % gi, g)
                return out, rid_
        for rid_, rx in self.url_drop:
            if rx.search(u):
                return None, rid_
        return u, None

    # ------------------------------------------------------------------ titles
    def _note(self, text):
        """True when a parenthesis or a clause of a title is a research note: a process word, or ranking commentary."""
        t = text.strip(" ,;:")
        return bool(t) and bool((self.title_process and self.title_process.search(t))
                                or (self.title_ranking and self.title_ranking.search(t)))

    def clean_title(self, s):
        """A provider, tier or category without its research notes (rules title_rule): a parenthesis that holds a
        note goes, an unclosed one at the end too; after the first spaced dash, the first clause that holds a note goes
        with every clause after it. The vendor and the product stay, and a title is never emptied."""
        if not isinstance(s, str) or not s or not (self.title_process or self.title_ranking):
            return s
        t = s
        # innermost parentheses first, so "(re-check only (not a discovery))" goes whole
        while True:
            n = re.sub(r"\s*\(([^()]*)\)", lambda m: "" if self._note(m.group(1)) else m.group(0).replace("(", "\x00").replace(")", "\x01"), t)
            if n == t:
                break
            t = n
        t = t.replace("\x00", "(").replace("\x01", ")")
        m = re.search(r"\s*\(([^()]*)$", t)  # a parenthesis a migration cut before it closed
        if m and self._note(m.group(1)):
            t = t[:m.start()]
        # the first spaced dash outside a parenthesis
        m = next((x for x in re.finditer(r"\s[\u2014\u2013-]\s", t)
                  if t[:x.start()].count("(") == t[:x.start()].count(")")), None)
        if m:
            head, tail = t[:m.start()], t[m.end():]
            parts, depth, quote, cur = [], 0, None, ""
            for i, ch in enumerate(tail):
                if quote:
                    quote = None if ch == quote else quote
                elif ch in "\"'\u2018\u201c" and (i == 0 or not tail[i - 1].isalnum()):
                    quote = {"\u2018": "\u2019", "\u201c": "\u201d"}.get(ch, ch)
                elif ch in "([":
                    depth += 1
                elif ch in ")]":
                    depth = max(0, depth - 1)
                if ch == "," and depth == 0 and not quote and tail[i + 1:i + 2] == " ":
                    parts.append(cur)
                    cur = ""
                    continue
                cur += ch
            parts.append(cur)
            keep = []
            for p in parts:
                if self._note(p):
                    break
                keep.append(p)
            if len(keep) < len(parts):
                t = head + (t[m.start():m.end()] + ",".join(keep).strip() if keep and ",".join(keep).strip() else "")
        if t == s:
            return s
        t = re.sub(r"\s{2,}", " ", t).strip(" ,;:-\u2014\u2013")
        return t if t else s

    # ------------------------------------------------------------------ prose
    def clean_prose(self, s, fp):
        """-> (new string or None, [(rule, before)]). Cached per (string, path class)."""
        if not self.trig_rx.search(s.lower()) and not any(rx.search(s) for _, rx, _ in self.pre) and "dossier" not in s:
            return s, []
        key = (s, fp.split(".")[0] if fp.startswith("identity_cost") else "")
        hit = self._prose_cache.get(key)
        if hit is None:
            hit = self._clean(s, fp)
            self._prose_cache[key] = hit
        return hit

    def _clean(self, s, fp):
        log = []
        out = []
        changed = False
        if self.record_path and "dossier" in s:
            n = self.record_path.sub(lambda m: "%s/%s" % m.groups() if "%s/%s" % m.groups() in self.public_rids
                                     else m.group(0), s)
            if n != s:
                log.append(("R00", s[:240]))
                s = n
                changed = True
        for rid_, rx, to in self.pre:
            n = rx.sub(to, s)
            if n != s:
                log.append((rid_, s[:240]))
                s = n
                changed = True
        prev_held = None
        for clause in clauses(s):
            orig = clause
            c = clause
            verdict = None
            for r in self.clauses:
                if r["skip_paths"] and fp.startswith(r["skip_paths"]):
                    continue
                low = c.lower()
                if not any(t in low for t in r["triggers"]):
                    continue
                bare = CODE.sub(" ", c) if r["class"] == "legal" else (blank_quoted(c) if r["skip_quoted"] else c)
                act = r["action"]
                if act == "tidy":
                    # a tidy rule rewrites a form (a relative date) with its own neutralisers and never withholds
                    n = c
                    for nrx, nto in r["local"]:
                        n = nrx.sub(nto, n)
                    if n != c and r["re"].search(bare):
                        log.append((r["id"] + "-tidied", c[:240]))
                        c = n
                    continue
                if act == "token":
                    def rep(m, r=r):
                        if r["skip"] and r["skip"].search(m.group(0)):
                            return m.group(0)
                        return r["to"]
                    n = r["re"].sub(rep, c)
                    if n != c:
                        log.append((r["id"], c[:240]))
                        c = n
                    continue
                if not r["re"].search(bare):
                    continue
                if act == "rewrite":
                    # keep the case of the first letter, so "The client must" becomes "A user must"
                    n = r["re"].sub(lambda m, to=r["to"]: to[:1].upper() + to[1:] if m.group(0)[:1].isupper() else to, c).strip()
                    log.append((r["id"], c[:240]))
                    c = n
                    continue
                if act == "drop":
                    verdict = r["id"]
                    break
                if act == "legal":
                    if r["keep_if_quantity"] and self.qty.search(c):
                        continue
                    if r["local"]:
                        # a legal rule with neutralisers of its own (L3) rewrites every clause it matches, with or
                        # without a number: the terms phrase goes and the technical rest stays, when the rule no longer
                        # matches the rest and the rest still says something. Otherwise the clause is held when it
                        # carries a number and withheld when it does not
                        n = c
                        for nrx, nto in r["local"]:
                            n = nrx.sub(nto, n)
                        n = re.sub(r"\s+([.,;:])", r"\1", re.sub(r"\s{2,}", " ", n)).strip()
                        if n != c.strip() and not r["re"].search(CODE.sub(" ", n)) and len(WORDS.findall(n)) >= 3:
                            log.append((r["id"] + "-neutralised", c[:240]))
                            c = n
                            continue
                        verdict = r["id"] + ("-held" if self.qty.search(c) else "")
                        break
                    if self.qty.search(c):
                        n = c
                        for nrx, nto in self.legal_neut:
                            n = nrx.sub(nto, n)
                        n = re.sub(r"\s+([.,;:])", r"\1", re.sub(r"\s{2,}", " ", n)).strip()
                        if n != c:
                            log.append((r["id"] + "-neutralised", c[:240]))
                            c = n
                        if r["re"].search(CODE.sub(" ", c)):
                            verdict = r["id"] + "-held"
                            break
                        continue
                    verdict = r["id"]
                    break
                if act == "narrative":
                    n = c
                    for nrx, nto in self.neutralise:
                        n = nrx.sub(nto, n)
                    n = n.strip(" ,;:-")
                    if n and n != c.strip(" ,;:-") and not r["re"].search(blank_quoted(n) if r["skip_quoted"] else n):
                        log.append((r["id"] + "-neutralised", c[:240]))
                        # a clause cut at a semicolon keeps it, so the next clause still reads as a second clause
                        semi = ";" if c.rstrip().endswith(";") and not n.endswith(";") else ""
                        c = (n[:1].upper() + n[1:] if c[:1].isupper() else n) + semi
                        continue
                    verdict = r["id"] + ("-held" if self.qty.search(c) else "")
                    break
            if not verdict and prev_held and FOLLOWER.match(c.lstrip()):
                verdict = prev_held + "-follows"
            if verdict:
                log.append((verdict, orig[:240]))
                changed = True
                prev_held = verdict.split("-")[0]
                continue
            after_held = prev_held is not None
            prev_held = None
            if c != orig:
                changed = True
            if c.strip():
                # a clause that came after a withheld clause and a semicolon now starts a sentence
                if after_held and out and out[-1].rstrip().endswith((".", "!", "?")) \
                        and re.match(r"[a-z]+\b(?![.'’-])", c.lstrip()):
                    c = c.lstrip()
                    c = c[:1].upper() + c[1:]
                    changed = True
                out.append(c)
        if not changed:
            return s, log
        res = tidy(" ".join(out).strip(" ;"), s)
        return (res or None), log

    def truncated(self, src, nv):
        """True when the text ends where a migration cut it: it does not end a sentence, and the source, the
        projected text, or the source after a clause boundary (". ", "; ", ": ") is exactly the cut length."""
        L = self.trunc_len
        if not L or not nv:
            return False
        # a value that a migration cut and marked already ends with the mark, right after the cut word
        if src.endswith(self.trunc_mark) and (len(src) in self.trunc_marked or re.search(r"\w" + re.escape(self.trunc_mark) + "$", src)):
            return nv.rstrip().endswith(self.trunc_mark)
        if nv.rstrip().endswith(self.trunc_end):
            return False
        if len(src) == L or len(nv) == L:
            return True
        return any(len(src) - m.end() == L for m in re.finditer(r"(?<=[.;:!?])\s+", src))

    # ------------------------------------------------------------------ project one record
    def project(self, rid, rec):
        """-> (projected dict, tally Counter, strip rows [(path, rule, before)], unknown rows [(path, class, rule)])."""
        tally = collections.Counter()
        strip = []
        unknown = []

        def walk(v, p, op):
            # p is the path in the source record (rules match it, the private strip log keeps it); op is the path in
            # the published record, with renamed keys, which the public unknown rows carry
            if isinstance(v, dict) and v:
                out = {}
                for k, x in v.items():
                    q = p + (k,)
                    fp = folded(q)
                    rule = self.drop_rule(fp)
                    if rule:
                        n = count_leaves(x)
                        tally["withheld"] += n
                        strip.append((jpath(q), rule, json.dumps(x, ensure_ascii=False)[:240]))
                        continue
                    nk = self.rename.get(fp, k)
                    out[nk] = walk(x, q, op + (nk,))
                return out
            if isinstance(v, list) and v:
                return [walk(x, p + (i,), op + (i,)) for i, x in enumerate(v)]
            return leaf(v, p, op)

        def leaf(v, p, op):
            if not isinstance(v, str):
                tally["kept"] += 1
                return v
            fp = folded(p)
            key = p[-1] if not isinstance(p[-1], int) else (p[-2] if len(p) > 1 else "")
            jp = jpath(p)
            pjp = jpath(op)
            if (key in URL_KEYS and re.match(r"(?:https?:|probe:)", v)) or fp == "evidence[].url":
                nu, rule = self.rewrite_url(v)
                if rule:
                    strip.append((jp, rule, v[:240]))
                    if nu is None:
                        tally["withheld"] += 1
                        unknown.append((pjp, "private-url", rule))
                        return None
                    tally["modified"] += 1
                    return nu
                tally["kept"] += 1
                return v
            t = self.templates.get((fp, v))
            if t:
                tid, cls, _ = t
                text = self.template_text[cls]
                unknown.append((pjp, cls, tid))
                strip.append((jp, tid, v[:240]))
                if text is None:
                    tally["withheld"] += 1
                    return None
                tally["modified"] += 1
                return text
            if len(p) == 1 and key in self.title_paths:
                nv = self.clean_title(v)
                if nv != v:
                    tally["modified"] += 1
                    strip.append((jp, self.title_id, v[:240]))
                    return nv
                tally["kept"] += 1
                return v
            if len(p) == 1 and key in TOP_SKIP:
                tally["kept"] += 1
                return v
            for bid, brx, bpaths in self.boiler:
                if fp in bpaths and brx.search(v):
                    tally["withheld"] += 1
                    strip.append((jp, bid, v[:240]))
                    unknown.append((pjp, "boilerplate", bid))
                    return None
            src = v
            nv, log = self.clean_prose(v, fp)
            for rule, before in log:
                strip.append((jp, rule, before))
            if nv is not None and self.truncated(src, nv):
                # the last word is the one the migration cut, so it goes; a value that is only that word goes whole
                cut = nv.strip()
                if cut.endswith(self.trunc_mark):
                    cut = cut[:-len(self.trunc_mark)].rstrip()
                cut = cut[:cut.rfind(" ")] if " " in cut else ""
                cut = cut.rstrip(" ,;:-(\u2014\u2013")
                nv = cut + self.trunc_mark if cut else None
                strip.append((jp, "X%d" % self.trunc_len, src[:240]))
                if nv is None:
                    log = [("X%d" % self.trunc_len, src[:240])] + log
            if nv is None:
                tally["withheld"] += 1
                unknown.append((pjp, "withheld", log[0][0] if log else "?"))
                return None
            if nv != src:
                tally["modified"] += 1
                if any(r.endswith("-held") for r, _ in log):
                    unknown.append((pjp, "partly-held", next(r for r, _ in log if r.endswith("-held"))))
                return nv
            tally["kept"] += 1
            return src

        return walk(rec, (), ()), tally, strip, unknown
