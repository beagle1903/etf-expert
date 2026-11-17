# Official issuer supplementation — 17 November 2026

## Decision: change the route before scaling

Official sources materially supplement Yahoo across this diagnostic sample.
They do **not** yet establish a complete, consistently dated, unattended or
licensed data route. Continue source-linked manual research if useful; change
the collection/access approach before claiming broader automated coverage.
No portfolio construction or selection readiness is established. No subsequent
issue was started.

All 24 original listings remain in the report: 12 US and 12 EU, including five
bond research intentions in each group. These are diagnostic listings, not a
fixed app universe, 24 independent exposures, or an eligible investment pool.

## Live observations

The first probes were VWCE.DE, VAGF.DE, SXR8.DE and EUNA.DE. All four official
factsheets returned HTTP 200 PDFs. The first extraction attempt failed because
the PDF page object did not support the context-manager pattern used. Explicit
resource closing fixed the implementation; that failed run remains local.

The route was then tried across all 24. The complete first pass took 40.5 seconds
(24 HTTP attempts, 7,747,736 saved response bytes, including failed/non-PDF
responses where returned). Follow-up candidates recovered AGG and IBCI factsheets.
The final result is **23 parsed factsheets, plus limited structured identity from
QQQ's product page**. This is one-session availability, not a reliability test.

| Source fact extracted | US / 12 | EU / 12 | Interpretation |
|---|---:|---:|---|
| Identifier | 12 | 12 | 11 US CUSIPs and QQQ ISIN; 12 EU ISINs; source claims, not independent legal verification |
| Benchmark | 11 | 12 | QQQ not recovered by the direct parser |
| Fee with source metric and percent unit | 11 | 12 | OCF, TER and gross expense ratio remain separately labelled |
| Fund net assets | 10 | 12 | Fund and ETF/share-class assets are separate fields; million units retained |
| Share/ETF assets | 5 | 12 | Not assumed equal to fund assets |
| Distribution characteristic | 10 | 12 | SPY and QQQ unresolved in this route; income use differs from payment frequency |
| Some composition weights | 11 | 12 | Top positions, issuers or allocation summaries; incomplete holdings |
| Composition with an unambiguous extracted date | 11 | 11 | VAGF allocation date left unresolved because page statements conflict |
| Explicit fund base currency | 0 | 3 | No substitution from listing, class or performance currency |
| Explicit share-class currency | 0 | 12 | US omissions are limits of these documents/parser, not proof unavailable elsewhere |
| Explicit hedging target | 0 | 2 | VAGF and EUNA EUR hedging; other absences remain unresolved |
| Duration and maturity | 5 / 5 bonds | 5 / 5 bonds | Appropriate bond fields, not universal equity exclusions |
| Yield measure | 4 / 5 bonds | 5 / 5 bonds | BND not recovered; SEC yield, YTM and yield to worst are not interchangeable |
| Numeric credit summary in text | 5 / 5 bonds | 1 / 5 bonds | US bucket weights and VAGF average rating; other EU credit charts need review |

These counts include undated values and source candidates whose Yahoo-code
attribution needs manual review. They are not counts of fully usable records.
IWM also supplies a SEC yield, so the generated all-listing yield-field count
includes that equity fund; the bond-specific count above excludes it.
The [generated field report](issuer-coverage-2026-11-17.md) preserves each missing
field, collection time, source date, source URL and failed attempt.

## Starting four: what the sources actually supply

| Listing | Official source claim | Fee | Currency / income | Composition and bond limits |
|---|---|---|---|---|
| VWCE.DE | Vanguard FTSE All-World UCITS ETF, IE00BK5BQT80; FTSE All-World Index | OCF 0.14% yearly | USD base/class, EUR Deutsche Börse listing; accumulated; hedging not established | October 31 top ten account for about 24.9%; characteristics footnote says September 30 |
| VAGF.DE | Vanguard Global Aggregate Bond UCITS ETF, IE00BG47KH54; Bloomberg Global Aggregate Float Adjusted and Scaled Index in EUR | OCF 0.08% yearly | USD base, EUR hedged accumulating class, EUR listing | Average duration 6.0 years, maturity 8.2 years, yield to worst 4.66%, average quality AA-; October page header and September characteristic footnote conflict |
| SXR8.DE | iShares Core S&P 500 UCITS ETF, IE00B5BMR087; S&P 500 Index | TER 0.07% yearly | USD class, EUR listing; accumulating; base/hedging unresolved | Dated partial top holdings; composition October 31, other facts November 6 |
| EUNA.DE | iShares Core Global Aggregate Bond UCITS ETF, IE00BDBRDM35; Bloomberg Global Aggregate Bond Index | TER 0.10% yearly | USD base, EUR hedged accumulating class, EUR listing | Effective duration 6.06 years and maturity 8.08 years, other-data date November 6; top issuers October 31; credit chart needs manual recovery |

Source PDFs: [VWCE](https://fund-docs.vanguard.com/FTSE_All-World_UCITS_ETF_USD_Accumulating_9679_EU_INT_UK_EN.pdf),
[VAGF](https://fund-docs.vanguard.com/Global_Aggregate_Bond_UCITS_ETF_EUR_Hedged_Accumulating_9443_EU_INT_UK_EN.pdf),
[SXR8](https://www.ishares.com/gls-download/literature/fact-sheet/cspx-ishares-core-s-p-500-ucits-etf-fund-fact-sheet-en-de.pdf),
[EUNA](https://www.ishares.com/gls-download/literature/fact-sheet/aggh-ishares-core-global-aggregate-bond-ucits-etf-fund-fact-sheet-en-de.pdf).
These URLs are mutable; exact retrieved bytes/hashes stay in the local run.

VAGF's yield is based on underlying local currencies; it is not a promised
EUR-hedged investor return. EUNA's printed yield-to-worst value lacks a percent
sign; the report retains it without silently normalizing. Inflation-linked IBCI
prints YTM 4.04% and a separate yield-to-worst value 1.93. Do not infer that
these are equivalent yield concepts or compare them mechanically with SEC yield.

## Dates, identity and extraction findings

- iShares EU sheets distinguish October 31 composition/net assets from November 6
  other facts. Duration/maturity are assigned the latter date. Collection time is
  separate from both. US sheets are mostly September 30; LQD returned June 30.
- Vanguard US fees refer to the most recent prospectus. The replay leaves their
  effective dates unresolved rather than making the factsheet date an effective
  fee date. SPY's header date is September 30; its 0.0945% gross expense ratio is
  a percent value, not a fraction or rounded 0.09%.
- The VTI PDF names a Morningstar US Total Market benchmark while printing the
  CRSPTMT index ticker. This internal naming/ticker tension is preserved, not
  repaired from memory. Corroborate before any benchmark-dependent comparison.
- Exact listing codes appear for 10 EU candidates. EXSA.DE and IBCI.DE require
  ticker/venue review because issuer Reuters codes differ. Visual inspection of
  page 3 confirms Xetra ticker EXSA, EUR, RIC STOXXIEX.DE, and Xetra ticker IBCI,
  EUR, RIC IBEI.DE, respectively. The automatic report deliberately leaves these
  exact-code matches unresolved; neither sample symbol was renamed. SPY's ticker
  is graphical; the rendered header and extracted CUSIP were inspected manually.
- All 12 EU listing tables identify EUR listing currency after the above manual
  reviews and Vanguard table inspection. The parser maps eight directly from
  aligned iShares RIC/currency rows. It leaves the other four for manual review.
- ISIN/CUSIP plus a matching listing helps attribute a source claim. It does not
  verify all legal relationships, establish equal economic exposure across
  classes, or establish independent risk across funds. No exhaustive registry
  was built and no eligibility exclusions were made.
- EUNA and IBCI credit charts visibly contain numeric weights, but the extractor
  loses their labels/numbers. EUNA page 3, for example, shows AAA 11.57%, AA
  38.57%, A 31.30%, BBB 14.02%, not rated 3.99% and cash/derivatives 0.53%.
  These manual observations do not count as automated credit-field recovery.
  No full-holdings overlap can be established from top-ten/top-issuer summaries.

## Failures and practical effort

- AGG's initial `core-us` PDF candidate returned 404; the discovered `core-u-s`
  route returned a PDF. IBCI's initial PDF slug returned HTTP 200 HTML; the
  `eur-inflation-linked` route returned a PDF. Failed candidates remain in the
  manifest and evidence; HTTP 200 is never sufficient PDF success.
- QQQ's legacy content URL and current factsheet link both returned HTML. The
  product HTML exposes ISIN US46090E1038, ticker QQQ and its class name through
  JSON-LD. Its dynamic facts were not available to this direct parser. Search
  snippets were not substituted for a collected source response. Browser/session
  selection or a separately permitted source is still needed; no login,
  impersonation, cookie workaround or anti-bot bypass was attempted.
- Three direct iShares `latest-holdings.csv` probes (SXR8, EUNA and IBCI) returned
  HTTP 400, including the IBCI link observed in the downloaded product page.
  No usable CSV coverage is claimed, and that route was not extended to the
  remaining listings. The factsheet route, however, was attempted across all 24.
- Human work comprised locating issuer URLs, correcting two failed slugs,
  checking listing tables, reading access terms and visually reviewing PDF pages.
  This effort was not separately timed, and there is no measured per-new-fund
  maintenance cost. Automated request timings are in each run. There is no
  established catalogue discovery or unattended refresh process here.
- No account or paid data subscription was used; licensing cost and permission
  for recurring automated access remain unestablished. No new service or
  infrastructure was added. PDF extraction justified one dependency.

## Access and reuse observations

Checked on November 17 during this session; these are operational findings, not
a legal opinion or a blanket licence. Public HTTP access is not reuse permission.

| Issuer/source | Observed restrictions and implication |
|---|---|
| [Vanguard UK terms](https://www.vanguard.co.uk/professional/terms-and-conditions) | Limited personal informational noncommercial licence; redistribution restricted; repeated automated access is restricted. These terms explicitly apply to that website, not every Vanguard entity/site. The two UK-format PDFs also say professional audience only. Applicability/permission for recurring use of fund-docs and US materials is unresolved. |
| [iShares UK terms](https://www.ishares.com/uk/individual/en/compliance/terms-and-conditions) | Personal/internal context and broad copying/redistribution restrictions; country/audience conditions. PDF marketing/copyright notices remain relevant. German/global-download and US site-specific rights were not cleared by reading the UK terms. |
| [State Street US terms](https://www.ssga.com/us/en/footer/terms-and-conditions) | Personal printouts or reasonable internal copies are described; broader transfers restricted. This does not establish permission to republish holdings or operate a data service. |
| [Invesco US terms](https://www.invesco.com/us/en/resources/terms-of-use.html) | Limited access with restrictions on repeated automated access and data-mining tools; no recurring automated QQQ route is cleared. The product page also targets US residents. |

Raw PDFs/HTML, full extracted text, rendered review images and paired JSON stay
local and ignored. The repository contains tooling, source URLs and a factual
coverage assessment, not redistributed source documents. Before a standing
collector or broader distribution, resolve source-specific permission or use a
permitted data supplier; do not treat this experiment as that clearance.

## Reproduction and focused verification

`scripts/check_issuers.py` performs bounded sequential HTTP requests, captures
redirect destinations, status, type, collection times, hashes and failures, and
extracts actual PDF bytes with `pypdfium2` 5.15.2. Python was 3.14.0. It uses the
unchanged universe as its denominator and requires source candidates for every
listing. Subset probes are explicit. `scripts/assess_issuers.py` replays local
responses, including the QQQ structured fallback, without network access.
Commands are in the README.

Local evidence folders:

- `data/runs/issuers-20261117T173946050410Z/`: four initial downloads and extraction errors.
- `data/runs/issuers-20261117T174001860718Z/`: all-24 first pass, 17:40:01–17:40:42 UTC.
- `data/runs/issuers-20261117T174127895555Z/`: eight follow-up attempts, 17:41:27–17:41:44 UTC.
- `data/runs/issuers-20261117T174613957126Z/`: three CSV failures, 17:46:13–17:46:17 UTC; final replay report/JSON.

UTC collection times above correspond to 20:39–20:46 Istanbul. The earlier
Yahoo run `data/runs/20261117T172137188429Z/` is preserved untouched.

Offline verification: ten tests passed (three existing Yahoo tests and seven
issuer tests). They cover field-specific dates and fee units, zero/missing
distinction, prose mistaken for an identifier, absent hedging, conflicting date
statements and duration footnotes, graph headings without numeric evidence,
limited QQQ JSON-LD fallback, HTTP-200 HTML failure, and retention of a missing
candidate in reports. These tests do not establish live source reliability.

Visual review covered VWCE pages 1/3, VAGF pages 1/3, SXR8 page 1, EUNA pages
1/3, VTI page 1, SPY pages 1/2, EXSA page 3 and IBCI page 3. It confirmed
important units, mixed dates, graphical extraction loss and listing-code
differences; it was not independent verification of every source fact.
