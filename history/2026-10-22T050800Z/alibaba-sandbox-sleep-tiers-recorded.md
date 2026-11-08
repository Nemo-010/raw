# Alibaba's sandbox prices three sleep states, and that is the axis the topic was missing

- **When:** 2026-10-22T05:08:00Z
- **Status:** observed
- **Supersedes:** `dossier/compute/alibaba-agentrun.json` (free tier "the source card records a free tier without a credit amount", no lifecycle field)
- **Superseded by:** that record, rewritten on 2026-10-22 with the three states priced separately
- **Evidence:** `https://help.aliyun.com/zh/agent-sandbox/product-overview/billing-overview` read 2026-10-22
- **Confidence:** documented

## What we believed

That the Agent Sandbox product had a free tier of an unknown size, and that the
question "what happens to my state when the machine stops" was unanswerable from
the corpus. `docs/expansion/compute.md` lists state durability on stop versus
delete as an axis **"almost nothing"** establishes.

## What we found

The billing page answers it, in a table of four lifecycle states with the meter
for each:

| state | what happens | what bills |
| --- | --- | --- |
| 活跃 (active) | running and answering | vCPU, memory, disk |
| 浅休眠 (shallow sleep) | automatic when idle; memory snapshot kept | memory, disk |
| 深休眠 (deep sleep) | the whole instance, memory included, is frozen to persistent storage | disk only |
| 销毁 (destroyed) | permanently terminated | nothing |

The trigger for shallow sleep is stated precisely, and it is the same test Azure
puts on Container Apps: **CPU below 0.01 core, network below 1,000 bytes a second,
or no request**. Two independent vendors converging on those thresholds suggests
the numbers come from a shared measurement convention rather than from either
vendor's taste.

The free allowance is 15 GiB of rootfs disk, and the page adds a clause no record
carried: *"深休眠期间不享受 15 GiB 免费磁盘额度"* — the 15 GiB is withdrawn while an
instance is deep-asleep or snapshot-saved. So the cheapest state is the one that
does not get the free disk.

## How we found it

One read of the billing page. It had never been opened here: the record's evidence
row named the corpus card and said in `confidence_note` that "no page was read in
this session".

## What it cost us

Nothing was wrong in the record; it simply carried no lifecycle field, so a reader
asking "can I park this machine for a week" got no answer. Three of the expansion
plan's seven axes — wall-clock, state durability, and even product class — were
answerable from one page nobody had opened.

## What a future session should do differently

⭐ **A sandbox vendor's billing page is the lifecycle document.** The feature page
says what the product does; the billing page says what it charges in each state,
which is the same question as what it preserves. Read the second one first.

⚠ **Check whether the free allowance survives the cheap state.** Here it does not:
15 GiB of free disk applies while running and while shallow-asleep, and is
withdrawn in deep sleep. A provider can give a quota and then charge for the state
where you would want to sit on it.
