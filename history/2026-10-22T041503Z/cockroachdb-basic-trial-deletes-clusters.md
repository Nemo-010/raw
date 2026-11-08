# CockroachDB Basic's trial was recorded as ending in "interruption", and it ends in an unrecoverable deletion

- **When:** 2026-10-22T04:15:03Z
- **Status:** corrected
- **Supersedes:** `dossier/databases-kv/cockroachdb-basic.json` (`retention`, `limits`, `binding`), `docs/databases-kv/free/mysql-and-distributed.md` §CockroachDB Basic, `docs/databases-kv/free/postgres-always-on.md` §CockroachDB Basic
- **Superseded by:** `dossier/databases-kv/cockroachdb-basic.json` as corrected, and the two documents
- **Evidence:** `cockroachlabs.com/docs/cockroachcloud/free-trial` and `cockroachlabs.com/docs/cockroachcloud/plan-your-cluster-basic`, both read 2026-10-22
- **Confidence:** documented

## What we believed

`retention.stated` read "the trial ends when the last credit is used or the credit expires, and a
payment method must be on file by then to avoid interruption". The finding the documents carried was
the card ambiguity between two first-party pages.

## What we found

The page states: "If the trial ends and a payment method has not been provided, a 30 day grace
period begins where your organization's clusters are throttled, and you are restricted from
modifying their configuration". Then: "If the end of the grace period is reached and no payment
method has been added, all clusters in the organization are deleted. Deleted clusters can not be
restored."

For a zero-budget requirement, that is the only free relational tier in this topic whose
published end state is that the data is gone.

## How we found it

An adversarial review quoted the two sentences from the page the record already cited. The record's
own paraphrase, "to avoid interruption", is a soft rendering of a hard sentence that sits three
paragraphs further down the same page.

## What it cost us

The answer to the question the whole topic asks. "What happens after the free tier" is the topic's
title, and for the one provider whose answer is deletion the document stopped at the card. A reader
comparing CockroachDB against TiDB on the card question was comparing the smaller of the two
differences.

## What a future session should do differently

**Read the page to its end when the page is about the end.** The free-trial page exists to describe
what happens when the trial stops; the record read its first half, which describes the credits. A
record that paraphrases a page should quote the sentence it is paraphrasing, because a paraphrase
is where "deleted, unrecoverably" becomes "interruption".
