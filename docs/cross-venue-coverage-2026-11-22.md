# U.S. and Xetra issuer evidence pilot, 22 November 2026

Five of the eight pinned listings are comparison-ready under the existing
180-day evidence rules. Every request matched a venue row and an issuer
share-class identifier. The three unresolved listings all come from Vanguard.
The gaps are the supported fee metric and the documented duration method.

The [cohort](../data/issue-18-cohort.json) was committed before collection
(`1b06fd5`). It uses iShares and Vanguard, with one S&P 500 equity anchor and
one broad bond ETF per issuer and market. IVV, VOO and the previously
unresolved IUSB carry forward from issue #17. The other targets complete
the matrix by mandate. All eight slots were filled without substitution.
The bonds span different universes and hedging arrangements. This
purposeful sample measures source coverage for these listings.

| Issuer | U.S. requested / ready | Xetra requested / ready | Total requested / ready |
|---|---:|---:|---:|
| iShares | 2 / 2 | 2 / 2 | 4 / 4 |
| Vanguard | 2 / 1 | 2 / 0 | 4 / 1 |
| Total | 4 / 3 | 4 / 2 | 8 / 5 |

Within the U.S., NYSE Arca was 2/2 ready and Nasdaq was 1/2 ready.
Across both markets, equities were 3/4 ready and bonds were 2/4 ready.

## Evidence by listing

Fee values are in annual basis points. The U.S. factsheet dates establish
when the issuer reported each ratio. They do not establish its original
effective date. The iShares German factsheets separately date portfolio
breakdowns and other data. Each row has sourced trading currency.

| Listing and issuer document | Share-class ID and issuer benchmark | Reported fee and observation date | Bond duration and credit | Ready |
|---|---|---|---|---|
| [IVV](https://www.ishares.com/us/literature/fact-sheet/ivv-ishares-core-s-p-500-etf-fund-fact-sheet-en-us.pdf) | CUSIP 464287200 · S&P 500 Index (USD) | Expense ratio 3 · Jun 30 | — | Yes |
| [IUSB](https://www.ishares.com/us/literature/fact-sheet/iusb-ishares-core-universal-usd-bond-etf-fund-fact-sheet-en-us.pdf) | CUSIP 46434V613 · BBG U.S. Universal Index (USD) | Expense ratio 6 · Sep 30 | Effective 5.53 years and credit weights · Sep 30 | Yes |
| [SXR8](https://www.ishares.com/gls-download/literature/fact-sheet/cspx-ishares-core-s-p-500-ucits-etf-fund-fact-sheet-en-de.pdf) | ISIN IE00B5BMR087 · S&P 500 Index | TER 7 · Nov 6 | — | Yes |
| [EUNA](https://www.ishares.com/gls-download/literature/fact-sheet/aggh-ishares-core-global-aggregate-bond-ucits-etf-fund-fact-sheet-en-de.pdf) | ISIN IE00BDBRDM35 · Bloomberg Global Aggregate Bond Index | TER 10 · Nov 6 | Effective 6.06 years · Nov 6. Credit weights · Oct 31 | Yes |
| [VOO](https://fund-docs.vanguard.com/F0968.pdf) | CUSIP 922908363 · S&P 500 Index | Expense ratio 3 · Sep 30 | — | Yes |
| [BND](https://fund-docs.vanguard.com/F0928.pdf) | CUSIP 921937835 · Bloomberg U.S. Aggregate Adjusted Float Index | Expense ratio 3 · Sep 30 | Average 5.7 years and credit weights · Sep 30. Effective method unverified | No |
| [VUAA](https://fund-docs.vanguard.com/SandP_500_UCITS_ETF_USD_Accumulating_9694_EU_INT_UK_EN.pdf) | ISIN IE00BFMXXD54 · S&P 500 Net Total Return | Ongoing charges figure 7 · Oct 31. Metric unsupported | — | No |
| [VAGF](https://fund-docs.vanguard.com/Global_Aggregate_Bond_UCITS_ETF_EUR_Hedged_Accumulating_9443_EU_INT_UK_EN.pdf) | ISIN IE00BG47KH54 · Bloomberg Global Aggregate Float Adjusted and Scaled Index in EUR | Ongoing charges figure 8 · Oct 31. Metric unsupported | Average 6.0 years and credit weights · Oct 31. Effective method unverified | No |

Identity, currency and issuer exposure evidence cover 8/8. Dated fee
observations cover 8/8, with supported metrics for 6/8. Numeric credit
breakdowns cover 4/4 bonds and labeled effective duration covers 2/4.
BND's 69.0% U.S. Government bucket includes Treasury and agency exposure.
It remains an unsplit category in the credit calculation. EUNA's credit
values were checked against the rendered chart. Comparison readiness
does not resolve credit uncertainty or prove holdings overlap.

## Live collection and claim reconciliation

- Fourteen direct requests began between 08:18:05 and 08:18:48 UTC on
  22 November. Twelve returned HTTP 200. Two failures were retained:
  IUSB's short product URL returned 403 and the legacy factsheet URL
  returned 404. The full current product URL, renamed PDF and summary
  prospectus were accessible. The September factsheet supplies the dated
  fee and bond evidence missing in #17. The prospectus dated February 27
  separately reports 0.06% total annual fund operating expenses.
- Nasdaq's directory carried its November 20 21:33 source stamp. The
  Xetra file downloaded on November 22 carried **November 23** in its
  update field. All four requested Xetra rows agreed with the retained
  November 20 file, collected that day at 10:51 UTC. Replay used the
  November 20 file for Xetra. Both source dates and responses are saved.
  Four U.S. quote metadata lookups supplied USD and matching venue
  family around 08:19 UTC. Their fields carry no observation date.
- The iShares Xetra factsheet has AGGH in the issuer ticker column for
  EUNA. Its Bloomberg/RIC fields use EUNA/EUNA.DE, and ISIN and WKN agree
  with the exchange row. Vanguard lists VUAA as the Deutsche Börse ticker
  and VUA1.DE as a RIC. The table uses the exchange mnemonics. There
  were no unresolved same-field conflicts in the accepted claims.
- Manual evidence review and preparation took about **3 minutes elapsed**
  from the first downloads completing at 08:18:10 UTC through the reviewed
  snapshot at 08:21:10 UTC. That window includes follow-up downloads,
  extraction and replay setup. It excludes cohort design and report writing.
  Active time and per-listing time were not measured.

## Offline replay and next work

Raw files, HTTP attempts with timestamps and hashes, original and prior
venue files, quote metadata, extracted text and bond page images,
`assemble-review.py`, `cohort.json`, `reviewed.json` and the outputs are
saved locally in ignored `data/runs/issue18-2026-11-22/`. The local files
are required for exact replay. The tracked cohort and this report give
the request and outcome in a fresh checkout.

```powershell
$run = "data/runs/issue18-2026-11-22"
uv run --offline --no-sync python "$run/assemble-review.py"
uv run --offline --no-sync python scripts/prepare_snapshot.py "$run/cohort.json" "$run/reviewed.json" --output "$run/snapshot.json"
uv run --offline --no-sync python scripts/screen_etfs.py "$run/snapshot.json" --as-of 2026-11-22 --output "$run/comparison.md"
```

The replay made no network calls and retained all eight listings, with
five ready and three unknown. No allocation was evaluated.

Prioritize issuer PDFs and a small source registry that records stable
fund identifiers, alternate issuer URL paths, and field-specific dates.
Before expanding the cohort, decide whether to support ongoing charges
as a separate named metric and seek a Vanguard source or methodology
note that explicitly establishes effective duration. Keep a manual check
for chart-only credit weights, venue ticker aliases and source dates that
fall after the comparison date. The eight observations are too few to
estimate issuer-wide coverage or manual review throughput.
