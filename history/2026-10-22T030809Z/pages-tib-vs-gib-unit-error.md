# Pages is 47.68 TiB, not 48.8 TiB: a unit was printed as the wrong magnitude

- **When:** 2026-10-22T03:08:09Z
- **Status:** corrected
- **Supersedes:** `docs/storage/free/cloudflare-edge.md` section "The arithmetic, and one unit error to fix first"
- **Superseded by:** `docs/storage/free/cloudflare-edge.md` section "The arithmetic, and one unit error to fix first"
- **Evidence:** `developers.cloudflare.com/pages/platform/limits/` read 2026-10-22, 200 with 7,360 bytes: 20,000 files on the Free plan, 25 MiB per file, 100 projects per account
- **Confidence:** measured

## What we believed

The seed's dossier records and its report both stated "~488 GiB per project, ~48.8 TiB per
account". The second figure is the first multiplied by 100 with the unit left as it was.

20,000 files x 25 MiB is 488.28125 GiB. Times 100 projects is 48,828.125 GiB. That is 47.68 TiB,
not 48.8 TiB. The printed figure is the gibibyte count with a tebibyte label on it.

## What we found

The three numbers that produce it are all correct and all verbatim on the page: 20,000 files on
the Free plan, a 25 MiB maximum per file, and a limit of 100 projects per account which the page
notes "is not routinely increased".

100 x 20,000 x 25 MiB = 47.68 TiB. The archive tier's ceiling is 2.3% lower than published.

The 47.68 figure was already stated correctly in one place in the seed: the third review's
break-even table derived 2,000,000 slots from the same inputs. So the corpus held both numbers and
the wrong one was in the recommendation.

## How we found it

The unit rule in `docs/conventions/README.md` makes this a check rather than an inference: a
gibibyte count divided by 1,024 is a tebibyte count, and 48,828 GiB divided by 1,024 is 47.68.
The same document warns that the corpus states 200 Mbit/s as "2.16 TiB per day" when it is 2.16 TB
and 1.96 TiB, which is the identical error in a different row.

## What it cost us

Nothing, and that is why it survived three reviews. A 2.3% error changes no decision: 20 TiB at a
10.49 MiB mean needs 2,000,000 slots either way, and 42 projects either way.

That is exactly the shape of error a review does not catch. Each of the three reviews checked
whether the arithmetic produced the headline, and it does, because the headline is the arithmetic's
output with a wrong label. Nobody re-derived the label.

## What a future session should do differently

Check the unit independently of the arithmetic. A chain of correct multiplications that ends in the
wrong unit is invisible to every check that recomputes the chain, and a reader who spots it cannot
tell whether the number or the label is wrong.

Where a quantity is large enough that the two units are close in magnitude (48,828 GiB against
47.68 TiB), write the byte count once and convert from it. The convention's own instruction is to
work the arithmetic through where it matters, and this is the case that demonstrates why.
