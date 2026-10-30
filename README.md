# NCNS Digital

Independent static agency website in the approved Cinematic Luxury × Premium Minimalism direction. Milestone A was approved and merged in PR #2; its squash commit `87e8de3` is the visual baseline. Milestone B completes the agency sections and local interactive tools for owner review.

## Run locally

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

No frontend installation or build is needed. All fonts and imagery are local. The original `assets/ncns-original-logo.webp` is unchanged. `styles.css` retains the approved opening-frame design; `milestone-b.css` extends the site below it and adds restrained, accessible interactions.

## Current experience

- Original cinematic hero and three service images, with a single composite halo and shallow scenery depth. Pointer movement does not transform the logo lettering.
- Detailed websites, branding and AI/workflow capabilities; native accessible detail panels.
- Three-step local requirements builder, honest copyable draft, clipboard fallback and transfer to an editable project brief.
- Keyboard-accessible Discover → Design → Build → Improve timeline, standalone About, explicit coming-next work section and complete footer navigation.
- Reduced-motion support, paused motion in hidden tabs, useful content/navigation without JavaScript and local font fallbacks.

The builder assembles user choices locally. It is not an AI service or price quotation. The contact section only copies a brief; it sends no enquiry, email, payment or booking. No analytics, tracking, backend, portfolio cases or deployment are enabled.

## Validation and review

```sh
node --check main.js
python3 tests/milestone_b_browser.py
python3 tests/record_milestone_b.py
python3 tests/record_milestone_b.py --mobile
```

QA tools require Python Playwright, Pillow, system Chromium (`/usr/bin/chromium`) and FFmpeg for recordings. The server must be running. `python3 tests/browser_smoke.py` remains a compatibility entry point for the current acceptance suite.

[Milestone B QA, screenshots, videos and limitations](docs/qa/milestone-b/README.md) · [Exact approved reference](reference/README.md) · [Asset provenance and licenses](assets/scenery/README.md)

Historical Milestone A evidence remains under `docs/qa/issue-1-rework/`. Milestone B requires a new draft PR targeting main and owner visual approval before any merge or publication. Portfolio cases are a separate later milestone.
