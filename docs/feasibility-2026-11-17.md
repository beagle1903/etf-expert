# First data feasibility pass — 17 November 2026

## Result

One Yahoo pass across the 24 listings in `data/universe.json` completed without captured stage exceptions. All 24 returned quote type ETF and 22 daily price rows. This establishes initial price availability for this selected sample, not broader market coverage or repeatable service reliability.

See [the measured report](coverage-2026-11-17.md) for every listing and missing field.

The sample covers US listings plus German and Dutch listings. It does not test every EU exchange, all issuers or all strategies. Research labels are intentions; no official legal identity or benchmark verification was performed.

## Material gaps

- Category: 12/12 US, 0/12 EU in the profile response.
- Net assets: 12/12 US, 5/12 EU.
- Raw expense fields: 12/12 US, 10/12 EU. Units and economic comparability still need validation before fee comparisons.
- Nonempty reported top holdings: 9/12 US, 7/12 EU. AGG and LQD each returned only one row. Nonempty does not mean representative or complete.
- The requested benchmark and ISIN keys were absent from every profile response. Other Yahoo interfaces were not tested for these fields.
- Profile and holdings observation dates were not established. Collection time cannot substitute for those dates.

## Decision and next work

Retain Yahoo as a candidate price source. Do not build eligibility or portfolio allocation on this diagnostic alone. Next, test official issuer supplementation for identity, benchmark, fees, share-class characteristics and dated composition across this same sample. Begin with VWCE.DE and VAGF.DE, which lack expense data here, plus one equity and one bond iShares example. Record sources and unresolved gaps; expand the check to the remaining sample before claiming coverage.

Define the minimum evidence for comparison separately from evidence for selection. Bond risk needs appropriate measures such as duration and credit quality; absence of equity-style top-ten holdings should not automatically become a universal bond exclusion rule. Any such rule remains undecided.

Do not restrict the eventual application to these 24 listings. This is a diagnostic sample. A larger discovery and coverage pass follows a successful source route.

## Reproduction and evidence

Command: `uv run python scripts/check_coverage.py`. Python 3.14.0; yfinance 0.2.66; dependencies pinned in `uv.lock`. The initial project commit was `75ae059`.

Local ignored run: `data/runs/20261117T172137188429Z/`. It contains the exact sample, environment, raw stage responses, per-listing collection times, source links and incremental/final report. The final report was generated at 17:22:50 UTC (20:22:50 Istanbul). Raw provider data stays local. Committed report counts are dated observations.

Three offline tests passed: missing/zero fee distinction, blank/nonfinite missingness, and separate listing/price/quote-type counts. The live run emitted upstream pandas deprecation warnings; no stage exception was captured. No LLM, GUI, Docker, framework or harness subagent was used.
