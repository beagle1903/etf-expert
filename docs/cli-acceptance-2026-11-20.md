# CLI acceptance — 20 November 2026

**Accepted for local research with a reviewed dataset.** A fresh checkout
discovered the broader cohort, replayed source collection and issuer review,
assembled the snapshot, screened all 40 listings, and constructed two
illustrative portfolios. The verified scope is one issuer across US and
Xetra listings. Issuer document selection and fact review still require
manual work. Recurring unattended issuer collection and permission for
recurring use remain unverified.

## What was run

The clean worktree started at merged commit `b1cb625` on Windows with
Python 3.14.0 and uv 0.9.7. Setup and offline tests used the locked environment.

```powershell
uv sync --locked --dev --python 3.14.0
uv run --offline --no-sync pytest -q
```

**Live observation.** Both venue downloads returned HTTP 200 on 20 November
at 10:51 UTC (13:51 Istanbul). Nasdaq's file was stamped 03:04 in its
source format. The Xetra file was dated 20 November. The source filters
yielded 5,811 Nasdaq rows and 3,196 Xetra rows. The ten-per-group rule
selected the same 40 listing keys as the 18 November cohort. This run
collected venue data. The dated issuer evidence used below came from
the original review.

```powershell
uv run --offline --no-sync python scripts/check_broader_coverage.py data/runs/acceptance-live-2026-11-20 --fetch nasdaq xetra --per-group 10 --timeout 25
```

**Offline evidence replay.** The worktree received copies of the original
run folders and three local profiles. The 18 November bulk check reused
all four requested cached inputs, retained nine attempts and five access
or parse errors, and preserved all 40 listings. The SEC response was
HTTP 403. Four issuer catalogue or product responses lacked usable data.
The local issuer-review replay reproduced the saved JSON byte for byte,
retaining 69 attempts, including six logged errors. The review collected
issuer evidence on 18 November between 17:55 and 18:09 UTC. The documented
per-listing sources and observation dates remain available in the
[issuer review](full-cohort-coverage-2026-11-18.md).

```powershell
$run = "data/runs/acceptance-2026-11-20"
$cohort = "data/runs/broader-2026-11-18/pilot-universe.json"
uv run --offline --no-sync python scripts/check_broader_coverage.py data/runs/broader-2026-11-18 --fetch nasdaq xetra ishares-us danimoth
uv run --offline --no-sync python data/runs/full-cohort-review.py
uv run --offline --no-sync python scripts/prepare_snapshot.py $cohort "$run/reviewed.json" --output "$run/snapshot.json"
uv run --offline --no-sync python scripts/screen_etfs.py "$run/snapshot.json" --as-of 2026-11-18 --output "$run/comparison.md"
uv run --offline --no-sync python scripts/build_portfolio.py "$run/snapshot.json" "$run/illustrative-profile.json" --output "$run/portfolio.json"
uv run --offline --no-sync python scripts/build_portfolio.py "$run/snapshot.json" "$run/illustrative-profile-alternate.json" --output "$run/portfolio-alternate.json"
uv run --offline --no-sync python scripts/build_portfolio.py "$run/snapshot.json" "$run/illustrative-profile-infeasible.json" --output "$run/portfolio-infeasible.json"
```

The historical review script and cache are local evidence from issue #3.
They are ignored by Git. The maintained handoff starts with the reviewed
JSON and pinned discovery cohort. For a fresh sample, prepare the JSON
using the [routine and record format](../README.md#local-workflow). For the
acceptance replay, `reviewed.json` was an exact copy of the 18 November
`manual-coverage.json`. Profile contents and the two changes are in the
[portfolio example](portfolio-rules.md#example-on-the-saved-40-listings).

## Results and failure cases

| Scenario | Requested | Researched | Comparison-ready | Eligible | Selected |
|---|---:|---:|---:|---:|---:|
| Base EUR profile | 40 | 40 | 40 | 11 | 5 |
| Exclude 2B7A and raise duration cap to 6 years | 40 | 40 | 40 | 11 | 5 |
| Lower duration cap to 4.29 years | 40 | 40 | 40 | 8 | 0 |
| Omit 2B7A review and insert a same-date 31IG fee conflict | 40 | 39 | 38 | 9 | 0 |

All eligible listings were considered directly. The shortlist count was
null. The base profile selected 31IG, 32XG, 2B7A, 2B7B and 2B7C. In the
alternative, 2B7D replaced the explicitly excluded 2B7A. The higher cap
admitted 33GI. At the same fee, 31IG and 32XG came first in the ticker
tie-break. Both portfolios independently reconciled to **10,000 basis
points, 100,001 initial cents and 9,999 recurring cents**. The tighter
duration profile had zero qualifying bonds and left both cash budgets
unallocated.

A separate copy of the reviewed input removed 2B7A and added a conflicting
13 bp TER to 31IG on the same date as its original 12 bp claim.
`prepare_snapshot.py` kept both requested listings in the output.
The report showed 38 comparison-ready and two unknown, with a missing
review for 2B7A and two conflicting fees for 31IG. The base profile then
had only one qualifying bond for two requested positions. The command
returned exit status 1 and saved its reason with zero allocations.

```powershell
uv run --offline --no-sync python scripts/prepare_snapshot.py $cohort "$run/reviewed-partial.json" --output "$run/snapshot-partial.json"
uv run --offline --no-sync python scripts/screen_etfs.py "$run/snapshot-partial.json" --as-of 2026-11-18 --output "$run/comparison-partial.md"
uv run --offline --no-sync python scripts/build_portfolio.py "$run/snapshot-partial.json" "$run/illustrative-profile.json" --output "$run/portfolio-partial.json"
```

Reopening the saved evidence in new processes reproduced the comparison
Markdown and base portfolio JSON byte for byte. The selected positions'
input evidence retained their listing source and collection timestamp.
The local replay made no new requests. The final offline test suite
passed 32 tests.

This validates the documented sequence of commands for the reviewed
broader cohort. The retained source failures, manual review effort,
unknown hedging and limited evidence of holdings overlap bound the
comparisons and selection. The reports are illustrative local outputs.
