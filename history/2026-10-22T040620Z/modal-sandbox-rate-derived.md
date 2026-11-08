# The Modal sandbox rate was a hardcoded literal, 3.2 times the page's own arithmetic

- **When:** 2026-10-22T04:06:20Z
- **Status:** corrected
- **Supersedes:** `docs/compute/README.md` §The three facts (the 39-hour headline), `docs/compute/free/sandboxes-container-vm.md` §Modal, `docs/compute/paid/sandboxes-container-vm.md` §Modal, `docs/compute/paid/minimum-bill.md` §The keep-alive, `docs/compute/free/free-tier-census.md` §The nine recurring credits, `dossier/compute/modal.json`
- **Superseded by:** the same sections, plus `scripts/report/compute-price.py --modal`, which derives the figure
- **Evidence:** `modal.com/pricing` raw HTML (read 2026-10-22): `CPU (non-preemptible) Physical core (2 vCPU equivalent) $ 0.00003942 / core / sec`, `Memory (non-preemptible) $ 0.00000667 / GiB / sec`, and `each physical core is equivalent to 2 vCPUs as offered by AWS or GCP`
- **Confidence:** documented

## What we believed

Modal's Sandbox at 2 vCPU / 4 GiB cost USD 0.76 an hour, so the USD 30 monthly
credit bought about 39 hours. That sentence was the topic's headline: it appeared
in the README's "three facts that decide every recommendation", in the free
sandbox table, in the paid sandbox table, in the minimum-bill table, and in the
census of recurring credits. It was the number the topic quoted most often.

## What we found

USD 0.76 is not the 2 vCPU / 4 GiB rate. It is the **8 vCPU / 8 GiB** rate at the
same card: 4 physical cores plus 8 GiB is USD 0.7597 an hour. The 2 vCPU / 4 GiB
shape is **USD 0.2380** an hour, and the USD 30 credit buys **126 hours**.

The arithmetic, from the page's own numbers:

```
1 physical core  x 0.00003942 x 3600 s = USD 0.1419/h
4 GiB            x 0.00000667 x 3600 s = USD 0.0960/h
                                       = USD 0.2380/h

USD 30 / 0.2380 = 126.1 sandbox hours
300 h = USD 71.39      730 h = USD 173.71
```

Two things made this hard to see. The first is that a physical core is 2 vCPU on
Modal's card, and the page says so in a sentence, so "2 vCPU" is one core and not
two. Charging two cores for two vCPUs is a silent factor of two. The second is
that the 3x non-preemptible multiplier is real, which makes any large number look
explained: a reader who checks that the multiplier was applied stops there.

## How we found it

An adversarial review of the topic compared a generator constant against the
vendor's published table and found they disagreed by 3.2 times. The rate existed
as `modal = 0.76` on one line of a script under `.tmp/`, with no expression
producing it from a published number.

The page's table is dropped by Markdown extraction, which is why the earlier read
never saw it: the extracted text carries the prose and none of the per-second
rates. The same is true of Oracle's 10 TB egress sentence. Reading the raw HTML
found both.

## What it cost us

A headline. Seven locations in five documents, one dossier record, and the
ranking the topic was built around. The record and the documents also disagreed
before this correction: `modal.json` said 79 hours, the documents said 39, and the
page says 126, so one provider carried three answers.

The error was also in the house style's blind spot. The generator that produced
every other paid figure took its rate from a record that cites a page. Modal's
rate was the one input asserted rather than derived, so it was the one input that
could be wrong without any of the cross-checks firing.

## What a future session should do differently

⭐ **A constant in a generator is a claim with no citation.** Every other row in
`scripts/report/compute-price.py` now names the rate card and the field it came
from. The Modal row failed because it was the only one that did not.

⚠ **Check the unit conversion, not only the multiplier.** Two independent errors
were possible here and both were made: the multiplier was applied (correctly) and
the vCPU-to-core conversion was skipped (wrongly). A reader who verifies the
harder-looking fact and not the easier one checks nothing.

⚠ **Four of these shapes disagree if you assume one vCPU is one core.** The same
question decides E2B, Daytona and Freestyle, all of which price per vCPU-hour
rather than per core-hour. Modal is the only one of the four that publishes the
conversion, which is why it is the only one this correction can settle.
