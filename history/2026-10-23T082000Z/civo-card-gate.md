# Civo needs a verified card before it will create an instance

- **When:** 2026-10-23T08:20:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/civo.json`, whose `identity_cost.kind` read `email` on the reasoning that the signup form carries no card field, and `docs/compute/free/credit-ranking.md`, which called Civo the one large balance that asks for neither a card nor a phone
- **Superseded by:** Civo's own billing documentation, read on 2026-10-23, states that a payment method must be on file at all times and that no instance or cluster can be created until the card is verified. The signup form and the usable product have two different gates, and only the second one matters
- **Evidence:** `https://www.civo.com/docs/account/billing` read 2026-10-23: "Civo services are chargeable, which is why you need a valid payment method on file at all times, and won't be able to create Kubernetes clusters or instances before your card is verified." The same page states "We do not support using a 'virtual' or pre-paid card as a payment type."
- **Confidence:** documented

The mistake is a category error between the signup form and the product. A form that asks for a name, an email address and a password is not a card-free gate if the account cannot spend its credit until a card is verified. The first page a reader sees is the form, and the sentence that decides usability is one link away in the billing documentation.

This matters more than a normal correction because the ranking placed Civo first among the offers that avoid a card, and the reason for excluding Azure and AWS was a refused signup. A card is now the documented gate on six of the ten ranked offers, not five.

The same pass found two more Civo facts that the record did not carry. Billing is hourly and rounded up, not per second, and the printed monthly price is "illustrative examples using an 'average month' of 730 hours" rather than a cap. A stopped instance also keeps billing in full, so pausing does not stretch the credit. Those are now in the record's limits and notes.
