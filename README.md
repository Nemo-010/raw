# raw

A research corpus of verified claims about cheap capacity: **what can be obtained
for free, or for very little money, and what it costs in constraints.**

The answer is not a list of prices. It is a set of claims, each with a source and
a date, and each naming the limit that actually binds.

---

## What this is

A public research corpus of cheap capacity. It records which services meet a
need, which do not, and why.

The corpus assumes no local hardware and no institutional login, and prices only
free, trial and cheapest-paid capacity. Every resource it records belongs to
somebody else.

**The target is every cheap resource, not storage.**

| resource | what it is for |
|---|---|
| storage | a hot working set of about 10 TiB, a 20 TiB cold archive, and 500 GB to 1 TiB of egress per day |
| compute | a machine that stays up, a sandbox for an agent, GPU time |
| inference | a model that answers without a card |
| egress, email, DNS, databases, CI runners, credentials | getting traffic out, sending mail, a name, state, a build, access |

A free GPU hour is a finding of the same rank as a free terabyte.

Programmatic access is required where the resource is programmatic. Hard filters for
storage: a reachable interface (S3, REST, WebDAV, SFTP, OCI,
Git, or a protocol a wrapper could speak), free or Cloudflare-covered egress, and
registration with an email address at most. Every finding states what
registration costs: email, phone, card, or an institutional login.

## What is covered

| topic | the question it answers | state |
|---|---|---|
| [storage](docs/storage/README.md) | where 20 TiB live, and where 1 TiB/day comes from | 20 TiB and 1 TiB/day answered; four ways to hold 20 TiB priced |
| [netdisk-pan](docs/netdisk-pan/README.md) | which drive can be mounted, and which public instance is real | measured; 9-month half-life |
| [compute](docs/compute/README.md) | what can be run, for how long, before it is reaped | priced by duty cycle, with the cart price beside the page price |
| [coding-subs](docs/coding-subs/README.md) | which subscription buys the most agent work per dollar | prices and quotas per plan |
| [inference](docs/inference/README.md) | what answers a completion request without a card | probed; no renewal loop yet |
| [crawler-scraper](docs/crawler-scraper/README.md) | how to read the web at scale, and what to do at a wall | includes the broker manual |
| [egress](docs/egress/README.md) | how traffic gets out, or a service gets in | WireGuard ingress answered; relay measured |
| [email](docs/email/README.md) | how to send and receive mail for nothing | inbound and outbound composition answered |
| [databases-kv](docs/databases-kv/README.md) | where state lives after the free tier | the after-the-tier question answered for every qualifying record |
| [domains-dns](docs/domains-dns/README.md) | the cheapest name for a service | the cheapest complete endpoint priced |
| [ci-cd-runners](docs/ci-cd-runners/README.md) | what can be run by pretending it is a build | runners and artifact storage priced |
| [debrid](docs/debrid/README.md) | which service turns the least money into the most retrieved bytes | page reads only; no account |
| [ip-proxy](docs/ip-proxy/README.md) | what the upstream sees as the caller's address, and how to change it | registration class checked for a sample only |
| [dev-services](docs/dev-services/README.md) | which monitoring, job, queue or auth service is free with no card | records only; no provider document |
| [data-apis](docs/data-apis/README.md) | which data API gives free calls, and whether a dump exists | records only; no provider document |

Each topic has a README. Read the README first. It states the answer, the
constraint that binds, and which document answers which question.

[`expansion/`](docs/expansion/README.md) is not a topic. It holds the gap analyses
for three areas, each with its measured gap, its discovery method, its
verification gate and its staleness policy.
[`maintenance.md`](docs/maintenance.md) is the operating schedule: what to run
weekly, monthly and quarterly, and how to read a red gate.

## How to read it

Read in this order. Each step is short.

1. **This file.** It is the front door.
2. **[BRIEF.md](BRIEF.md).** It is the slow state: what is covered, what is
   settled, what is dead, and which checks are red. Read it before researching
   anything, so work that is already done is not repeated.
3. **The topic README** for the question. It gives the answer and the map.
4. **The document** the topic README names. It gives the numbers.
5. **[dossier/](dossier/README.md)** when a number needs checking. One JSON
   record per provider. It is the source of truth; every table in `docs/` is a
   view of it.

The findings are published as technical data only, in the public repository
[`f-shy/fshy.ajam.dev`](https://github.com/f-shy/fshy.ajam.dev). The published
corpus is `data/` in that repository: a projection of `dossier/` with process
narrative, personal details and terms text stripped. To query from a terminal,
run `scripts/fr help` ([scripts/fshy/README.md](scripts/fshy/README.md)).

An agent with no memory of earlier work reads **[AGENTS.md](AGENTS.md)**
instead. It is the router: which document owns a question, and what "done" means.

## How to read a number here

Every claim carries a rung on the evidence ladder. The rung is in the sentence,
not in a legend to decode.

| rung | what it means |
|---|---|
| `measured` | a request was run in this repository and the result recorded |
| `documented` | a vendor page said so, and the page and the date are cited |
| `reported` | a third party said so: a forum, a blog, an aggregator |
| `inferred` | reasoned from other evidence, which is named |
| `unverified` | somebody asserted it, and the reason it could not be checked is given |

A number with no rung is a defect. Report it.

## The findings that matter most

Five claims carry most of the weight. Each one is a pointer to its evidence.

**Free capacity is real, and it is bounded by one specific limit.** Cloudflare
Pages holds 488 GiB per project across 100 projects. What binds is 25 MiB per
file, and the fact that the total only exists if objects average at least
10.49 MiB. At 1 MiB per object, the same offer collapses to 1.9 TiB.
(`dossier/storage/cloudflare-pages.json`, `measured`.)

**Anonymous capacity exists and is large.** BigFile.net accepts 256 GB per object
with no account and no published quota. What binds is a sliding 365-day retention
and the absence of any index. (`dossier/storage/bigfile-net.json`, `measured`.)

**The cheapest paid answer is often cheaper than the free one, in time.** A
20 TB Hetzner Storage Box (BX41) costs EUR 40.60 per month excluding VAT, with
unlimited traffic. (`dossier/storage/hetzner-storage-box-bx41.json`, `documented`.)

**Identity is the binding constraint, not quota.** Academic and institutional
infrastructure publishes quotas of 10 to 150 TB. Almost all of it requires an
institutional login. A quota that cannot be reached is worth zero, and the
document must say so in the same sentence it quotes the number.
(`docs/storage/free/`, `documented`.)

**A public instance that advertises write access usually cannot write.** Of 169
hostnames probed, 30 exposed an anonymous AList or OpenList mount list and one
accepted a write and returned the bytes; 14 of the 30 advertise a write they refuse.
([`docs/netdisk-pan/README.md`](docs/netdisk-pan/README.md) owns these numbers, `measured`.)

## Withdrawn claims

A claim withdrawn here is one a reader would otherwise act on. The reasoning, and
every entry that did not reach this table, is in [`history/`](history/README.md).

| the claim | what took it away | the correction |
|---|---|---|
| "A Yggdrasil volunteer peer at 200 Mbit/s carries 2.16 TB/day, so one free lane clears the serving volume" | 2026-10-22: Yggdrasil's own about page states it has "no native exit nodes, nor does it have any concept of exit nodes, for providing access to the public Internet". The 2.16 TB/day is overlay capacity between two Yggdrasil nodes and no part of that traffic can traverse it. | [`history/2026-10-22T052900Z/`](history/2026-10-22T052900Z/yggdrasil-has-no-exit-nodes.md), `docs/egress/free/bulk-egress.md` §Yggdrasil public peers |
| "Cloudflare Email Routing for inbound plus Brevo for outbound is a complete mail pair on one domain" | 2026-10-22: nobody had run it, and the two halves meet at `_dmarc` rather than at SPF, because Brevo writes no SPF record below a dedicated IP. Two SPF records return `permerror` under RFC 7208 and void the domain's SPF entirely. | [`history/2026-10-22T052901Z/`](history/2026-10-22T052901Z/cloudflare-brevo-chain-was-never-run.md), `docs/email/free/inbound.md` §The DNS composition |
| "Eight of nine AList instances advertised `write: true` and eight refused PUT" | 2026-10-22: the AList findings record eight that advertised it, and all eight refused. The "nine" invented a denominator. | [`history/2026-10-22T033211Z/`](history/2026-10-22T033211Z/methodology-coherence-fixes.md), `METHODOLOGY.md` section 5.3 |

## Method

The discipline is in **[METHODOLOGY.md](METHODOLOGY.md)**. It is not optional and
it is not a summary. It defines:

- the evidence ladder, and what each rung requires;
- the seven binding constraints, and why naming one is mandatory;
- the rules;
- the challenge protocol, for pages that fight back;
- how a research question is scoped, evidenced and handed over;
- the staleness policy, because every fact here expires.

The slow state of the corpus (what is covered, what is settled, what is dead,
which checks are red) is **[BRIEF.md](BRIEF.md)**. The work queue is the open
issues labelled `rq:research`.

## What this repository will not do

It will not give legal or terms-of-service advice. A ban, a throttle or a data
loss is recorded as a one-line technical note, and a finding is not softened
because using it might breach a term.

It will not state a number it did not read or measure. A gap is acceptable and is
labelled. A plausible invention is not.

## Layout

```text
AGENTS.md        router for an agent with no memory: which document owns what
METHODOLOGY.md   the discipline, the evidence ladder, the rules
BRIEF.md         the slow state: covered, settled, dead, and the checks that are red
README.md        this file

docs/            the findings, by topic: docs/<topic>/{free,paid}/<slug>.md
dossier/         one JSON record per provider. The source of truth
history/         superseded claims and abandoned directions. Never deleted
sources/         third-party captures with a manifest. Script-maintained
references/      pruned documents cited here that could vanish. Hand-maintained

scripts/         probe, broker wrappers, validation, staleness, discovery, gate
tools/           compiled tools, only where a script is the wrong shape
```

## Working here

Three light checks run locally in seconds:

```bash
python scripts/dossier/validate.py --schema scripts/dossier/schema.json dossier/
python scripts/report/render.py --check
scripts/rq check
```

The heavy gate runs in CI on a pushed head, never in the research checkout, where a research session does not
run it ([`AGENTS.md`](AGENTS.md) section 2 rule 14); an own clone can run it: `sh scripts/gate.sh --root .` and
`scripts/rq gatecmp --base origin/main`. CI runs both on every pushed head.

## Licence

0BSD. See [LICENSE](LICENSE).

Third-party material in this corpus, its origin, its licence and what that means
for how much to trust it, is recorded in **[sources/SEED.md](sources/SEED.md)**.
