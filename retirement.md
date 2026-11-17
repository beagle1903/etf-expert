# ETF Research App — Clean Start and Archive Decision

Decision recorded: **17 November 2026**

This document preserves the purpose, useful results, limitations and lessons of
`agents-lab` / `agentic-etf-advisor`, and sets a direction for a possible successor.
It is intended to stand alone as the README of a clean start.

repo link: https://github.com/beagle1903/agentic-etf-advisor

**Decision: stop development on the existing repository and preserve it as an
archive.** The central larger-universe user journey was not delivered. A working
twenty-fund starter does not satisfy that requirement.

This records the decision; it does not assert that GitHub's archive setting has
been applied. Creating this document does not delete files, discard unfinished
work, change repository settings, or authorize another implementation attempt.

## The goal

Build a usable, local ETF research and portfolio decision-support app that can
work across a meaningfully larger fund universe, rather than repeatedly returning
to the same small packaged list.

The user should be able to:

1. Define a research universe and see its actual coverage and limitations.
2. Supply objectives, risk preferences, horizon, cash amounts and exclusions.
3. Collect attributable fund facts with source dates and explicit missing data.
4. Compare the researched funds and understand every exclusion.
5. Generate an illustrative portfolio from the eligible pool, with transparent
   selection and allocation rules.
6. Inspect sources, costs, concentrations, overlapping exposures and uncertainty.
7. Change inputs and understand why the result changed—or why it did not.

A larger research universe and a small final portfolio are different things. A
five-position draft can be useful after researching a broad universe. Repeatedly
selecting five positions from the same fixed twenty candidates does not prove
broader research capability.

The app is educational decision support. It must not execute trades, guarantee
returns, present an illustrative allocation as established suitability, or hide
data limitations behind a generated explanation.

## What the existing project actually delivered

| Capability                 | Evidence and limit at the decision date                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Local dashboard            | Streamlit app runs and presents policy, evidence, screening and an illustrative portfolio.                                                                                                       |
| Twenty-fund starter        | On 17 November, a live collection completed for 20/20 candidates; 17 passed screening and a five-position draft reached human review. This was a dated observation, not a reliability guarantee. |
| Source accountability      | Material fields retain provenance, timestamps and missingness; unsupported evidence can block selection.                                                                                         |
| Deterministic construction | Weight and cash arithmetic, sleeve and position constraints, and explanations of inclusion are implemented. This is not expected-return optimization.                                            |
| Human review               | Approve, edit and reject flows, typed revisions and audit history exist. Policy-only revision and approval were exercised in this session; the live ETF draft was left awaiting user review.     |
| Comparisons                | Candidate comparisons and partial reported-holdings overlap are available. They do not establish complete portfolio overlap or independent economic risk.                                        |
| Optional integrations      | Retrieval stores, provider explanations and PostgreSQL checkpoints exist. Their full live operation was not established by this session.                                                         |
| Broader catalogue          | Discovery and bounded research-job machinery exists for up to 100 selected listings, with five collected per explicit batch. A complete broader live user journey remained unverified.           |
| Investment quality         | No claim was established that these portfolios improve investment outcomes.                                                                                                                      |

The starter result used the default demonstration profile. Its five positions
were SPY, QQQ, VEA, BND and AGG. This describes software behavior, not a portfolio
recommendation.

## Existing technology stack

This is the stack of the archived project, **not a requirement to reproduce it**.

| Layer                  | Technology                                                            | Purpose                                                              |
| ---------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Runtime and packaging  | Python 3.12–3.13, `uv`, `pyproject.toml`, locked dependencies         | Application runtime and reproducible installation                    |
| Workflow               | LangGraph                                                             | State transitions, human-review interrupts and resumable execution   |
| Contracts and settings | Pydantic, pydantic-settings                                           | Typed validation, configuration and serializable state               |
| User interfaces        | Streamlit, Typer                                                      | Local dashboard and command-line operations                          |
| Market data            | Yahoo Finance through yfinance and bounded curl_cffi transport        | Listing checks and research facts; unofficial development data       |
| Additional sources     | Bounded Vanguard holdings client; ECB adapter for applicable FX paths | Specific composition and currency evidence                           |
| Retrieval              | Chroma                                                                | Semantic retrieval of source material                                |
| Relationships          | Neo4j                                                                 | Source-linked structured relationship context                        |
| Durable checkpoints    | PostgreSQL, psycopg, LangGraph PostgreSQL saver                       | Optional saved review and lifecycle storage                          |
| Model explanations     | Ollama / Ollama Cloud and OpenRouter adapters                         | Optional structured explanations validated against supplied evidence |
| Observability          | Optional LangSmith integration                                        | Tracing and evaluation support                                       |
| Local infrastructure   | Docker Compose                                                        | Optional Chroma, Neo4j and PostgreSQL services                       |
| Quality tooling        | pytest, Ruff, mypy and offline evaluators                             | Behavioral checks, code quality and regression evidence              |

The starter path can use its prepared evidence without Docker, Chroma, Neo4j or
PostgreSQL. The broader catalogue publication/review path uses the evidence
stores. Explanation generation is optional and requires a configured provider.

## What went wrong

### 1. The central user outcome stayed unresolved

The user reports spending more than a month trying to work with a larger set of
funds. Despite substantial implementation, the practical demonstration kept
returning to a limited starter universe. The repository accumulated capabilities
without establishing the larger-universe experience the user wanted.

### 2. Component completion was confused with product readiness

Merged changes, passing tests, catalogue discovery and a successful small-universe
demo were useful evidence, but did not prove the complete broader journey:
discover, collect, validate, publish, research, construct and review.

The agent also communicated progress too broadly. In this session, saying that
the starter “now works” did not address the unchanged universe. Recommending
another bounded catalogue attempt then repeated a route already tried, without
first identifying a materially different approach.

### 3. Scope reduction did not solve the original problem

On 15 November, the original broader readiness requirements in Issues 117 and
123 were retired. The completion scope was narrowed to the delivered twenty-lead
starter. Those broader requirements were **withdrawn, not passed**.

That was an explicit scope decision, not evidence that the larger-universe
problem had been solved. Subsequent status summaries needed to keep this
distinction prominent.

### 4. Data coverage and identity remained limiting factors

A directory listing is not a complete, usable research record. Required source
fields can be unavailable, stale or unsupported. A verified ticker and exchange
do not establish legal Fund/share-class identity or independent exposure.

Historical broader work retained unresolved eligible-pool, identity and live
publication/reopening/review evidence gaps. Implementing validators and catalogue
jobs did not supply the missing source evidence.

The lesson is to demonstrate that obtainable data can support the intended
universe before committing to the surrounding architecture. Weakening checks or
silently treating missing values as valid would not resolve this problem.

### 5. Architecture and process grew ahead of demonstrated user value

The project contains substantial retrieval, graph, persistence, replay, identity,
compatibility and workflow machinery. Much of it serves legitimate correctness
needs. Our retrospective assessment is that its combined operational and
maintenance cost outpaced the user value demonstrated by the broader workflow.

Process work also became a recurring concern; ADR 0049 later replaced prospective
ticket-ledger and finite-phase machinery with a shorter working agreement. The
history should be retained, but a successor should not inherit every mechanism
merely because it already exists.

### 6. Some inputs suggested more personalization than the calculation supplied

Risk tolerance and objective choose the current policy split. Horizon and maximum
tolerable drawdown are required context, but do not change that split, enforce a
loss limit or assess horizon suitability. The latest change discloses this
clearly; it does not add the missing decision behavior.

### 7. Even startup success was narrower than it appeared

The initial launch installed dashboard dependencies only. Policy-only review
worked, but starter collection stopped with `transport_blocked` before attempting
any funds because yfinance was missing. Installing the locked data extra allowed
the next collection to complete.

This was a setup failure, not a Docker outage. A successful health check and a
working policy screen did not prove that the actual research task was ready.

## Why we decided to archive

The decision followed the user's observation that the app still presented the
same limited list, followed by their reminder that larger-universe attempts had
already consumed more than a month.

The agent acknowledged that another proposal to repeat the catalogue route was
not a sufficient answer and recommended stopping development and archiving the
repository. The user then requested this clean-start record.

The reason is not that every component is broken or worthless. The project
produced reusable engineering and documented evidence. The reason is that the
core desired outcome remained unproven, and further polishing of the starter or
repetition of the same approach lacked a convincing basis.

Archiving preserves the work, failed outcomes, unfinished work and lessons without
continuing to present the repo as an actively progressing solution. Deleting the
repository would unnecessarily destroy that reference material.

## Conditions for a genuinely different clean start

A successor is a proposal, not an authorized implementation or a promised result.

1. **Agree on the observable outcome first.** Define the desired markets,
   categories and research breadth. Choose a concrete larger set that cannot be
   satisfied by the old twenty-fund starter. Keep research coverage separate from
   final position count.
2. **Prove the data route before building the app.** Use one small, reproducible
   script to measure coverage, field completeness, timestamps, identity quality,
   request limits and operational cost across that set. Document source terms
   and any manual evidence requirements.
3. **Make a stop decision from that evidence.** If the required data cannot be
   obtained reliably within the agreed cost and effort, stop or explicitly change
   the goal. Do not answer a failed broader test by quietly shrinking the universe.
4. **Build one complete vertical slice.** From the agreed larger set, produce a
   transparent comparison and a reviewable illustrative draft. Show counts at
   every stage and explain every exclusion. Exercise failure and a fresh-session
   reopening if persistence is part of the agreed outcome.
5. **Keep the initial stack small.** Prefer a Python collection/validation script,
   typed records and local JSON or SQLite storage. Add a simple interface after
   the data and selection journey works. The exact stack remains undecided.
6. **Add infrastructure only for a demonstrated need.** LangGraph, vector search,
   a graph database, a server database and LLM explanations must each earn their
   place. A larger fund list alone does not require all of them.
7. **Make input behavior explicit.** State which inputs affect selection or
   weights, which are only context, and what the calculation does not establish.
8. **Report evidence precisely.** Separate implemented, tested with synthetic data,
   observed live, repeatably usable, and unverified. Test counts and merged PRs
   support specific claims; they do not substitute for the user acceptance demo.

Reuse algorithms, contracts or tests selectively after the successor needs them.
Do not automatically migrate old checkpoints, compatibility branches, ticket
machinery, infrastructure or financial assumptions.

## Historical references

Source baseline checked on 17 November 2026: merged main
`cbefbc04c9586d0bc90474ccda625b1b21f083a1`.

- [Product vision](https://github.com/beagle1903/agentic-etf-advisor/blob/cbefbc04c9586d0bc90474ccda625b1b21f083a1/docs/product/vision.md)
- [System architecture](https://github.com/beagle1903/agentic-etf-advisor/blob/cbefbc04c9586d0bc90474ccda625b1b21f083a1/docs/architecture/system.md)
- [Broader-scope retirement and preserved unresolved outcomes](https://github.com/beagle1903/agentic-etf-advisor/blob/cbefbc04c9586d0bc90474ccda625b1b21f083a1/docs/iterations/052-issue123-scope-retirement.md)
- [Implemented bounded catalogue workflow](https://github.com/beagle1903/agentic-etf-advisor/blob/cbefbc04c9586d0bc90474ccda625b1b21f083a1/docs/catalogue-research.md)
- [Shorter prospective working agreement, ADR 0049](https://github.com/beagle1903/agentic-etf-advisor/blob/cbefbc04c9586d0bc90474ccda625b1b21f083a1/docs/architecture/decisions/0049-prospective-working-agreement.md)
- [Context-only input disclosure, ADR 0053](https://github.com/beagle1903/agentic-etf-advisor/blob/cbefbc04c9586d0bc90474ccda625b1b21f083a1/docs/architecture/decisions/0053-context-only-allocation-inputs.md)

The 17 November live startup, dependency repair, collection and displayed draft
are observations from the archive-decision conversation. They are not presented
as committed acceptance evidence or proof of the historical broader requirements.
