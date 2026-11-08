# Three claims downgraded on review

- **When:** 2026-10-24T11:15:00Z
- **Status:** corrected
- **Supersedes:** the `measured` rung of `ip-proxy/clouds-as-exit-sources`, the `fails-quota` verdict of `ip-proxy/ippeak-dual-ntt`, the free-list decay written as a ratio, and the AnchoredIP correction that a `notes` string promised and did not apply
- **Superseded by:** those three records and `egress/anchoredip`, rewritten on 2026-10-24
- **Evidence:** the records named in "Where the corrections live"; the quotes are in each record's `evidence[]`
- **Confidence:** documented

An adversarial review of the new `ip-proxy` topic found three claims whose stated
rung was higher than the evidence, and one correction that had been promised but
not applied. Each is recorded here because the corrected number is in `docs/` and
the correction is here.

## 1. `clouds-as-exit-sources` was `measured`, is now `documented`

The record's own notes said: *"the allocation class of the other four is inferred
from their ASN ownership."* `METHODOLOGY.md` §3.1 makes a record's class the
**weakest** rung among the fields its verdict depends on, and the verdict
(`fails-egress`) rests on the allocation class. One class was measured with RDAP
(Oracle, `129.146.0.1`); four were inferred. The weakest rung decides, so the record
is `documented`.

The ASN numbers and holders are measured and reproduce: AS31898 Oracle, AS396982
Google, AS16509 Amazon, AS8075 Microsoft, AS24940 Hetzner.

## 2. `ippeak-dual-ntt` was `fails-quota`, is now `fails-egress`

The record's `binding_note` said: *"Traffic is unlimited, so no byte quota fails
first and volume-quota is the wrong name for what binds."* A verdict of
`fails-quota` therefore named a constraint the record says does not exist. What
fails is the registration-class claim, so the verdict is `fails-egress`.

## 3. The free-list decay was reported as a ratio, not a survival count

`docs/ip-proxy/free/free-lists.md` and the topic README said 60% of a pre-verified
list survives 22 minutes, and extrapolated a 10,000-line list to 2,000 and then
1,200 addresses. Three things were wrong:

- **21 over 35 is a ratio of two yields, not a survival rate.** The record already
  said so: intersected on host and port, 10 of the 35 that worked at the first
  check worked at the second, which is 29%.
- **The base was wrong.** 35% of 10,000 is 3,500, not 2,000.
- **The extrapolation had no measurement behind it.** The sample was 100 lines from
  1,751.

Both documents now report the intersection and refuse to extrapolate.

## 4. The AnchoredIP correction was written in a `notes` string and not applied

`dossier/ip-proxy/anchoredip-registration-corrected.json` said the egress record
*"must stop implying ISP registration"* and named `dossier/egress/anchoredip.json`
as the file to fix. That file was not changed, and no history entry existed.

It is applied now: `dossier/egress/anchoredip.json` carries the measured class as a
fifth evidence row (`ASSIGNED PA` under an individual in Kazakhstan, holder
`TROPYNIN-AS Tropynin Oleg`), and its `transit_note` says the registration class is
neither ISP nor organisation. The old sentence was true and incomplete rather than
false; it invited an ISP reading the registry does not support.

**Where the corrections live.** `docs/ip-proxy/README.md`,
`docs/ip-proxy/free/free-lists.md`, `docs/ip-proxy/paid/vpn-exits.md`,
`dossier/ip-proxy/clouds-as-exit-sources.json`,
`dossier/ip-proxy/ippeak-dual-ntt.json`, `dossier/egress/anchoredip.json`.

⚠ **What the review could not settle, and what would.** The IMC 2020 paper is
paywalled at ACM and the reviewer could not open it; the quotes in
`docs/ip-proxy/free/prefix-leases.md` were read from the full text in this session
and are verbatim. A reader who cannot reach the paper should treat the `/48`
argument as `documented` from a secondary description of it.
