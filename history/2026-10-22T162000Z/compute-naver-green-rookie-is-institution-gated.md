# NAVER's KRW 200,000 credit is for students and staff of a participating institution

- **When:** 2026-10-22T16:20:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/naver-cloud-platform.json` verdict `trial-only`
- **Superseded by:** `dossier/compute/naver-cloud-platform.json` verdict `fails-identity`; `docs/compute/free/forum-hosts.md`
- **Evidence:** vendor pages and campaign rules read 2026-10-22 through `scripts/broker/broker.sh`; the exact URLs and quoted sentences are in each record's `evidence[]`
- **Confidence:** documented

## What we believed

That the NAVER Cloud entry was a trial any new account could start, gated on a card and a
Korean phone number.

## What we found

The KRW 200,000 Green Rookie credit and the technical-certification exam voucher are
addressed to students and staff of a participating institution. That is an institution gate
on top of the residency and card gates the record already carried.

## What it changes

The verdict becomes `fails-identity`. The card and the Korean phone were already recorded;
what this adds is that even a Korean resident needs an affiliation, which makes the offer
unreachable on two independent counts rather than one.
