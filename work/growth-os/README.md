# NCNS Growth OS — functional interactive concept prototype

This is the first implementation under **Milestone C2 / Issue #8** and the owner-approved [Growth Partner Strategy](../../docs/NCNS-GROWTH-PARTNER-STRATEGY.md).

It is an independently authored **business operations interface** in a dedicated `/work/growth-os/` path, **not another agency website or a static mockup**. The approved main NCNS Digital homepage remains unchanged.

## What works right now
- Switch reporting windows (this month / previous month / quarter) and acquisition sources; real client-side sums and funnel percentages recompute.
- Inspect sample leads and operator follow-ups; change a stage and mark an allowed follow-up complete. An opted-out sample record does **not** offer a follow-up button.
- Adjust qualifying rate, close rate, average won-deal revenue and gross margin; actual browser calculations immediately update the illustrative forecast and gross contribution less acquisition spend.
- Generate a rule-based action plan from the sample metrics and any task changes. Copy it, with a manual selection fallback, or download a local JSON file containing the selected assumptions and current plan.
- Read the **Build → Operate → Grow** commercial partnership path and return to the NCNS project enquiry. Keyboard focus states and mobile layout are included.

## Honesty / limitations
All leads, names, spend, sales and results are fictional. These UI workflows are genuine local JavaScript interactions but no live CRM, AI model, ad platform, customer database, payment or messaging system is connected. Forecasts are deterministic arithmetic, **not financial projections or profit guarantees**. The contribution estimate excludes labor, fulfillment, taxes and overhead, so it is **not net profit**. Pipeline records are a small operator sample, *not the whole aggregate funnel*. No network submission, local persistence, data analytics or tracking is implemented.

## How to review locally
At the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Visit: **http://127.0.0.1:8000/work/growth-os/**

No package install or bundler is needed for the browser app. The root-level emblem uses the existing original NCNS asset.

## Functional and responsive smoke checks
```sh
node --check work/growth-os/app.js
python3 tests/growth_os_browser.py
```

The Playwright test generates 1440, 390 and 360px full-page evidence under `docs/qa/milestone-c2/growth-os/`. Requires system Chromium and Python Playwright. These checks still need to be **executed and reviewed** in a real Chromium environment; do not claim the screenshots or test pass before running them.

## What the owner should review
1. Visual quality and clear "business pays for this" story — the app should feel more substantial than a screenshot of a website.
2. The period/channel controls, actual formula changes, pipeline state and operator follow-up.
3. Demo integrity and explicit synthetic-data status.
4. The remaining gaps before this can be used as the flagship of the six-piece portfolio: cross-section nav, richer filters, stronger process/metrics explanations, accessibility audit, screenshot comparison, handoff to the future Demand Engine, and contextual integration with an approved challenge-first portfolio index.

**Draft review only. Do not merge into main or publish until owner approval.**
