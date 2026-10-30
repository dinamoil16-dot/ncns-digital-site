## Milestone C1: visual concepts only

Proposes three distinct fictional portfolio directions for owner approval: Asterwake (premium marine refit/estimate UX), Kern/9 (industrial specification/RFQ and simulated operational handoff), and Auven (design-led consumer audio/configuration commerce).

Includes original local art, independent HTML/CSS proposal boards, six primary desktop/mobile Chromium screenshots, module close-ups, a consistent NCNS review index, comparison/recommendation, static URL architecture, detailed future flow/validation definitions and asset provenance. Kern/9 is the recommended first direction for its combination of visual craft, lead qualification and explainable workflow depth.

The entire approved agency site is unchanged. These are visual proposals with explicitly inactive sample module controls; no complete demo, real CRM, quote service, checkout, backend, tracking or deployment is built. Names and sample prices are tentative/fictional.

## Validation

- `python3 tests/portfolio_concepts.py`: Chromium renders at 1440, 390 and 360px; assets load locally; no JS errors or horizontal overflow; index/board return navigation works without JavaScript; proposed action controls remain disabled.
- Reviewed full desktop and mobile boards; glyph issues corrected with SVG.
- New files only under `docs/portfolio/concepts/` and `tests/portfolio_concepts.py`.

[Concept review and six primary screenshots](docs/portfolio/concepts/README.md) · [Three-direction sheet](docs/portfolio/concepts/screenshots/three-directions.webp)

Refs #6. Draft for visual approval first. Do not build full demos, modify the approved agency site, merge or deploy until the owner approves the direction(s).
