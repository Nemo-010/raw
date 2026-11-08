#!/usr/bin/env python3
"""test_entity.py: the names of vendor entities (scripts/fshy/entity.py).

A name is never cut at a separator or in a phrase ("Forgejo and", "56IDC.Net /"), never cut at 60 characters in
the middle of a word, and a web-page title that three entities share is not their name. The cases are written
strings, and the whole corpus: every entity of the real dossier/ is named and checked. Standard library only.
Exit 0 when every case passes, 1 otherwise.

  python scripts/fshy/test_entity.py [-v]
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import entity  # noqa: E402

FAILED = []
PASSED = [0]
VERBOSE = "-v" in sys.argv


def check(name, cond, detail=None):
    if cond:
        PASSED[0] += 1
        if VERBOSE:
            print("ok    " + name)
    else:
        FAILED.append(name)
        print("FAIL  %s%s" % (name, ("  -- " + str(detail)[:300]) if detail is not None else ""))
    return cond


def main():
    dn = entity.display_name
    cases = [
        ("Forgejo and Gitea Actions (self-hosted)", "Forgejo and Gitea Actions"),
        ("56IDC.Net / 无聊云", "56IDC.Net"),
        ("envs.sh and null.slipfox.xyz (0x0 instances)", "envs.sh and null.slipfox.xyz"),
        ("mastodonapp.uk / mstdn.social / mastodon.social and the stock-Mastodon mass", "mastodonapp.uk"),
        ("bandwidth alliance / free-to-cloudflare peering as the egress answer", "bandwidth alliance"),
        ("小鹿乐玩iOS网盘IPA资源|路灯网盘-iOS砂壳分享网", "小鹿乐玩iOS网盘IPA资源"),
        ("Hetzner Storage Box", "Hetzner Storage Box"),
        ("C++ Builder", "C++ Builder"),
        ("Fast &", "Fast"),
        ("Proton Drive -", "Proton Drive"),
    ]
    for src, want in cases:
        got = dn(src)
        check("display_name(%r) is %r" % (src[:40], want), got == want, got)
    long_name = "a very long provider heading that has no separator in it and runs on past sixty characters of text"
    got = dn(long_name)
    check("a name longer than 60 characters is cut at a whole word", len(got) <= 60 and long_name.startswith(got) and long_name[len(got)] == " ", got)
    got = dn("one two three four five six seven eight nine ten eleven twelve thirteen of the")
    check("a cut name does not end in a connecting word", got.split()[-1].lower() not in entity.TAIL_STOP, got)
    check("a name with nothing but a stop word is kept", dn("and") == "and", dn("and"))
    check("an empty name is a question mark", dn("") == "?")

    # the whole corpus
    ex = json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8"))["exclude_records"]
    ex_re = re.compile(ex["re"], re.I)
    records = {}
    for p in sorted(glob.glob(os.path.join(REPO, "dossier", "*", "*.json"))):
        rid = os.path.basename(os.path.dirname(p)) + "/" + os.path.basename(p)[:-5]
        with open(p, encoding="utf-8") as f:
            o = json.load(f)
        if rid in ex["rids"] or ex_re.search(" ".join(str(o.get(k) or "") for k in ("slug", "provider"))):
            continue
        records[rid] = o
    ents, rec_eid = entity.resolve(records, REPO, entity.PSL())
    check("every record has an entity", set(rec_eid) == set(records), len(records) - len(rec_eid))
    names = {e: v["name"] for e, v in ents.items()}
    bad = [(e, n) for e, n in names.items() if n.split()[-1].lower().strip(",;:") in entity.TAIL_STOP and len(n.split()) > 1]
    check("no entity name ends in a connecting word or a separator", not bad, bad[:5])
    bad = [(e, n) for e, n in names.items() if n != entity.trim_name(n) and len(n) > entity.NAME_CAP]
    check("no entity name is cut at 60 characters in a phrase", not bad, bad[:5])
    bad = [(e, n) for e, n in names.items() if re.search(r"\s[/|]$", n)]
    check("no entity name ends in a slash or a bar", not bad, bad[:5])
    count = {}
    for e, v in ents.items():
        count.setdefault(v["name"], []).append((e, v["domain"]))
    bad = [(n, es) for n, es in count.items() if len(es) > 2 and all(d for _, d in es)]
    check("three entities of different domains never share one name (a web-page title)", not bad, bad[:3])
    for eid, want in (("56idc", "56IDC.Net"), ("forgejo", "Forgejo"), ("envs", "envs.sh"), ("larksuite", "Lark"),
                      ("blinkenshell", "Blinkenshell"), ("mastodonapp", "mastodonapp.uk")):
        if eid in names:
            check("entity %s is named %r" % (eid, want), names[eid] == want, names[eid])
        else:
            check("entity %s exists" % eid, False)
    for eid, dom in (("591meta", "591meta.com"), ("applep12", "applep12.vip"), ("vx365", "vx365.vip")):
        check("entity %s that shared a page title is named by its domain %s" % (eid, dom), names.get(eid) == dom, names.get(eid))

    print("%d checks, %d failed" % (PASSED[0] + len(FAILED), len(FAILED)))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
