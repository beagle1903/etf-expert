# Source-backed ETF records — 18 November 2026

Issue #2 used the observations saved on 17 November. The normalization step
made no live requests. The issuer feasibility result still calls for a
different collection route before scaling. [Issuer feasibility assessment](issuer-feasibility-2026-11-17.md)

## Local JSON format

The output contains `requested_listings`, a `summary` and one entry in
`records` for each member of the original universe snapshot. Symbol and market
identify a requested listing in this dataset. `research_intent` preserves the
original sample label. The four field groups represent distinct facts.

| Group | Examples |
|---|---|
| `listing` | Provider venue code, ticker name, trading currency |
| `share_class` | ISIN or CUSIP claim, class currency, fees, income use and hedging |
| `fund` | Issuing entity, fund base currency and fund net assets |
| `exposure` | Benchmark, partial composition, duration, maturity, yield and credit |

The `identity` block records the evidence status of the listing-to-class and
class-to-fund links. An issuer observation with an exact listing code and a
syntactically valid, non-conflicting identifier supports a namespaced class
key such as `ISIN:IE00B5BMR087`. Two such listings can share the same key.
Ticker-only and manually reviewed matches remain unresolved in this replay.
An issuing company can be an umbrella for multiple funds. The observations
supply no stable fund key with an attributable class-to-fund link, so all
fund keys are null. Benchmark names and tickers are exposure evidence.

Each field contains a status, a list of claims and any issue codes. Claims
retain the source field, raw value, reported unit and observation date.
The source references carry collection timestamps, URLs, issuer date
statements and attribution notes. Issuer attempts retain redirects, hashes,
errors and local raw-file references when available. Yahoo observations
retain provider-reported errors and price/holdings row counts. The ignored
original Yahoo file holds the raw observations. Yahoo's asset claim remains
in source coverage because its scope is unverified.

- `missing` has no claim. `unattributed` has issuer evidence without a
  sufficient listing-code or ticker claim. `reported` means a source made a
  claim with a listing attribution, including provisional ticker-only
  attribution. Review the identity block and the observation date before use.
- `conflicting` preserves disagreeing comparable claims or unresolved source
  date statements. Different known observation dates can describe changes and
  remain available. Different values with the same or an unknown date are
  flagged for the fields this converter compares. Differing identifiers
  within the same scheme block the link even across dates. Advanced
  equivalence and conflict detection for corpus-specific exposure fields
  remains open.
- `review` flags mismatched raw fee figures where source units or fee
  definitions prevent a like-for-like comparison. It is separate from
  `conflicting` in the summary. Undated claims retain a null `as_of` even
  when a collection timestamp is available.
- A documented issuer annual percent is multiplied by 100 to give basis points
  as a decimal string. For example, SPY's 0.0945% is 9.45 bp. Gross expense
  ratio, expense ratio, TER and OCF retain separate metric labels. Yahoo fee
  fields retain their values and names with null units and no converted amount.
  A zero from a source stays zero.

## Evidence needed for decisions

| Decision | Minimum evidence |
|---|---|
| Compare listing choices for the same class | Attributable class identifier, venue and trading currency for each listing. Price/liquidity comparison also needs dated, comparable trading observations. |
| Compare recurring fund charges | Attributed share class, documented annual units, comparable fee definitions and observation or effective date. |
| Compare economic exposures | Attributed benchmark or strategy, sufficiently current composition for the comparison, and any material class hedge or currency differences. Compare equity markets, sectors or holdings where relevant. Compare bond duration, maturity, credit and currency exposure where relevant. Yield comparisons require the same definition and a known unit. |
| Establish eligibility or select portfolio positions later | Define freshness, investability and exposure constraints for the intended decision. Obtain supporting evidence for each material constraint. Partial issuer weights can describe concentration within their scope. Full overlap requires comparable holdings or equivalent evidence. |

These are evidence requirements for later work. The converter preserves gaps
with no eligibility exclusions or screening thresholds.

## Diagnostic conversion

The [README](../README.md#source-backed-etf-records) gives the replay commands.
The output is local under `data/runs/`. Counts below describe conversion of
saved evidence, including 35 issuer attempts of which 10 recorded an error.

| Result | Listings |
|---|---:|
| Requested and converted | 24 |
| With at least one source observation | 24 |
| Source-supported listing-to-class link | 10 |
| Unresolved listing-to-class link | 14 |
| Unresolved class-to-fund link | 24 |
| At least one conflicting field | 2 |
| Raw fee difference requiring review | 2 |

The unresolved listing links comprise all 12 US listings and two EU listings
(EXSA.DE and IBCI.DE). Prior manual reviews of SPY, EXSA.DE and IBCI.DE remain in
the feasibility assessment. The replay has no structured attestation for them.

- VTI's issuer benchmark name and Bloomberg ticker disagree in the saved
  factsheet. Both are retained with a benchmark conflict.
- VAGF.DE's composition, duration, maturity, yield and credit fields retain
  unresolved section dates from the source.
- IBGS.AS and IEAC.AS have issuer TERs of 0.10% and 0.09%, respectively. Yahoo
  reports a raw `netExpenseRatio` of 0.2 for each, with units and observation
  dates unverified in the saved run.

Offline tests exercise fee conversion, dated changes and unresolved conflicts,
cross-listing links, separate currencies, and retention of failed and missing
records. The next data task must establish wider coverage suitable for the
intended comparisons.
