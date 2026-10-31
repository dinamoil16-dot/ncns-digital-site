# Standalone agency review — PR #14

Updated Issue #13: website first. This QA serves only this branch. **No Growth OS app, portfolio branch, external system or worktree overlay is required.** No messages, account actions, merge to main or deployment.

## Actual screenshots

| Width | Full site | Twelve-service catalog | Build → Operate → Grow | Contact |
| --- | --- | --- | --- | --- |
| 1440 | [Full](full-1440.png) | [Services](capabilities-1440.png) | [Partnership](work-1440.png) | [Brief](contact-1440.png) |
| 1024 | [Full](full-1024.png) | [Services](capabilities-1024.png) | [Partnership](work-1024.png) | [Brief](contact-1024.png) |
| 768 | [Full](full-768.png) | [Services](capabilities-768.png) | [Partnership](work-768.png) | [Brief](contact-768.png) |
| 390 | [Full](full-390.png) | [Services](capabilities-390.png) | [Partnership](work-390.png) | [Brief](contact-390.png) |
| 360 | [Full](full-360.png) | [Services](capabilities-360.png) | [Partnership](work-360.png) | [Brief](contact-360.png) |

Also captured: process, about, FAQ, service directory, no-JS, exact approved/current hero and historical before/after states. Long section captures suppress only the fixed one-pixel scroll-progress overlay to avoid a stitching line through content. No generated website imagery is used as evidence.

## Actual browser videos

[Desktop MP4](walkthrough-1440.mp4) · [Mobile MP4](walkthrough-390.mp4). Normal-motion real Chromium, approximately 18 seconds each; source WebM files and timings are in [recordings.json](recordings.json). Journey: unchanged hero → service pillars → automation scope → Build/Operate/Grow → requirements builder → local brief/copy. No UI activity was synthesized; MP4 is only a silent encoding of the real recording.

## Before / after

[Desktop comparison](journey-before-after-1440.webp) · [Mobile comparison](journey-before-after-390.webp) · [Measured historical/current boundary](before-after.json).

The prior standalone `d6f4aac` branch linked to a missing `/work/growth-os/` route (actual expected HTTP 404). Current pages have zero links to that unavailable app. Work now explains the partnership; five pillars lead to twelve concrete scopes and the brief. The service directory links only to actual sections. The agency no longer depends on a portfolio release.

## Verified behavior

[Main results](results.json): 1440×900, 1024×900, 768×1024, 390×844, 360×780. Twelve families, five pillars; each scope CTA populates the correct form selection; mobile menu/Escape, skip link, keyboard process tabs, native FAQ; Experience Lab validation/back/reset and transfer; clipboard success and forced failure; Unicode/special-character email encoding using test-only recipients; missing contact config; native no-JS content; pause/resume and reduced motion; all internal public routes/anchors; no overflow, JS/resource errors, external requests or writes in the real user journey.

[Hero regression](hero-regression.json): pixel-identical against approved main `bb405bf` at all five widths. The original emblem SHA-256 is checked in the suite. [Side by side desktop](hero-approved-current-1440.webp) and [mobile](hero-approved-current-390.webp).

[Retained Milestone B regression](regression-b-results.json): real clipboard read/write, font-load failure, no-JS at desktop/mobile, normal halo clock, pointer parallax/card tilt, hidden-tab pause and reduced-motion reset. All five viewports passed. Observed local layout shift was 0 in these samples; measured subresource transfer was 709,919 bytes at 1440/1024 and 399,391 at 768/390/360. These are local Chromium observations, not field Core Web Vitals or physical-device certification.

Performance changes are deliberately small: primary reading font preload removes stylesheet-dependent font discovery; native disclosures/controls avoid a new UI framework; no demo runtime or unapproved preview art is loaded; the production preparation allowlist excludes internal QA/marketing/git material. The approved scenic hero retains its existing responsive assets and motion. No unsupported percentage improvement or universal performance guarantee is claimed.

## Reproduce

- `node --check main.js` and `node --check contact.js`.
- `python3 tests/agency_site_browser.py` — serves this repository on its own ephemeral port.
- `python3 tests/approved_hero_regression.py` — requires current `origin/main`; compares actual pixels.
- `python3 tests/agency_before_after.py` — uses historical ancestor `d6f4aac`, not a demo overlay.
- `python3 tests/record_agency_site.py` — Playwright + FFmpeg; records real normal motion, never sends.
- Legacy regression: serve this root, set `NCNS_TEST_URL` and optional `NCNS_QA_OUTPUT`, then run `python3 tests/milestone_b_browser.py`. `browser_smoke.py` remains its compatibility entry.

Use system Chromium or install Playwright Chromium. Playwright video needs its encoder; this environment used compatible system FFmpeg through `/tmp/ncns-playwright/ffmpeg-1011/ffmpeg-linux` with `PLAYWRIGHT_BROWSERS_PATH=/tmp/ncns-playwright`. No-JS and font failures are browser fallbacks, not a substitute for testing another browser engine. A test-only GitHub Actions workflow is included; no CI run is claimed here.

## Explicit remaining gates

Email/WhatsApp values and real delivery are unverified. Opening the owner-confirmed Instagram profile does not prove a DM was received. Canonical domain/hosting/DNS, legal operating/retention details, Safari/iOS/Firefox and actual modest-device release checks remain. Owner visual/function approval precedes any merge or publication. Portfolio is deferred, not a blocker.
