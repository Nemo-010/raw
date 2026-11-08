# Three compute lanes were recorded paid-only when the free lane existed behind an institution

- **When:** 2026-10-22T15:02:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/heroku.json` verdict `qualifies-with-caveat`; `dossier/compute/e2e-networks.json` verdict `trial-only`; `dossier/compute/thunder-compute.json` verdict `paid-only`
- **Superseded by:** `heroku` `fails-identity`; `e2e-networks` `fails-identity`; `thunder-compute` `fails-identity`; `docs/compute/free/student-and-education.md`; `docs/compute/free/regional-clouds.md`
- **Evidence:** vendor pages read 2026-10-22 through `scripts/broker/broker.sh read`; the exact URLs and quoted sentences are in each record's `evidence[]` and in the body below
- **Confidence:** documented

## What we believed

That Heroku had no free tier, that the E2E Networks offer was a trial of unstated size, and
that Thunder Compute sold capacity only.

## What we found

Each of the three publishes a free lane on a page other than its pricing page, and each lane
is gated on an institution rather than on a card.

Heroku, `https://www.heroku.com/github-students/`, read 2026-10-22: "If you are registered
with the GitHub Student Developer Pack, you are eligible to receive platform credits worth
$13 per month for 24 months (for a total value of $312)." The Student Developer Pack itself
requires the applicant to be "enrolled in a degree- or diploma-granting program" and to
"provide documents that prove your current student status".

E2E Networks, `https://www.e2enetworks.com/startup-program`, read 2026-10-22: "$5K (INR 5
Lakh) in free-to-use AI Cloud credits" for AI Explorer, with eligibility "Established,
legally incorporated company" and "10 or fewer employees". The self-serve account FAQ
requires "Copy of any one identity proof document" and "Copy of any one address proof", with
activation that "may take up to 3 business days".

Thunder Compute, `https://www.thundercompute.com/students`, read 2026-10-22: "Only students
enrolled at US universities qualify. Sign up with your university email; credit is added
automatically." and "Student credit $20.00".

## What it changes

All three become `fails-identity`, and each carries the door in `binding_note`. The distinction
that matters is that a card is reachable and a degree, a company registration
or a US university enrolment is not. Recording the lane as `paid-only` hid capacity that
exists; recording it without the gate would have hidden the reason it cannot be used.

Two secondary facts are kept in `notes` rather than in the verdict: E2E also gives a
20-infra-credit signup bonus behind phone OTP and document review, and Heroku's incoming note
blamed a card when the failing gate is the student check.

## The transferable point

A pricing page is not the inventory of a provider's free capacity. Student pages, startup
programmes and regional microsites each carry a lane the pricing page omits, and the gate on
that lane decides the verdict.
