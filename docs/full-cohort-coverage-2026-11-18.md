# Full-cohort ETF coverage — 18 November 2026

**40 of 40 listings met the documented comparison evidence gate in this
one-time issuer-document review.** The cohort is unchanged from the
[broader discovery pilot](broader-coverage-2026-11-18.md). The target was
32 of 40 overall and at least 8 of 10 in each group.

| Original group | Requested | Reviewed | Comparison-ready |
|---|---:|---:|---:|
| US equity | 10 | 10 | 10 |
| US bonds | 10 | 10 | 10 |
| Xetra equity | 10 | 10 | 10 |
| Xetra bonds | 10 | 10 | 10 |

Each listing has a share-class identifier tied to its venue, a verified
trading currency, a dated annual fee with its source label, and issuer
benchmark or strategy evidence. All 20 bond listings also have dated
effective duration and dated numeric credit evidence. The result supports
building the first comparison workflow in issue #4 on this saved cohort.
It establishes point-in-time research coverage for one issuer on the
specified venues. Refresh reliability, rights for recurring collection,
and coverage of other issuers remain open.

## Evidence and limitations

- The eight [previously reviewed listings](dated-source-check-2026-11-18.md)
  were reused. The remaining 32 were checked against the same requirements.
  Candidate issuer URLs were located using the earlier local catalogue
  snapshot. Only the matched issuer factsheets, prospectus and listing
  pages supplied the comparison evidence. Xetra listings were joined on the
  exact venue ISIN. US issuer listing tables were matched by ticker and
  exchange code, including cases where the same ticker trades in more than
  one currency or venue. [Nasdaq Trader directory definitions](https://www.nasdaqtrader.com/Trader.aspx?id=SymbolDirDefs) ·
  [Xetra tradable instruments](https://www.cashmarket.deutsche-boerse.com/cash-en/trading/Tradable-Instruments-Xetra/)
- **AGGM** changed name, ticker and underlying index on 1 September 2026.
  The issuer's linked June GBF sheet carries the same CUSIP but describes
  the old benchmark, fee and portfolio. The selected evidence is the
  revised prospectus and the product page's 17 November duration and
  credit breakdown. The June document, failed new-name URL and abbreviated
  product URL were retained in the attempt log.
  [Revised prospectus](https://www.ishares.com/us/literature/summary-prospectus/sp-ishares-government-credit-bond-etf-2-28.pdf) ·
  [Dated product fields](https://www.ishares.com/us/products/239462/ishares-1-10-year-u-s-aggregate-bond-etf)
- **36B4** initially returned a valid PDF for the accumulating share class.
  That claim was excluded. The selected distributing-class PDF matches
  `IE00BGDQ0V72`. **2B7B, 2B7J and 36B3** also needed revised document
  candidates after a gateway error or HTML responses. No failed or
  mismatched source was credited.
  [36B4 factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/sujd-ishares-msci-japan-sri-ucits-etf-fund-fact-sheet-en-de.pdf)
- **CALI** has dated credit evidence, with 99.82% accounted for by the
  printed buckets. The unexplained 0.18 percentage points remain unknown.
  **34GI** retains its reported −0.04% cash/derivatives line. The review
  preserved raw credit weights without inserting categories or rescaling
  totals. The Xetra credit charts were read visually. Full credit tables
  stay with the saved evidence.
  [CALI factsheet](https://www.ishares.com/us/literature/fact-sheet/cali-ishares-short-term-california-muni-active-etf-fund-fact-sheet-en-us.pdf) ·
  [34GI factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/34gi-ishares-ibonds-dec-2034-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf)
- Fees preserve gross, net, annual operating expenses and TER as distinct
  measures. Most dates describe the issuer observation. AGGM uses its
  prospectus revision date. The oldest attributed fee observations are
  AAXJ and BKF on 30 June. Issue #4 still needs explicit freshness and
  fee-basis rules for each comparison. A credit breakdown for a fund of
  funds such as BYLD remains an issuer-reported exposure measure.
  [BYLD factsheet](https://www.ishares.com/us/literature/fact-sheet/byld-ishares-yield-optimized-bond-etf-fund-fact-sheet-en-us.pdf)

## Source accounting and replay

The follow-up recorded 56 requests across 18:06–18:09 UTC on 18 November
(21:06–21:09 Istanbul), with about 64 seconds of summed request time.
Five recorded requests returned HTTP or document-format errors. Two other
responses were readable PDFs for a different class or an earlier strategy.
An initial collection process stopped during PDF extraction. Saved
responses were retained, and the remaining documents were collected
serially. All 32 listings reached a usable result. No data subscription
was purchased. Manual source selection and chart-review time were not
measured separately.

The offline check matched all 40 rows and their order to
`data/runs/broader-2026-11-18/pilot-universe.json`, verified the saved
response hashes, and reproduced the four group counts from
`data/runs/full-cohort-2026-11-18/manual-coverage.json`. That local JSON
contains source references, separate dates, fee labels, benchmark or
strategy evidence, and the full reported credit buckets. It references
source PDFs, HTML, and attempts in that directory and
`data/runs/dated-source-check-2026-11-18/`. The local review script
`data/runs/full-cohort-review.py` replays those observations without
network requests. The table below provides the issuer links for
checking the findings independently. Downloaded source files and the
full normalized dataset are kept in ignored local storage.

## Listing evidence

The credit column shows the largest disclosed rating bucket. Observation
dates are listed alongside each figure. Every row passed this coverage gate.

### US equity

| Listing | Trading currency | Annual fee and date | Sources |
|---|---|---|---|
| AAXJ | USD | 0.72% expense ratio (2026-06-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/aaxj-ishares-msci-all-country-asia-ex-japan-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239601/ishares-msci-all-country-asia-ex-japan-etf) |
| ACWI | USD | 0.32% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/acwi-ishares-msci-acwi-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239600/ishares-msci-acwi-etf) |
| ACWV | USD | 0.20% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/acwv-ishares-msci-global-min-vol-factor-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239605/ishares-msci-global-min-vol-factor-etf) |
| ACWX | USD | 0.32% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/acwx-ishares-msci-acwi-ex-u-s-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239594/ishares-msci-acwi-ex-u-s-etf) |
| AQLT | USD | 0.22% gross / 0.20% net (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/aqlt-ishares-msci-global-quality-factor-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/340396/ishares-msci-global-quality-factor-etf) |
| BALQ | USD | 0.35% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/balq-ishares-nasdaq-premium-income-active-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/346870/ishares-nasdaq-premium-income-active-etf) |
| BKF | USD | 0.72% expense ratio (2026-06-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/bkf-ishares-msci-bic-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239614/ishares-msci-bic-etf) |
| CNYA | USD | 0.60% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/cnya-ishares-msci-china-a-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/273318/ishares-msci-china-a-etf) |
| CRBN | USD | 0.20% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/crbn-ishares-low-carbon-optimized-msci-acwi-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/271054/ishares-low-carbon-optimized-msci-acwi-etf) |
| DMXF | USD | 0.12% expense ratio (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/dmxf-ishares-esg-advanced-msci-eafe-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/314362/ishares-esg-advanced-msci-eafe-etf) |

### US bond

| Listing | Trading currency | Annual fee and date | Effective duration (years) and date | Largest credit bucket and date | Sources |
|---|---|---|---|---|---|
| AGGM | USD | 0.03% annual operating expenses (2026-09-01) | 4.21 (2026-11-17) | AA Rated 76.48% (2026-11-17) | [Prospectus](https://www.ishares.com/us/literature/summary-prospectus/sp-ishares-government-credit-bond-etf-2-28.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239462/ishares-1-10-year-u-s-aggregate-bond-etf), [risk](https://www.ishares.com/us/products/239462/ishares-1-10-year-u-s-aggregate-bond-etf) |
| AGZ | USD | 0.15% expense ratio (2026-09-30) | 3.44 (2026-09-30) | AA Rated 98.95% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/agz-ishares-agency-bond-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239457/ishares-agency-bond-etf) |
| BEMB | USD | 0.15% expense ratio (2026-09-30) | 5.34 (2026-09-30) | BBB Rated 32.85% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/bemb-ishares-j-p-morgan-broad-usd-emerging-markets-bond-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/329561/ishares-j-p-morgan-broad-usd-emerging-markets-bond-etf) |
| BGRN | USD | 0.20% expense ratio (2026-09-30) | 4.61 (2026-09-30) | BBB Rated 37.36% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/bgrn-ishares-usd-green-bond-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/305296/ishares-usd-green-bond-etf) |
| BREM | USD | 0.50% expense ratio (2026-09-30) | 5.95 (2026-09-30) | BBB Rated 29.26% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/brem-ishares-emerging-markets-bond-active-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/346525/ishares-emerging-markets-bond-active-etf) |
| BTOT | USD | 0.10% gross / 0.09% net (2026-09-30) | 5.29 (2026-09-30) | AA Rated 61.76% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/btot-ishares-total-usd-fixed-income-market-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/347943/ishares-total-usd-fixed-income-market-etf) |
| BYLD | USD | 0.41% gross / 0.13% net (2026-09-30) | 5.76 (2026-09-30) | BBB Rated 26.90% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/byld-ishares-yield-optimized-bond-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/264127/ishares-yield-optimized-bond-etf) |
| CALI | USD | 0.25% gross / 0.20% net (2026-09-30) | 1.21 (2026-09-30) | AA rated 51.49% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/cali-ishares-short-term-california-muni-active-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/332497/ishares-short-term-california-muni-active-etf) |
| CEMB | USD | 0.50% expense ratio (2026-09-30) | 4.18 (2026-09-30) | BBB Rated 33.05% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/cemb-ishares-j-p-morgan-em-corporate-bond-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239525/ishares-j-p-morgan-em-corporate-bond-etf) |
| CMBS | USD | 0.25% expense ratio (2026-09-30) | 3.62 (2026-09-30) | AA Rated 58.38% (2026-09-30) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/cmbs-ishares-cmbs-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239459/ishares-cmbs-etf) |

### Xetra equity

| Listing | Trading currency | Annual fee and date | Sources |
|---|---|---|---|
| 2B7A | EUR | 0.15% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/iuus-ishares-s-p-500-utilities-sector-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 2B7B | EUR | 0.15% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/iums-ishares-s-p-500-materials-sector-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 2B7C | EUR | 0.15% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/iuis-ishares-s-p-500-industrials-sector-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 2B7D | EUR | 0.15% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/iucs-ishares-s-p-500-consumer-staples-sector-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 2B7J | EUR | 0.20% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/suws-ishares-msci-world-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 2B7K | EUR | 0.20% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/susw-ishares-msci-world-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 36B3 | EUR | 0.20% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/ised-ishares-msci-europe-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 36B4 | EUR | 0.20% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/sujd-ishares-msci-japan-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 36B5 | EUR | 0.25% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/semd-ishares-msci-em-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 36BZ | EUR | 0.40% TER (2026-11-06) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/cnya-ishares-msci-china-a-ucits-etf-fund-fact-sheet-en-de.pdf) |

### Xetra bond

| Listing | Trading currency | Annual fee and date | Effective duration (years) and date | Largest credit bucket and date | Sources |
|---|---|---|---|---|---|
| 28IX | EUR | 0.20% TER (2026-11-05) | 1.48 (2026-11-05) | BBB 42.18% (2026-10-31) | [Factsheet](https://www.blackrock.com/gls-download/literature/fact-sheet/28ix-ishares-ibonds-dec-2028-term-corp-crossover-ucits-etf-fund-fact-sheet-en-dk.pdf) |
| 31IG | EUR | 0.12% TER (2026-11-06) | 4.30 (2026-11-06) | BBB 47.95% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/31ig-ishares-ibonds-dec-2031-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 32XG | EUR | 0.12% TER (2026-11-06) | 5.10 (2026-11-06) | BBB 47.90% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/32xg-ishares-ibonds-dec-2032-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 33GI | EUR | 0.12% TER (2026-11-06) | 5.85 (2026-11-06) | BBB 53.37% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/33gi-ishares-ibonds-dec-2033-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 34GI | EUR | 0.12% TER (2026-11-06) | 6.60 (2026-11-06) | BBB 49.31% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/34gi-ishares-ibonds-dec-2034-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 35AI | EUR | 0.12% TER (2026-11-06) | 7.33 (2026-11-06) | A 50.43% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/35ai-ishares-ibonds-dec-2035-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 36B1 | EUR | 0.45% TER (2026-11-06) | 6.31 (2026-11-06) | BBB 37.47% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/emes-ishares-jp-morgan-advanced-em-bond-ucits-etf-fund-fact-sheet-en-de.pdf) |
| 36B7 | EUR | 0.25% TER (2026-11-04) | 5.60 (2026-11-04) | A 44.68% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/36b7-ishares-global-corp-bond-ucits-etf-fund-fact-sheet-en-gb.pdf) |
| 3SUD | EUR | 0.50% TER (2026-11-06) | 6.36 (2026-11-06) | BBB 33.77% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/3sud-ishares-j-p-morgan-em-bond-ucits-etf-fund-fact-sheet-en-de.pdf) |
| AEGE | EUR | 0.10% TER (2026-11-06) | 6.02 (2026-11-06) | AA 38.66% (2026-10-31) | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/aege-ishares-global-aggregate-bond-esg-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
