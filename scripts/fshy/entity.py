"""Vendor entity resolution. The dossier has no provider key; a record is an offer.

Anchor per record, first that applies:
  1. an override in registry/entities.tsv (rid -> eid, optional display name)
  2. the URL: an umbrella host keeps its full hostname, a code/community platform
     keys on platform/owner, an aggregator gives no key, anything else keys on its
     registrable domain (Public Suffix List, vendored in data/)
  3. the normalised provider name, then the slug without a trailing -N
A record anchored on a name joins the domain cluster whose dominant name equals it.
There is no other transitive merge, so one odd record cannot bridge two vendors.
Records stay the unit of verdict; an entity only groups them.
"""
import collections
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

PLATFORM = {"github.com", "gitlab.com", "codeberg.org", "bitbucket.org", "sourceforge.net", "huggingface.co",
            "gitee.com", "npmjs.com", "pypi.org", "reddit.com", "medium.com", "t.me", "hub.docker.com",
            "x.com", "twitter.com", "youtube.com", "discord.gg", "discord.com", "gist.github.com"}
UMBRELLA_SUFFIX = ("europa.eu", "gov.uk", "github.io", "gitlab.io", "pages.dev", "workers.dev", "vercel.app",
                   "netlify.app", "herokuapp.com", "readthedocs.io", "web.app", "firebaseapp.com", "notion.site",
                   "blogspot.com", "substack.com", "carrd.co", "glitch.me", "repl.co", "onrender.com")
AGGREGATOR = {"vpspricetracker.com", "lowendbox.com", "lowendtalk.com", "web.archive.org", "archive.org",
              "nodeseek.com", "hostloc.com", "linux.do", "v2ex.com", "serverhunter.com", "alternativeto.net",
              "news.ycombinator.com", "producthunt.com", "slant.co"}
RESERVED_PATH = {"features", "pricing", "docs", "enterprise", "marketplace", "sponsors", "settings", "about",
                 "security", "login", "join", "site", "topics", "collections", "orgs", "apps", "spaces",
                 "models", "datasets", "projects", "explore", "search", "en", "zh"}
GENERIC = {"free", "cloud", "storage", "api", "app", "the", "vps", "hosting", "host", "server", "tier", "plan",
           "account", "s3", "drive", "mail", "proxy", "vpn", "web", "data", "service", "services", "online"}


class PSL:
    def __init__(self, path=os.path.join(HERE, "data", "public_suffix_list.dat")):
        self.rules, self.wild, self.exc = set(), set(), set()
        self.version = ""
        with open(path, encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if ln.startswith("// VERSION:"):
                    self.version = ln.split(":", 1)[1].strip()
                if not ln or ln.startswith("//"):
                    continue
                ln = ln.split()[0].lower()
                if ln.startswith("!"):
                    self.exc.add(ln[1:])
                elif ln.startswith("*."):
                    self.wild.add(ln[2:])
                else:
                    self.rules.add(ln)

    def registrable(self, host):
        labels = host.lower().strip(".").split(".")
        if len(labels) < 2:
            return host
        best = 1
        for i in range(len(labels)):
            cand = ".".join(labels[i:])
            if cand in self.exc:
                best = len(labels) - i - 1
                break
            if cand in self.rules:
                best = max(best, len(labels) - i)
            if i + 1 < len(labels) and ".".join(labels[i + 1:]) in self.wild:
                best = max(best, len(labels) - i)
        if best >= len(labels):
            return host
        return ".".join(labels[-(best + 1):])


def host_path(u):
    m = re.match(r"https?://([^/:?#@]+)(?::\d+)?([^?#]*)", u or "")
    if not m:
        return None, ""
    h = m.group(1).lower().strip(".")
    if h.startswith("www."):
        h = h[4:]
    return h, m.group(2)


def core_name(p):
    p = unicodedata.normalize("NFKC", p or "")
    p = re.split(r"\s+[\(\[]|\s+[-–—|:]\s+|,\s|:\s|\s/\s", p)[0]
    p = re.sub(r"[^\w\s.+-]", " ", p.lower())
    p = re.sub(r"\b(free|tier|plan|account|the|inc|ltd|llc|gmbh)\b", " ", p)
    return re.sub(r"\s+", " ", p).strip()


# the last word of a name is never one of these: "Forgejo and" and "56IDC.Net /" are a name cut at a separator
TAIL_STOP = {"and", "or", "of", "the", "for", "with", "to", "in", "on", "at", "a", "an", "by", "via", "as", "from",
             "&", "+", "/", "-", "\u2013", "\u2014", "|"}
NAME_CAP = 60


def trim_name(p, cap=NAME_CAP):
    """A name of at most cap characters that ends in a whole word and in no connecting word or separator."""
    p = (p or "").strip()
    if len(p) > cap:
        cut = p[:cap]
        p = cut[:cut.rfind(" ")] if " " in cut else cut
    words = p.split()
    while len(words) > 1 and words[-1].lower().strip(",;:") in TAIL_STOP:
        words.pop()
    return " ".join(words).rstrip(" ,;:/|-\u2013\u2014") or p


def display_name(p):
    p = unicodedata.normalize("NFKC", p or "").strip()
    p = re.split(r"\s+[\(\[]|\s+[-\u2013\u2014|:]\s+|,\s|:\s|\s/\s|[|\uff5c]", p)[0].strip()
    return trim_name(p) or "?"


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48]


def load_overrides(repo):
    path = os.path.join(repo, "registry", "entities.tsv")
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if not ln.strip() or ln.startswith("#") or ln.startswith("rid\t"):
                continue
            c = ln.rstrip("\n").split("\t")
            out[c[0]] = (c[1], c[2] if len(c) > 2 and c[2] else None)
    return out


def resolve(projected, repo, psl):
    """projected: {rid: projected record}. -> (entities {eid: {...}}, rec_eid {rid: eid})."""
    overrides = load_overrides(repo)
    anchor = {}
    names = {}
    for rid, o in sorted(projected.items()):
        names[rid] = core_name(o.get("provider"))
        if rid in overrides:
            anchor[rid] = ("o", overrides[rid][0])
            continue
        url = o.get("url") or next((e.get("url") for e in (o.get("evidence") or []) if isinstance(e, dict)
                                    and isinstance(e.get("url"), str) and e["url"].startswith("http")), None)
        h, path = host_path(url)
        key = None
        if h:
            reg = psl.registrable(h)
            if h in PLATFORM or reg in PLATFORM:
                seg = [s for s in path.split("/") if s]
                lab = reg.split(".")[0]
                slug = o.get("slug", "")
                if seg and seg[0].lower() not in RESERVED_PATH and not (slug == lab or slug.startswith(lab + "-")):
                    key = ("p", "%s/%s" % (reg, seg[0].lower()))
                else:
                    key = ("d", reg)
            elif h.endswith(UMBRELLA_SUFFIX) or h.endswith(".gov") or h.endswith(".edu") or ".ac." in h or ".edu." in h or ".gov." in h:
                key = ("h", h)
            elif reg not in AGGREGATOR and h not in AGGREGATOR:
                key = ("d", reg)
        if key is None:
            n = names[rid]
            if n and len(n) >= 4 and n not in GENERIC:
                key = ("n", n)
            else:
                key = ("s", re.sub(r"-\d+$", "", o.get("slug", rid)))
        anchor[rid] = key

    clusters = collections.defaultdict(list)
    for rid, k in anchor.items():
        clusters[k].append(rid)
    # dominant name of each URL-anchored cluster
    dom_by_name = {}
    for k, members in sorted(clusters.items()):
        if k[0] in ("d", "h", "p"):
            c = collections.Counter(names[m] for m in members if names[m])
            if c:
                top = c.most_common(1)[0][0]
                if top and len(top) >= 4 and top not in GENERIC:
                    dom_by_name.setdefault(top, k)
    merged = collections.defaultdict(list)
    for k, members in clusters.items():
        if k[0] == "n" and k[1] in dom_by_name:
            merged[dom_by_name[k[1]]].extend(members)
        else:
            merged[k].extend(members)

    entities, rec_eid, used = {}, {}, collections.Counter()
    # larger clusters claim an id first, so github.com (39 records) is `github` and github.ai is `github-2`
    for k, members in sorted(merged.items(), key=lambda kv: (-len(kv[1]), kv[0][0], kv[0][1])):
        members.sort()
        disp = collections.Counter(display_name(projected[m].get("provider")) for m in members)
        name = max(disp.items(), key=lambda kv: (kv[1], -len(kv[0]), kv[0]))[0]
        if len(disp) > 1:
            # many products of one vendor: name the vendor by the leading words most of them share,
            # else by the domain label when most names contain it
            best = None
            for nw in (2, 1):
                pre = collections.Counter(" ".join(n.split()[:nw]) for n in disp.elements() if len(n.split()) >= nw)
                if pre:
                    word, cnt = pre.most_common(1)[0]
                    if word.split()[-1].lower().strip(",;:") in TAIL_STOP:
                        continue   # "Forgejo and", "56IDC.Net /": the shared words are cut in a phrase; take one word
                    if cnt * 2 >= len(members) and len(word) >= 3 and word.lower() not in GENERIC:
                        best = word
                        break
            if best is None and k[0] == "d":
                lab = k[1].split(".")[0]
                hits = sum(1 for n in disp.elements() if lab in n.lower())
                if len(lab) >= 3 and hits * 10 >= len(members) * 3:
                    best = next((w for n in disp.elements() for w in n.split() if w.lower() == lab), lab.capitalize())
            if best:
                name = best
        kind, val = k
        if kind == "o":
            eid = val
            pin = next((overrides[m][1] for m in members if overrides[m][1]), None)
            name = pin or name
            how, domain = "override", None
        elif kind == "d":
            lab = val.split(".")[0]
            eid = slugify(lab if lab not in ("my", "app", "go", "get", "try", "use", "the") else val)
            how, domain = "domain", val
        elif kind == "h":
            eid, how, domain = slugify(val), "host", val
        elif kind == "p":
            eid, how, domain = slugify(val.replace(".com", "").replace(".co", "")), "platform", val.split("/")[0]
        else:
            eid, how, domain = slugify(val) or "x", "name", None
        eid = eid or "x"
        used[eid] += 1
        if used[eid] > 1:
            eid = "%s-%d" % (eid, used[eid])
        tops = collections.Counter(names[m].split(" ")[0] for m in members if names[m])
        review = None
        if len(members) >= 4 and tops and tops.most_common(1)[0][1] * 2 < len(members):
            review = "mixed-names"
        entities[eid] = {"eid": eid, "name": name, "domain": domain, "how": how, "members": members,
                         "topics": sorted({m.split("/")[0] for m in members}), "review": review}
        for m in members:
            rec_eid[m] = eid
    by_name = collections.defaultdict(list)
    for e in entities.values():
        by_name[e["name"]].append(e)
    for name, es in by_name.items():
        if len(es) > 2 and all(e["domain"] for e in es):
            for e in es:
                e["name"] = e["domain"]
    return entities, rec_eid
