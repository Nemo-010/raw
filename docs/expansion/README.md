# Expansion — what this corpus should cover next, and why

This directory holds the gap analyses for three areas, each with a different
decay rate and a different verification gate.

| area | why it is thin | what closing it buys |
|---|---|---|
| [`netdisk-pan.md`](netdisk-pan.md) | the population churns at ~7.5% per month, so a static list is obsolete before it is published | a loop that finds new instances and proves capability, so the topic stays current |
| [`compute.md`](compute.md) | machines are priced, and what can be run on them is established for only part of the catalogue; whole categories are missing | a topic that answers the real question: what runs, for how long, with what network, and what state survives |
| [`free-inference.md`](free-inference.md) | endpoints die in days, and nothing renews the list | a topic that stays current, because a document older than a month is a hypothesis |

## What an expansion plan owes

A plan here is not a wish list. It owes four things, and a plan missing any of
them is a note:

1. **The gap, quantified.** How many providers are known, how many are believed
   missing, and on what evidence. "This area is thin" is not a measurement.
2. **The discovery method.** The exact queries, sources, lists and forums that
   find new candidates, written as a procedure a script can run.
3. **The verification gate.** How a candidate becomes a record, and specifically
   what must be *measured* rather than read. Each area has a different gate —
   a capability probe for a pan instance, a wall-clock test for a sandbox, a
   completion request for an inference endpoint.
4. **The staleness policy and the loop that enforces it.** How often the area is
   re-checked, and what the check does when a provider has died. Each of these
   three decays at a different rate, and the plan must state the rate.

## Sequencing

The three are ordered by what unblocks the most work:

- **netdisk-pan** first. It is the only one with a measured half-life, so it is
  the one that actively rots. Its discovery loop is also the template the other
  two reuse.
- **free-inference** second. It rots fastest in wall-clock terms but its
  verification is a single HTTP request, so a loop is cheap.
- **compute** last. It rots slowest — a provider's free tier rarely changes
  within a quarter — but it needs the most research per provider, because the
  questions are about behaviour rather than limits.

## What to do with these

Read the plan, then work its steps in order. Each plan names the exact files it
creates or amends, so the shape does not have to be decided.

**These plans are not findings.** They contain no provider records and no
measurements. A plan's output goes into `docs/` and `dossier/` like any other
research, and the plan is amended to say what was found — a plan that claims a
result it did not produce is the same defect as a document that states an
unverified number.
