# Cua rents no machine

- **When:** 2026-10-26T11:33:32Z
- **Status:** corrected
- **Supersedes:** the `qualifies-with-caveat` verdict of `compute/cua-windows` as a Windows host with 2 live sessions and 20 remote hours a month
- **Superseded by:** `dossier/compute/cua-windows.json`, rewritten on 2026-10-26
- **Evidence:** `cua.ai/pricing`, read 2026-10-26, quoted in this entry and in the record
- **Confidence:** documented

**What was claimed.** `dossier/compute/cua-windows.json` recorded "Cua Fleet
(Windows Server)" as a Windows host with a free allowance of "up to 2 live
sessions and 20 remote hours a month". The verdict was `qualifies-with-caveat`,
and `docs/compute/paid/os-hosts.md` counted it as one of five qualifying Windows
records and as the only Windows allowance that renews with no stated end.

**What took it away.** The live pricing page, read on 2026-10-26:

> Cua Spaces turns the Macs, Linux boxes and cloud VMs your team already has
> into shared desktops. ... You bring the computers; Cua doesn't rent them.
>
> `cua.ai/pricing`, read 2026-10-26

The same page defines a remote hour as "time spent using your computers from
somewhere else. Using a computer from itself is free." The earlier record quoted
that sentence and read it as a rented host. It says the opposite: the computer
is the customer's.

**What is true now.** Cua sells relay seats onto hardware the customer already
owns. The 20 free remote hours are relay hours, not machine hours. No Windows
host is rented, so the record's `qualifies-with-caveat` verdict is withdrawn and
the record is `dead`. The free tier is worth zero as compute without owned
hardware. The record's `free_tier` now states this, and its `notes` names the
misreading.

**Where the correction lives.** `dossier/compute/cua-windows.json` carries the
new verdict, the live quote and this entry in `history`.
`docs/compute/paid/os-hosts.md` now counts four qualifying Windows records
instead of five and marks the Cua row `dead`. `docs/compute/paid/windows-vps.md`
states the same correction in its remote-desktop section.

⚠ **What would reopen it.** A Cua product page that sells a Windows Server
machine with a licence and a persistent disk. The current page states that Cua
does not rent machines, so a reopen needs a new product, not a new reading.
