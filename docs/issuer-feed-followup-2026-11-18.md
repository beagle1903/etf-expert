# Issuer feed follow-up — 18 November 2026

Two configured iShares screener responses matched all 40 listings in the
[frozen pilot](broader-coverage-2026-11-18.md). The responses add 20 US
share-class identifiers and effective duration for all 20 bonds. They
leave fee and duration dates unresolved and provide no bond credit
breakdowns. The comparison result remains **0 of 40** against the original
threshold of 32 of 40 and 8 of 10 in every group.

## Saved bulk replay

The earlier probes queried the catalogue HTML and unconfigured product-data
URLs. This follow-up read the configuration published with the US and
German screener pages, then queried the data endpoints with those site and
product parameters. The output keeps the exact request URL, collection time
and raw-response hash. The US v3.1 endpoint and the configured German endpoint
each returned a populated product-number map. The US v3 endpoint also
returned data in a different tabular shape. The German spreadsheet URL
returned HTTP 405 to the GET probe. No spreadsheet coverage was credited.
[US screener](https://www.ishares.com/us/products/etf-investments) ·
[German screener](https://www.ishares.com/de/privatanleger/de/produkte/produktliste)

| Evidence | US equity / 10 | US bonds / 10 | Xetra equity / 10 | Xetra bonds / 10 |
|---|---:|---:|---:|---:|
| Joined configured issuer row | 10 | 10 | 10 | 10 |
| Attributable share-class identifier | 10 | 10 | 10 | 10 |
| Raw fee figure | 10 | 10 | 10 | 10 |
| Dated annual fee | 0 | 0 | 0 | 0 |
| Effective duration figure | — | 10 | — | 10 |
| Dated duration and credit | — | 0 | — | 0 |
| Comparison-ready | 0 | 0 | 0 | 0 |

The US join requires the venue ticker and the issuer catalogue product
number. The Xetra join uses the exact venue ISIN, preserving the local ticker
and trading currency from the venue even when the issuer displays another
listing. The maps contain 483 US ticker keys and 867 German ISIN keys after
filtering for issuer ETF rows with identifiers. Only the 40 pilot matches
were verified. The fees and duration in the replay retain the issuer's
display strings and raw figures. NAV, yield or performance dates do not date
the fee or duration. The US feeds still leave US trading currency and an
explicit exposure description unresolved under the pilot rules. Xetra keeps
the earlier secondary benchmark evidence.

The two retained screener requests were collected between 17:24 and 17:26 UTC
(20:24 and 20:26 Istanbul) and took about 45 seconds of summed request time.
They used public catalogue responses without a subscription. One run
establishes that those routes worked at collection time. Refresh reliability,
publisher permission for recurring use and coverage across other issuers
remain unverified.

## Other live probes

- **SEC prospectus data.** The October 2026 risk/return archive adds a
  series/class/ticker table and could help with dated US fees. Its published
  ZIP returned HTTP 403 in this environment. No rows were credited, and the
  archive would still need a separate source for current bond risk.
  [SEC prospectus risk/return data](https://www.sec.gov/data-research/sec-markets-data/mutual-fund-prospectus-riskreturn-summary-data-sets)
- **FundFacts API demo.** Queried the same 40 ISINs, paced at one request
  every 2.2 seconds or more. The response returned four Xetra products
  (2B7D, 2B7K, 36BZ and 36B7) and zero US products. The other 36 were
  HTTP 404 `not_cached`; the demo serves already loaded products, so the
  result measures demo availability only. Two of the four responses were
  marked stale. No account or paid lookup was used. [Demo endpoint documentation](https://fundfactsapi.com/docs/endpoints#get-demofundsisin)
- **36B7 document check.** The demo bond response includes a 0.25% ongoing
  charge, 5.5 years of effective duration, credit weights and an overall
  data date of 16 November. A separately inspected issuer factsheet supports
  a 0.25% TER and reports 5.60 years with a 4 November observation date.
  Keep these as distinct observations. The demo's overall date alone
  supplies no separate fee or credit date. [Issuer factsheet](https://www.ishares.com/uk/professional/en/literature/fact-sheet/36b7-ishares-global-corp-bond-ucits-etf-fund-fact-sheet-en-gb.pdf?siteEntryPassthrough=true&switchLocale=y)

Keep issue #3 open. The issuer feed is useful for identity and discovery
enrichment. A sample from a permitted feed or export should explicitly
include the original 40 with fee metric and date, bond duration method and
date, credit breakdown or rating and date, US trading currency, and sources
or field definitions. Evaluate the same threshold before committing to
recurring access or starting issue #4.

## Reproduction

Use a copy of the saved broader-coverage snapshot to keep the original
observations intact. The follow-up replay used
`data/runs/broader-2026-11-18-followup`. The source probe attempts and raw
responses for the SEC and FundFacts checks are stored separately under
`data/runs/broader-2026-11-18/alternate`.

```powershell
# Collect the two screener inputs into the copied snapshot
uv run python scripts/check_broader_coverage.py data/runs/broader-2026-11-18-followup --fetch ishares-de-screener ishares-us-screener --timeout 60

# Replay the same local inputs offline
uv run --offline --no-sync python scripts/check_broader_coverage.py data/runs/broader-2026-11-18-followup
uv run --offline --no-sync pytest
```

Offline verification covers duplicate US tickers, an unattributed product,
an Xetra join against a different issuer ticker, a zero duration claim and
preservation of missing dates.
