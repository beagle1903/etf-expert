# Official issuer field coverage — 2026-11-17

Saved-response replay. Source claims only; no eligibility, complete identity or overlap validation. Missing is unresolved, never zero. All 24 original listings remain in the denominator.

| Field recovered | US / 12 | EU / 12 |
|---|---:|---:|
| identifier | 12 | 12 |
| legal_entity | 0 | 12 |
| benchmark | 11 | 12 |
| fee | 11 | 12 |
| net_assets | 10 | 12 |
| share_assets | 5 | 12 |
| base_currency | 0 | 3 |
| share_currency | 0 | 12 |
| hedging | 0 | 2 |
| distribution | 10 | 12 |
| composition | 11 | 12 |
| duration | 5 | 5 |
| maturity | 5 | 5 |
| yield | 5 | 5 |
| credit_quality | 5 | 1 |

Counts measure extracted fields, including undated values and source candidates with unresolved listing matches. Read each record before attributing facts. Duration, maturity and credit are applicable to five bond sample intentions per market; equity absence is not an exclusion.

## SPY

Source: [issuer document](https://www.ssga.com/library-content/products/factsheets/etfs/us/factsheet-us-en-spy.pdf)

Collected UTC: 2026-11-17T17:40:37.866613+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: Manual header review required: ticker is graphical; CUSIP extracted

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Key Features • The State Street® SPDR® S&P 500® ETF Trust seeks to provide investment results that, before expenses, correspond generally to the price and yield performance of the S&P 500® Index (the “Index”) • The S&P 500 Index is a diversified large cap U.S.

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 78462F103 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | S&P 500® Index |  | unresolved |
| fee | 0.0945 | percent per year; gross expense ratio | 2026-09-30 |
| net_assets | MISSING / unresolved |  |  |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | MISSING / unresolved |  |  |
| composition | Top 10 Holdings‡ Weight (%) NVIDIA CORP 8.38 APPLE INC 7.37 MICROSOFT CORP 5.77 AMAZON.COM INC 3.71 ALPHABET INC CL A 3.06 BROADCOM INC 2.53 ALPHABET INC CL C 2.46 META PLATFORMS INC CLASS A 2.42 MICRON TECHNOLOGY INC 1.82 TESLA INC 1.52 | partial holdings; Weight (%) table | 2026-09-30 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ssga.com/library-content/products/factsheets/etfs/us/factsheet-us-en-spy.pdf) — 2026-11-17T17:40:37.866613+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/SPY-22.pdf`

## VTI

Source: [issuer document](https://fund-docs.vanguard.com/F0970.pdf)

Collected UTC: 2026-11-17T17:40:23.912094+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard Morningstar Total Stock Market ETF | VTI As of September 30, 2026 Investment approach • Seeks to track the performance of the Morningstar US Total Market Index. • Large-, mid-, and small-cap equity diversified across growth and value styles.

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 922908769 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | Morningstar US Total Market Index |  | 2026-09-30 |
| fee | 0.03 | percent per year; Expense ratio 1 | unresolved |
| net_assets | $2,322,816 million | USD million ($ source notation) | 2026-09-30 |
| share_assets | $689,219 million | USD million; ETF shares, not whole fund | 2026-09-30 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Quarterly |  | 2026-09-30 |
| composition | Tenlargest holdings and%of total netassets 2 NVIDIA Corp. 7.1 % Apple Inc. 6.6 % Microsoft Corp. 5.2 % Alphabet Inc. 4.9 % Amazon.com Inc. 3.3 % Broadcom Inc. 2.3 % Meta Platforms Inc. 2.2 % Micron Technology Inc. | partial holdings or aggregate weights in percent | 2026-09-30 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Fee refers to most recent prospectus; effective date not established by factsheet date.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/F0970.pdf) — 2026-11-17T17:40:23.912094+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/VTI-12.pdf`

## QQQ

Source: [issuer document](https://www.invesco.com/us/en/financial-products/etfs/invesco-qqq-trust-series-1.html)

Collected UTC: 2026-11-17T17:41:41.171657+00:00

Source dates: `{}`

Listing: Product JSON-LD ticker QQQ; exchange and source observation date unresolved

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Invesco QQQ Trust, Series 1

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | US46090E1038 | ISIN | unresolved |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | MISSING / unresolved |  |  |
| fee | MISSING / unresolved |  |  |
| net_assets | MISSING / unresolved |  |  |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | MISSING / unresolved |  |  |
| composition | MISSING / unresolved |  |  |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Factsheet links returned HTML. Fallback only recovers explicit structured identity. Dynamic fee, holdings, currencies and distribution remain unresolved in this route.

Attempts:

- [factsheet](https://www.invesco.com/us-rest/contentdetail?contentId=1b6ee2b7fe2ef410VgnVCM100000c2f1bf0aRCRD) — 2026-11-17T17:40:39.154565+00:00; HTTP 200; ValueError: Expected PDF, received non-PDF response; no coverage credited; raw `issuers-20261117T174001860718Z/QQQ-23.html`
- [factsheet](https://www.invesco.com/us-rest/contentdetail?contentId=1b6ee2b7fe2ef410VgnVCM100000c2f1bf0aRCRD) — 2026-11-17T17:41:31.698286+00:00; HTTP 200; ValueError: Expected PDF, received non-PDF response; no coverage credited; raw `issuers-20261117T174127895555Z/QQQ-23.html`
- [factsheet](https://www.invesco.com/content/dam/invesco/us/en/product-documents/etf/fact-sheet/qqq-invesco-qqq-etf-fact-sheet.pdf) — 2026-11-17T17:41:39.763825+00:00; HTTP 200; ValueError: Expected PDF, received non-PDF response; no coverage credited; raw `issuers-20261117T174127895555Z/QQQ-26.html`
- [product](https://www.invesco.com/us/en/financial-products/etfs/invesco-qqq-trust-series-1.html) — 2026-11-17T17:41:41.171657+00:00; HTTP 200; saved; raw `issuers-20261117T174127895555Z/QQQ-27.html`

## VEA

Source: [issuer document](https://fund-docs.vanguard.com/F0936.pdf)

Collected UTC: 2026-11-17T17:40:25.424792+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard FTSE Developed Markets ETF | VEA As of September 30, 2026 Investment approach • Seeks to track FTSE Developed All Cap ex US Index. • International equity diversified across growth and value styles. • Developed markets in Canada and the major

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 921943858 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | FTSE Developed All Cap ex US Index |  | 2026-09-30 |
| fee | 0.03 | percent per year; Expense ratio 1 | unresolved |
| net_assets | $313,544 million | USD million ($ source notation) | 2026-09-30 |
| share_assets | $231,615 million | USD million; ETF shares, not whole fund | 2026-09-30 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Quarterly |  | 2026-09-30 |
| composition | Tenlargest holdings and%of total netassets 2 Samsung Electronics Co. Ltd. 3.2 % SK hynix Inc. 2.3 % ASML Holding NV 2.2 % HSBC Holdings plc | partial holdings or aggregate weights in percent | 2026-09-30 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Fee refers to most recent prospectus; effective date not established by factsheet date.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/F0936.pdf) — 2026-11-17T17:40:25.424792+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/VEA-13.pdf`

## VWO

Source: [issuer document](https://fund-docs.vanguard.com/F0964.pdf)

Collected UTC: 2026-11-17T17:40:26.924902+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard FTSE Emerging Markets ETF | VWO As of September 30, 2026 Investment approach • Seeks to track the performance of the FTSE Emerging Markets All Cap China A Inclusion Index. • Passively managed, using index sampling. • The fund invests substan

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 922042858 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | FTSE Emerging Markets All Cap China A Inclusion Index |  | 2026-09-30 |
| fee | 0.06 | percent per year; Expense ratio 1 | unresolved |
| net_assets | $164,653 million | USD million ($ source notation) | 2026-09-30 |
| share_assets | $125,416 million | USD million; ETF shares, not whole fund | 2026-09-30 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Quarterly |  | 2026-09-30 |
| composition | Tenlargest holdings and%of total netassets 2 Taiwan Semiconductor Manufacturing Co. Ltd. 16.4 % Tencent Holdings Ltd. 2.9 % Alibaba Group Holding Ltd. 2.2 % MediaTek Inc. | partial holdings or aggregate weights in percent | 2026-09-30 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Fee refers to most recent prospectus; effective date not established by factsheet date.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/F0964.pdf) — 2026-11-17T17:40:26.924902+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/VWO-14.pdf`

## VT

Source: [issuer document](https://fund-docs.vanguard.com/F3141.pdf)

Collected UTC: 2026-11-17T17:40:28.341725+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard Total World Stock ETF | VT As of September 30, 2026 Investment approach • Seeks to track the performance of the FTSE Global All Cap Index. • Passively managed, using index sampling. • Fund remains fully invested. • Broad exposure across deve

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 922042742 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | FTSE Global All Cap Index |  | 2026-09-30 |
| fee | 0.06 | percent per year; Expense ratio 1 | unresolved |
| net_assets | $101,182 million | USD million ($ source notation) | 2026-09-30 |
| share_assets | $81,752 million | USD million; ETF shares, not whole fund | 2026-09-30 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Quarterly |  | 2026-09-30 |
| composition | Tenlargest holdings and%of total netassets 2 NVIDIA Corp. 4.6 % Apple Inc. 4.1 % Microsoft Corp. 3.3 % Alphabet Inc. 3.1 % Amazon.com Inc. 2.1 % Taiwan Semiconductor Manufacturing Co. Ltd. | partial holdings or aggregate weights in percent | 2026-09-30 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Fee refers to most recent prospectus; effective date not established by factsheet date.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/F3141.pdf) — 2026-11-17T17:40:28.341725+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/VT-15.pdf`

## IWM

Source: [issuer document](https://www.ishares.com/us/literature/fact-sheet/iwm-ishares-russell-2000-etf-fund-fact-sheet-en-us.pdf)

Collected UTC: 2026-11-17T17:40:31.429827+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: IWM iShares Russell 2000 ETF Fact Sheet as of September 30, 2026 FUND DESCRIPTION The iShares Russell 2000 ETF seeks to track the Russell 2000 Index. The fund offers broad exposure to U.S.small-cap stocks. GROWTH OF HYPOTHETICAL $10,000 SINCE INCEPTION Fund (U

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 464287655 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | Russell 2000 Index |  | 2026-09-30 |
| fee | 0.19 | percent per year; Expense Ratio | 2026-09-30 |
| net_assets | $78,041.73 FEE | million; currency as printed, $ not silently treated as USD | 2026-09-30 |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Quarterly |  | 2026-09-30 |
| composition | TOP HOLDINGS (%) TWIST BIOSCIENCE 0.43% BLK CSH FND TREASURY SL AGENCY 0.38% MOOG INC CLASS A 0.37% JFROG 0.36% 10X GENOMICS CLASS A 0.36% UMB FINANCIAL 0.32% BRIGHTSPRING HEALTH SERVICES INC 0.32% GLAUKOS 0.32% VIASAT INC 0.30% HUT CORP 0.30% Total of Portfolio 3.46% | partial weights in percent; never complete overlap | 2026-09-30 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | 30 Day SEC Yield : 1.18% | source label; yield unit unresolved if % absent | 2026-09-30 |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ishares.com/us/literature/fact-sheet/iwm-ishares-russell-2000-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:40:31.429827+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/IWM-17.pdf`

## BND

Source: [issuer document](https://fund-docs.vanguard.com/F0928.pdf)

Collected UTC: 2026-11-17T17:40:29.827787+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard Total Bond Market ETF | BND As of September 30, 2026 Investment approach • Seeks to track the performance of the Bloomberg U.S. Aggregate Float Adjusted Index. • Passively managed using index sampling. • Broad exposure to the taxable investm

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 921937835 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | Bloomberg U.S. Aggregate Float Adjusted Index |  | 2026-09-30 |
| fee | 0.03 | percent per year; Expense ratio 1 | unresolved |
| net_assets | $389,338 million | USD million ($ source notation) | 2026-09-30 |
| share_assets | $161,442 million | USD million; ETF shares, not whole fund | 2026-09-30 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Monthly |  | 2026-09-30 |
| composition | Distibution by effective maturity Under 1 Year 0.2 % 1 - 5 Years 42.8 % 5 - 10 Years 36.0 % 10 - 15 Years 5.1 % 15 - 20 Years 5.3 % 20 - 25 Years 4.0 % Over 25 Years 6.6 % | partial holdings or aggregate weights in percent | 2026-09-30 |
| duration | Average duration 5 5.7 years | years | 2026-09-30 |
| maturity | Average effective maturity 6 8.3 years | years | 2026-09-30 |
| yield | MISSING / unresolved |  |  |
| credit_quality | Distribution by credit quality 2 U.S. Government 69.0 % AAA 3.1 % AA 3.6 % A 12.0 % BBB 12.2 % BB 0.0 % B 0.0 % CCC or Lower 0.0 % Not rated 0.0 % | rating bucket weights in percent | 2026-09-30 |

- Fee refers to most recent prospectus; effective date not established by factsheet date.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/F0928.pdf) — 2026-11-17T17:40:29.827787+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/BND-16.pdf`

## AGG

Source: [issuer document](https://www.ishares.com/us/literature/fact-sheet/agg-ishares-core-u-s-aggregate-bond-etf-fund-fact-sheet-en-us.pdf)

Collected UTC: 2026-11-17T17:41:36.941756+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: AGG iShares Core U.S. Aggregate Bond ETF Fact Sheet as of September 30, 2026 FUND DESCRIPTION The iShares Core U.S. Aggregate Bond ETF seeks to track an index that includes U.S. investment-grade bonds. The fund offers a way to gain broad exposure to the total

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 464287226 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | Bloomberg US Aggregate Bond Index |  | 2026-09-30 |
| fee | 0.03 | percent per year; Expense Ratio | 2026-09-30 |
| net_assets | $135,651.66 FEE | million; currency as printed, $ not silently treated as USD | 2026-09-30 |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Monthly |  | 2026-09-30 |
| composition | TOP HOLDINGS (%) BLACKROCK CASH CL INST SL AGENCY 2.93% TREASURY NOTE 0.40% TREASURY NOTE 0.40% TREASURY NOTE (OLD) 0.40% TREASURY NOTE 0.40% TREASURY NOTE 0.40% TREASURY NOTE 0.39% TREASURY NOTE 0.39% TREASURY NOTE 0.38% TREASURY NOTE 0.38% Total of Portfolio 6.47% | partial weights in percent; never complete overlap | 2026-09-30 |
| duration | Effective Duration : 5.71 yrs | years | 2026-09-30 |
| maturity | Weighted Avg Maturity : 8.21 yrs | years | 2026-09-30 |
| yield | 30 Day SEC Yield : 5.04% | source label; yield unit unresolved if % absent | 2026-09-30 |
| credit_quality | CREDIT RATINGS (%) Fund Cash and/or Derivatives 0.81 AAA Rated 2.21 AA Rated 73.62 A Rated 11.84 BBB Rated 11.52 BB Rated 0.00 B Rated 0.00 Not Rated 0.00 | rating bucket weights in percent | 2026-09-30 |


Attempts:

- [factsheet](https://www.ishares.com/us/literature/fact-sheet/agg-ishares-core-us-aggregate-bond-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:40:32.880714+00:00; HTTP 404; HTTPError: HTTP Error 404: Not Found; raw `issuers-20261117T174001860718Z/AGG-18-error.html`
- [factsheet](https://www.ishares.com/us/literature/fact-sheet/agg-ishares-core-us-aggregate-bond-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:41:30.418826+00:00; HTTP 404; HTTPError: HTTP Error 404: Not Found; raw `issuers-20261117T174127895555Z/AGG-18-error.html`
- [factsheet](https://www.ishares.com/us/literature/fact-sheet/agg-ishares-core-u-s-aggregate-bond-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:41:36.941756+00:00; HTTP 200; saved; raw `issuers-20261117T174127895555Z/AGG-24.pdf`

## SHY

Source: [issuer document](https://www.ishares.com/us/literature/fact-sheet/shy-ishares-1-3-year-treasury-bond-etf-fund-fact-sheet-en-us.pdf)

Collected UTC: 2026-11-17T17:40:34.177162+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: SHY iShares 1-3 Year Treasury Bond ETF Fact Sheet as of September 30, 2026 FUND DESCRIPTION The iShares 1-3 Year Treasury Bond ETF seeks to track an index that includes U.S. Treasury bonds with remaining maturities between one and three years. The fund offers

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 464287457 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | ICE U.S. Treasury 1-3 Year Bond Index |  | 2026-09-30 |
| fee | 0.15 | percent per year; Expense Ratio | 2026-09-30 |
| net_assets | $26,281.54 FEE | million; currency as printed, $ not silently treated as USD | 2026-09-30 |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Monthly |  | 2026-09-30 |
| composition | TOP HOLDINGS (%) TREASURY NOTE 2.10% TREASURY NOTE 1.99% TREASURY NOTE 1.82% TREASURY NOTE 1.73% TREASURY NOTE 1.62% TREASURY NOTE 1.53% TREASURY NOTE 1.50% TREASURY NOTE 1.48% TREASURY NOTE 1.41% TREASURY NOTE 1.39% Total of Portfolio 16.57% | partial weights in percent; never complete overlap | 2026-09-30 |
| duration | Effective Duration : 1.84 yrs | years | 2026-09-30 |
| maturity | Weighted Avg Maturity : 1.95 yrs | years | 2026-09-30 |
| yield | 30 Day SEC Yield : 4.53% | source label; yield unit unresolved if % absent | 2026-09-30 |
| credit_quality | CREDIT RATINGS (%) Fund Cash and/or Derivatives 0.53 AA Rated 99.47 | rating bucket weights in percent | 2026-09-30 |


Attempts:

- [factsheet](https://www.ishares.com/us/literature/fact-sheet/shy-ishares-1-3-year-treasury-bond-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:40:34.177162+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/SHY-19.pdf`

## TIP

Source: [issuer document](https://www.ishares.com/us/literature/fact-sheet/tip-ishares-tips-bond-etf-fund-fact-sheet-en-us.pdf)

Collected UTC: 2026-11-17T17:40:35.472402+00:00

Source dates: `{"document": "2026-09-30", "composition": "2026-09-30", "other": "2026-09-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: TIP iShares TIPS Bond ETF Fact Sheet as of September 30, 2026 FUND DESCRIPTION The iShares TIPS Bond ETF seeks to track an index that includes U.S. Treasury inflation-protected securities. The fund offers a way to potentially hedge against inflation and divers

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 464287176 | CUSIP | 2026-09-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | ICE U.S. Treasury Inflation Linked Bond Index |  | 2026-09-30 |
| fee | 0.18 | percent per year; Expense Ratio | 2026-09-30 |
| net_assets | $14,229.89 FEE | million; currency as printed, $ not silently treated as USD | 2026-09-30 |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Monthly |  | 2026-09-30 |
| composition | TOP HOLDINGS (%) TREASURY (CPI) NOTE 4.05% TREASURY (CPI) NOTE 3.98% TREASURY (CPI) NOTE 3.97% TREASURY (CPI) NOTE 3.74% TREASURY (CPI) NOTE 3.44% TREASURY (CPI) NOTE 3.42% TREASURY (CPI) NOTE 3.42% TREASURY (CPI) NOTE 3.33% TREASURY (CPI) NOTE 3.23% TREASURY (CPI) NOTE 3.22% Total of Portfolio 35.80% | partial weights in percent; never complete overlap | 2026-09-30 |
| duration | Effective Duration : 6.18 yrs | years | 2026-09-30 |
| maturity | Weighted Avg Maturity : 7.02 yrs | years | 2026-09-30 |
| yield | 30 Day SEC Yield : 2.23% | source label; yield unit unresolved if % absent | 2026-09-30 |
| credit_quality | CREDIT RATINGS (%) Fund Cash and/or Derivatives 0.00 AA Rated 100.00 | rating bucket weights in percent | 2026-09-30 |


Attempts:

- [factsheet](https://www.ishares.com/us/literature/fact-sheet/tip-ishares-tips-bond-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:40:35.472402+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/TIP-20.pdf`

## LQD

Source: [issuer document](https://www.ishares.com/us/literature/fact-sheet/lqd-ishares-iboxx-investment-grade-corporate-bond-etf-fund-fact-sheet-en-us.pdf)

Collected UTC: 2026-11-17T17:40:36.573243+00:00

Source dates: `{"document": "2026-06-30", "composition": "2026-06-30", "other": "2026-06-30", "statements": []}`

Listing: US ticker header plus source identifier; no exchange-independent legal verification

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: LQD iShares iBoxx $ Investment Grade Corporate Bond ETF Fact Sheet as of June 30, 2026 FUND DESCRIPTION The iShares iBoxx $ Investment Grade Corporate Bond ETF seeks to track an index that includes U.S. dollar-denominated investment grade corporate bonds. The

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | 464287242 | CUSIP | 2026-06-30 |
| legal_entity | MISSING / unresolved |  |  |
| benchmark | Markit iBoxx USD Liquid Investment Grade Index |  | 2026-06-30 |
| fee | 0.14 | percent per year; Expense Ratio | 2026-06-30 |
| net_assets | $33,113.14 FEE | million; currency as printed, $ not silently treated as USD | 2026-06-30 |
| share_assets | MISSING / unresolved |  |  |
| base_currency | MISSING / unresolved |  |  |
| share_currency | MISSING / unresolved |  |  |
| hedging | MISSING / unresolved |  |  |
| distribution | Monthly |  | 2026-06-30 |
| composition | TOP HOLDINGS (%) BLK CSH FND TREASURY SL AGENCY 0.86% USD CASH 0.50% ANHEUSER-BUSCH COMPANIES LLC 0.18% META PLATFORMS INC 0.16% CVS HEALTH CORP 0.16% T-MOBILE USA INC 0.15% AMAZON.COM INC 0.14% GOLDMAN SACHS GROUP INC/THE 0.14% META PLATFORMS INC 0.14% META PLATFORMS INC 0.14% Total of Portfolio 2.57% | partial weights in percent; never complete overlap | 2026-06-30 |
| duration | Effective Duration : 7.92 yrs | years | 2026-06-30 |
| maturity | Weighted Avg Maturity : 12.89 yrs | years | 2026-06-30 |
| yield | 30 Day SEC Yield : 5.24% | source label; yield unit unresolved if % absent | 2026-06-30 |
| credit_quality | CREDIT RATINGS (%) Fund Cash and/or Derivatives 1.36 AAA Rated 0.99 AA Rated 11.09 A Rated 46.33 BBB Rated 40.23 | rating bucket weights in percent | 2026-06-30 |


Attempts:

- [factsheet](https://www.ishares.com/us/literature/fact-sheet/lqd-ishares-iboxx-investment-grade-corporate-bond-etf-fund-fact-sheet-en-us.pdf) — 2026-11-17T17:40:36.573243+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/LQD-21.pdf`

## VWCE.DE

Source: [issuer document](https://fund-docs.vanguard.com/FTSE_All-World_UCITS_ETF_USD_Accumulating_9679_EU_INT_UK_EN.pdf)

Collected UTC: 2026-11-17T17:40:01.862395+00:00

Source dates: `{"document": "2026-10-31", "composition": "2026-10-31", "other": "2026-10-31", "statements": ["Data as at 31 October 2026", "Data as at 31 October 2026", "Data as at 30 September 2026"]}`

Listing: Exact listing code appears in issuer document: VWCE.DE

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard FTSE All-World UCITS ETF (USD) Accumulating - An exchange-traded fund Inception date: 23 July 2019 Total assets (million) $88,844 | Share class assets (million) $62,185 as at 31 October 2026 Key ETF facts Exchange ticker SEDOL Reuters Bloomb

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00BK5BQT80 | ISIN | 2026-10-31 |
| legal_entity | Vanguard Funds plc |  | 2026-10-31 |
| benchmark | FTSE All-World Index |  | 2026-10-31 |
| fee | 0.14 | percent per year; Ongoing Charges Figure† | 2026-10-31 |
| net_assets | $88,844 | million; currency symbol as printed | 2026-10-31 |
| share_assets | $62,185 | million; share class, currency symbol as printed | 2026-10-31 |
| base_currency | USD |  | 2026-10-31 |
| share_currency | USD |  | 2026-10-31 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulated |  | 2026-10-31 |
| composition | Top 10 holdings Apple Inc. 4.8% NVIDIA Corp. 4.6 Microsoft Corp. 3.7 Alphabet Inc. 2.8 Amazon.com Inc. 2.3 Taiwan Semiconductor Manufacturing Co. Ltd. 1.7 Broadcom Inc. 1.5 Meta Platforms Inc. 1.3 Tesla Inc. 1.1 Eli Lilly & Co. 1.1 Top 10 approximately equals 24.9% of net assets | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Conflicting section dates; do not assign the document date to every characteristic. See dated assessment and raw PDF.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/FTSE_All-World_UCITS_ETF_USD_Accumulating_9679_EU_INT_UK_EN.pdf) — 2026-11-17T17:40:01.862395+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/VWCE.DE-0.pdf`

## SXR8.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/cspx-ishares-core-s-p-500-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:04.152336+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: SXR8.DE

Automatically mapped listing currency: EUR

Header: PASSIVE SXR8 iShares Core S&P 500 UCITS ETF U.S. Dollar (Accumulating) iShares VII plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is marketi

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00B5BMR087 | ISIN | 2026-11-06 |
| legal_entity | iShares VII plc |  | 2026-11-06 |
| benchmark | S&P 500 Index |  | 2026-11-06 |
| fee | 0.07 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 156,934.33 USD | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 153,792.74 USD | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | USD |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulating |  | 2026-11-06 |
| composition | Top 10 Holdings APPLE 7.70% NVIDIA 7.58% MICROSOFT 5.93% AMAZON.COM INC 3.61% ALPHABET CLASS A 2.51% BROADCOM INC 2.37% META PLATFORMS CLASS A 2.08% ALPHABET CLASS C 2.02% ELI LILLY 1.74% TESLA INC 1.72% Total of Portfolio 37.26% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/cspx-ishares-core-s-p-500-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:04.152336+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/SXR8.DE-2.pdf`
- [holdings](https://www.ishares.com/uk/individual/en/products/253743/ishares-sp-500-b-ucits-etf-acc-fund/latest-holdings.csv) — 2026-11-17T17:46:13.959165+00:00; HTTP 400; HTTPError: HTTP Error 400: Bad Request; raw `issuers-20261117T174613957126Z/SXR8.DE-29-error.html`

## EUNL.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/swda-ishares-core-msci-world-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:08.243906+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: EUNL.DE

Automatically mapped listing currency: EUR

Header: PASSIVE EUNL iShares Core MSCI World UCITS ETF U.S. Dollar (Accumulating) iShares III plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is mark

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00B4L5Y983 | ISIN | 2026-11-06 |
| legal_entity | iShares III plc |  | 2026-11-06 |
| benchmark | MSCI World Index (Net) |  | 2026-11-06 |
| fee | 0.2 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 150,680.95 USD | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 146,648.56 USD | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | USD |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulating |  | 2026-11-06 |
| composition | Top 10 Holdings APPLE 5.62% NVIDIA 5.23% MICROSOFT 4.09% AMAZON.COM INC 2.59% ALPHABET CLASS A 1.82% BROADCOM INC 1.64% META PLATFORMS CLASS A 1.50% ALPHABET CLASS C 1.45% TESLA INC 1.27% ELI LILLY 1.26% Total of Portfolio 26.47% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/swda-ishares-core-msci-world-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:08.243906+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/EUNL.DE-4.pdf`

## IS3N.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/eimi-ishares-core-msci-em-imi-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:09.998739+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: IS3N.DE

Automatically mapped listing currency: EUR

Header: PASSIVE IS3N iShares Core MSCI EM IMI UCITS ETF U.S. Dollar (Accumulating) iShares plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is marketi

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00BKM4GZ66 | ISIN | 2026-11-06 |
| legal_entity | iShares plc |  | 2026-11-06 |
| benchmark | MSCI Emerging Markets Investable Market Index (USD) (Net) |  | 2026-11-06 |
| fee | 0.18 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 43,355.63 USD | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 41,768.87 USD | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | USD |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulating |  | 2026-11-06 |
| composition | Top 10 Holdings TAIWAN SEMICONDUCTOR MANUFACTURING 13.90% SAMSUNG ELECTRONICS LTD 6.11% SK HYNIX 4.55% TENCENT HOLDINGS 2.33% ALIBABA GROUP HOLDING 1.60% MEDIATEK 1.35% CHINA CONSTRUCTION BANK CORP H 0.85% SAMSUNG ELECTRONICS NON VOTING PRE 0.81% HON HAI PRECISION INDUSTRY 0.72% HDFC BANK 0.64% Total of Portfolio 32.86% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/eimi-ishares-core-msci-em-imi-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:09.998739+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/IS3N.DE-5.pdf`

## IUSN.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/wsml-ishares-msci-world-small-cap-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:12.222462+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: IUSN.DE

Automatically mapped listing currency: EUR

Header: PASSIVE IUSN iShares MSCI World Small Cap UCITS ETF U.S. Dollar (Accumulating) iShares III plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00BF4RFH31 | ISIN | 2026-11-06 |
| legal_entity | iShares III plc |  | 2026-11-06 |
| benchmark | MSCI World Small Cap Index (Net) |  | 2026-11-06 |
| fee | 0.35 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 8,956.62 USD | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 8,956.62 USD | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | USD |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulating |  | 2026-11-06 |
| composition | Top 10 Holdings MODERNA 0.72% TENET HEALTHCARE CORP 0.22% US FOODS HOLDING 0.22% USD CASH 0.21% GUARDANT HEALTH 0.21% VIATRIS 0.21% ROKU CLASS A 0.20% OVINTIV 0.19% RUBRIK CLASS A 0.19% ROYAL GOLD 0.18% Total of Portfolio 2.55% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/wsml-ishares-msci-world-small-cap-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:12.222462+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/IUSN.DE-6.pdf`

## SXRV.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/csndx-ishares-nasdaq-100-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:14.063584+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: SXRV.DE

Automatically mapped listing currency: EUR

Header: PASSIVE SXRV iShares NASDAQ 100 UCITS ETF U.S. Dollar (Accumulating) iShares VII plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is marketing

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00B53SZB19 | ISIN | 2026-11-06 |
| legal_entity | iShares VII plc |  | 2026-11-06 |
| benchmark | NASDAQ 100 Index |  | 2026-11-06 |
| fee | 0.3 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 30,027.37 USD | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 28,010.18 USD | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | USD |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulating |  | 2026-11-06 |
| composition | Top 10 Holdings APPLE 8.18% NVIDIA 8.02% MICROSOFT 6.30% MICRON TECHNOLOGY 4.49% AMAZON.COM INC 4.21% ADVANCED MICRO DEVICES 3.70% TESLA INC 3.42% META PLATFORMS CLASS A 2.98% WALMART 2.70% ALPHABET CLASS A 2.67% Total of Portfolio 46.67% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |


Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/csndx-ishares-nasdaq-100-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:14.063584+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/SXRV.DE-7.pdf`

## EXSA.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/exsa-ishares-stoxx-europe-600-ucits-etf-de-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:15.891152+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Unresolved

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: PASSIVE EXSA iShares STOXX Europe 600 UCITS ETF (DE) Euro (Distributing) Germany iShares October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is marke

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | DE0002635307 | ISIN | 2026-11-06 |
| legal_entity | BlackRock Asset Management Deutschland AG |  | 2026-11-06 |
| benchmark | STOXX Europe 600 Index (EUR) |  | 2026-11-06 |
| fee | 0.2 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 10,573.02 EUR | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 9,605.92 EUR | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | EUR |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Distributing; Up to 4x per year |  | 2026-11-06 |
| composition | Top 10 Holdings ASML HOLDING 4.07% ROCHE PS PAR AG 2.29% NOVARTIS AG 2.05% SHELL 2.00% HSBC HOLDINGS PLC 1.95% ASTRAZENECA PLC 1.93% NESTLE SA 1.76% SAP 1.58% SIEMENS N AG 1.45% TOTALENERGIES 1.45% Total of Portfolio 20.53% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Not applicable to equity sample intention |  |  |
| maturity | Not applicable to equity sample intention |  |  |
| yield | MISSING / unresolved |  |  |
| credit_quality | Not applicable to equity sample intention |  |  |

- Exact Yahoo listing code absent; review issuer ticker, exchange and currency table. No automatic identity match.

Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/exsa-ishares-stoxx-europe-600-ucits-etf-de-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:15.891152+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/EXSA.DE-8.pdf`

## VAGF.DE

Source: [issuer document](https://fund-docs.vanguard.com/Global_Aggregate_Bond_UCITS_ETF_EUR_Hedged_Accumulating_9443_EU_INT_UK_EN.pdf)

Collected UTC: 2026-11-17T17:40:03.002727+00:00

Source dates: `{"document": "2026-10-31", "composition": "2026-10-31", "other": "2026-10-31", "statements": ["Data as at 31 October 2026", "Data as at 30 September 2026"]}`

Listing: Exact listing code appears in issuer document: VAGF.DE

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: Vanguard® Vanguard Global Aggregate Bond UCITS ETF EUR Hedged Accumulating - An exchange-traded fund Inception date: 18 June 2019 Total assets (million) €5,970 | Share class assets (million) €2,422 as at 31 October 2026 Key ETF facts Exchange ticker SEDOL Reut

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00BG47KH54 | ISIN | 2026-10-31 |
| legal_entity | Vanguard Funds plc |  | 2026-10-31 |
| benchmark | Bloomberg Global Aggregate Float Adjusted and Scaled Index in EUR |  | 2026-10-31 |
| fee | 0.08 | percent per year; Ongoing Charges Figure† | 2026-10-31 |
| net_assets | €5,970 | million; currency symbol as printed | 2026-10-31 |
| share_assets | €2,422 | million; share class, currency symbol as printed | 2026-10-31 |
| base_currency | USD |  | 2026-10-31 |
| share_currency | EUR |  | 2026-10-31 |
| hedging | EUR hedged |  | 2026-10-31 |
| distribution | Accumulated |  | 2026-10-31 |
| composition | Market allocation United States 47.3% Japan 5.8 France 5.6 Germany 5.3 United Kingdom 4.6 Canada 4.0% Italy 3.7 Supranational 3.3 Spain 2.6 Australia 2.0 | aggregate market weights in percent | unresolved |
| duration | Average duration 6.0 years | years | unresolved |
| maturity | Average maturity 8.2 years | years | unresolved |
| yield | Yield to worst 4.66% | source label; yield unit unresolved if % absent | unresolved |
| credit_quality | Average quality AA- | rating | unresolved |

- Conflicting section dates; do not assign the document date to every characteristic. See dated assessment and raw PDF.

Attempts:

- [factsheet](https://fund-docs.vanguard.com/Global_Aggregate_Bond_UCITS_ETF_EUR_Hedged_Accumulating_9443_EU_INT_UK_EN.pdf) — 2026-11-17T17:40:03.002727+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/VAGF.DE-1.pdf`

## EUNA.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/aggh-ishares-core-global-aggregate-bond-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:06.140864+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: EUNA.DE

Automatically mapped listing currency: EUR

Header: PASSIVE AGGH iShares Core Global Aggregate Bond UCITS ETF Hedged Euro (Accumulating) iShares III plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This docum

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00BDBRDM35 | ISIN | 2026-11-06 |
| legal_entity | iShares III plc |  | 2026-11-06 |
| benchmark | Bloomberg Global Aggregate Bond Index |  | 2026-11-06 |
| fee | 0.1 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 14,565.57 USD | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 2,650.65 EUR | million; share class | 2026-10-31 |
| base_currency | USD |  | 2026-11-06 |
| share_currency | EUR |  | 2026-11-06 |
| hedging | EUR hedged |  | 2026-11-06 |
| distribution | Accumulating |  | 2026-11-06 |
| composition | TOP ISSUERS UNITED STATES TREASURY 19.30% JAPAN (GOVERNMENT OF) 7.58% CHINA PEOPLES REPUBLIC OF (GOVERNMENT) 6.70% FEDERAL NATIONAL MORTGAGE ASSOCIATION 3.00% FEDERAL HOME LOAN MORTGAGE CORPORATION 2.86% UK CONV GILT 2.59% FRANCE (REPUBLIC OF) 2.51% ITALY (REPUBLIC OF) 2.50% CHINA DEVELOPMENT BANK 2.36% GOVERNMENT NATIONAL MORTGAGE ASSOCIATION II 2.29% Total of Portfolio 51.69% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Effective Duration : 6.06 yrs | years | 2026-11-06 |
| maturity | Average Weighted Maturity : 8.08 yrs | years | 2026-11-06 |
| yield | Yield to Worst : 4.27 | source label; yield unit unresolved if % absent | 2026-11-06 |
| credit_quality | MISSING / unresolved |  |  |

- Credit chart exists; numeric rating weights not recovered by text extractor. Manual/chart or separate download route needed.
- Yield to Worst lacks a printed % sign in extracted value; retained raw, not normalized against YTM/SEC yield.

Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/aggh-ishares-core-global-aggregate-bond-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:06.140864+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/EUNA.DE-3.pdf`
- [holdings](https://www.ishares.com/uk/individual/en/products/291770/ishares-core-global-aggregate-bond-ucits-etf-aggh-hedged/latest-holdings.csv) — 2026-11-17T17:46:15.302761+00:00; HTTP 400; HTTPError: HTTP Error 400: Bad Request; raw `issuers-20261117T174613957126Z/EUNA.DE-30-error.html`

## IBGS.AS

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/ibgs-ishares-govt-bond-1-3yr-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:17.791992+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: IBGS.AS

Automatically mapped listing currency: EUR

Header: PASSIVE IBCA iShares € Govt Bond 1-3yr UCITS ETF Euro (Distributing) iShares plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is marketing mat

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00B14X4Q57 | ISIN | 2026-11-06 |
| legal_entity | iShares plc |  | 2026-11-06 |
| benchmark | BBG EU Term 1-3 Year Index (EUR) |  | 2026-11-06 |
| fee | 0.1 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 1,744.53 EUR | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 1,742.02 EUR | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | EUR |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Distributing; Semi-Annual |  | 2026-11-06 |
| composition | TOP ISSUERS GERMANY (FEDERAL REPUBLIC OF) 32.19% ITALY (REPUBLIC OF) 28.08% FRANCE (REPUBLIC OF) 25.64% SPAIN (KINGDOM OF) 14.03% Total of Portfolio 99.94% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Effective Duration : 1.88 yrs | years | 2026-11-06 |
| maturity | Average Weighted Maturity : 1.95 yrs | years | 2026-11-06 |
| yield | Yield to Worst : 3.36 | source label; yield unit unresolved if % absent | 2026-11-06 |
| credit_quality | MISSING / unresolved |  |  |

- Credit chart exists; numeric rating weights not recovered by text extractor. Manual/chart or separate download route needed.
- Yield to Worst lacks a printed % sign in extracted value; retained raw, not normalized against YTM/SEC yield.

Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/ibgs-ishares-govt-bond-1-3yr-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:17.791992+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/IBGS.AS-9.pdf`

## IEAC.AS

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/ieac-ishares-core-corp-bond-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:40:19.629797+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Exact listing code appears in issuer document: IEAC.AS

Automatically mapped listing currency: EUR

Header: PASSIVE EUN5 iShares Core € Corp Bond UCITS ETF Euro (Distributing) iShares III plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is marketing

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00B3F81R35 | ISIN | 2026-11-06 |
| legal_entity | iShares III plc |  | 2026-11-06 |
| benchmark | BBG Euro Corporate Index (EUR) |  | 2026-11-06 |
| fee | 0.09 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 14,390.61 EUR | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 9,519.16 EUR | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | EUR |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Distributing; Semi-Annual |  | 2026-11-06 |
| composition | TOP ISSUERS BANQUE FEDERATIVE DU CREDIT MUTUEL SA 1.45% BNP PARIBAS SA 1.33% BPCE SA 1.12% ING GROEP NV 1.12% CREDIT AGRICOLE SA 1.09% ORANGE SA 0.95% SOCIETE GENERALE SA 0.94% ENGIE SA 0.91% BANCO SANTANDER SA 0.88% GOLDMAN SACHS GROUP INC/THE 0.86% Total of Portfolio 10.65% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Effective Duration : 4.37 yrs | years | 2026-11-06 |
| maturity | Average Weighted Maturity : 5.16 yrs | years | 2026-11-06 |
| yield | Yield to Worst : 4.20 | source label; yield unit unresolved if % absent | 2026-11-06 |
| credit_quality | MISSING / unresolved |  |  |

- Credit chart exists; numeric rating weights not recovered by text extractor. Manual/chart or separate download route needed.
- Yield to Worst lacks a printed % sign in extracted value; retained raw, not normalized against YTM/SEC yield.

Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/ieac-ishares-core-corp-bond-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:19.629797+00:00; HTTP 200; saved; raw `issuers-20261117T174001860718Z/IEAC.AS-10.pdf`

## IBCI.DE

Source: [issuer document](https://www.ishares.com/gls-download/literature/fact-sheet/ibci-ishares-eur-inflation-linked-govt-bond-ucits-etf-fund-fact-sheet-en-de.pdf)

Collected UTC: 2026-11-17T17:41:38.194164+00:00

Source dates: `{"document": null, "composition": "2026-10-31", "other": "2026-11-06", "statements": ["as at: 31-Oct-2026", "data as at 06-Nov-2026"]}`

Listing: Unresolved

Automatically mapped listing currency: unresolved; see source table/manual assessment

Header: PASSIVE IBCI iShares EUR Inflation Linked Govt Bond UCITS ETF Euro (Accumulating) iShares plc October 2026 Performance, Portfolio Breakdowns, Net Assets, and Distribution Yield information as at: 31-Oct-2026. All other data as at 06-Nov-2026. This document is

| Field | Source value | Unit / scope | Observation date |
|---|---|---|---|
| identifier | IE00B0M62X26 | ISIN | 2026-11-06 |
| legal_entity | iShares plc |  | 2026-11-06 |
| benchmark | BBG Euro Government Inflation-Linked Bond Index (EUR) |  | 2026-11-06 |
| fee | 0.09 | percent per year; Total Expense Ratio : | 2026-11-06 |
| net_assets | 1,817.05 EUR | million; currency as printed, $ not silently treated as USD | 2026-10-31 |
| share_assets | 1,817.05 EUR | million; share class | 2026-10-31 |
| base_currency | MISSING / unresolved |  |  |
| share_currency | EUR |  | 2026-11-06 |
| hedging | MISSING / unresolved |  |  |
| distribution | Accumulating |  | 2026-11-06 |
| composition | TOP ISSUERS FRANCE (REPUBLIC OF) 40.36% ITALY (REPUBLIC OF) 34.28% SPAIN (KINGDOM OF) 16.09% GERMANY (FEDERAL REPUBLIC OF) 9.21% Total of Portfolio 99.94% | partial weights in percent; never complete overlap | 2026-10-31 |
| duration | Effective Duration : 7.01 yrs | years | 2026-11-06 |
| maturity | Average Weighted Maturity : 7.63 yrs | years | 2026-11-06 |
| yield | Weighted Avg YTM : 4.04% | source label; yield unit unresolved if % absent | 2026-11-06 |
| credit_quality | MISSING / unresolved |  |  |

- Exact Yahoo listing code absent; review issuer ticker, exchange and currency table. No automatic identity match.
- Credit chart exists; numeric rating weights not recovered by text extractor. Manual/chart or separate download route needed.

Attempts:

- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/ibci-ishares-inflation-linked-govt-bond-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:40:21.377090+00:00; HTTP 200; ValueError: Expected PDF, received non-PDF response; no coverage credited; raw `issuers-20261117T174001860718Z/IBCI.DE-11.html`
- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/ibci-ishares-inflation-linked-govt-bond-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:41:27.897843+00:00; HTTP 200; ValueError: Expected PDF, received non-PDF response; no coverage credited; raw `issuers-20261117T174127895555Z/IBCI.DE-11.html`
- [factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/ibci-ishares-eur-inflation-linked-govt-bond-ucits-etf-fund-fact-sheet-en-de.pdf) — 2026-11-17T17:41:38.194164+00:00; HTTP 200; saved; raw `issuers-20261117T174127895555Z/IBCI.DE-25.pdf`
- [product](https://www.ishares.com/uk/individual/en/products/251739/ishares-inflation-linked-govt-bond-ucits-etf) — 2026-11-17T17:41:42.690447+00:00; HTTP 200; saved; raw `issuers-20261117T174127895555Z/IBCI.DE-28.html`
- [holdings](https://www.ishares.com/uk/individual/en/products/251739/ishares-eur-inflation-linked-govt-bond-ucits-etf/latest-holdings.csv) — 2026-11-17T17:46:16.180903+00:00; HTTP 400; HTTPError: HTTP Error 400: Bad Request; raw `issuers-20261117T174613957126Z/IBCI.DE-31-error.html`
