# ETF Expert

A simple local US+EU ETF research project. The first milestone measures whether obtainable data supports useful comparison across a broader universe. Portfolio selection comes after that evidence.

Early phases use Python scripts and local JSON/Markdown files. No GUI, Docker, agent framework, in-app LLM, or harness subagents.

## First milestone: data feasibility

The initial diagnostic sample contains 24 listings: 12 US and 12 EU listings across equity and bond strategies. It is a deliberately chosen coverage sample, not a complete catalogue or an eligible portfolio pool. EU means listing venue; underlying investments may be global. London listings are excluded from this sample.

```powershell
uv sync
uv run python scripts/check_coverage.py
uv run pytest
```

The check collects Yahoo profile data, recent daily prices and reported top holdings. It saves raw responses locally under ignored `data/runs/` and generates a coverage report with per-listing failures and missing fields. Zero numeric values count as present; missing values never become zero. Reported holdings are partial and cannot establish complete overlap.

The sample labels are research intentions, not verified classifications. Yahoo trading currency is not assumed to be fund base currency. Collection time does not establish the observation date of a profile or holdings field.

Next: inspect the real gaps, test issuer supplementation for material missing fields, then demonstrate comparison and transparent selection on the broader pool. No portfolio recommendation or suitability claim is made.

## Observed first pass

On 17 November 2026, all 24 sample listings returned recent daily prices and ETF quote types. Category coverage was 12/12 US and 0/12 EU; nonempty reported holdings were 9/12 US and 7/12 EU. These are field-availability observations, not validation of accuracy or investment eligibility. See the [feasibility assessment and next step](docs/feasibility-2026-11-17.md) and [per-listing report](docs/coverage-2026-11-17.md).

Yahoo/yfinance is an unofficial research route; access and reuse remain subject to source terms. See [yfinance](https://github.com/ranaroussi/yfinance) and [Yahoo terms](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html). Raw provider responses are not committed.

The previous project's outcome and lessons are preserved in [retirement.md](retirement.md).

## Official issuer supplementation experiment

Issue #1 tested the same 24 listings against official sources. See the
[dated assessment](docs/issuer-feasibility-2026-11-17.md) and
[per-listing field report](docs/issuer-coverage-2026-11-17.md).
The result is **change the route before scaling**: 23 parsed factsheets and a
limited QQQ product-page fallback supply useful facts, but do not establish a
complete, permitted, unattended research service.

`data/issuer_sources.json` contains manually located URL candidates, including
failed candidates. It is an experiment manifest, not a catalogue or eligibility
list. Raw PDFs, HTML, extracted text, collection metadata and JSON assessments
remain in ignored `data/runs/`. The only new runtime dependency is `pypdfium2`
for extracting the downloaded factsheets.

Live collection command (review the source-specific access limitations in the
assessment before repeating downloads):

```powershell
uv run python scripts/check_issuers.py
# Explicit probe; it does not establish coverage of the complete sample:
uv run python scripts/check_issuers.py --symbols VWCE.DE VAGF.DE SXR8.DE EUNA.DE --kinds factsheet
```

Replay the actual saved evidence without network access:

```powershell
uv run python scripts/assess_issuers.py data/runs/issuers-20261117T174001860718Z data/runs/issuers-20261117T174127895555Z data/runs/issuers-20261117T174613957126Z --output data/runs/issuers-20261117T174613957126Z/assessment.md
uv run pytest
```

The replay writes Markdown plus a paired JSON assessment. On another machine,
use locally collected run folders in chronological order; the ignored evidence
is not distributed with the repository. A report distinguishes extracted source
claims, dated composition, undated fields and failures. Missing base currency or
hedging is not filled from a trading or performance currency. Bond measures are
not universal equity requirements. No selection or allocation is implemented.

## Source-backed ETF records

Convert the saved diagnostic observations to one local JSON record per requested
listing. The converter works offline and preserves the evidence needed to review
listing and share-class links, fees, currencies and material gaps.
See the [record format, comparison requirements and replay findings](docs/etf-records-2026-11-18.md).

```powershell
uv run --offline --no-sync python scripts/assess_issuers.py data/runs/issuers-20261117T174001860718Z data/runs/issuers-20261117T174127895555Z data/runs/issuers-20261117T174613957126Z --output data/runs/issuers-20261117T174613957126Z/assessment-records.md
uv run --offline --no-sync python scripts/normalize_records.py data/runs/issuers-20261117T174613957126Z/assessment-records.json --yahoo-run data/runs/20261117T172137188429Z --output data/runs/records-2026-11-18.json
```

Use your local run folders. Omit `--yahoo-run` for an issuer-only conversion.
Regenerate any earlier assessment JSON from its saved run folders so the
converter receives each successful issuer observation.

## Broader coverage pilot

Issue #3 tested venue-level discovery and bulk research for 40 additional
listings across US and Xetra equity and bond groups. The initial bulk
sources left material comparison evidence unresolved for every listing.
The one-time issuer-document review later cleared the evidence gate for
all 40. See the [initial bulk pilot](docs/broader-coverage-2026-11-18.md)
and the [full-cohort review](docs/full-cohort-coverage-2026-11-18.md).

## Offline comparison and screening

Run `scripts/screen_etfs.py` on the saved 40-listing review. It renders a
source-linked Markdown table with a reason for every screening result.
The [comparison rules and examples](docs/comparison-rules.md) document
the local input, evidence dates and supported filters.

```powershell
uv run --offline --no-sync python scripts/screen_etfs.py data/runs/full-cohort-2026-11-18/manual-coverage.json --as-of 2026-11-18
```

## Continuous integration

GitHub Actions runs the offline tests on pull requests targeting `main` and on
pushes to `main`. The single Windows job uses Python 3.14.0 and uv 0.9.7, installs
the locked dependencies, then runs `uv run --offline --no-sync pytest`.

Dependency installation needs network access. The tests use supplied inputs;
the workflow does not run the live Yahoo or issuer collectors and does not need
the ignored local evidence. It performs no deployment. To run the same checks
locally with Python 3.14.0 selected:

```powershell
uv sync --locked --dev --python 3.14.0
uv run --offline --no-sync pytest
```
