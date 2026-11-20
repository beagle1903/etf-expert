# User ticker pilot — 20 November 2026

The approved [25-ticker request](../data/issue-17-tickers.json) was pinned
before screening. The trial adds these listings to the unchanged, reviewed
40-listing baseline. The U.S. directory was collected at 10:51 UTC on
20 November; all 25 tickers matched exactly one ETF row. It establishes
venue candidates, not issuer identity or economic exposure.

| Offline replay | Requested | Comparison-ready | Eligible | Selected |
|---|---:|---:|---:|---:|
| Baseline | 40 | 40 | 3 | 3 |
| Baseline + trial | 65 | 57 | 18 | 3 |

Both runs use the same US, USD, 100% equity profile, three positions and
25 bp cap on the specifically named `expense_ratio` metric. The comparison
date was advanced from 18 to 20 November for both runs to include the new
evidence; all other profile fields remain the same. The baseline selects
DMXF, ACWV and CRBN; the expanded run selects IVV, VB and VEA. The rule
orders by the named fee, then ticker and venue, not by a user's economic
exposure preference. The three new selections all report 3 bp; this is an
illustration, not a recommendation.

## Trial decisions

All 25 had an issuer-evidence review, though eight were not
comparison-ready. `Comparison-ready` accepts any usable named fee; the
profile separately requires `expense_ratio`.

| Ticker | Decision or evidence gap |
|---|---|
| IVV, VB, VEA | Selected by fee and ticker ordering. |
| VOO, VTI, VTV, VUG | Eligible at 3 bp, outside the three positions after the ticker tie-break. |
| VIG | Eligible at 4 bp; position limit reached. |
| VXUS | Eligible at 5 bp; position limit reached. |
| IJR, VWO | Eligible at 6 bp; position limit reached. |
| IXUS | Eligible at 7 bp; position limit reached. |
| VGT | Eligible at 9 bp; position limit reached. |
| VNQ | Eligible at 13 bp; position limit reached. |
| IWM | Eligible at 19 bp; position limit reached. |
| NOBL | Fails the 25 bp cap: dated issuer expense ratio is 35 bp. |
| SPY | Comparison-ready, but its dated issuer factsheet reports gross and net expense ratios; the requested `expense_ratio` is missing. |
| QQQ, QQQM | Total expense ratio reported, but its field-specific date and the requested `expense_ratio` metric were not established. |
| SCHD, SCHG | Direct issuer pages returned HTTP 403. Indexed issuer excerpts provide identities, benchmarks and total expense ratios, but no established fee observation date or requested metric. |
| XLF, XLK, XLV | Issuer pages provide gross expense ratios, but a field-specific date and the requested metric were not established. |
| IUSB | Issuer indexed evidence identifies fixed income, so the equity-only profile excludes it. Its direct product page returned HTTP 403; fee date, duration and credit evidence remain unresolved. |

The eight unresolved profile results include SPY, which is comparison-ready
on a different metric. IUSB is a measured asset-class exclusion even though
its bond evidence is incomplete. No fee metric is silently converted to
another. Yahoo currency and exchange observations are undated; collection
timestamps do not supply observation dates. Issuer factsheets used for the
passing new equities are dated June or September 2026. The original 40
issuer records were collected on 18 November; VTI, VEA, VWO, IWM and SPY
reuse issuer documents collected on 17 November. New issuer downloads and
Yahoo checks were made on 20 November. The local attempt log retains 403s
even where a separate factsheet or an indexed excerpt was available.

## Interpretation and next work

The larger pool produces a meaningful **numerical** choice: 18 eligible
listings for three positions instead of exactly three. It does not establish
that the selected mix best represents the user's desired exposures. In
particular, issuer labels such as `S&P 500 Index` and `S&P 500 Index (USD)`
are not normalized as equivalent; exact label matching is not a holdings
overlap analysis. Fee ordering and ticker tie-breaks can overwhelm an
exposure preference. Fund identifiers establish share-class identity, not
economic independence.

Recommend an exposure-preferences and evidence-backed benchmark identity
ticket next, before adding more allocation rules. Fee comparability also
deserves follow-up: explicitly decide which issuer metrics can be compared
and with what evidence, rather than relabeling them. Review tooling is worth
improving after the desired evidence and comparison policy is specified.

Manual source selection, checking and preparation took roughly several
minutes during the pilot; individual review time was not instrumented, so
this is not a per-fund productivity measurement. The work reused the saved
40-fund review, five older issuer factsheets and the earlier Nasdaq file;
it is not a benchmark for a fresh end-to-end collection.

## Local evidence and replay

The requested list is tracked. Raw source files, collection attempts,
individual Yahoo observations, `cohort.json`, `reviewed.json`, the assembled
snapshots and outputs remain locally in ignored
`data/runs/issue17-2026-11-20/`. The baseline snapshot remains in
`data/runs/acceptance-2026-11-20/snapshot.json`. Historical PDF sources
referenced by the review remain in `data/runs/issuers-20261117T174001860718Z/`.
These ignored files are required to reproduce this particular historical
pilot; a fresh Git checkout alone does not contain the research.

```powershell
$run = "data/runs/issue17-2026-11-20"
uv run --offline --no-sync python scripts/discover_tickers.py data/issue-17-tickers.json "$run/nasdaq.raw" "$run/venue-source.json" --output "$run/discovered-replay.json"
uv run --offline --no-sync python scripts/prepare_snapshot.py "$run/cohort.json" "$run/reviewed.json" --output "$run/trial-replay.json"
uv run --offline --no-sync python scripts/build_portfolio.py data/runs/acceptance-2026-11-20/snapshot.json "$run/profile.json" --output "$run/baseline-replay.json"
uv run --offline --no-sync python scripts/build_portfolio.py "$run/expanded-snapshot.json" "$run/profile.json" --output "$run/expanded-replay.json"
uv run --offline --no-sync python scripts/screen_etfs.py "$run/expanded-snapshot.json" --as-of 2026-11-20 --output "$run/comparison-replay.md"
```

The combined snapshot is retained directly, with every baseline and trial
record and the source attempts. Replay does not access the network.
