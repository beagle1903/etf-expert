# ETF comparison and screening rules

The CLI reads the saved, manually reviewed cohort from issue #3. It applies
user-specified research filters as of a required date. All requested listings
appear in the report, including explicit exclusions and unresolved cases.
The examples are research queries and carry no investment eligibility decision.

- A comparable row needs a venue and ticker, a supported CUSIP or ISIN, a
  trading currency, issuer exposure evidence and a sourced annual fee
  observation. Bonds also need dated effective duration and numeric credit
  weights. The default permitted age is 180 calendar days, including day
  180. The oldest fee in the verified snapshot is 141 days old as of
  18 November 2026. Callers can set a different age. Undated, future,
  stale and conflicting evidence produces an unknown on a relevant rule.
  For each fee metric the CLI checks claims on the latest observation date
  on or before the comparison date. A future claim can coexist with a usable
  earlier observation. The date controls evidence checks within the snapshot.
- Fee caps name the metric and use annual basis points. Expense ratio, net
  or gross expense ratio, annual operating expenses and TER have separate
  caps. A listing passes the fee rule if one of the explicitly requested
  metrics is usable and meets its cap. If every requested metric can be
  evaluated and exceeds its cap, the rule fails. Any unresolved requested
  alternative makes that result unknown. Separate fee rules let a query
  express different caps without assuming different measures are equivalent.
- The duration cap applies to bonds and uses effective duration in years.
  The below-investment-grade cap uses disclosed ratings below BBB−. Cash
  and derivatives stay separate. Unrated, ambiguous categories and the
  unaccounted portion form an uncertainty range. A cap inside the range is
  unknown. A known lower bound above the cap is a failure. The full
  reported distribution is retained without rescaling. Minor rounding
  above 100% is accepted within 0.10 percentage points.
- Trading currency filters refer to the listing. They say nothing about
  portfolio currency exposure or hedging. The report displays any explicit
  hedge evidence supplied by the dataset. A hedge filter on bonds requires
  dated evidence of the hedge target or explicit unhedged status.
- Explicit market, strategy, currency and symbol exclusions are visible.
  A measured failure takes precedence over other unknowns because it is
  sufficient to rule out the listing under the query. Otherwise unknown
  evidence prevents a pass. All numeric maximums are inclusive.
- A matching, supported identifier in the same namespace can link
  multiple listings to a share class. Matching exposure labels are
  reported separately. The source set has limited holdings evidence, so
  the report makes no estimate of portfolio overlap. Each listing remains
  in the report and there is no shortlist.

## Saved input

The CLI reads the `records` array in the local issuer-reviewed
`manual-coverage.json` from issue #3. Each row has a unique market, venue
and symbol, an identifier and sources, fee claims, exposure text and bond
risk evidence when available. A partial row can use nulls for unresolved
facts. Optional `conflicts` names the affected fields, for example
`["identifier", "exposure", "duration", "credit"]`. A fee conflict can
name `fee` or the precise metric. If the source proves a hedge target,
`currency_hedge` carries `target`, `as_of` and a `source` URL. The
target may be a currency code or `unhedged`. Optional
`share_class_currency` and `fund_base_currency` appear separately when supplied.

Comparison-ready counts the rows with the baseline evidence needed to
compare. Passed, failed and unknown describe the requested filter result.
Explicit exclusions are included in failed and shown as a subtotal.

## Saved 40-listing demonstration

Run against the [reviewed cohort](full-cohort-coverage-2026-11-18.md).
The following examples use the same date and input. The thresholds illustrate
the mechanics of the CLI.

```powershell
$snapshot = "data/runs/full-cohort-2026-11-18/manual-coverage.json"
$reports = "data/runs/full-cohort-2026-11-18"
uv run --offline --no-sync python scripts/screen_etfs.py $snapshot --as-of 2026-11-18 --output "$reports/comparison.md"
uv run --offline --no-sync python scripts/screen_etfs.py $snapshot --as-of 2026-11-18 --market EU --strategy bond --fee-cap ter=20 --max-duration 5.10 --max-below-ig 5 --output "$reports/xetra-bond-screen.md"
uv run --offline --no-sync python scripts/screen_etfs.py $snapshot --as-of 2026-11-18 --market US --strategy equity --fee-cap expense_ratio=32 --exclude-symbol ACWI --output "$reports/us-equity-screen.md"
uv run --offline --no-sync python scripts/screen_etfs.py $snapshot --as-of 2026-11-18 --market EU --strategy bond --hedged-to EUR --output "$reports/xetra-hedge-screen.md"
```

| Query | Input | Comparison-ready | Passed | Failed | Unknown | Explicit exclusions |
|---|---:|---:|---:|---:|---:|---:|
| Baseline evidence | 40 | 40 | 40 | 0 | 0 | 0 |
| Xetra bonds with cost, duration and credit caps | 40 | 40 | 2 | 38 | 0 | 30 |
| US equities with expense ratio cap and ACWI excluded | 40 | 40 | 4 | 35 | 1 | 31 |
| Xetra bonds requiring a dated EUR hedge | 40 | 40 | 0 | 30 | 10 | 30 |

31IG and 32XG pass the bond screen. 32XG is exactly at the 5.10-year
boundary. 28IX meets the fee and duration limits. Its known
below-investment-grade weight of 56.60% fails the credit cap.
AQLT has separate gross and net observations, so the specific
`expense_ratio` filter returned unknown. The 10 Xetra bonds in the hedge
screen have no separately dated hedge evidence in the saved snapshot.
The Markdown reports retain the reason and source links for each row.

CNYA and 36BZ share the MSCI China A Inclusion Index label and have
different identifiers. The report lists the exposure-label match and
shows no supported share-class cross-listing in this cohort.

The demonstration replay used existing local files. The CLI made no network
requests. The cohort and reports stay under ignored `data/runs/`.
