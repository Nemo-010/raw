# Reserved capacity, and when it beats paying per token

Committed throughput is a contract for a rate rather than a bill for a total. A
client reserves a number of tokens per minute for a term and pays for the reservation
whether it uses it or not. That trade pays when the workload is steady and loses when
it is spiky, and the whole decision is one comparison between the reserved rate and
the peak rate the same tokens would cost without it.

No vendor here publishes a committed-throughput price on a page that rendered, and no
reservation was taken. Every number below is labelled with how it was obtained, and
where none was obtained the row says so.

The answer: **no committed-throughput offer is documented anywhere in these two
topics, and the only reserved capacity found is described from the provider's side,
not the buyer's.** OpenCode Go states that it buys bulk discounts and reserves GPU
capacity from model providers and passes the savings on as a higher monthly ceiling
(`documented`, 2026-10-22). That is a subscription with a reservation behind it, which
is the closest this market comes to the class.

## The comparison

Sorted by how much of the offer is public. `Rate basis` is what the price is per, and
it is the field that makes two offers comparable or not.

| Provider | Offer | Term | Rate basis | Verified | Verdict |
| --- | --- | --- | --- | --- | --- |
| OpenCode Go and Go Plus | a per-model monthly dollar ceiling backed by reserved GPU capacity | monthly | dollars per model per month | documented | qualifies-with-caveat |
| Anthropic, Google, OpenAI committed throughput | not documented | - | - | unverified | unverified |
| Together, Fireworks dedicated endpoints | not documented | - | - | unverified | unverified |

## The shape, and why it is rare in this market

A committed-throughput contract is sold by vendors whose customers run inference as a
product. It requires a forecast, a term and a minimum spend, and it is priced against
the vendor's on-demand rate rather than against a competitor's. None of that suits a
buyer with no forecast and no minimum spend, and this market has priced accordingly:
the coding subscription is the mass-market form of the same idea, with the reservation
made on the vendor's side and resold as a monthly ceiling.

OpenCode Go's own explanation is the clearest statement of the mechanism found. The
page says that for most models the included monthly usage is delivered "through bulk
discounts and reserved GPU capacity", and that for models where no discount could be
negotiated the included usage is lower (`documented`, `opencode.ai/docs/go`, read
2026-10-22).

That second sentence is worth more than the first. It explains why six of Go's
per-model ceilings are USD 15 and the rest are between USD 30 and USD 240: the
ceiling is a function of the discount the provider obtained, not of the model's
quality or size. So a reader comparing two models by their ceiling is comparing two
purchasing deals.

## When it would beat paying per token

The arithmetic is the same for any reservation. A reservation wins when the reserved
rate times the committed volume is less than the on-demand rate times the volume
actually consumed, and it loses by exactly the unused fraction when the volume does
not arrive.

For a reader buying one plan, the class is out of scope. The reservation needs a
forecast, a term and a minimum spend, and none of the three is available at that size.
The class is documented here so it can be skipped in one read.

## What did not work

- **Four routes to a committed-throughput price.** None of Anthropic, Google, OpenAI,
  Together or Fireworks published one on a page read, so all five rows are
  `unverified` and carry no number.
- **Treating a subscription ceiling as a reserved rate.** OpenCode Go's ceiling is a
  reservation resold, and it is priced in dollars per model per month rather than in
  tokens per minute of a term, which is a different instrument.
- **Comparing a reservation to an on-demand rate without the utilisation.** The
  reservation is cheaper per token at full utilisation and more expensive at any
  other level, and the crossover is the only number that matters.

## Chaining

Nothing here chains. A reservation is the one instrument in this topic that requires a
forecast, and a workload that grows rather than holds steady does not provide one. The
class is recorded so it can be skipped in one read.
