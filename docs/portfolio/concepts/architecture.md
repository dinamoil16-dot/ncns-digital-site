# Proposed portfolio architecture — not implemented in C1

## Two layers, two responsibilities

The future portfolio index follows NCNS's approved black/silver/ice-blue visual system and original emblem. Each fictional concept has its own visual identity inside a small, consistent NCNS concept wrapper. Shared navigation/provenance must not make a fictional brand look like an actual client.

C1 files live under `docs/portfolio/concepts/` with `noindex,nofollow`. The existing root site, scripts, styles, assets and Selected Work remain untouched. The review index is a review artifact, not a new published section of the agency site.

## Future static URL contract

| URL | Static file | Purpose |
| --- | --- | --- |
| `/work/` | `work/index.html` | NCNS-branded index; concepts explicitly labelled fictional |
| `/work/asterwake/` | `work/asterwake/index.html` | Approved marine concept and bounded local refit builder |
| `/work/kern9/` | `work/kern9/index.html` | Approved industrial concept and RFQ/routing simulator |
| `/work/auven/` | `work/auven/index.html` | Approved consumer concept and configuration calculator |

Use directory indexes and trailing slashes, not SPA history routing or query-only page identities. Relative navigation makes the structure work under a root domain or a repository base path. Asset URLs must be relative to the page or generated from one configured `BASE_PATH`; do not hardcode an unapproved NCNS domain.

No production canonical hostname is known or assigned in C1. Once static deployment is separately authorized, emit absolute canonicals as `<approved-origin><BASE_PATH>/work/<slug>/`; normalise `/index.html` to the directory URL if the chosen static host supports redirects. Do not publish fake canonical hosts now. Keep draft concept pages unindexed until publication is explicitly approved.

## Visitor path after approval

1. In a later approved coding task, replace the existing Selected Work placeholder with explicit concept cards / a link to `./work/`. **Do not modify it during C1.**
2. `/work/` presents three industries with a short commercial problem, a concept badge and a “Try the concept” link. No fake client statistics, testimonials or real-business attribution.
3. A demo page keeps a quiet NCNS review/context strip: “Fictional portfolio concept”, “All concepts” → `../`, “Back to NCNS” → `../../#work`. The brand-specific header and content sit below it.
4. “Try the builder” scrolls to the actual implemented module on the same page; no dead CTA, hidden paid service or full-page mockup image.
5. A local copy/download result states the sample/simulation boundary and offers an explicit return to the concept index or agency work section. Do not rely solely on browser history for the return path.

The C1 review index already supports only the analogous review navigation: index → board → index / unchanged agency site. No live work route or root-site entry point is added yet.

## Isolation and data design

Each future demo gets scoped styles and a small ES module; the agency's `main.js` and baseline styles are not reused as a global application shell. Share only tiny helpers for clipboard fallback, numeric validation and accessible step navigation. Retain independently licensed fonts/assets per route and avoid loading all three concept bundles on the index.

Keep future demo fixtures in small versioned local JSON files: rates and assumptions for Asterwake; rule matrix and sample part metadata for Kern/9; fictional catalogue/prices for Auven. No secrets, personal data, network SDKs, authentication, tracking or real CRM endpoints. Outputs stay in memory or a user-triggered local text/JSON download. No persistence is needed by default.

## Performance, accessibility and build scope

- Static HTML/CSS first; no large animation framework, model viewer or unnecessary WebGL. Future functional code target: under 35 KB compressed per demo, excluding local imagery/fonts; measure rather than assume.
- Responsive hero images (roughly 720/1200/1600 widths), explicit dimensions, lazy secondary imagery and font subsetting where the OFL allows it. Target initial transfer under 500 KB desktop / 350 KB mobile after optimisation, and CLS below 0.05; these are proposed budgets, not C1 achievements.
- Native fieldsets/labels, visible focus, keyboard step controls, error summary linked to invalid fields, units in labels and polite result announcements. Swatches need text labels; no colour-only status. Reset must be predictable.
- Reduced motion disables nonessential parallax/transitions; static imagery must remain convincing. Do not animate critical price/validation text in a way that hides changes.
- C2 acceptance includes 1440, 1024, 768, 390 and 360 widths, touch/keyboard, no-JS meaningful content, font failures, no outbound writes, validation edge cases and actual animation evidence where implemented.

Approve names/art direction and one bounded flow first. Then build only that approved flow, test it and request functional review. Production integrations, physical product claims, real supplier pricing, payments, deployments and other cases remain separate approvals.
