# Dated ETF evidence spot check — 18 November 2026

**8 of 8 listings met the existing evidence requirements in a one-off
manual review.** This is the first successful check of the fee and bond-risk
fields across all four groups. The other 32 listings still need verification.
The full-cohort gate remains at least 32 of 40 and at least 8 of 10 per group.
[Original pilot and gate](broader-coverage-2026-11-18.md)

## Morningstar export

Morningstar documents ETF expense ratios, effective duration, portfolio dates,
and credit-quality dates and weights. Its public trial form requests a
professional email address, company, role, business phone and country.
No account-free evaluation export for this cohort was located. No trial was
requested and no Morningstar rows were scored.
[ETF data fields](https://admainnew.morningstar.com/WebHelp/Research/Searches/ETF.htm) ·
[Morningstar Direct trial](https://www.morningstar.com/try/asset-management)

## Issuer-document check

Selected two members of each original group. The US sample includes
fee waivers, and the Xetra bond sample includes two target-maturity
funds with materially different credit exposures. Issuer factsheets
provided the instrument identifier and benchmark or strategy for each.
US listing currency was read from the exact ticker and exchange in the
issuer's listing table. Xetra currency and identity were joined by the
original venue ticker and ISIN. The four bond rows have dates for
both duration and credit. Fee dates below are observations in dated
factsheets. An observation date does not establish the date a fee took effect.

| Group and listing | Identifier and trading venue | Annual fee and observation date | Exposure or benchmark | Sources |
|---|---|---|---|---|
| US equity ACWI | CUSIP 464288257, Nasdaq, USD | Expense ratio 0.32%, 30 Sep | MSCI All Country World Index (Net) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/acwi-ishares-msci-acwi-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239600/ishares-msci-acwi-etf) |
| US equity AQLT | CUSIP 46438G497, Cboe BZX, USD | Gross 0.22%, net 0.20%, 30 Sep | MSCI ACWI Quality Index (Net) | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/aqlt-ishares-msci-global-quality-factor-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/340396/ishares-msci-global-quality-factor-etf) |
| US bonds AGZ | CUSIP 464288166, NYSE Arca, USD | Expense ratio 0.15%, 30 Sep | Bloomberg U.S. Agency Bond Index | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/agz-ishares-agency-bond-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/239457/ishares-agency-bond-etf) |
| US bonds BTOT | CUSIP 46438G240, NYSE Arca, USD | Gross 0.10%, net 0.09%, 30 Sep | Bloomberg US Total Fixed Income Market Index | [Factsheet](https://www.ishares.com/us/literature/fact-sheet/btot-ishares-total-usd-fixed-income-market-etf-fund-fact-sheet-en-us.pdf), [listing](https://www.ishares.com/ch/professionals/en/products/347943/ishares-total-usd-fixed-income-market-etf) |
| Xetra equity 2B7A | IE00B4KBBD01, XETR, EUR | TER 0.15%, 6 Nov | S&P 500 Capped 35/20 Utilities Index NTR | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/iuus-ishares-s-p-500-utilities-sector-ucits-etf-fund-fact-sheet-en-de.pdf) |
| Xetra equity 2B7K | IE00BYX2JD69, XETR, EUR | TER 0.20%, 6 Nov | MSCI World SRI Select Reduced Fossil Fuel Index EUR | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/susw-ishares-msci-world-sri-ucits-etf-fund-fact-sheet-en-de.pdf) |
| Xetra bonds 28IX | IE000Q0UH3Y7, XETR, EUR | TER 0.20%, 5 Nov | Bloomberg MSCI December 2028 Maturity EUR Corporate Crossover ESG Screened Index | [Factsheet](https://www.blackrock.com/gls-download/literature/fact-sheet/28ix-ishares-ibonds-dec-2028-term-corp-crossover-ucits-etf-fund-fact-sheet-en-dk.pdf) |
| Xetra bonds 31IG | IE000I2WYEU9, XETR, EUR | TER 0.12%, 6 Nov | Bloomberg MSCI December 2031 Maturity EUR Corporate ESG Screened Index | [Factsheet](https://www.ishares.com/gls-download/literature/fact-sheet/31ig-ishares-ibonds-dec-2031-term-corp-ucits-etf-fund-fact-sheet-en-de.pdf) |

All observation dates in the tables are in 2026.

| Listing | Effective duration and date | Credit evidence and portfolio date |
|---|---|---|
| AGZ | 3.44 years, 30 Sep | 98.95% AA and 1.05% cash or derivatives, 30 Sep |
| BTOT | 5.29 years, 30 Sep | Credit table includes 61.76% AA and 12.86% BBB, 30 Sep |
| 28IX | 1.48 years, 5 Nov | 42.18% BBB, 41.99% BB, 14.61% B, 0.44% unrated and 0.79% cash or derivatives, 31 Oct |
| 31IG | 4.30 years, 6 Nov | 7.15% AA, 44.81% A, 47.95% BBB and 0.09% cash or derivatives, 31 Oct |

Read the two Xetra credit charts on page 3 of the downloaded PDFs. The
charts sum to 100.01% and 100.00%, respectively, at source precision. The
issuer dates the two charts with its portfolio breakdowns and the two
duration figures with its other data. AQLT's factsheet reports its fee
waiver through 31 December 2029. BTOT reports its waiver through 28 June 2030.

## Access and scale

The eight source PDFs downloaded on 18 November at about 17:55 UTC
(20:55 Istanbul). All returned HTTP 200. The downloaded PDFs and extracted text stay
local in ignored `data/runs/dated-source-check-2026-11-18/`, with the
download URL, timestamps and hashes. The four US listing pages took five
attempts. The abbreviated ACWI URL returned HTTP 403, and the issuer's
full product URL supplied the USD Nasdaq row. The timing of human
document discovery and review was not tracked separately.

The existing factsheet parser extracted eight fees and four duration
figures. It missed the two target-maturity ISINs because it expects
two trailing digits, and missed the two Xetra chart values. The 28IX
BlackRock-hosted document also exposed a parser limitation in benchmark
and duration-date mapping. The manual result uses the printed documents.
It does not depend on the unmerged issuer-feed integration.

The next coverage run should use a permitted evaluation export if one is
available. The public-document route can also extend this check to the
other 32 original listings. Either route needs the same dates, fee
bases, duration method and credit evidence as this check. Retain the
per-listing source and access result. Measure review effort across the
whole cohort before deciding whether a recurring collector is worthwhile.
