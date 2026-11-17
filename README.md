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
