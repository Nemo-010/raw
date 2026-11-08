# Hurricane Electric's free DNS was recorded with `interface: rest` beside a detail field saying it has no REST API

- **When:** 2026-10-22T04:15:05Z
- **Status:** corrected
- **Supersedes:** `dossier/domains-dns/he-dns.json` (`interface`, `interface_detail`, `limits`, `identity_cost`, `confidence`), `docs/domains-dns/free/managed-dns.md` (the two comparison tables)
- **Superseded by:** `dossier/domains-dns/he-dns.json` as corrected
- **Evidence:** `dns.he.net/`, read 2026-10-22
- **Confidence:** documented

## What we believed

`"interface": ["rest"]`, with `interface_detail` reading "a web panel; **no documented REST API for
record management**, and the dynamic-update path is a key-based URL". The record's `confidence` was
`documented`, and its single evidence entry was a probe of the login portal returning 200 with 16,458
bytes.

## What we found

Three defects in one small record, and the page states the facts the record needed.

The interface field contradicted the sentence beside it. The only programmatic path is a key-based
dyndns URL that takes `ipv4` and `ipv6` separately, with a `txt=` variant for ACME DNS-01 and the
note that the dynamic record must first be created in the panel. It cannot create a zone and cannot
enumerate records, so it is not a REST API and `rest` is the field a reader filters on.

The `documented` rung covered the eligibility gate, not the caps. The page does state the gate: "The
Open Beta has been expanded and now includes our IPv6 certification or tunnelbroker account holders,
Colocation customers and those with Transit services". Nobody had read it, because the only evidence
entry was a probe of the portal.

And the `limits[]` entry carried a `write-gated` value whose content was "the record and query caps
are unpublished", which is a statement about an absence and not a limit.

## How we found it

An adversarial review read the two fields against each other. The page was then read here and turned
out to state the gate, the multiple-domains-per-account claim and the dyndns syntax.

## What it cost us

A filter result. Where programmatic access is required, `interface` is the field a reader
uses to decide whether a provider is reachable at all, and `rest` on a provider with no record API
admits it into a set it does not belong in.

## What a future session should do differently

**A probe of a login page proves a login page.** It is the cheapest possible evidence and it says
nothing about the interface, the caps or the gate. When a record's only evidence is a 200 from a
portal, the record is `unverified` on every field except reachability, and this one was set to
`documented` on the strength of it.
