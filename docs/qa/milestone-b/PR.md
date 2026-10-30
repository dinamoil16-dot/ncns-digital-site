## Milestone B

Completes the agency website below the approved Milestone A opening frame: detailed services, a real local requirements builder, keyboard-accessible process timeline, standalone About, honest upcoming-work section, offline project brief and footer navigation. The builder validates choices, creates a copyable draft and transfers it to the brief without sending data.

Adds restrained group reveals, service hover/focus depth, active navigation and visibility-aware motion. Pointer movement affects scenery rather than distorting the original emblem. The approved 1440×604 hero is pixel-identical in the reduced-motion comparison; the original artwork and base styles are unchanged.

## Validation

- `node --check main.js` and `git diff --check` pass.
- `python3 tests/milestone_b_browser.py` passes at 1440×900, 1024×768, 768×900, 390×844 and 360×780.
- Keyboard/touch navigation, process tabs, builder validation, native clipboard, manual fallback, transfer/restart, reduced motion, hidden-tab guards, no-JS and font-failure paths checked. No JS errors, overflow, failed resources or data submissions.
- Actual approximately 20s desktop/mobile Chromium recordings show hero motion, services, native scrolling and the working lab.

[QA report, screenshots and videos](docs/qa/milestone-b/README.md) · [Hero A/B comparison](docs/qa/milestone-b/hero-before-after.webp)

Refs #4. Draft for owner visual review. No portfolio cases, backend, analytics, merge or deployment. Milestone B must be approved before proceeding.
