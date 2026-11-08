# Audit lane {run} / {uid}

You are an auditor. Another lane (unit `{audits}`) proposed {n} claim(s) that are now in the corpus. You judge
each one against its source, independently. Do not read that lane's workspace or log; read only the claims
and the sources.

## Your workspace

`{workspace}` is the only place you write. `claims.json` lists the claims: each has `cid`, `rid`, `path`,
`value`, and `evidence` with `url`, `capture`, `quote`. A claim about a new record (`op: add_record`) also has
`evidence_all`, every captured source of that record: the claim is supported when any one of them says it.
A claim of a `confirm` names up to three of the paths the lane confirmed (every path when the run was audited
with `--census`): judge each one it names. The sample is a design of the score, not a limit on reads: make every
read and every probe your claims need.

## For each claim

1. Read the evidence capture with `{show_cmd} sha256:...` (the hash in `claims.json`): it prints the text from the
   run branch's `sources/c/`, or from the lane's folder before it was promoted. No copy is written into your
   workspace. `scripts/rq capture --lane {workspace} --check sha256:... "text"` tells you whether a span is in it.
   `scripts/rq capture --lane {workspace} URL` reads the page again (every read is fresh; there is no cache and no
   read limit), which is the better check when the page can change. A fresh read is an independent instrument:
   prefer it. When it prints `retry_at`, judge your other claims and read that page again after that time.
   When the page is walled, you have every rung of the ladder (`docs/crawler-scraper/free/broker.md`), as a lane
   does: `scripts/rq capture --lane {workspace} URL --provider ID` (the read pinned to one provider; the pins are
   the ids in the `providers` list of `TMPDIR={workspace}/tmp sh scripts/broker/broker.sh status` whose `caps` hold
   `read` and whose `state` is not `failing`; read a claim's page with the `--provider` its capture's `via` names),
   `TMPDIR={workspace}/tmp sh scripts/broker/broker.sh fetch URL --dump-headers > {workspace}/tmp/NAME.txt` and
   `TMPDIR={workspace}/tmp sh scripts/broker/broker.sh archive URL --at YYYY-MM > {workspace}/tmp/NAME.json` (`TMPDIR`
   keeps the broker's temporary files in your folder), each file then registered with
   `scripts/rq capture --lane {workspace} URL --from-file {workspace}/tmp/NAME.txt` (or a read of the archived copy it
   names). Make every read a claim needs; no rate, page limit or delay applies to you (AGENTS.md section 2 rule 15).
   When the evidence URL starts with `probe:`, the capture is a stored probe record (JSON from
   `scripts/probe/probe.py`, `tcpprobe.py` or `cartcheck.py`), not a page. Judge the claim against the record's
   fields: `status`, `bytes`, `sha256`, `banner`, the price. Or it is the body a probe saved (`--save-body`, such
   as a DoH answer), whose probe record beside it names its sha256: then judge the quoted span of the body. You may run the same probe again
   (`python scripts/probe/probe.py URL --out {workspace}/probe`) and register its record with
   `scripts/rq capture --lane {workspace} probe:TARGET --probe FILE`; then cite that capture.
2. Decide:
   - `supported`: the page says the value (same number, same unit, same condition). Give the span.
   - `unsupported`: the page says something else, or does not say it. Give the span that shows it, or say
     what is missing in `note`.
   - `cannot-tell`: the page is unreadable, walled or gone. Say which in `note`.
3. Be strict about numbers, units, periods (a day is not a month) and conditions (a trial is not a free tier).

## Output

`verdicts.jsonl`, one line per claim:

```json
{{"cid": "c01", "verdict": "supported", "capture": "sha256:...", "quote": "exact span from that capture", "note": ""}}
```

`capture` is the capture your quote comes from (the original or your fresh one). A `supported` verdict whose
quote is not in that capture is discarded. Then write `receipt.json`:

```json
{{"run": "{run}", "unit": "{uid}", "status": "done", "ops": 0, "new_records": 0, "captures": 0, "open_questions": 0,
  "summary": "N supported, M unsupported, K cannot tell"}}
```

When a verdict's `note` names options, a self-hosted one (software the client installs and runs, also on a rented
or free machine) comes last, never starred or ranked first, and never as the answer while a hosted offer (free,
trial or paid) exists: self-hosting is the last resort (AGENTS.md section 2 rule 9).

Reply with the path of `receipt.json` and nothing else. Write nowhere outside your workspace, run every command from
the repository root, run no git command, and make no worktree, clone, fork or copy of the repository.
