# macOS and Windows hosts: what a non-Linux machine costs, and who gives one away

Thirty-six records in this topic price a machine that is not Linux: 23 macOS
hosts and 13 Windows ones. Both classes share one structure and not one
market. **The macOS class is decided by a licence, and the Windows class is
decided by a surcharge on an ordinary VM.** The 13 Windows records are cloud
and desktop products. The cheap Windows VPS market is a different class and is
priced in [`windows-vps.md`](windows-vps.md). That document sweeps sixteen
lanes: the floor is **USD 8.11 a month on Layer7's annual cycle** for 4 cores,
16 GiB and 80 GB, and **USD 10.14 a month on its monthly cycle**, not the USD
40.00 that a licence-supplied search produced. At least 316 distinct provider labels were
read and nothing below USD 8.11 was found.

The answer, in one paragraph. **No record in either class gives a free machine
that a reader can log into and keep.** Ten of the 23 macOS records are
continuous-integration products with a macOS lane rather than Mac hosts. The
free capacity in that lane is build minutes, and eight of the ten macOS
`qualifies*` rows are CI. The two macOS rows that are not CI are a
device-testing service with no stated quota (Revyl) and, as the last resort, a
self-hosted licence for Macs the reader already has (Tart + Orchard, 100 CPU
cores free). On Windows, four of the 13 records carry a `qualifies*` verdict
and no two qualify the same way. Two are an account clock and two are a
one-time credit. Cua's 20 remote hours were recorded as a monthly allowance;
its live page states that it rents no machine and connects to the customer's
own compute, which makes it self-hosted, and the record is `dead`. A Windows
licence is a surcharge a reader can compute. At Daytona's rates a 2 vCPU / 4
GiB Windows sandbox costs USD 246.16 for a month at 24/7. USD 125.27 of that
is the licence, and 50.9 per cent is the real price of the operating system.

## The count that decides both classes

| class | records | `qualifies*` | `trial-only` | `paid-only` |
| --- | --- | --- | --- | --- |
| macOS host | 24 | 10 | 2 | 12 |
| Windows host | 13 | 4 | 2 | 6 |
| both | 37 | 14 | 4 | 18 |

One of the 13 Windows records is `dead` and is not in the verdict columns.

Rung on the 37: 32 are `documented`, four are `reported` (`aws-ec2-mac`,
`aws-ec2-windows`, `blacksmith`, `limrun`) and one is `unverified` (`autocomputer`, whose
origin answered every fetch route with a 429 challenge). ⛔ **Not one of the 37 was booted**,
so every number below is a page read and no boot was observed.

## The macOS lane is mostly CI, and that is the answer to most of it

Ten of the 23 macOS records sell a build service. Each one is a way to run a job on a
machine that is destroyed afterwards, and none of them is a Mac a reader can log into.
The prices belong to [`ci-cd-runners`](../../ci-cd-runners/README.md), so this document
does not reprice them.

| Provider | What the free allowance meters | macOS in the record | Price owner |
| --- | --- | --- | --- |
| Xcode Cloud | 25 compute hours a month with a USD 99 a year membership | Apple's own build service | `ci-cd-runners` |
| Bitrise | build credits, no number published | mobile CI, iOS is the main lane | `ci-cd-runners` |
| Codemagic | free below 100,000 MAU of the app | mobile CI, Mac builders | `ci-cd-runners` |
| Expo | EAS build minutes, no count published | React Native build service | `ci-cd-runners` |
| Buildkite hosted | 2,000 **Linux** vCPU-minutes a month | the free pool is Linux only | `ci-cd-runners` |
| CircleCI | a free tier the price list does not state | macOS executors are a paid class | `ci-cd-runners` |
| Cirrus Runners | none published; a subscription | dedicated runners to 4 M4 Pro cores | `ci-cd-runners` |
| Blacksmith | USD 12 a month of credit, not re-read | GitHub Actions runners | `ci-cd-runners` |
| Depot | 2,000 sandbox minutes inside a 7-day trial | GitHub Actions runners | `ci-cd-runners` |
| WarpBuild | none; USD 0.003 a minute upward | Arm, Intel and Apple Silicon lanes | `ci-cd-runners` |

⭐ **The one row that is not a Mac lane at all is Buildkite's.** Its free pool is 2,000
Linux vCPU-minutes a month, and the record states the Linux word (`buildkite.com/pricing`,
read 2026-10-22). A reader who files that row under macOS has been misled by a category,
not by a number.

⚠ **Depot is the only one of the ten that states a trial rather than a tier.** It is also
the one a reader is most likely to over-value. 2,000 sandbox minutes sounds like a month of
work and it expires in seven days (`depot.dev/pricing`, read 2026-10-22).

**The two macOS `qualifies*` rows that are not CI.**

**Tart + Orchard, by Cirrus Labs**, is a licence and not a machine. A Free Tier licence
applies by default with no purchase: 100 CPU cores across Tart and 4 Orchard workers, with
Gold at USD 12,000 a year for 500 cores and Platinum at USD 36,000 for 3,000
(`tart.run/licensing/`, read 2026-10-22). The arithmetic is the boundary: 100 cores is 12
Mac minis at 8 cores each, and a thirteenth does not fit.

⚠ **That free core count is a permission, not capacity.** The software runs on Apple
hardware, and the reader owns none, so the 100 cores are worth zero tonight. It is
recorded because a reader who does rent a Mac needs to know the licence costs nothing, and
because the corpus must not present a permission as a machine.

**Revyl** gives "a free start" on mobile test automation against real iOS devices, and its
record states no quota, no plan and no price for the paid ladder (`revyl.com`, read
2026-10-22). A free start with no allowance behind it is a signup page, and the row is
`qualifies-with-caveat` on the strength of the word free.

⚠ **Two of these ten are placeholders and one is a vocabulary defect.** `circleci` and
`cirrus-runners` both carry the literal sentence "the source card records a free tier
without a credit amount", which is a placeholder rather than a finding. Worse,
`cirrus-runners` carries `qualifies-with-caveat` while its own `free_tier_kind` is `none`:
the verdict inherited a tier the field says does not exist.

## The licence, which is the macOS constraint

Three records put a licence between the reader and a Mac, and the licence is a different
object in each: a core count, an Apple membership, and a key that phones home. It is the
one axis where the macOS class has more free capacity than the Windows class and less of it
usable. This table is a view of three rows already listed above, read along the licence
axis rather than the price axis.

| Provider | Free | Bound by | What it actually gives |
| --- | --- | --- | --- |
| Xcode Cloud | 25 compute hours a month | USD 99 a year membership | Apple-run build minutes |
| Tart + Orchard (self-hosted) | 100 CPU cores, 4 workers | the core count, and hardware owned | permission for Macs the reader owns |
| Anka Build Cloud (self-hosted) | a 30-day trial licence | a licensing server over the internet | the paid twin of Tart |

**Xcode Cloud carries the cheapest macOS hour in this class and it is not the free one.**
The membership is USD 99 a year, which is USD 8.25 a month, and it includes 25 compute
hours, so the hour costs USD 0.33. The add-on hours cost more: USD 49.99 for 100 is
USD 0.50 an hour, and the largest block, USD 3,999.99 for 10,000, is USD 0.40
(`developer.apple.com/xcode-cloud/`, read 2026-10-22). ⭐ **The membership hour is cheaper
than every overage hour**, so a reader who needs more than 25 hours should compare a second
membership against the add-on ladder before buying one.

**Anka Build Cloud** is the same idea sold: a licence key activated against Veertu's
licensing server, a 30-day trial, and a yearly subscription priced per host and model
rather than per core (`docs.veertu.com/anka/licensing/`, read 2026-10-22). The record is
`paid-only` and its `free_tier_kind` is `trial`, which is a trial in the licence and not
capacity.

## The rental, priced by the hour and by the month

Nine of the 12 `paid-only` macOS records rent a machine by the hour or the month, and none
has a free tier. The other three are a licence (Anka), a host whose price table did not
render (Limrun), and a per-minute runner (WarpBuild). Eight of the nine publish an entry
price, and the spread across those eight is 26 times for substantially similar hardware.
The deciding variable is the billing unit rather than the chip.

| Provider | Entry price | Shape | Minimum billed | What binds |
| --- | --- | --- | --- | --- |
| HostMyApple | USD 24.99 a month | 3 GB, 60 GB SSD | 30 days | the RAM |
| Green Mini | EUR 59 a month | dedicated Apple hardware | not stated | EUR 85 for M4 and M6 |
| MacinCloud | USD 59 a month | 4-core Intel, 8 GB, 120 GB | not stated | no trial on dedicated plans |
| Scaleway Apple silicon | EUR 75 a month, EUR 0.11/h for an M1 | 8 vCPU M1 | not stated | a private network is EUR 9.99 extra |
| OakHost | EUR 120 a month | dedicated Mac mini | not stated | the device is assigned after checkout |
| MacStadium | monthly or annual, no entry price | Apple Silicon | 30 days | nothing published |
| Flow Swiss Mac | CHF 0.27 an hour or CHF 199 a month | Apple Silicon | 24 hours | billed while stopped |
| RentaMac | monthly, 24/7 access | Apple Silicon | not stated | payment starts access |
| use.computer | USD 0.90 an hour | M4 Mac mini | 24 hours | the hour rate |

**The hourly and monthly rates disagree, and the disagreement is the finding.** Flow Swiss
charges CHF 199 a month and CHF 0.27 an hour, so 730 hours at the hourly rate is
CHF 197.10. The hourly rate is CHF 1.90 cheaper and no month exists in which the plan wins.
Scaleway is the other way. 730 hours at EUR 0.11 is EUR 80.30 against EUR 75 a month, so
the plan wins by EUR 5.30 for a machine that stays up. The break-even is 682 hours, which is
93 per cent of a month.

⛔ **Flow Swiss's 24-hour minimum and billing while stopped is the trap in this class.** A
stopped Mac is not a free Mac and the cheapest possible booking is CHF 6.48. Apple's licence
is why the provider does it (`doc.flow.swiss`, read 2026-10-22).

⚠ **The hourly lane is 26 times the monthly lane.** use.computer at USD 0.90 an hour is
USD 657 for a month at 24/7 against HostMyApple's USD 24.99 for a month. The two are not the
same machine and the cheaper one is the weaker one. This is a comparison of the market's
spread and not a recommendation. A workload that runs ten hours a day costs less by the
hour, and one that must answer at 03:00 costs less by the month.

⚠ **MacinCloud states that its dedicated plans carry no trial.** That is the reverse of the
usual arrangement and worth quoting because a reader assumes otherwise
(`macincloud.com/pages/dedicated.html`, read 2026-10-22). The record covers the dedicated
page and says so.

**limrun** is recorded as `paid-only` at the `reported` rung, with no price and no shape.
The site states that pricing is split between idle and active and the extractor did not
render the table (`lim.run`, read 2026-10-22). A dash in every money column is the honest
reading, and one browser session would fill it.

## Windows, where the licence is a surcharge

Four Windows records carry a `qualifies*` verdict and no two of them qualify the same way.
Two are a month clock on the account: Azure at 12 months and WorkSpaces at 3. Two are a
one-time credit: Daytona at USD 200 and GCE at USD 300. Cua's 20 remote hours were recorded as
a monthly allowance until 2026-10-26, when the live page stated that Cua rents no machine;
the record is `dead`. The rest are paid, and the paid ones differ only in
how the licence is presented.

| Provider | Free allowance | What decides it | Identity | Verdict |
| --- | --- | --- | --- | --- |
| Azure Virtual Machines | 750 h each of three burstable shapes, 12 months | the 12-month clock | email | qualifies-with-caveat |
| Daytona Windows | USD 200 of compute, no card | USD 0.0858 a vCPU-hour surcharge | email | qualifies-with-caveat |
| GCE Windows | USD 300 one-time credit | the credit | email | qualifies-with-caveat |
| AWS WorkSpaces | 5 Performance AutoStop **Ubuntu** desktops, 100 h, 3 months | a Paid account plan at signup | card | qualifies-with-caveat |
| Windows 365 | a time-limited trial | a monthly subscription | email | trial-only |
| AWS EC2 Windows | USD 100 credit | the 6-month account clock | email | trial-only |
| Windows 365 for Agents | none | USD 0.40 an hour per Cloud PC | email | paid-only |
| Vultr Windows | none | a licence added to the plan | email | paid-only |
| Microsoft Dev Box | none | closed to new customers | email | paid-only |
| Minicor | none | a platform sale, no price published | email | paid-only |
| AutoComputer | none | `unverified`: no route reached the page | email | paid-only |
| Cyberdesk (self-hosted) | none | an SDK, no plan published | email | paid-only |
| Cua (self-hosted) | none; the page rents no machine | 20 relay hours on a computer the reader owns | email | dead |

⭐ **Azure's 750 hours is one always-on machine, and the arithmetic is why.** A month is 730
hours, so 750 covers a VM that never stops with 20 hours spare, and three burstable
families at that figure is three machines rather than one
(`azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/`, read 2026-10-22).
⚠ A Stopped VM still bills its allocated cores and only a Deallocated VM stops the charge,
which is the difference between a free month and a bill.

**Daytona Windows prices the licence in one number, and it doubles the box.** A Windows
sandbox bills USD 0.0858 a vCPU-hour on top of USD 0.0504 of compute, USD 0.0162 a GiB-hour
of memory and USD 0.000108 a GiB-hour of storage after the first 5 GiB (`daytona.io/pricing`,
read 2026-10-22). At the 2 vCPU / 4 GiB shape this topic prices, a month at 24/7 is
USD 73.58 of compute and USD 47.30 of memory. That is USD 120.89, and it matches the Linux
figure the topic uses elsewhere. The licence adds USD 125.27 and the box becomes
USD 246.16. ⛔ **The surcharge is 1.7 times the compute rate and 50.9 per cent of the
Windows bill.** That is what an operating system costs when a provider resells it by the
hour.

**GCE Windows sells the licence by the vCPU band and only the licence.** Google Compute
Engine's Windows Server premium image is USD 0.06 an hour for 4 or fewer vCPUs and USD 0.13
above that (`cloud.google.com/compute/disks-image-pricing`, read 2026-10-22). 730 hours at
USD 0.06 is USD 43.80 for the licence alone, which is 6.75 times Hetzner Cloud's entire
USD 6.49 Linux box. ⚠ The USD 300 credit buys 5,000 hours at that rate. That is 208 days of
a 24/7 licence at 4 vCPUs or fewer and nothing towards the machine. The free e2-micro
allowance does not carry a Windows image, so GCE has no free Windows row at all.

**Cua Fleet's 20 remote hours a month is 40 minutes a day.** The record defines a remote
hour as an hour with at least one live session through the relay, and the same use from the
machine itself is free (`cua.ai/pricing`, read 2026-10-22). 20 hours is 2.7 per cent of a
month. USD 25 a seat buys 200 hours and 5 sessions.

**Windows 365 and Windows 365 for Agents are two products.** The Cloud PC is a monthly
subscription from 2 vCPU, 8 GB and 128 GB with a separate trial
(`microsoft.com/en-us/windows-365/business/compare-plans-pricing`, read 2026-10-22). The
Agents product is USD 0.40 an hour per Cloud PC plus USD 5 a month per Cloud PC to keep it
instantly available (`learn.microsoft.com`, read 2026-10-22). A month at 24/7 on the Agents
product is USD 297. ⭐ **The USD 5 is the price of not being reaped**, and it is the only
row in this class that sells availability as a line item.

**Vultr Windows adds a licence to the plan and publishes no free compute tier.** The support
article states that Windows licences are not in the base monthly price and need an
additional fee based on the selected plan (`docs.vultr.com`, read 2026-10-22). The record
takes the same verdict as the Linux `vultr` record after the pricing page showed no free
compute tier. The minimum billed unit is one hour, which is the coarsest granularity in the
class after the Mac hosts.

**Microsoft Dev Box** is closed to new customers and retiring 2028-09-18. It is recorded as
`paid-only` with that sentence rather than `dead`, because a product that is winding down is
not a product that has gone.

⚠ **Cyberdesk and Minicor are not host prices at all.** Cyberdesk sells an SDK for driving
portals and Minicor sells a transportation-management platform. Neither publishes a plan, a
price or free capacity (`cyberdesk.io` and `minicor.com`, read 2026-10-22). They sit in the
class because a catalogue filed them there, and a reader comparing their money columns is
comparing two dashes.

## WorkSpaces is in the Windows table and it is not a Windows row

⚠ **AWS WorkSpaces appears in the table above for one reason: it is the service a reader
searches for by the Windows name.** The free allowance does not name Windows. It names 5
Performance AutoStop **Ubuntu** desktops with 100 combined hours a month, 80 GB of root and
100 GB of user volume, free for up to three months
(`aws.amazon.com/workspaces/desktop-as-a-service/pricing/`, read 2026-10-22). The record's
own provider name carries "Windows" and its free allowance carries Ubuntu, and both are
quoted in the same record.

So the row is a Linux desktop on a Windows-hosted service. It gives this class no Windows
machine, and a reader who counts it as one has counted a Linux row. It is kept because the
service name is what a search lands on, and ⛔ **a Paid account plan is required at signup**,
which means an account on the free plan cannot open the console to provision one at all.
WorkSpaces Pools closed to new customers on 2026-07-31. The 100 combined hours is 100 of the
730 hours in a month, which is 13.7 per cent.

## The minimum billing increment decides the floor

The class has a mechanism that no price column shows: what a provider charges for the
smallest possible booking. It runs from one second to thirty days, and it decides whether a
short job is affordable far more than the hourly rate does. **Fourteen of the 37 records
carry a numeric minimum in `extras.granularity`**, and the other 23 state none, so this
table covers the 14 and a dash would be wrong for the rest.

| Minimum billed | Providers | What it means for a short job |
| --- | --- | --- |
| 1 s | CircleCI | a 90-second job bills 90 seconds |
| 60 s | Bitrise, Blacksmith, Codemagic, Expo, WarpBuild, AWS EC2 Windows, GCE Windows | a job rounds up to one minute |
| 1 h | Vultr Windows | a 5-minute boot bills an hour |
| 24 h | Flow Swiss Mac, use.computer, AWS EC2 Mac | the cheapest booking is a day |
| 30 days | HostMyApple, MacStadium | the cheapest booking is a month |

⭐ **Three Mac hosts force a full day and two force a full month**, which is Apple's licence
showing up as a rounding rule. A reader who prices a 2-hour Mac build from an hourly rate
has priced a product that does not exist at that duration.

## What neither class gives

⛔ **No free macOS or Windows machine that a reader can log into and keep.** The macOS free
lane is build minutes and a licence. The Windows free lane is a 12-month clock on Azure, a
3-month clock on WorkSpaces and a 6-month account on AWS, all three of which are trials.
Cua's 20 remote hours are not a Windows machine: they are relay hours on a computer the
customer already owns. The paid Windows VPS market is separate and is priced in
[`windows-vps.md`](windows-vps.md); its cheapest usable row is USD 8.11 a month on
Layer7's annual cycle, or USD 10.14 on its monthly cycle.

**No usable macOS answer without a signed app.** A Mac that runs a build and cannot sign an
app does nothing a build needs, and the signing identity is Apple Developer Program
membership at USD 99 a year. That is the same membership Xcode Cloud's 25 hours sit behind,
and the build numbers are [`ci-cd-runners`](../../ci-cd-runners/README.md)'s.

**No egress term on 31 of the 37.** Six records state anything at all and 31 are silent.
Flow Swiss includes 20 TB a month and Codemagic includes egress. AWS EC2 Windows carries
100 GB a month across all AWS services. MacStadium, HostMyApple and Scaleway's private
network say "unlimited" without a rate. ⚠ **"Unlimited" is a claim about a missing limit,
not a capacity figure.** A silent egress term on a Mac that streams a build artefact is the
same trap as everywhere else in this topic.

## Contradictions in the records

**`compute/circleci.json` says the free tier has no credit amount, and
`ci-cd-runners/circleci-free.json` records 30,000 credits.** Both were read on 2026-10-22.
The compute record cites `circleci.com/pricing/price-list/`, which prices machine time in
credits and states no plan, so the placeholder is honest about the page it read and wrong
about the provider. The CI topic read `circleci.com/pricing/` and got the number. ⛔ **The
CI record is right and this class has been carrying a placeholder that one other page
already answered**, which is the cheapest kind of gap to close.

**"Cirrus" is two products and two records, and neither is the other.** This class carries
`cirrus-runners` (Cirrus Runners, `cirrus-runners.app/pricing/`), which sells dedicated
physical cores by subscription. The CI topic carries `cirrus-ci` (Cirrus CI,
`cirrus-ci.com/`), which gives 50 compute credits a month that its FAQ equates to 10,000
Linux CPU-minutes or 500 macOS minutes. ⚠ **A reader who searches the brand lands on
whichever record is nearer and gets the wrong free tier**, and the two are not tiers of one
service.

**`cirrus-runners` disagrees with itself inside one record.** It carries
`qualifies-with-caveat` and `free_tier_kind: none`, and its own pricing page publishes no
free tier. That is the vocabulary defect `gaps.md` names. This document leaves the
verdict as the record has it and states the conflict rather than resolving it silently,
because choosing the kinder reading is how a paid product gets listed as free.

**Three of the ten CI rows are in this class on a category and not on a fact.** Buildkite's
free pool is Linux vCPU-minutes. Codemagic's free tier is metered on the app's
monthly active users, not on build time. Expo's page states that EAS has a free tier and
publishes no count for it. None of the three is a macOS allowance, and the record's
`category: macOS host` is the only thing that puts them here.

## What did not work

- **A free dedicated Mac**: none exists. MacinCloud's dedicated page states no trial.
- **AWS EC2 Mac as a cheap Mac**: a Mac instance bills on the same on-demand model as any
  EC2 host, with a 24-hour minimum and a 6-month account clock.
- **A macOS build without a licence**: Tart's free 100 cores need hardware the reader does
  not own, so the free core count is a permission and not capacity.
- **Windows 365 as a server**: it is a Cloud PC subscription and the trial is separate.
- **Dev Box**: closed to new customers.
- **"Unlimited" bandwidth as a capacity figure**: three rows claim it and none states a rate.
- **AutoComputer**: `unverified`, because no route in the challenge protocol reached the page.
- **Buildkite's free pool as macOS**: the record states Linux vCPU-minutes.

## What this cannot establish

⛔ **Nothing here was measured and nothing was booted.** Not one of the 37 records was
launched, so the licence surcharge, the minimum billing unit and the trial clock are page
reads. `gaps.md` records that the topic's four `measured` records measure a transport, a
listing or a price, never a quota.

**Whether a rented Mac is usable for a build is unestablished.** The records price a machine
and none reports a boot, so the difference between a Mac that starts in a second and one
that starts in an hour is unmeasured for all nine rentals.

**The Windows free lane beyond Azure is a single row.** AWS WorkSpaces is Ubuntu and GCE has
no free Windows image, so the class rests on one 12-month allowance. Windows 365's trial is
stated without a length, and the record cannot say how many days it is.

**What a Windows licence costs on a rented Mac.** No record in this class states one, so
the surcharge is computed from Daytona and GCE and observed nowhere.
