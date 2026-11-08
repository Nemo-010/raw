# The clock: which machines have a deadline, and what it is

The front page of this topic states that the binding constraint on compute is time and
not money. This document tests that claim against the records, and the test is
uncomfortable. ⛔ **67 of the 1,411 records carry a numeric clock at all**: 52 carry a
numeric `wall_clock_min` and 24 a numeric `idle_reap_s`, with 9 carrying both. The other
1,344 say something about time in prose, or say nothing, and a sentence is not a number a
reader can schedule against. The two tables below are a selection, not the full set: they
list 24 wall-clock rows and 13 idle rows, against 52 and 24 in the records.

So the claim is probably right and it is not yet evidenced. This page states what the
records do carry, ranks the clocks that exist, and names the ones that are described
rather than stated.

## Why the clock outranks the price

A sandbox bills while it runs. That makes its monthly cost a function of how long it is
held, and it makes the session cap the only number that decides whether a workload fits
at all. A sandbox at USD 0.24 an hour is USD 2.40 a month at ten hours a day and
USD 173.71 at 24/7, and it is the same rate.

A workload that exceeds the cap does not run slowly. It does not run. That is the
difference between a limit and a price: a price is a budget, and a cap is a wall.

## The wall-clock caps, shortest first

These are a selection of the records that state a maximum session, in a numeric field or
in the vendor's own sentence. A reader planning a job longer than any row here needs a
different product.

| Provider | Cap | What it is |
| --- | --- | --- |
| Riza | 30 s | function invocation |
| Yepcode | 30 s | a serverless run |
| Browserless | 2 min | a browser session |
| AWS Lambda | 15 min | per invocation |
| AWS Lambda MicroVMs | 15 min | per invocation |
| Browserbase | 15 min | a browser session on Free |
| Steel | 15 min | a browser session |
| Vercel Sandbox | 45 min | maximum session |
| E2B | 60 min | per session |
| Arga Labs | 60 min | automatic expiry |
| Collimate | 60 min | per session |
| Google Cloud Run | 60 min | per request, the maximum |
| Killercoda | 60 min | per scenario |
| Remote Browser | 60 min | per session |
| Solari | 60 min | per session |
| Cloudcruise | 120 min | per session |
| Lightning AI | 240 min | a forced restart on the free Studio |
| GitHub Actions | 360 min | per job on a hosted runner |
| Google Cloud Shell | 720 min | the hard maximum |
| Google Colab | 720 min | per notebook, conditional |
| Flow Swiss Mac | 1,440 min | the minimum allocation, not a cap |
| Modal | 1,440 min | the maximum, via the timeout argument |
| Railway | 1,440 min | the anonymous box's claim window |
| Sandbox as a Service | 1,440 min | per sandbox |

⭐ **The median of these rows is one hour.** Fifteen of the 24 are 60 minutes or less, and
the two shortest are measured in seconds. A workload that needs to stay up is not in this
table at all.

⚠ **Two rows are not caps and are in this table because their records carry a window
that is not a cap.** Flow Swiss Mac's 1,440 minutes is a *minimum* allocation and a bill;
Railway's is the window in which an anonymous box must be claimed. A reader who sorts this
column ascending and picks the largest has picked a floor and a deadline.

## The idle reaps, shortest first

An idle reap is a different mechanism from a wall-clock cap, and it is kinder to a
workload that keeps working. A session that is touched keeps going and one that waits is
killed, so the question is whether the workload is bursty or periodic.

| Provider | Idle window | What resets it |
| --- | --- | --- |
| Blaxel | 5 s | standby after 5 s without a connection |
| Modal | 60 s | the keep-alive after the last input, and it is billed |
| Amp Orbs | 300 s | activity |
| CreateOS | 300 s | activity |
| Daytona | 900 s | activity; 15 minutes by default |
| Render | 900 s | inbound HTTP requests and WebSocket messages |
| SF Compute | 900 s | activity; a node that goes idle bills for its window |
| Azure App Service F1 | 1,200 s | a direct request only, not a portal visit |
| Azure Cloud Shell | 1,200 s | activity |
| Kaggle Notebooks | 1,200 s | activity; 20 minutes of interactive idle |
| Google Cloud Shell | 2,400 s | activity |
| Koyeb | 3,600 s | inbound traffic; not configurable |
| Hugging Face ZeroGPU | 172,800 s | a visitor; the Space sleeps after 48 hours |

⛔ **Blaxel's five seconds is the harshest clock in the topic.** The sandbox goes to
standby after five seconds without a connection, so a process that waits for anything
suspends. That is a correct design for a request-response product and a wall for an agent
that waits for a human.

⚠ **Azure App Service F1's 20 minutes is reset by a direct request and nothing else.**
The record quotes the page: a portal visit or a Kudu request does not reset the timer.
A keepalive that pings the wrong endpoint does not keep the app awake.

## The clocks that are described and not stated

Thirty-nine sandbox records say something about time and carry no number. Across the
whole topic, 98 records carry a note and no numeric clock. They are the topic's largest
evidentiary gap, and the shapes are worth naming because each one is a different
problem.

**A cap the customer sets.** `ainclave` quotes the vendor: "We do not bound how long a
session may run." `alibaba-agentrun` states no vendor wall-clock cap and that the customer
sets the caps. `archal` states a sandbox resets to its baseline between runs with no
clock. Those are three different sentences with one meaning: there is no server-side
deadline, and the record cannot put a number in the field.

**A cap stated for one tier and not another.** `brimble` records a 120-minute sandbox cap
for its Hacker tier and no cap for its others. `archil` gives 30 minutes of sandbox
compute in total on Free as a hard cap with no overage, which is a quota rather than a
clock and is filed in the note.

**A clock that is the process's own lifetime.** `butter` states the sandbox's lifetime is
the client process's lifetime. `beam` states no automatic reap, because the VM bills per
second while running.

**A cap that was not read.** `agent-37` records that an auto-sleep setting exists and
that the interval was not read on a page that answered. That is the honest label, and it
is also a one-request fix.

**A default that is not a limit.** `lizard` records that the raw API expires nothing when
`timeoutMs` is 0 and that the SDK and CLI default to 300 seconds. A default is what the
tool does, not what the server enforces, and confusing the two is how a session that
worked in a test dies in production.

**A billing tick mistaken for a cap.** `declaw` meters every 30 seconds against
provisioned resources and bills a lagging tick at most 90 seconds. That is a rounding
rule, not a deadline.

⚠ **Eleven records carry a number and a time unit inside a prose note while their
numeric field is empty**, and three of the eleven state a real cap: `archil` at 30
minutes of sandbox compute, `lizard` at a 300-second default, and `boat` at a 30-second
command. The other eight name a billing floor, a trial clock or an example session, and
none of them is a deadline. ⚠ The distinction matters because a reader scanning the
notes for a number will find eleven and only three are caps.

## The login clocks, which are a third mechanism

A pubnix shell has no session cap and no idle reap. It has an account expiry that
watches whether a human logged in, and the window runs from 30 days to five years.

| Host | Clock | What resets it |
| --- | --- | --- |
| hashbang | 30 days | an SSH login, or the presence of `/home/<user>/.keep-account` |
| SDF Public Access UNIX | 2 years | a UNIX login, read from `lastlog` |
| ctrl-c.club | 5 years | a login |
| tilde.green | none stated | the host states idle accounts are welcome |
| tilde.club | none found | no idle policy on any first-party page |
| serv00 | none published | no idle kill and no expiry stated |
| tilde.town | no expiry, and no port | services and cron are local-only |

⛔ **hashbang's 30 days is the shortest clock in the topic that a file can defeat.**
`/home/<user>/.keep-account` is the opt-out and it is a one-line cron on any other
machine.

⚠ **SDF's clock reads `lastlog`, so a background job does not keep the account alive.**
A process that runs for two years and never logs in is still an expired account, which
is the opposite of how a sandbox clock works.

⚠ **`tilde.zone` was demoted for a related reason.** It answers SSH and serves a
Mastodon instance rather than a shell, so a banner proves a host and not a free account.

## What this means for the four shapes

| the workload | the shape that fits | why |
| --- | --- | --- |
| a job under an hour | any sandbox in the wall-clock table | the median cap is exactly one hour |
| a job of several hours | a VPS, or a sandbox with a stated 24-hour maximum | Modal, Railway and Sandbox as a Service are the only 1,440-minute rows |
| a process that waits | a VPS, or a runtime with no idle reap | a 15-minute reap kills anything that blocks on input |
| a daemon that answers at 03:00 | Oracle, the Google e2-micro, or a pubnix shell | three free rows, and the rest of the topic cannot serve |

⭐ **The third row is the one the topic's price tables hide.** A sandbox at USD 2.17 a
month is cheap and it reaps in 15 minutes, so it cannot host a workload that waits for
input. The price column ranks a product that fails the first requirement.

## What is not established

⛔ **No clock here was observed.** Every number on this page is a vendor sentence read on
2026-10-22. Not one session was held and timed, so the difference between a documented
reap and an enforced one is unmeasured everywhere in the topic.

**The eleven prose-only numbers sit outside their numeric fields.** They are listed
above as findings rather than repaired, because a count over the numeric column and a
count over the notes disagree and a reader should see both.

**No provider was tested for a clock that resets on creation rather than on activity.**
That distinction decides whether a keepalive works, and no record in this topic states
which kind its clock is.

**The 370 records with no clock statement are not all clockless.** Some providers
publish no deadline because there is none, and some because the page does not say. The
records distinguish those in prose and the field cannot, which is why the field is
empty on both.
