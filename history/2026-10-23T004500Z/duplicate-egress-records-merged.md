# Four providers had two records each

- **When:** 2026-10-23T00:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/egress/6project.json`, `netassist-tb.json`, `tunnelbroker-se.json` and `hoppy-network.json`, which duplicated `6project-org`, `netassist-tunnelbroker`, `karabro-tunnelbroker-se` and `hoppy`
- **Superseded by:** the four surviving records, each carrying the other's evidence merged and a `notes` sentence naming where it came from
- **Evidence:** the four pairs were written by different lanes from the same vendor; each pair's `url` and `free_tier.stated` named the same product, and the merge kept the higher-confidence record and the union of both evidence arrays
- **Confidence:** documented

## What happened

Two lanes read the same provider and wrote a record each. The rule is one
provider, one file, so the duplicates were merged rather than deleted: the
surviving record keeps both evidence arrays, both `limits[]` sets and both
`extras`, and its `notes` names the record it absorbed.

## What was kept and what went

- `6project` into `6project-org`, which keeps the higher rung and the routed
  prefix detail.
- `netassist-tb` into `netassist-tunnelbroker`, which is the vendor's own name.
- `tunnelbroker-se` into `karabro-tunnelbroker-se`, because the broker rebranded.
- `hoppy-network` into `hoppy`, which is the provider's name.

No claim was dropped. The four that were removed existed only as duplicates, and
every fact in them is in the surviving record.
