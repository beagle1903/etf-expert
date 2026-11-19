# Illustrative ETF portfolio rules

The portfolio command uses the complete saved cohort and the comparison rules
from issue #4. A profile sets the comparison date, market, trading currency,
and an equity or bond allocation, or both. Each allocation specifies its
weight in basis points, number of positions, and the fee metric used to rank
its candidates. Optional fee caps apply to that same metric. Optional bond
limits use dated effective duration, credit weights, and hedge evidence.
The profile may explicitly exclude listing symbols. The evidence age defaults
to 180 days as in comparison. All profile fields affect the rules or cash
arithmetic. There are no horizon or drawdown inputs.

## Selection and weights

1. Screen every requested listing. A candidate must be in the requested
   market, currency and asset class, pass the applicable comparison rules,
   and have a usable observation for the profile's named fee metric.
2. If eligible listings for the same class disagree on asset class or
   exposure label, mark those identity links unresolved for this run.
   Consider all remaining eligible listings. In each asset class, order
   by the named annual fee in basis points, then symbol and venue.
3. Starting with the least expensive listing, take up to the requested
   count, with at most one listing per supported class identifier and
   one listing per exact exposure label within an asset class. Label
   matching ignores case and whitespace. This is a simple way to avoid
   known duplicates. It does not establish independent risks or complete
   holdings overlap, and it can group distinct strategies under the same
   published label. If the count is infeasible, return a blocker and
   omit allocations for the entire portfolio.
4. Split each asset-class allocation equally among the selected positions
   at one basis point precision. Assign any leftover basis points in
   selection order. Exposure weights and position counts are profile
   inputs. Fees affect the choice of positions within an asset class.

## Cash

The profile supplies initial and recurring cash in its trading currency.
USD and EUR use cents. Cash can be zero. The command computes each position's
ideal share of each budget separately, floors to cents, then assigns any
leftover cents by descending fractional remainder and selection order.
The amounts represent fractional-share dollar or euro budgets. There are
no price, share quantity, transaction-cost, cash reserve or FX calculations.
For cash ties, asset-class names are sorted alphabetically, then the
selection order within each asset class is used.

Requested, researched, eligible, shortlisted and selected counts are
reported separately. The CLI uses all eligible rows directly, so the
shortlist count is null. The report preserves per-listing evidence and
reasons, including exclusions, unknowns and eligible rows omitted by the
position count or known duplicate rules. Each candidate and selected
position includes its input record under `evidence`, preserving collection
metadata, field dates, and any hedge evidence.
Researched means there is a source link for the fee, exposure or bond risk.
Comparison-ready follows the baseline evidence rules for the comparison
date. Eligible applies the profile and rejects conflicting identity links.
The output includes distinct exposure-label capacity and the fee at each
asset class's selection cutoff. An infeasible profile exits with status 1,
saves its reasons when given an output path, and leaves both cash budgets
unallocated.

## Example on the saved 40 listings

Save this profile as a local JSON file. Cash values are decimal strings in
the selected currency. The weights, caps and budgets illustrate the command.

```json
{
  "as_of": "2026-11-18",
  "market": "EU",
  "currency": "EUR",
  "initial_cash": "1000.01",
  "recurring_cash": "99.99",
  "allocations": [
    {
      "strategy": "equity",
      "positions": 3,
      "weight_bps": 6001,
      "fee_metric": "ter",
      "fee_cap_bps": 25
    },
    {
      "strategy": "bond",
      "positions": 2,
      "weight_bps": 3999,
      "fee_metric": "ter",
      "fee_cap_bps": 20,
      "max_duration_years": 5.10,
      "max_below_ig_pct": 5
    }
  ]
}
```

```powershell
$folder = "data/runs/full-cohort-2026-11-18"
uv run --offline --no-sync python scripts/build_portfolio.py "$folder/manual-coverage.json" "$folder/illustrative-profile.json" --output "$folder/illustrative-portfolio.json"
```

The dated [issuer-reviewed cohort](full-cohort-coverage-2026-11-18.md)
produced 40 requested, 40 researched, 40 comparison-ready, 11 eligible
and 5 selected listings. 32XG is at the 5.10-year duration cap. There are
exactly two eligible bonds under this profile. The three equities are
selected from nine eligible listings, with ticker order deciding which
three of the four 15 bp sector ETFs fit.

| Listing | Weight | Initial EUR | Recurring EUR |
|---|---:|---:|---:|
| 31IG | 20.00% | 200.00 | 20.00 |
| 32XG | 19.99% | 199.90 | 19.99 |
| 2B7A | 20.01% | 200.11 | 20.00 |
| 2B7B | 20.00% | 200.00 | 20.00 |
| 2B7C | 20.00% | 200.00 | 20.00 |
| **Total** | **100.00%** | **1,000.01** | **99.99** |

In the second run, adding `"excluded_symbols": ["2B7A"]` and raising the
duration cap to `6` replaced 2B7A with 2B7D. The change admitted 33GI, which
ranked behind the first two equal-cost bond listings. The position weights
and total cash were identical. Lowering that duration cap to `4.29` produced
zero qualifying bonds for two requested positions and withheld the entire
allocation. All three runs replayed saved issuer evidence offline.
