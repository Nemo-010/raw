#!/usr/bin/env python3
"""Selftest for the public projection (scripts/fshy/rules/projection.json).

Each case is one input string at one field path and the public text it must become (None = withheld).
A rule edit that starts publishing process narrative, personal details or terms text, or that starts
dropping a technical number, fails here before it reaches the wiki.

usage: python scripts/fshy/test_projection.py      exit 0 all pass, 1 a case failed
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import project  # noqa: E402

CASES = [
    # (field path, input, expected public text or None, what it proves)
    ("notes", "Free tier is 10 GB with 1 GB/day egress.", "Free tier is 10 GB with 1 GB/day egress.",
     "plain technical text is kept verbatim"),
    ("notes", "This record was not re-checked in this session.", None,
     "a process-only sentence is withheld"),
    ("notes", "The seed recorded the quota. The quota is 5 GB per file.", "The quota is 5 GB per file.",
     "only the narrative sentence goes; the technical one stays"),
    ("evidence[].proved", "Pricing table lists 1 TB for EUR 3.20 [undated in the seed; dated to the seed pass]",
     "Pricing table lists 1 TB for EUR 3.20", "the migration date stamp is removed, the quote stays"),
    ("notes", "It is the cheapest 8 GiB shape in the lane at USD 4.58 a month.",
     "It is the cheapest 8 GiB shape at USD 4.58 a month.", "a narrative phrase carrying a number is neutralised, not dropped"),
    ("notes", "Merged from payment-rails: the floor is USD 12.", "The floor is USD 12.",
     "a merge prefix is removed and the number kept"),
    ("chaining", "none reachable for this client: the box needs a university email.", "the box needs a university email.",
     "the client framing is removed"),
    ("notes", "The client is a self-taught data scientist.", None, "the client profile is withheld"),
    ("notes", "Uploads are capped at 25 MiB under the Terms of Service.", "Uploads are capped at 25 MiB.",
     "a limit sourced from a terms page keeps its number and loses the legal framing"),
    ("notes", "Using it for piracy is illegal.", None, "legality commentary with no number is withheld"),
    ("evidence[].proved", "Free column: 10 concurrent VMs, Persistent VMs forbidden, 4 vCPU maximum",
     "Free column: 10 concurrent VMs, Persistent VMs forbidden, 4 vCPU maximum",
     "restriction wording that states a technical limit with a number is kept"),
    ("notes", "Contact jane.doe@example-host.com for quota raises.", "Contact [address removed] for quota raises.",
     "a personal email address is replaced"),
    ("notes", "Contact support@example-host.com for quota raises.", "Contact support@example-host.com for quota raises.",
     "a role address is kept: it is procedure, not a person"),
    ("notes", "Measured from .tmp/work/probe.json on the operator box.", None, "a scratch pointer is withheld"),
    ("identity_cost.detail", "A legal entity must sign up; individuals cannot.", "A legal entity must sign up; individuals cannot.",
     "a legal-entity requirement is an identity gate and stays"),
    ("notes", "The API answers {\"error\":\"infringing_file\"} for removed links.",
     "The API answers {\"error\":\"infringing_file\"} for removed links.", "an API error string is technical"),
    # issue #20: the client and the operator are not public, the software client is
    ("notes", "The home region matters: the client has no region in his own country.", None,
     "the client's circumstances are withheld"),
    ("binding_note", "At the client's 1 TiB/month the effective price is EUR 16 per TB.", None,
     "a price worked out on the client's workload is withheld"),
    ("egress.terms", "At the 500 GB to 1 TiB a day serving rate this is about 10 days of traffic. Egress is 5 TB a month.",
     "Egress is 5 TB a month.", "the workload sentence goes, the vendor's number stays"),
    ("notes", "It clears the 20 TiB archive in one order.", None, "the archive workload is withheld"),
    ("egress.terms", "No hosted allowance exists: the software runs on a host the client supplies.",
     "No hosted allowance exists: the software runs on a host a user supplies.", "the client as an actor becomes a user"),
    ("notes", "The client must run a PostgreSQL instance.", "A user must run a PostgreSQL instance.",
     "a rewrite at the start of a sentence keeps the capital"),
    ("notes", "It is the cheapest shape for this client's stack.", "It is the cheapest shape for a user's stack.",
     "this client is always the person"),
    ("notes", "The L4 rules cannot pass the client IP over TOA; the client sends a URL and the server pulls it.",
     "The L4 rules cannot pass the client IP over TOA; the client sends a URL and the server pulls it.",
     "the client as software is technical and stays"),
    ("notes", "Self-service order through the client area with an email account.",
     "Self-service order through the client area with an email account.", "a vendor's client area stays"),
    ("evidence[].quote", "Registration must come from the client's residential ISP.",
     "Registration must come from the client's residential ISP.", "a vendor quote is not rewritten"),
    ("notes", "What I could not establish: whether a phone number is required. The hold is USD 1.", "The hold is USD 1.",
     "first-person process narrative is withheld"),
    ("notes", "The operator's stated pain was that free tiers demand a card.", None, "the operator's circumstances are withheld"),
    ("notes", "This row answers the operator's question about holds.", None, "the operator's questions are process"),
    ("notes", "The operator published a key-rotation notice on 2026-05-15.",
     "The operator published a key-rotation notice on 2026-05-15.", "a vendor's operator is a technical subject"),
    # the merge review of PR #50: the shapes the first rules let through
    ("identity_cost.detail", "Listing and replay need nothing; Save Page Now needs the operator's Internet Archive keys",
     "Listing and replay need nothing", "the operator's own keys are withheld"),
    ("notes", "The status file reports a 50-unit pool for this deployment, which is the operator's account, not the vendor tier.",
     None, "the operator's own account is withheld"),
    ("retention.stated", "until the operator's account or tenant fails;", "until the operator's account or tenant fails;",
     "a public instance's operator is a technical subject"),
    ("chaining", "It is the cheapest option once, and the worst option for a client serving 500 GB a day.", None,
     "a workload written as 'a client serving' is withheld"),
    ("notes", "The card is what stops a client with no card. The minimum top-up is USD 5.", "The minimum top-up is USD 5.",
     "the circumstances of 'a client with no' are withheld"),
    ("limits_note", "A client without a descriptive User-Agent may be blocked.",
     "A client without a descriptive User-Agent may be blocked.", "an HTTP client is technical and stays"),
    ("egress.terms", "No traffic figure is stated in the write-ups I read.", "No traffic figure is stated in the write-ups.",
     "'I read' is neutralised and the fact stays"),
    ("notes", "There is one ambiguity I could not close. The port is 443.", "The port is 443.",
     "a first-person process note is withheld"),
    ("limits_note", "I measured 15 MiB accepted and 25 MiB rejected.", None, "a first-person measurement note is withheld"),
    ("notes", "It is the most interesting recurrence in this assignment.", "It is the most interesting recurrence.",
     "'this assignment' is neutralised"),
    ("notes", "cocalc.com/pricing now 404s through the broker.", "cocalc.com/pricing now 404s.",
     "the operator's page reader is neutralised out of a fact"),
    ("notes", "The broker returned 200 with 184 KB of HTML whose rows are all 'Loading...'.", None,
     "a sentence about the page reader is withheld"),
    ("identity_cost.detail", "A registration on the broker site is required.", "A registration on the broker site is required.",
     "a vendor that is a broker keeps its site"),
    # the second merge review of PR #50: first person by shape, the broker in any wording, session narrative
    ("notes", "Two machines had stock and I concluded the range was sold out.", None,
     "first person with any verb is withheld"),
    ("free_tier.stated", "The 'free trial' I searched for does not exist.", None, "first person after a quote is withheld"),
    ("notes", "My first read of the cart was wrong.", None, "my as the author is withheld"),
    ("evidence[].proved", "plan row fields, transcribed and joined by me: [XS] 2 GB", "plan row fields, transcribed and joined: [XS] 2 GB",
     "'by me' is neutralised and the row stays"),
    ("notes", "775 hours is our division at the Nova-3 rate.", "775 hours is a division at the Nova-3 rate.",
     "the author's arithmetic keeps its number"),
    ("identity_cost.detail", "The vendor answers 'I'm afraid we don't have a backend. We plan one.' in its forum.",
     "The vendor answers 'I'm afraid we don't have a backend. We plan one.' in its forum.",
     "a quoted vendor sentence keeps its I and we, even across a full stop"),
    ("free_tier.stated", "We only bill for outgoing traffic.", "We only bill for outgoing traffic.",
     "a vendor's own we copied into a field is the vendor's voice and stays"),
    ("free_tier.stated", "Linux I at EUR 4.99/month: 2 vCores.", "Linux I at EUR 4.99/month: 2 vCores.",
     "a roman numeral in a plan name is not a pronoun"),
    ("identity_cost.detail", "Accepted documents: driving licence, My Number card.", "Accepted documents: driving licence, My Number card.",
     "a product name with My stays"),
    ("interface_detail", "The HTML site returns 403 to this broker's egress on every path tried.",
     "The HTML site returns 403 on every path tried.", "'this broker's egress' is neutralised and the status stays"),
    ("notes", "The census called it reported because the read broker's Markdown view drops it.", None,
     "'the read broker' is withheld"),
    ("evidence[].proved", "'Free API egress' (read via read broker)", "'Free API egress'",
     "a read note is neutralised and the quote stays"),
    ("notes", "The pricing page returned a broker-side 504.", "The pricing page returned a 504.",
     "'broker-side' is neutralised and the status stays"),
    ("free_tier.stated", "Each user of the tunnel broker gets a /48.", "Each user of the tunnel broker gets a /48.",
     "a tunnel broker is a vendor class"),
    ("notes", "Those are the session's readings of the rendered pages.", None, "'the session's' as process is withheld"),
    ("chaining", "Recorded so the next session does not apply.", None, "'the next session' is withheld"),
    ("free_tier.stated", "Both returned 521 on every probe across the session.", "Both returned 521 on every probe.",
     "'across the session' is neutralised"),
    ("limits[].value", "the session times out after 20 minutes", "the session times out after 20 minutes",
     "a vendor's session is a technical unit"),
    # round 2: this repository's process (N14) and its private files and tools (pointer rules F1, F2)
    ("notes", "Not in dossier/compute (searched: affordablebytes, no record). The two pages agree on 6 GB.",
     "The two pages agree on 6 GB.", "a dedupe search of this repository is withheld"),
    ("notes", "The 2-hour task cap is a number the census did not have.", None, "the census is withheld"),
    ("notes", "The census gave Codeberg 8-core runners; the vendor table gives 4.", "The vendor table gives 4.",
     "a clause about the census goes and the vendor fact stays, with a capital letter"),
    ("probe.note", "the saved run this record cites, kept in sources/ so it survives a clean tree; re-run it with "
     "scripts/probe/tcpprobe.py", None, "a private path and a private tool are withheld"),
    ("notes", "New provider for the corpus. The trial excludes cron.", "The trial excludes cron.",
     "a new-provider note is withheld"),
    ("notes", "They said 'Not in the corpus: `ls dossier/compute | grep -i x` returns nothing'.", None,
     "a path of this repository inside quotes is withheld (F2)"),
    ("notes", "The euro sign is written as EUR because every string in this file is ASCII; no price was converted.",
     "The euro sign is written as EUR because every string in this record is ASCII; no price was converted.",
     "'this file' becomes 'this record'"),
    ("evidence[].proved", "probe.py record: status 200, 97 bytes", "probe record: status 200, 97 bytes",
     "the name of the probe tool goes and the measurement stays"),
    ("storage.notes", "Excluded by the brief's backup-service remit anyway.", None, "the brief is withheld"),
    ("notes", "The corpus already holds Kaggle's weekly 30-hour GPU quota.",
     None, "the corpus as the subject of a sentence is process narrative and is withheld (N17, round 4)"),
    ("notes", "would-settle: the order page's price for each of the eight rows.", None, "what would settle a row is process"),
    ("notes", "The tier is not stated on the pricing page; one signup would settle it.", "The tier is not stated on the pricing page.",
     "a clause naming the check that would settle a value is process, and the fact before it stays"),
    ("notes", "A checkout page would settle both the amount and the expiry.", None, "what would settle a value is process"),
    ("notes", "The block is announced by AS 64500. A trial would also settle the registration class.",
     "The block is announced by AS 64500.", "a clause with a word between 'would' and 'settle' is process too"),
    ("notes", "The notice is about the documentation; it would be settled by reading the live policy after an upload.",
     "The notice is about the documentation.", "'would be settled by' names the check that would settle a value"),
    ("notes", "Billing disputes are settled within 30 days.", "Billing disputes are settled within 30 days.",
     "a vendor's own 'settled' with no 'would' stays"),
    ("notes", "Recorded as qualifies-with-caveat rather than dead because the terms page still served.", None,
     "how a row was filed is process"),
    ("notes", "Already inventoried in A-P8 but only as a footnote.", None, "a wave id marks a clause of the research process"),
    ("notes", "Corrected 2026-10-22: the record states no free tier exists, so the verdict is paid-only.",
     "The record states no free tier exists, so the verdict is paid-only.", "a correction date prefix is neutralised"),
    ("evidence[].proved", "the site returns HTTP 530 through every broker route (read, fetch, crawl, archive)", None,
     "a broker route is the page reader"),
    ("notes", "That is a measurement artefact of this repository's broker and not evidence about NZBIndex.", None,
     "'this repository's broker' is withheld"),
    ("notes", "The site is a 2011-era broker with an email login.", "The site is a 2011-era broker with an email login.",
     "a vendor that is a broker stays"),
    # round 2: the client's serving target and workloads (P15)
    ("limits_note", "3,000 GB is 100 GB a day, 10 percent of the 1 TB a day serving target.",
     "3,000 GB is 100 GB a day.", "a share of the serving target goes and the arithmetic stays"),
    ("binding_note", "250 GB is 0.227 TiB, about a quarter of the target, and UDP is behind the paid plan as well.",
     "250 GB is 0.227 TiB, and UDP is behind the paid plan as well.", "a share of the target goes"),
    ("binding_note", "Error 3 is the one a 1 TiB/month client meets.", None, "a 1 TiB/month client is withheld"),
    ("price_per_tb_month", "5 TB workload: BX21 = EUR 2.18/TB/mo.", "at 5 TB: BX21 = EUR 2.18/TB/mo.",
     "a workload label becomes a size"),
    ("free_tier.stated", "0.5 GB/month free \u2014 three orders of magnitude short.", "0.5 GB/month free.",
     "an unnamed comparison with the workload goes"),
    ("evidence[].proved", "1 an HTML body in place of the target.", "1 an HTML body in place of the target.",
     "a target that is a URL stays"),
    ("chaining", "a 0.5 GB service runs 146 hours, six days", "a 0.5 GB service runs 146 hours, six days",
     "a service with a memory size stays"),
    # round 3: the research process in other words (N16)
    ("notes", "The dossier holds firebase-studio.json, which is a different product. Hosting is free up to 10 GB.",
     "Hosting is free up to 10 GB.", "the dossier as a word is withheld"),
    ("chaining", "it composes with Spaces (dossier compute record huggingface-spaces-zerogpu)",
     "it composes with Spaces (compute/huggingface-spaces-zerogpu)", "a dossier record named in brackets becomes its id"),
    ("tooling", "Native rclone backend per BRIEF \u00a71.1, and an S3 gateway.", "Native rclone backend, and an S3 gateway.",
     "a brief section number is neutralised"),
    ("notes", "Neither seed's number survives: talaria's USD 3.50 is a plan that does not exist. The plan is EUR 4.",
     "The plan is EUR 4.", "the seed agents are withheld"),
    ("notes", "Batch 1 carried the 30-day expiry. The credit expires after 30 days.", "The credit expires after 30 days.",
     "a batch number is withheld"),
    ("reliability_note", "Not covered in round 1. The quota is 10 GB.", "The quota is 10 GB.", "a round number is withheld"),
    ("notes", "Candidates: (a) the tier is perpetual; refuted, the table says 12 months. (b) The tier needs a card; "
     "confirmed. The tier is 12 months.", "The tier is 12 months.",
     "a candidates block goes whole: its enumerated readings and verdicts follow the withheld head"),
    ("notes", "Abandonment condition: if RD ever publishes a list, re-run it. RD has 120 hosts.", "RD has 120 hosts.",
     "an abandonment condition is withheld"),
    ("binding_note", "no hosted endpoint is offered, so any egress begins with a host a user must obtain from the compute "
     "lane libp2p mesh.", None, "a run-on that names the compute lane is withheld"),
    ("notes", "the one grep hit is compute/hashbang, which mentions the name). The two L40S rows differ by region.",
     "The two L40S rows differ by region.", "a grep hit is withheld, and its closing bracket with it"),
    ("binding_note", "300 GB is 60% of the filter and 0.1 MB/s is 8.6 GB a day, so the throttle binds first.", None,
     "a share of the filter is a comparison with the workload"),
    ("free_tier.stated", "Already recorded by the D-D1 agent; the portal is read-only for outsiders.",
     "The portal is read-only for outsiders.", "an agent by id is withheld, and the next clause starts with a capital"),
    # round 3, send-back of #56: other words for the same shapes
    ("chaining", "Pin the CID on a free pinning service (BRIEF 2.1). Reads are free.", "Reads are free.",
     "a private document by name and section, with no section sign"),
    ("retention.stated", "Deleted after 30 days (BRIEF DEAD-ENDS precedent: the same host). Files expire.", "Files expire.",
     "a private document by name alone"),
    ("notes", "One record for the provider and its two seed sub-findings. The quota is 2 TB.", "The quota is 2 TB.",
     "seed sub-findings are an earlier draft"),
    ("notes", "Named in the aggregators lane's Seen list without a record. The host is live.", "The host is live.",
     "a research lane by name"),
    ("extras.payment.entry_price", "a sibling lane records EUR 2.5 / 15 days", None, "a sibling lane is a research lane"),
    ("notes", "Recorded to close the survey, not to recommend. The plan is USD 3.", "The plan is USD 3.",
     "the research survey is withheld"),
    ("notes", "The survey is the second gate: a form after signup.", "The survey is the second gate: a form after signup.",
     "a vendor's survey stays"),
    ("free_tier.stated", "50 GB per project, so it fails the 500 GB-per-unit bar. Uploads use S3.", "Uploads use S3.",
     "the workload as a bar is withheld"),
    ("egress.terms", "Fits the 500 GB/day job if you front it with a free CDN. Egress is free.", "Egress is free.",
     "the workload as a job is withheld"),
    ("egress.terms", "unlimited traffic under a Fair usage policy on a 600 Mbit/s port",
     "unlimited traffic on a 600 Mbit/s port", "a fair-use policy goes whole with its adjective"),
    # round 3, second send-back of #56: a vendor's lane, a scratch machine and a technical floor are facts
    ("limits_note", "50 requests a day binds: a 1,000-item job takes 20 days on the no-card lane, and the 20 rpm cap "
     "spends the day's 50 requests in under three minutes.", "50 requests a day binds: a 1,000-item job takes 20 days "
     "on the no-card lane, and the 20 rpm cap spends the day's 50 requests in under three minutes.",
     "a vendor's no-card lane is a product route, not a research lane"),
    ("free_tier.stated", "The vendor names the independent-researcher lane directly: up to USD 5,000 in credits.",
     "The vendor names the independent-researcher lane directly: up to USD 5,000 in credits.",
     "a vendor's programme lane stays"),
    ("notes", "Read from the vendor page by the cheap-paid lane. The plan is USD 3.", "The plan is USD 3.",
     "a research lane by name stays withheld"),
    ("chaining", "Egg for the always-on box, iwinv for the per-day scratch box; both break at a 300 GB monthly traffic wall.",
     "Egg for the always-on box, iwinv for the per-day scratch box; both break at a 300 GB monthly traffic wall.",
     "a scratch box is a machine, not the research scratch tree"),
    ("notes", "The price is owned by scratch seed-western/records/x.json. The quota is 2 TB.", "The quota is 2 TB.",
     "a path in the research scratch tree stays withheld"),
    ("reliability_note", "The Free plan caps RAM at 0.5 GB, which is below the floor of most runtimes.",
     "The Free plan caps RAM at 0.5 GB, which is below the floor of most runtimes.", "a technical floor stays"),
    ("limits_note", "the per-feature multiplier is unpublished, so the binding constraint is unknown above the floor",
     "the per-feature multiplier is unpublished, so the binding constraint is unknown above the floor",
     "a vendor's tier floor stays"),
    ("notes", "10 GiB is 50x below the floor. Files expire.", "Files expire.", "the reader's floor stays withheld"),
    ("limits_note", "Files API request size capped at 500 MB (Messages 32 MB, Batch 256 MB).",
     "Files API request size capped at 500 MB (Messages 32 MB, Batch 256 MB).", "a vendor's Batch API size stays"),
    ("notes", "The cheapest site in the lane is on a .mu domain. Prices are in Rs.",
     "The cheapest site is on a .mu domain. Prices are in Rs.", "a full stop that starts a name keeps its space"),
    ("notes", "Sustained rate is 3.09 Mbit/s. Candidates considered for the claim: a soft rule; the page publishes no threshold.",
     "Sustained rate is 3.09 Mbit/s. The page publishes no threshold.",
     "a clause after a withheld clause and a semicolon starts a sentence"),
    # round 3: the names of operator projects (P16, P17, F1)
    ("evidence[].proved", "HTTP 200, 14 bytes. Log cf-codex/evidence/experiments/05-proton-worker/logs/final.json at "
     "2026-10-03T19:09:40Z.", "HTTP 200, 14 bytes.", "a path inside an operator project is a pointer and is withheld"),
    ("evidence[].proved", "create table, insert and select returned hello-f-research; max_connections 450",
     "create table, insert and select returned a test string; max_connections 450", "a test string that names this repository is replaced"),
    # round 3: relative dates and boilerplate (T1, B1)
    ("confidence_note", "The pricing page was read today and states 5 GB.", "The pricing page was read and states 5 GB.",
     "'read today' loses the relative date and keeps the clause"),
    ("confidence_note", "One page read moves it to documented.", None, "a boilerplate sentence alone is withheld"),
    ("confidence_note", "The page states 5 GB. verified_at is the instant its evidence URLs were fetched on 2026-10-22, "
     "read from the fetch log, not typed.", "The page states 5 GB.", "a boilerplate sentence inside a clause is deleted"),
    # round 3: the text left after a withhold (R3-A-06)
    ("notes", "New provider for the corpus. This is why it is listed here. Plans start at USD 2.",
     "Plans start at USD 2.", "a demonstrative that points at a withheld clause goes with it"),
    # live walk 2 (W2-03): a numbered rule of the research method (N18); a vendor's numbered clause stays
    ("limits_note", "The player re-encodes the upload, so originals are not what gets served \u2014 rule 4 disqualifier.",
     "The player re-encodes the upload, so originals are not what gets served.", "a rule-number tail goes and the fact stays"),
    ("tooling", "The docs tell you to shard across connections, which is rule 6 in action.",
     "The docs tell you to shard across connections.", "'which is rule N in action' goes"),
    ("reliability_note", "Anonymous read is a 1-hour signed S3 redirect, so re-resolve per request (rule 8); the quota API is rate-limited.",
     "Anonymous read is a 1-hour signed S3 redirect, so re-resolve per request; the quota API is rate-limited.",
     "a parenthesised rule number goes"),
    ("reliability_note", "Rule 1 applies: the download path must be discovered from the UI.",
     "The download path must be discovered from the UI.", "'Rule N applies:' goes and the sentence starts with a capital"),
    ("reliability_note", "This is exactly the upload-open / read-gated failure in rule 2. Do not count it as storage.",
     "This is exactly the upload-open / read-gated failure. Do not count it as storage.", "'in rule N' goes"),
    ("reliability_note", "Fails rule 4 outright. Measured on a live asset: the original is 2 MB.",
     "Measured on a live asset: the original is 2 MB.", "a clause that is only a rule verdict is withheld"),
    ("egress.terms", "Downloads 302 to a presigned URL with X-Amz-Expires=60, so rule 8 applies hard: re-resolve per request.",
     "Downloads 302 to a presigned URL with X-Amz-Expires=60: re-resolve per request.", "', so rule N applies:' becomes a colon"),
    ("identity_cost.detail", "an email address and a top-up of at least RUB 5,000: rule 3.1 requires a top-up.",
     "an email address and a top-up of at least RUB 5,000: rule 3.1 requires a top-up.", "a vendor's numbered clause is kept"),
    # live walk 2 (W-39): Markdown emphasis in a value (T2); a footnote asterisk stays
    ("notes", "**$0 ingress, $0 egress, $0 request fees** on the same page.", "$0 ingress, $0 egress, $0 request fees on the same page.",
     "bold markers go and the words stay"),
    ("notes", "The *combined* quota is 20 GB.", "The combined quota is 20 GB.", "italic markers go"),
    ("free_tier.stated", "5 GB free. 'Unlimited*' Personal at USD 12.99/mo, *see terms.", "5 GB free. 'Unlimited*' Personal at USD 12.99/mo, *see terms.",
     "a footnote asterisk after a word is not emphasis"),
    # use rights and licence terms (L3): the terms phrase goes, the technical fact beside it stays
    ("notes", "personal, non-commercial use", None, "L3: a use class alone is withheld"),
    ("notes", "viewing, downloading and printing FRED content is a permitted personal use", None,
     "L3: a permitted use is withheld"),
    ("notes", "no sharing of data or derived results with a third party without written approval", None,
     "L3: a sharing condition and the vendor's written approval are withheld"),
    ("free_tier.notes", "Every self-service plan, Free included, allows commercial use with attribution and a link to the original article.",
     None, "L3: a commercial-use and attribution condition is withheld"),
    ("evidence[].quote", "Results of the search services are allowed for usage outside of the Service.", None,
     "L3: a quoted right to reuse results is withheld"),
    ("retention.stated", "geocoding results may be stored permanently for most uses; map content may not be kept in a server-side cache",
     None, "L3: a right to store results, and its refusal, are withheld"),
    ("notes", "Storage: caching of responses for application performance is permitted; a systematic store of the content to "
     "compete, redistribute or avoid the limits is not. Bulk path: none.", "Bulk path: none.",
     "L3: a caching permission and the clause that answers it go; the next sentence stays"),
    ("evidence[].quote", "Tresorit Basic is built for personal use. It gives you 3 GB of encrypted storage.",
     "It gives you 3 GB of encrypted storage.", "L3: a quoted use sentence goes and the quoted quota stays"),
    ("notes", "Storage: responses may be cached for up to 60 minutes.", None,
     "L3: a caching term that carries a number is held, not published"),
    ("free_tier.stated", "Free plan, USD 0: 100 calls a month, HTTPS included, non-commercial use; no historical news.",
     "Free plan, USD 0: 100 calls a month, HTTPS included; no historical news.", "L3: a use class in a list of limits goes"),
    ("free_tier.stated", "IP to City Lite databases as monthly CSV downloads with no account, under CC BY 4.0",
     "IP to City Lite databases as monthly CSV downloads with no account", "L3: a data licence beside the offer goes"),
    ("evidence[].quote", "Lite downloads are updated monthly and distributed under the Creative Commons Attribution License.",
     "Lite downloads are updated monthly and distributed.", "L3: 'distributed under a licence' keeps its verb"),
    ("chaining", "The free datasets on GitHub (CSV and JSON, CC BY 4.0) are a no-key bulk start.",
     "The free datasets on GitHub (CSV and JSON) are a no-key bulk start.", "L3: a licence in a list in brackets goes"),
    ("egress.terms", "Block: 500 GB for EUR 15.00, unlimited speed, 50 connections, account sharing allowed.",
     "Block: 500 GB for EUR 15.00, unlimited speed, 50 connections.", "L3: account sharing goes and the block stays"),
    ("free_tier.stated", "jsDelivr is free for personal and commercial use with no limits on bandwidth",
     "jsDelivr is free with no limits on bandwidth", "L3: 'for personal and commercial use' goes"),
    ("evidence[].proved", "the free tier covers development, evaluation and non-commercial use",
     "the free tier covers development and evaluation", "L3: the last use of a list goes and the list closes with 'and'"),
    ("identity_cost.detail", "Signing up confirms non-professional (personal use) status and asks for an email.",
     "Signing up confirms non-professional status and asks for an email.", "L3: a use class in brackets goes, the identity stays"),
    ("binding_note", "The daily credit cap binds first for personal use; the 10-user limit matters only when serving others.",
     "The daily credit cap binds first; the 10-user limit matters only when serving others.",
     "L3: 'for personal use' after a technical clause goes"),
    ("evidence[].proved", "the Free plan allows 100 requests a day", "the Free plan allows 100 requests a day",
     "L3: a quota the plan allows is technical"),
    ("evidence[].proved", "up to 120 requests per minute are allowed before HTTP 429",
     "up to 120 requests per minute are allowed before HTTP 429", "L3: a rate that is allowed is technical"),
    ("notes", "Rate limit: 60 requests a minute; the free tier allows 100 requests a day.",
     "Rate limit: 60 requests a minute; the free tier allows 100 requests a day.", "L3: a rate limit is technical"),
    ("notes", "The commercial plan costs USD 49 a month for 100,000 requests.",
     "The commercial plan costs USD 49 a month for 100,000 requests.", "L3: 'commercial plan' is a plan name"),
    ("interface_detail", "the license key goes in the X-License-Key header", "the license key goes in the X-License-Key header",
     "L3: a license key is a credential"),
    ("notes", "A Windows licence is included in the price.", "A Windows licence is included in the price.",
     "L3: a licence sold with a server is a price"),
    ("limits[].value", "commercial licences run from EUR 300 to EUR 1,800 a year",
     "commercial licences run from EUR 300 to EUR 1,800 a year", "L3: a software licence sold by size is a price"),
    ("evidence[].quote", "The Open Source Edition is free software licensed under the Apache2 License.",
     "The Open Source Edition is free software licensed under the Apache2 License.", "L3: a software licence stays"),
    ("egress.terms", "\"There's a fair-use allowance generous enough for game servers, web apps and personal use.\"",
     "\"There's a fair-use allowance generous enough for game servers, web apps and personal use.\"",
     "L3: personal use as a workload is not a right"),
    ("notes", "individual usage is limited by three rolling windows of 5 hours, 7 days and 30 days",
     "individual usage is limited by three rolling windows of 5 hours, 7 days and 30 days", "L3: individual usage is a meter"),
    ("evidence[].quote", "The free GeoLite City is less accurate and is not recommended for commercial use cases.",
     "The free GeoLite City is less accurate and is not recommended for commercial use cases.",
     "L3: 'commercial use cases' is advice, not a right"),
    ("evidence[].quote", "Offset guardrail: page_size must not exceed 5000 rows;", "Offset guardrail: page_size must not exceed 5000 rows;",
     "L3: 'must not' on a parameter is technical"),
    ("chaining", "Free projects are public, so their run data may be shared with other users",
     "Free projects are public, so their run data may be shared with other users", "L3: visibility of data is technical"),
    ("evidence[].proved", "'you can store files up to 5 TB'", "'you can store files up to 5 TB'",
     "L3: what a user can store is a quota"),
    ("notes", "An MAU is a non-internal user that authenticated during a month.",
     "An MAU is a non-internal user that authenticated during a month.", "L3: 'non-internal user' is a meter"),
    # blind test 2 (F-13): a path of this repository with a backward slash, and the process shapes the test found
    ("extras.verified[].capture", "captures\\cloudflare-workers-static-assets-developers-cloudflare-com-workers-platform-limits-.txt",
     None, "F1: a capture path with a backward slash is withheld, as the forward-slash one is"),
    ("notes", "The quota is read from sources\\c\\ab\\page.txt; it is 5 GB.", "It is 5 GB.",
     "F1: a sources path with backward slashes goes with its clause, the number stays"),
    ("notes", "Measured from .tmp\\work\\probe.json on the box.", None, "N5: a scratch path with backward slashes is withheld"),
    ("limits[].value", "10 requests a second authenticated, 1,000 an hour and 10 a second per IP keyless, per the platform research report",
     "10 requests a second authenticated, 1,000 an hour and 10 a second per IP keyless",
     "N19: 'per the platform research report' goes and the limits stay"),
    ("limits[].value", "site difficulty and JavaScript rendering multiply a group's ladder total; the research report records a factor up to 40",
     "site difficulty and JavaScript rendering multiply a group's ladder total",
     "N19: a clause sourced to the research report goes, the technical clause stays"),
    ("notes", "The rank-1 position comes from the Artificial Analysis search index as recorded in the platform's research report, "
     "not from a measurement here.", "The rank-1 position comes from the Artificial Analysis search index, not from a measurement here.",
     "N19: 'as recorded in the platform's research report' goes"),
    ("notes", "https://lightning.ai/sign-up redirects to the incident page, so no Studio started. Keep dead. Reopen when "
     "status.lightning.ai resolves the incident.", "https://lightning.ai/sign-up redirects to the incident page, so no Studio started.",
     "N19: 'Keep dead.' and 'Reopen when ...' are filing instructions"),
    ("notes", "hub.degirum.com is login-walled today. What would reopen it: LatticeWork relaunching AI Hub under a new domain.",
     "hub.degirum.com is login-walled today.", "N19: 'What would reopen it' is a filing condition"),
    ("notes", "The cart is closed. Two further things the incumbent row did not carry. (1) The IPv4 is NAT with only 20 ports.",
     "The cart is closed. Two further things. (1) The IPv4 is NAT with only 20 ports.",
     "N19: 'the incumbent row did not carry' goes and the list it introduces stays"),
    ("notes", "What the incumbent did not say is that the 8 GB rung exists at USD 119.99 a year.",
     "The 8 GB rung exists at USD 119.99 a year.", "N19: 'what the incumbent did not say' goes, the price stays"),
    ("chaining", "Because /download serves orig_file_cid and not the transcode, this is the only host in this slot where the bytes "
     "come back intact.", "Because /download serves orig_file_cid and not the transcode, this is the only host where the bytes come back intact.",
     "N19: 'in this slot' goes as 'in the lane' does, and the technical fact stays"),
    ("free_tier.stated", "Japanese incumbent GPU VM with an hourly, daily and monthly ladder in JPY.",
     "Japanese incumbent GPU VM with an hourly, daily and monthly ladder in JPY.", "N19: a market incumbent stays"),
    ("free_tier.stated", "Adapter is 'temporarily closed. It is scheduled to reopen in Q4 2026'.",
     "Adapter is 'temporarily closed. It is scheduled to reopen in Q4 2026'.", "N19: a vendor that reopens stays"),
    ("chaining", "none while suspended; if it reopens it would be the only free host that publishes a TCP port.",
     "none while suspended; if it reopens it would be the only free host that publishes a TCP port.", "N19: 'if it reopens' is the vendor's"),
    ("limits[].value", "up to two server slots per account", "up to two server slots per account", "N19: a server slot stays"),
]

# (input, expected public title, what it proves): the title rule H1 (provider, tier, category), live walk 2 (W2-03)
TITLE_CASES = [
    ("AWS Open Data Sponsorship Program (revisit) - uncapped, 2 years, but the signatory must be an organisation",
     "AWS Open Data Sponsorship Program - uncapped, 2 years, but the signatory must be an organisation", "a review state in parentheses goes"),
    ("Source Cooperative (re-verify) - uncapped public publishing, beta-gated, BYOB is the real lever",
     "Source Cooperative - uncapped public publishing, beta-gated", "a review state and a trailing commentary clause go"),
    ("datarade \u2014 see candidate entry (fails-quota)", "datarade", "a cross-reference after a dash goes"),
    ("polarbackup (precedent, not a candidate)", "polarbackup", "a precedent note goes"),
    ("Alibaba Cloud ACR Enterprise Edition / OSS-backed registries (structural note, not a candidate)",
     "Alibaba Cloud ACR Enterprise Edition / OSS-backed registries", "a structural note goes"),
    ("IEEE DataPort - 2 TB per dataset free upload, but every read costs $40/month (rule 2 in its purest form)",
     "IEEE DataPort - 2 TB per dataset free upload, but every read costs $40/month", "a rule number goes"),
    ("TheHost.ua KeepData \u2014 10 TB flat with traffic included, WebDAV/SFTP/Samba, the best Western-facing $/TB in the set",
     "TheHost.ua KeepData \u2014 10 TB flat with traffic included, WebDAV/SFTP/Samba", "'the best ... in the set' goes, the offer stays"),
    ("GitHub Container Registry (GHCR) via ORAS \u2014 known, numbers re-verified", "GitHub Container Registry (GHCR) via ORAS",
     "a review note goes with the clauses after it"),
    ("Ollama registry (registry.ollama.ai) \u2014 the strongest finding in this slot", "Ollama registry (registry.ollama.ai)",
     "ranking commentary goes and a technical parenthesis stays"),
    ("maverick1983/google-drive-service-account 45 tb recipe (the reference case", "maverick1983/google-drive-service-account 45 tb recipe",
     "an unclosed parenthesis with a note goes"),
    ("Micro Plus (cheapest listed plan)", "Micro Plus", "a tier loses its ranking note"),
    ("Spotify for Creators (formerly Anchor)", "Spotify for Creators (formerly Anchor)", "a former name stays"),
    ("Usenet indexer (web only, no Newznab API found)", "Usenet indexer (web only, no Newznab API found)", "a technical parenthesis stays"),
    ("Tencent Cloud Agent Runtime  -  Agent Sandbox", "Tencent Cloud Agent Runtime  -  Agent Sandbox", "a title with no note is untouched"),
    ("(revisit)", "(revisit)", "a title is never emptied"),
]

# the leak scan reads every text cell of the public store, including history titles, aliases and entity names,
# which no clause rule rewrites. (text, must the scan flag it, what it proves)
LEAK_CASES = [
    ("Not in dossier/compute (searched: x, no record).", True, "a dedupe search of this repository"),
    ("the 2-hour cap is a number the census did not have", True, "the census"),
    ("10 percent of the 1 TB a day serving target", True, "the serving target"),
    ("geocoding data from the US Census Bureau API", False, "a vendor census"),
    ("ipfs / shipyard (the 'ipfs-like service' the client half-remembers)", True, "a provider name about the client"),
    ("uptobox as a precedent for the client", True, "an alias that addresses the client"),
    ("The operator's stated pain was that free tiers demand a card", True, "the operator's circumstances"),
    ("the 500 GB to 1 TiB a day workload", True, "the client's serving workload"),
    ("dossier/egress/ajam-ssh-relay.json", True, "an operator-owned record named in a header"),
    ("What I could not establish: the phone step", True, "first-person process narrative"),
    ("https://fshy.ajam.dev/api/v1/help.txt", False, "the public site's own address"),
    ("the tunnel cannot pass the client IP", False, "the client as software"),
    ("the prefix is routed to the client's endpoint", False, "a routed endpoint"),
    ("the operator published a key-rotation notice", False, "a vendor's operator"),
    ("the worst option for a client serving 500 GB a day", True, "a workload as 'a client serving'"),
    ("Save Page Now needs the operator's Internet Archive keys", True, "the operator's own keys"),
    ("the most interesting recurrence in this assignment", True, "the brief of a session"),
    ("a client without a descriptive User-Agent", False, "an HTTP client"),
    ("the read broker's stored copy records the same 403", True, "the page reader under another name"),
    ("a broker-side HTTP 530", True, "a status written as the reader's"),
    ("each user of the tunnel broker", False, "a tunnel broker"),
    # a personal e-mail address or phone number in a published field (personal_scan, E1 and T1 to T4)
    ("write to jane.doe@gmail.com for a quota", True, "a personal e-mail address"),
    ("write to dr.person@university.edu for a quota", True, "a personal address on an institution's domain"),
    ("write to support@vendor-host.com for a quota", False, "a role address"),
    ("write to GRANTS@vendor-host.com", False, "a role address in capitals"),
    ("write to gcp-public-data@vendor-host.com", False, "a role word inside a longer role address"),
    ("the form's placeholder is user@example.com", False, "a placeholder on a reserved domain"),
    ("the probe address was probe@example.invalid", False, "a placeholder on a reserved top-level domain"),
    ("log in with ssh new@sdf.org to apply", False, "a login syntax that a service documents"),
    ("ssh -t -R 80:localhost:3000 stable@proxy.tunnl.gg.", False, "a documented login before a full stop"),
    ("a second person at the same host, sam@sdf.org", True, "an address on a documented host is not documented itself"),
    ("a contact point is [address removed]", False, "the token the projection writes"),
    ("call +49 30 1234 5678 in office hours", True, "a phone number with an international prefix"),
    ("the form's placeholder is '+40 721 234 567'", False, "a placeholder phone number"),
    ("20 + 200(0.12) = 44.00 and +86-gated", False, "arithmetic and a country gate are not phone numbers"),
    ("order confirmation by WhatsApp 0412 345 678", True, "a phone number after a label"),
    ("activation needs WhatsApp number verification in a format the operator sends", False, "the word phone, no number"),
    ("the sale ends phone 2026-10-24", False, "a date after a label"),
    ("reach the desk on 415 867 5309", True, "a phone number in the ddd ddd dddd shape"),
    ("tel 415-555-0132", False, "a number in the 555 exchange is a placeholder"),
    ("Forwarding: UDP 583-841-3346.mudcat.io:25566 -> 127.0.0.1:25565", False, "a host name that starts with digits"),
    ("WhatsApp (11) 91234-5678", True, "a phone number with a parenthesised area code"),
    ("captures\\cloudflare-pages-developers-cloudflare-com-pages-platform-limits-.txt", True,
     "a capture path of this repository with a backward slash (blind test 2, F-13)"),
    ("run it from .tmp\\work", True, "a scratch path with a backward slash"),
    ("the installer writes C:\\tools\\app.exe", False, "a vendor's Windows path is not this repository's"),
]

URL_CASES = [
    ("https://fetch.web.pkgforge.dev/https://catbox.moe/", "https://catbox.moe/", "a broker fetch URL becomes its origin"),
    ("https://www.hetzner.com/storage/storage-box/?__provider=fire", "https://www.hetzner.com/storage/storage-box/",
     "the reader parameter of a fetched address goes"),
    ("https://example.org/a?__provider=firecrawl&b=1", "https://example.org/a?b=1", "the reader parameter goes and the query stays"),
    ("https://archive.web.pkgforge.dev/capture/20260419203508/https://cirrus-ci.org/faq/",
     "https://web.archive.org/web/20260419203508/https://cirrus-ci.org/faq/", "a broker archive capture becomes web.archive.org"),
    ("https://api.gh.pkgforge.dev/repos/monosans/proxy-list", "https://api.github.com/repos/monosans/proxy-list",
     "the GitHub API mirror becomes api.github.com"),
    ("https://dash.vpn.ajam.dev/docs/measurements/sstp.md", None, "an operator host with no origin is withheld"),
    ("probe:unspecified", None, "a migration placeholder is withheld"),
    ("probe:sources/p/91/91472642eb7e0771796c8765b1819bbb4944969ac21a2e80affb02c211a59b7d.json.gz", "probe:kept-privately",
     "a stored copy in this repository is named as kept privately"),
    ("probe:broker-read https://lightningusenet.com/ 2026-10-23", "https://lightningusenet.com/",
     "a page reader note becomes its origin URL"),
    ("probe:vpngate-lane4-exit-asn-sweep", "probe:vpngate-exit-asn-sweep", "a lane label leaves a probe name"),
    ("https://example.com/pricing", "https://example.com/pricing", "an ordinary URL is kept"),
    ("probe:C:\\Users\\someone\\x.json", None, "U13: a Windows local path is withheld"),
    ("probe:run\\.tmp\\work\\probe.json", None, "U13: a scratch path with a backward slash is withheld (blind test 2, F-13)"),
    ("probe:\\home\\someone\\x.json", None, "U13: a home path with backward slashes is withheld (blind test 2, F-13)"),
]


def main():
    rules = json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8"))
    p = project.Projector(rules, [])
    fails = 0
    for path, inp, want, why in CASES:
        got, _ = p.clean_prose(inp, path)
        ok = got == want
        fails += not ok
        print("%s %s" % ("PASS" if ok else "FAIL", why))
        if not ok:
            print("     in:   %r\n     want: %r\n     got:  %r" % (inp, want, got))
    for inp, want, why in URL_CASES:
        got, _ = p.rewrite_url(inp)
        ok = got == want
        fails += not ok
        print("%s %s" % ("PASS" if ok else "FAIL", why))
        if not ok:
            print("     in:   %r\n     want: %r\n     got:  %r" % (inp, want, got))
    lrx = re.compile("|".join("(?:%s)" % x for x in rules["leak_scan"]))
    for text, want, why in LEAK_CASES:
        ok = bool(lrx.search(text)) == want
        fails += not ok
        print("%s leak scan %s: %s" % ("PASS" if ok else "FAIL", "flags" if want else "passes", why))
    rec = {"topic": "egress", "slug": "ajam-ssh-relay", "provider": "tcp.ssh.relay.ajam.dev"}
    ok = p.excluded(rec, "egress/ajam-ssh-relay")
    fails += not ok
    print("%s an operator-owned service is excluded whole" % ("PASS" if ok else "FAIL"))
    rec = {"topic": "storage", "slug": "catbox-moe", "provider": "catbox.moe", "url": "https://fetch.web.pkgforge.dev/https://catbox.moe/"}
    ok = not p.excluded(rec, "storage/catbox-moe")
    fails += not ok
    print("%s a third-party record reached through the broker is not excluded" % ("PASS" if ok else "FAIL"))
    extra = 0
    # round 2: a path of a published record becomes its id; a path of an unknown record is withheld with its clause
    q = project.Projector(rules, [{"topic": "compute", "slug": "lambda"}, {"topic": "coding-subs", "slug": "devin"}])
    for path, inp, want, why in [
            ("chaining", "at USD 3.99 per H100 hour (dossier/compute/lambda.json) USD 100 is 25 hours",
             "at USD 3.99 per H100 hour (compute/lambda) USD 100 is 25 hours", "a record path becomes the record id"),
            ("notes", "The pricing fact is Devin's, and it is recorded once, in dossier/coding-subs/devin.json",
             "The pricing fact is Devin's; see coding-subs/devin", "a cross-reference keeps the id and loses the process"),
            ("notes", "See dossier/compute/not-published.json for the rest.", None,
             "a path of a record that is not published is withheld")]:
        got, _ = q.clean_prose(inp, path)
        ok = got == want
        fails += not ok
        extra += 1
        print("%s %s" % ("PASS" if ok else "FAIL", why))
        if not ok:
            print("     in:   %r\n     want: %r\n     got:  %r" % (inp, want, got))
    # round 2: a key that is a research label is renamed or withheld
    out, _, _, _ = q.project("compute/x", {"topic": "compute", "slug": "x", "probe": {"file": "sources/2026-10-22/x.json"},
                                           "extras": {"wave2": {"class": "vps"}, "census_rows": ["x"], "talaria_m10h_usd": 9.5}})
    ok = out["extras"] == {"facets": {"class": "vps"}} and out["probe"] == {}
    fails += not ok
    extra += 1
    print("%s a research label key is renamed (wave2 -> facets) or withheld (census_rows, talaria_*, probe.file)" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     got: %r" % (out,))
    # terms keys of a record (K60 to K64) are withheld whole; a technical key beside them stays
    out, _, strip, _ = q.project("data-apis/x", {"topic": "data-apis", "slug": "x", "extras": {
        "data_licence": "personal, non-commercial use", "results_storage": "data may be cached for 24 hours",
        "results_storable": "yes, with attribution (CC BY 4.0)", "sharing": "allowed",
        "sharing_and_class_separated": "yes: sharing forbidden by the terms", "bulk_path": "monthly CSV downloads"}})
    ok = (out["extras"] == {"bulk_path": "monthly CSV downloads"}
          and sorted(r for _, r, _ in strip) == ["K60", "K61", "K62", "K63", "K64"])
    fails += not ok
    extra += 1
    print("%s the licence, storage-right and account-sharing keys are withheld (K60 to K64)" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     got: %r %r" % (out, strip))
    # a clause rule's defs: {NAME} stands for a named part, a quantifier {0,60} is left alone, and a circle is an error
    ok = project.expand(r"{A}x[^.]{0,60}{B}", {"A": "a{B}", "B": "b"}) == r"abx[^.]{0,60}b" and project.expand("{A}", None) == "{A}"
    try:
        project.expand("{A}", {"A": "{B}", "B": "{A}"})
        ok = False
    except ValueError:
        pass
    fails += not ok
    extra += 1
    print("%s defs expand a named part, leave a quantifier alone and refuse a circle" % ("PASS" if ok else "FAIL"))
    # round 2: a history title is published only when it states a technical fact
    hrx = re.compile(rules["history_title"]["narrative_re"])
    for title, want in [
            ("The operator decided seven open questions: three rules bind, three units and two topics are added", True),
            ("Research runs now have one writer and a second key, and the first four runs found ten defects in the harness", True),
            ("The rung beside a provider was the rung we wished it had", True),
            ("The census gave Codeberg 8-core runners and the vendor table gives 4", True),
            ("A review found 58 defects in the three answers", True),
            ("Hetzner's fair-use threshold is 250 TB/month, not 50 to 100, and the margin is 8.3x", False),
            ("Turso's free plan was recorded as having no idle clock, and it archives an inactive database after 10 days", False),
            ("Hugging Face Spaces has a free lane, and the ZeroGPU allowance recurs daily", False),
            ("The AWS US region is free", False)]:
        ok = bool(hrx.search(title)) == want
        fails += not ok
        extra += 1
        print("%s history title %s: %s" % ("PASS" if ok else "FAIL", "narrates" if want else "is technical", title[:60]))
    # round 3: truncated values, whole-value boilerplate and renamed keys in unknown rows
    cut = "x" * 160 + " the free tier is 5 GB and the paid tier is 20 G"
    cut = cut + "y" * (190 - len(cut))
    cut = cut[:181] + " pass mid"
    out, _, _, unk = q.project("storage/x", {"topic": "storage", "slug": "x", "notes": cut,
                                              "identity_cost": {"detail": "derived from the record's prose, not from an identity field, and no signup was executed: he unl"},
                                              "binding_note": "no constraint of a named kind was recorded; the verdict rests on the quota sentence rather than on a named limit",
                                              "extras": {"wave2": {"class": "x x x x x x x x x x x x x x x x x x x x x x x x x x x x the seed row says x"}}})
    ok = (out["notes"].endswith(" pass\u2026") and len(out["notes"]) < 190 and out["identity_cost"] == {"detail": None}
          and out["binding_note"] is None and all("wave" not in u[0] for u in unk))
    fails += not ok
    extra += 1
    print("%s a value cut at 190 ends at a whole word with an ellipsis; a template value is withheld; unknown rows "
          "carry the published key" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     got: %r / %r" % (out, unk))
    # a cut value whose last clause is only the cut word: the word goes, and a value of that word alone is withheld
    frag = "w" * (190 - len(" The quota is 5 GB; P")) + " The quota is 5 GB; P"
    out, _, _, _ = q.project("storage/y", {"topic": "storage", "slug": "y", "notes": frag})
    ok = out["notes"].endswith("5 GB\u2026") and not out["notes"].endswith("P\u2026")
    fails += not ok
    extra += 1
    print("%s a cut value loses its cut last word, also when that word is a clause of its own" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     got: %r" % (out["notes"][-60:],))
    # the personal-detail scan: its patterns are in leak_scan too, both allow-lists pass, and the source scan reads
    # published fields only
    spec = rules["personal_scan"]
    ok = all(pat["re"] in rules["leak_scan"] for pat in spec["patterns"])
    fails += not ok
    extra += 1
    print("%s every personal_scan pattern is also in leak_scan, which the public export applies to every file" % ("PASS" if ok else "FAIL"))
    erx = next(re.compile(pat["re"]) for pat in spec["patterns"] if pat["id"] == "E1")
    bad = [w for w in spec["role_words"] if erx.search("write to %s@vendor-host.com now" % w)]
    bad += [a for a in spec["documented_addresses"] if erx.search("use %s now" % a)]
    ok = not bad
    fails += not ok
    extra += 1
    print("%s every role word and documented address in personal_scan passes the e-mail pattern" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     flagged: %r" % (bad,))
    import build  # noqa: E402
    synthetic = [
        {"rid": "compute/a", "raw": {"topic": "compute", "slug": "a", "provider": "A", "notes": "ask jane.doe@gmail.com",
                                     "evidence": [{"url": "https://example.com/", "proved": "support@a.example.org"}]}},
        {"rid": "compute/b", "raw": {"topic": "compute", "slug": "b", "provider": "B", "extras": {"contact": "jane.doe@gmail.com",
                                     "operator": "tel +49 30 1234 5678", "operator_channel": "WhatsApp 0412 345 678"}}},
        {"rid": "compute/c", "raw": {"topic": "compute", "slug": "c", "provider": "C",
                                     "evidence": [{"url": "https://example.com/", "proved": "WhatsApp 0412 345 678"}]}},
        {"rid": "egress/ajam-ssh-relay", "raw": {"topic": "egress", "slug": "ajam-ssh-relay", "provider": "R",
                                                  "notes": "jane.doe@gmail.com"}},
    ]
    got = sorted((h[0].split()[0], h[0].split()[1], h[0].split()[2]) for h in build.personal_scan(synthetic, rules))
    ok = got == [("compute/a", "$.notes", "E1"), ("compute/c", "$.evidence[0].proved", "T2")]
    fails += not ok
    extra += 1
    print("%s the source scan flags a personal address or number in a published field, and reads neither a role address, "
          "a dropped field (extras.contact, extras.operator) nor an excluded record" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     got: %r" % (got,))
    for inp, want, why in TITLE_CASES:
        got = p.clean_title(inp)
        ok = got == want
        fails += not ok
        extra += 1
        print("%s title: %s" % ("PASS" if ok else "FAIL", why))
        if not ok:
            print("     in:   %r\n     want: %r\n     got:  %r" % (inp, want, got))
    # the title rule runs on the title fields of a projected record and never on its slug
    out, tally, strip, _ = p.project("storage/x", {"topic": "storage", "slug": "datarade-see-candidate-entry",
                                                   "provider": "datarade \u2014 see candidate entry (fails-quota)", "tier": "Micro Plus (cheapest listed plan)"})
    ok = (out["provider"] == "datarade" and out["tier"] == "Micro Plus" and out["slug"] == "datarade-see-candidate-entry"
          and tally["modified"] == 2 and {r for _, r, _ in strip} == {rules["title_rule"]["id"]})
    fails += not ok
    extra += 1
    print("%s the title rule rewrites provider and tier, logs its rule id and keeps the slug" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("     got: %r %r %r" % (out, tally, strip))
    n = len(CASES) + len(URL_CASES) + len(LEAK_CASES) + 2 + extra
    print("\n%d of %d cases pass" % (n - fails, n))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
