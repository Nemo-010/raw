# The Windows floor survived a sixteen-lane sweep, and three claims did not

- **When:** 2026-10-26T13:30:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/paid/windows-vps.md` and the Windows answer row in `BRIEF.md` section 3.8, as written on 2026-10-26T12:18:00Z
- **Superseded by:** `docs/compute/paid/windows-vps.md`
- **Evidence:** sixteen lane files and four merges in `.tmp/win-swarm/`, `lane-01.md` to `lane-16.md` and `merge-A.md` to `merge-D.md`; the top ten re-read live on 2026-10-26 between 15:06Z and 15:24Z in `.tmp/win-swarm/verify-top.md`, with the vendor captures named there
- **Confidence:** documented

**What was claimed.** The correction earlier on 2026-10-26 ranked six vendors. It
put Layer7 first at EUR 9.06 a month or EUR 86.97 a year, Rabisu second at
USD 10.99 a month or USD 8.79 annual with "a vendor FAQ that claims a genuine
licence", then NetVolo, HOSTKEY, Linveo and netcup. It also recorded that the
breadth gap was open: the first pass had priced provider-supplied licences only,
the corrected pass still covered 11 vendors, and a sixteen-lane sweep was queued.

**What the sweep did.** Sixteen lanes ran on 2026-10-26, one per segment, and each
wrote its own file before any corpus edit. The segments were the offer archives,
US budget hosts, Russia and the CIS, Europe, the Windows specialists, the RDP
resellers, Turkey and MENA, Asia-Pacific, rented dedicated servers, the
hyperscalers, hosted desktops, WHMCS and wholesale resellers, the price
aggregators, the install and policy checks, the licence channel, and a cart audit.
The lanes read about 200 provider names. The Windows-specialist merge alone ranks
58 rows that clear 16 GiB, 4 vCPU and 50 GB. The first two passes had covered 11
vendors and then 6.

**What held.** The floor did not move. Layer7 is still the cheapest machine at
EUR 9.06 a month, which is USD 10.14, for 4 cores, 16 GiB and 80 GB with a
Windows Server 2019 or 2022 evaluation image on the OS list. The rendered
configurator closes at 4.90 + 1.92 + 2.24 = 9.06. The annual figure is 86.97, from
47.04 + 18.43 + 21.50, and it is arithmetic on three printed annual components
rather than a rendered total, so it stays `inferred`. No page prints a VAT line,
so whether 9.06 is net or gross is still unstated. The first payment on the annual
term is USD 97.48 at 1.1209 USD/EUR, the rate read on 2026-10-26; at the table's
1.1193 it is USD 97.34.

**What changed.** Three claims moved and one number was added.

1. **Rabisu's licence is unresolved.** The configurator prices Windows Server
   2012R2, 2019 and 2022 at no surcharge, and the monthly cycle is the default.
   But no licence sentence appears on the configurator, on the home page or in the
   knowledgebase: "licen", "Licen", "genuine" and "license" all return zero matches
   on 127,944, 133,582 and 94,572 bytes. The quote the earlier entry relied on did
   not reproduce. A zero surcharge is evidence of a price, not of a licence, so the
   row is now the cheapest with a Windows image and no claim about the licence.
2. **HostBrr is out of the ranking.** One merge ranked its Value 16GB third at
   USD 11.00 for 4 cores, 16 GiB and 160 GB on the strength of page prose and a
   logo tile. The order page is a registration wall that reaches a different
   product group, prints a zero subtotal, and offers no OS selector before payment.
   The page states no IPv4 either.
3. **VDSina is priced per day, not per month.** USD 4.08 is a daily rate, said
   three ways on the page and in its own plan JSON. At 30 days it is about
   USD 122.40 a month, so the row leaves any monthly ranking.
4. **The licence has a number.** Windows Server Standard is USD 509.99 one-off for
   16 core licences, which is USD 14.17 a month over 36 months, against Microsoft's
   USD 1,176 suggested MSRP for the 2025 edition. Datacenter is USD 2,499.99, or
   USD 69.44 a month. Sixteen cores is a per-server minimum, so a 4 vCPU machine
   pays the same licence as a 16 core one.

**What else the sweep settled.** Three hosts cannot install Windows at all, on the
vendor's own words: DigitalOcean, Linode/Akamai and Hostinger. OVHcloud VPS runs
Windows only if it was selected at order time. Seven rows joined the ranking and
netcup left it: Virtarix at USD 27.40, where the licence is printed as a USD 16.00
OS template inside the price and the Linux twin at USD 11.40 makes the decomposition
exact; windowsvps.host at USD 36.00 with a Datacenter licence claimed included;
ServerPacket at USD 32.19, with the vendor's own pages 2.3 times apart for the same
shape; Kimsufi KS-3 at USD 64.00 all-in, which prints the licence as its own
USD 34.00 line on a USD 30.00 box; By-Hoster at USD 19.04, which states plainly that
it neither supplies nor resells a licence; Saganetwork at USD 8.23 ex VAT and
USD 9.88 paid, the cheapest row a buyer can start monthly, with its Windows path
unverified because the cart has no OS field; and InterServer at USD 40.00, which is
no longer the floor and is now one row among these.

**What is true now.** The cheapest machine that boots Windows at 16 GiB, 4 vCPU and
50 GB is Layer7 at EUR 9.06 a month (USD 10.14) or EUR 86.97 a year (USD 8.11 a
month). The cheapest startable monthly is Saganetwork at USD 8.23 ex VAT. The
cheapest with a Windows image at no surcharge is Rabisu at USD 10.99 monthly or
USD 8.79 annual, with the licence unresolved. The cheapest with the licence printed
is Virtarix at USD 27.40. No machine was booted and no order was placed.

**Where the correction lives.** `docs/compute/paid/windows-vps.md` owns the
ranking. `BRIEF.md` sections 3.8 and 5 carry the answer and the open items, and
`docs/compute/README.md`, `docs/compute/paid/README.md` and
`docs/compute/paid/os-hosts.md` state the same floor.

**What would reopen it.** A 16 GiB machine under USD 8.11 a month on a term a buyer
can start today. A Rabisu renewal that charges for the licence would remove the
leading licence row and leave Layer7 as the answer, but it would not move the
floor. A ServerPacket order screen that prices the shape at USD 167.88 a year would
put it fifth at about USD 13.99. A Contabo Windows add-on price would put a 24 GiB
machine at the EUR 14.00 machine rate into the table, and no row up to Virtarix
offers more than 16 GiB.

**What a future session should do differently.** Two lessons. A quoted sentence is
not a page: the Rabisu licence claim had been read in an earlier lane and did not
reproduce on any of the three pages that should carry it, and the row was ranked on
it for a day. Re-read the sentence on the vendor's own page before it becomes a
ranking input. And a JSON-LD block is not a price: HOSTKEY's ruble card carries
`"priceCurrency":"EUR"` beside a RUB 3,390 figure, which is how a ruble machine can
be read as a euro one, and the EUR 14.00 the corpus records for it sits on a
storefront that answers 403.
