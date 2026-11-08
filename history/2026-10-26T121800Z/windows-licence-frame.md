# The Windows VPS floor was priced as a licence, not as a machine

- **When:** 2026-10-26T12:18:00Z
- **Status:** corrected
- **Supersedes:** the Windows VPS floor of InterServer at USD 40.00 a month, and the exclusion of a trial or bring-your-own licence
- **Superseded by:** `docs/compute/paid/windows-vps.md` and six new Windows records, with the USD 8.11 floor
- **Evidence:** the vendor pages quoted in this entry, read 2026-10-26
- **Confidence:** documented

**What was claimed.** `docs/compute/paid/windows-vps.md`, written earlier on
2026-10-26, ranked the cheapest usable Windows machine at 16 GiB, 4 vCPU and
50 GB at **InterServer's USD 40.00 a month**, with Contabo at USD 47.01 as the
cheapest row whose licence is printed and Time4VPS at USD 52.88 at renewal. It
also excluded Cloudzy at USD 49.98 and netcup at EUR 26.92 because their Windows
licence is a trial or the buyer's own. The document said that a trial, a
bring-your-own licence and a 180-day evaluation "do not count".

**What took it away.** The exclusion is the error. The question asks for a machine
that runs Windows at 16 GiB, 4 vCPU and 50 GB. It does not ask who supplies the
licence. The live pages read on 2026-10-26 show that the machine and the licence
are separate purchases at most hosts:

> Aydin VPS x16 ... 6 Core CPU ... 16 GB Ram ... 120 GB SSD ... Windows / Linux
> ... Monthly $10.99/mo ... Annually $8.79/mo Save 20%
>
> `rabisu.com/panel/store/vps/aydin-vps-x16`, read 2026-10-26

> Base Price: EUR 4.90 ... CPU Cores: 2 ... RAM: 8 GB ... Total: EUR 4.90
> ... Windows 2019 Std EN Evaluation ... Windows 2022 Std EN Evaluation
>
> `account.layer7.net/shop/amd-epyc-cloud-server-vps-germany-frankfurt-main`,
> read 2026-10-26

The Layer7 configurator prints EUR 1.92 for 4 cores and EUR 2.24 for 16 GB, so
the same machine is EUR 9.06 a month with a Windows image on the OS list. Rabisu
prints USD 8.79 a month on the annual term and USD 10.99 on the monthly term.
Both are below USD 40.00 by a factor of four or more.

**What is true now.** The cheapest verified machine is Layer7 at EUR 9.06 a
month, which is USD 10.14, or EUR 86.97 a year, which is USD 8.11 a month, for
4 cores, 16 GiB and 80 GB, with a Windows Server 2022 evaluation image. Rabisu is
the cheapest row with a licence claim, at USD 10.99 a month or USD 8.79 on the
annual term, for 6 cores, 16 GiB and 120 GB. NetVolo is USD 13.98 on a three-year
prepayment, HOSTKEY is USD 15.67 plus an unpublished licence, Linveo is
USD 16.00, and netcup is USD 25.32 net.

The USD 7 Windows VPS that prompted the correction is real, and it is a smaller
machine. Hostmayo sells 1 GiB at USD 7.00, SteadyVPS sells 1 vCPU and 2 GiB at
USD 7.00, and Rabisu's Aydin VPS X12 is 4 cores, 12 GiB and 90 GB at USD 7.19 on
the annual term. The X12 misses the RAM floor by 4 GiB. The X16 is the next rung
at USD 8.79, which is USD 1.60 more a month.

**Where the correction lives.** `docs/compute/paid/windows-vps.md` is rewritten:
the first table ranks machines with the licence path in a column, a second table
keeps the licence-supplied rows, and a third table prices the USD 7 entry plans
and names the minimum each one fails. Six new records carry the new rows:
`rabisu-windows`, `layer7-windows`, `netvolo-windows`, `hostkey-windows`,
`linveo-windows` and `netcup-windows`. `dossier/compute/cloudzy-windows.json` is
unchanged and stays a near miss. `BRIEF.md`, `docs/compute/README.md`,
`docs/compute/paid/README.md` and `docs/compute/paid/os-hosts.md` now state the
USD 8.11 floor.

⚠ **What would reopen it.** A 16 GiB Windows-capable machine under USD 8.11 a
month, or a Rabisu renewal that charges for the licence that the FAQ says is
included. The first would lower the floor. The second would remove the leading
row and leave Layer7 at USD 10.14 as the answer.
