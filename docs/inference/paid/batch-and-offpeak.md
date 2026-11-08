# The half-price window, and how to work inside it

Three vendors in this market sell the same model at a lower price outside a named
window. The window is a property of the vendor's own capacity, and working inside it
requires nothing more than a scheduler and a UTC clock. For a workload that is a batch
job rather than an interactive session, it is the largest single discount available
without changing vendor.

The answer: **DeepSeek halves its rate outside two weekday windows, and the off-peak
period covers every weekend and the whole United States working day**
(`reported`, 2026-10-22). No vendor in this topic sells a batch discount that was
measured. One of them, OpenCode Go, prices the same model at both peak and
off-peak in its own default table.

## The comparison

Sorted by discount size. `Window` is stated in UTC because that is the only clock a
scheduler can compare against.

| Vendor | Discount | Peak window | Off-peak covers | Verified | Verdict |
| --- | --- | --- | --- | --- | --- |
| DeepSeek V4.1 Flash | 50 per cent | Monday to Friday, 01:00 to 04:00 and 06:00 to 10:00 UTC | all weekends and all other hours | reported | paid-only |
| OpenCode Go, DeepSeek V4.1 Flash | 50 per cent on input, cache and output | the same vendor windows | the same | documented | qualifies-with-caveat |
| Anthropic batch | 50 per cent | not a window: an asynchronous queue | any time | not read | unverified |
| Google Gemini batch | stated as a batch tier | not a window | any time | not read | unverified |
| Z.ai | 50 per cent off-peak | not read | not read | reported | paid-only |

## DeepSeek

DeepSeek's peak windows are Monday to Friday, 01:00 to 04:00 and 06:00 to 10:00 UTC,
which is 09:00 to 12:00 and 14:00 to 18:00 Beijing time (`reported`, from four
independent third-party summaries of the vendor page read on 2026-10-22; the vendor's
own table did not render through any route tried).

Off-peak is every weekend and all weekday hours outside those windows, which means
the entire United States working day is off-peak.

The discount is exactly half on input, output and cache read. A nightly batch run that
starts after 10:00 UTC and finishes before 01:00 UTC the next day never pays the peak
rate.

## OpenCode Go

OpenCode Go's table prices DeepSeek V4.1 Flash twice, as **Off-Peak** at USD 0.15
input, USD 0.60 output and USD 0.003 cache read, and as **Peak** at USD 0.30, USD 1.20
and USD 0.006, with the same USD 80 monthly ceiling on both (`documented`,
`opencode.ai/docs/go`, read 2026-10-22).

That is the only place in these two topics where a subscription publishes both the
peak and the off-peak rate for the same model under the same ceiling, which makes it
the cheapest comparison available: the ceiling is fixed in dollars, so an off-peak
workload buys twice the tokens for the same money.

## The batch tier, which is not a window

Anthropic and Google both sell an asynchronous batch tier at a discount, and neither
was read, so both rows are `unverified` and carry no number.

The difference from a time window is worth stating because it changes the design. A
window is a clock the caller waits for. A batch tier is a queue the caller submits to,
with its own turnaround time and its own failure mode, and a job that needs an answer
within the hour cannot use it whatever the discount.

## What did not work

- **Reading DeepSeek's own table.** Four extraction routes returned the model-naming
  page. The rate is third-party until a page renders it.
- **Assuming a local peak window.** The peak hours are the vendor's timezone, and a
  scheduler that uses local time pays the full rate half the time.
- **Treating a batch discount as a time window.** They are different mechanisms with
  different failure modes, and one is available to an interactive workload only in
  the sense that a queue is.

## Chaining

Off-peak is the cheapest way to run a nightly job and it composes with everything: a
job that already retries through a restart, in
[`../free/self-hosted-on-free-compute.md`](../free/self-hosted-on-free-compute.md),
also fits inside a UTC window. The constraint is that the job's duration must fit
between the windows, so a twelve-hour job does not benefit at all.
