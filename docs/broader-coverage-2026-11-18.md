# Broader ETF coverage — 18 November 2026

A [dated issuer-document spot check](dated-source-check-2026-11-18.md)
recovered the required evidence for eight members of the same cohort.
The [full-cohort issuer-document review](full-cohort-coverage-2026-11-18.md)
subsequently met the comparison gate for all 40.

## Scope set before collection

Test 40 additional listings, with 10 iShares equity and 10 iShares bond
listings in each market. Use US exchange listings from Nasdaq Trader and
German Xetra listings from Deutsche Börse. The EU scope is Xetra only. Issuer
catalogue classifications or explicit equity and bond terms in issuer product
names can guide sampling. Record the selection rule and any shortfalls. Keep
the 24 original listings outside this incremental experiment. One issuer limits
the number of formats under test and the conclusions about issuer breadth.

Use published bulk venue files and issuer catalogue views to test a route
with fewer requests than per-fund issuer scraping. Start with one bounded
snapshot of each input. Retain cache files locally. A snapshot file is a full
download with no pagination. Treat issuer catalogue coverage and any
per-listing evidence as separate from venue discovery.

The pilot supports the next comparison task only if at least 32 of 40
listings, including at least 8 of 10 in each market and strategy group, have
attributable listing and share-class identity, trading currency, a dated
annual fee with a defined basis and a credible exposure description.
Bond exposure also requires dated duration and credit evidence. The 80%
bar is a diagnostic threshold set below the first run's raw fee extraction
rate of 23/24, reflecting the incomplete identities and dates found in #2.
Track missing currency-hedging and composition evidence separately. These
are research acceptance criteria for the pilot.

Sources to evaluate

- [Nasdaq Trader symbol directory and field definitions](https://www.nasdaqtrader.com/Trader.aspx?id=SymbolDirDefs)
- [Deutsche Börse Xetra tradable instruments](https://www.cashmarket.deutsche-boerse.com/cash-en/trading/Tradable-Instruments-Xetra/)
- [iShares US ETF catalogue](https://www.ishares.com/us/products/etf-investments)
- [iShares German product catalogue](https://www.ishares.com/de/privatanleger/de/produkte/produktliste)
- [SEC series and class report](https://www.sec.gov/data-research/sec-markets-data/investment-company-series-class-information)

The issuer catalogue check also tests the published product-data responses.
If the German catalogue yields no fund rows, test the public Danimoth UCITS
snapshot as secondary evidence by exact ISIN. Its snapshot date can establish
the publisher's release date. Fee or risk field dates need their own evidence.

## Result and decision

The pilot reached all 40 additional listings and collected partial research
for each. **Zero met the bulk comparison requirements.** Keep issue #4
blocked for the broader pool. The venue files are useful discovery inputs.
Reaching the comparison goal still requires a source with attributable,
dated fee and risk fields. A permitted data export or a licensed feed could
be tested against this same frozen cohort before changing the scope.

### Discovery and exclusions

- Nasdaq rows require `ETF=Y`, `Test Issue=N` and `Nasdaq Traded=Y`. Preserve
  the source listing-exchange code. Sample named iShares products, using
  explicit bond words first and selected equity index names otherwise.
  This yielded 5,802 venue rows.
- Xetra rows require `Instrument Type=ETF`, `MIC Code=XETR` and active
  instrument and product statuses. The sample uses iShares abbreviated
  name prefixes plus the fixed-income assignment group or passive ETF
  group with an equity index name. This yielded 3,182 venue rows.
- Across the two files, 8,465 rows fell outside the issuer and strategy
  filters, and 10 matched symbols in the original sample. Within each
  group, sort by symbol, venue, currency and ISIN. Keep the first instance
  of each class or US symbol, then select the first ten. There were no
  duplicates under that rule in the scoped rows and 469 rows fell outside
  the pilot quota. This accounts for all 8,984 venue rows. The alphabetical
  rule overrepresents some strategies, such as Xetra target-maturity bonds.

| Scope | Matches | Requested | Research attempted | Research collected | Normalized | Unresolved | Comparison-ready |
|---|---:|---:|---:|---:|---:|---:|---:|
| US equity | 157 | 10 | 10 | 10 | 10 | 10 | 0 |
| US bonds | 114 | 10 | 10 | 10 | 10 | 10 | 0 |
| Xetra equity | 120 | 10 | 10 | 10 | 10 | 10 | 0 |
| Xetra bonds | 118 | 10 | 10 | 10 | 10 | 10 | 0 |

Attempted means a relevant research source was queried for the market.
Collected means a unique catalogue or regulator row joined to the listing.
Normalized means the pilot recorded the venue facts, matched research and
missing requirements in a consistent row. Unresolved means at least one
material comparison requirement lacks evidence. Each local record lists
its unresolved requirements.

### Material field coverage

| Evidence from saved bulk sources | US equity / 10 | US bonds / 10 | Xetra equity / 10 | Xetra bonds / 10 |
|---|---:|---:|---:|---:|
| Venue from exchange directory | 10 | 10 | 10 | 10 |
| Share-class identifier | 0 | 0 | 10 | 10 |
| Trading currency | 0 | 0 | 10 | 10 |
| Raw fee figure | 10 | 10 | 10 | 10 |
| Dated annual fee with defined basis | 0 | 0 | 0 | 0 |
| Explicit benchmark description | 0 | 0 | 10 | 10 |
| Dated duration | — | 0 | — | 0 |
| Dated credit | — | 0 | — | 0 |
| Publisher's hedge flag | 0 | 0 | 10 | 10 |
| Publisher's holdings count | 0 | 0 | 10 | 10 |
| Composition weights | 0 | 0 | 0 | 0 |

The 20 US matches come from the issuer's product table using the venue
symbol. Its gross and net percentages have distinct labels. Adjacent
dates refer to yield or return. The directory provides no trading
currency field, and the SEC download failed, leaving US class identifiers
unresolved in the replay. The 20 Xetra matches join by venue ISIN to
Danimoth's snapshot dated 3 August 2026. The snapshot retains per-row upstream
source and collection metadata. Its raw `ter`, benchmark, hedge flag and
count of holdings are secondary claims. The snapshot did not provide an
explicit fee unit and measurement date or the bond risk measures needed
here. A holdings count provides no weights. [Danimoth dataset](https://danimoth.com/dataset)

### Separate manual spot checks

These examples are members of the 40-listing cohort. They illustrate evidence
that can be found individually and are outside the bulk coverage counts.

- **ACWI** has issuer CUSIP 464288257 and Nasdaq venue, and its factsheet
  reports a 0.32% expense ratio and an MSCI ACWI benchmark in the document
  dated 31 March 2026. [ACWI factsheet](https://www.ishares.com/us/literature/fact-sheet/acwi-ishares-msci-acwi-etf-fund-fact-sheet-en-us.pdf)
- **AGZ** has issuer CUSIP 464288166, NYSE Arca venue, and a 0.15% expense
  ratio. Its factsheet also reports 3.44 years of effective duration and
  98.95% AA-rated exposure. [AGZ factsheet](https://www.ishares.com/us/literature/fact-sheet/agz-ishares-agency-bond-etf-fund-fact-sheet-en-us.pdf)
- **2B7A** has a Xetra listing in EUR and USD share-class currency.
  The issuer reports 0.15% TER under its 6 November 2026 date for other
  facts. This corroborates the secondary snapshot's raw `0.0015` for one
  ISIN. [2B7A factsheet](https://www.ishares.com/de/professionelle-anleger/de/literature/fact-sheet/iuus-ishares-s-p-500-utilities-sector-ucits-etf-fund-fact-sheet-en-de.pdf?siteEntryPassthrough=true&switchLocale=y)
- **AEGE** has issuer TER of 0.10% and option-adjusted duration of 5.98
  as of 13 November 2026. The official page identifies a USD benchmark
  version, while the secondary snapshot gives an EUR-hedged description.
  Preserve that distinction until the benchmark variants are reconciled.
  [AEGE issuer page](https://www.ishares.com/de/privatanleger/de/produkte/320169/)

### Access, dates and reproducibility

The saved batch attempted nine HTTP requests between 08:18:04 and 08:20:08 UTC
on 18 November, taking about 43 seconds of summed request time. The Nasdaq file
contained a creation timestamp of 18 November at 03:04 in its source format.
Xetra's header reported an update on 18 November. The US issuer fee table
supplied no fee observation date. The SEC attempted report was published on
1 June 2026 and returned HTTP 403. Both German catalogue routes returned
HTTP 200 shells with no research rows. Both issuer product-data responses
returned HTTP 200 with empty data.

No account or data subscription was used for the batch. Recurring access and
redistribution rights were unverified. The manual work consisted of finding
the published input URLs, checking source layouts and reviewing four issuer
documents or pages. That effort was not separately timed. Bulk inputs and
fund-level outputs stay under ignored `data/runs/`.

```powershell
# Fetch for a new snapshot in batches. Existing successful responses are reused by default.
uv run python scripts/check_broader_coverage.py data/runs/broader-2026-11-18 --fetch nasdaq xetra sec ishares-us ishares-de
uv run python scripts/check_broader_coverage.py data/runs/broader-2026-11-18 --fetch ishares-de-legacy ishares-de-data ishares-us-data danimoth

# Offline replay of the saved pilot
uv run --offline --no-sync python scripts/check_broader_coverage.py data/runs/broader-2026-11-18
uv run --offline --no-sync pytest
```

The pilot contains one full snapshot per successful source, with no list
pagination. `--fetch` selects the input batch and `--timeout` changes the
request timeout. To deliberately try again after a successful HTTP response
with unusable content, pass `--refresh` and the relevant source key.
The collector keeps earlier responses and errors. A failed follow-up
preserves the most recent parseable evidence. Use a new directory to change
the discovery cohort or use `--per-group` to run a different-sized pilot.
The snapshot stores the venue selection, attribution and accounting in
`pilot-universe.json`, and the evidence, per-row issues and coverage in
`coverage.json`.

Offline verification exercises filters and count reconciliation, retained
failure records, and reuse of prior successful evidence with a frozen
cohort. Offline tests make no network calls.
