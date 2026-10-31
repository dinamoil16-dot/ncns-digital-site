# PR #14 — agency website first / updated Issue #13

**Current priority: finish the standalone main agency website. Growth OS, portfolio, new 3D and marketing production are deferred. No PR #9 integration or portfolio approval is required for this site review.** Earlier two-worktree overlay evidence is historical, not a dependency.

## What changed

- Kept the exact approved cinematic hero markup, scenery, original emblem and opening three service cards. The core `styles.css` and original logo are unchanged. Five-width pixel comparison is against current approved main `bb405bf`.
- Added the complete twelve-family catalog under five navigable pillars. Every family explains its business problem, scoped examples, deliverable and next action; its CTA selects that exact service in the contact brief. [Coverage mapping](service-coverage.json).
- Replaced the demo-dependent Work section with Build → Operate → Grow: one defined project, optional monthly care and measured optimization, with explicit ownership/cost boundaries. No fake case studies or ROI.
- Finished process, about, native FAQ, footer, legal disclosures and a directory route. No unavailable Growth OS/portfolio links or unapproved preview art remain in the public site. `/solutions/` now points only to real service sections.
- Extended Experience Lab to all twelve service families. It remains a browser-local requirements tool, not an AI agent or sent enquiry. Back, validation, reset, copy and transfer-to-brief work.
- Owner-confirmed business email `ncns.digital@gmail.com`, Instagram `@ncns.digital` and WhatsApp `+7 906 323-14-57` now appear as clickable icon links. A direct **Formspree AJAX submission workflow is implemented** (name, reply email, required consent, validation, progress, errors and retry) and is **enabled with the owner-provided endpoint**. A one-time synthetic Formspree submission returned HTTP 200 and its notification was confirmed in the NCNS Gmail inbox. No Telegram. Browser-on-public-domain and reply-to checks remain.
- Added an explicit ambient-motion pause control in the footer, which survives visibility changes; system reduced-motion settings remain authoritative. Existing normal hero motion is unchanged.
- Added service structured data, updated SEO copy, an actual 1200×630 social preview using the unchanged emblem, primary-font preload, and a safe static preparation script. Canonical origin, sitemap and absolute share metadata are generated only after an owner-approved domain is supplied.

## Before → after journey

**Before:** Work → fictional-demo directory → Growth OS route absent from this branch (real HTTP 404); only three detailed service groups; contact had no configured public link.

**After:** Services → five pillars → any of twelve scoped offerings → preselected project brief. Or Work → Build/Operate/Grow → request review. Experience Lab → validated requirements → local brief/copy. Confirmed Instagram opens externally; email draft becomes available only when configured. No demo branch or overlay is used. [Actual before/after](../qa/agency-site/journey-before-after-1440.webp).

## Review and release gates

| Gate | Status |
| --- | --- |
| Standalone agency, no demo dependency | Complete locally; all public internal routes/anchors tested |
| Full service coverage / commercial model | Twelve families, five pillars; Build/Operate/Grow with scope and ownership |
| Approved hero and original emblem | Five pixel-identical hero comparisons; original SHA-256 checked |
| Five-width Chromium / keyboard / touch | 1440, 1024, 768, 390, 360; no overflow, JS/resource errors or external/write requests |
| Experience Lab / form / fallbacks | Validation, back/reset, selection, clipboard success/failure, no-JS native disclosure and email/config failure paths |
| Real screenshots and videos | [Agency evidence](../qa/agency-site/README.md), desktop/mobile recordings |
| Public email and WhatsApp | **Owner-confirmed contact icons configured; Formspree notification received in business Gmail; direct mailto delivery untested.** |
| Direct form delivery | **Live endpoint configured, one synthetic Formspree-to-Gmail notification received 31 Oct 2026 at 16:54 UTC. Actual public browser/Reply-To tests remain.** [Evidence and setup](FORM-DELIVERY.md). |
| Canonical domain / hosting / DNS | **Unconfirmed**; no public preview/deployment claimed |
| Legal operating details / hosting logs / retention | **Owner confirmation required before release** |
| Firefox, Safari/iOS, modest physical device | **Not certified by local Chromium tests; release checks pending** |
| Owner approval / merge / publication | **Pending**; no merge to main or deployment performed |

**Decision: automatic Formspree inbox notification delivery has been verified with one controlled test. Public launch is still NO-GO until a real-domain browser test, reply-to check, domain/hosting/legal decisions and final owner approval.** Portfolio is not a prerequisite.

## Reproduce

Install Python Playwright + Pillow, Node and Chromium. Current tests use system Chromium where available, otherwise Playwright's browser. Run `node --check main.js`, `node --check contact.js`, `python3 tests/agency_site_browser.py`, `python3 tests/approved_hero_regression.py`, `python3 tests/agency_before_after.py`. All serve their own local root, with no app overlay or external service. `tests/client_ready_browser.py` is a compatibility alias to the standalone agency suite.

`python3 tests/render_social_preview.py` renders the committed social preview from original HTML, with the original emblem unmodified. `python3 tests/record_agency_site.py` records normal-motion desktop/mobile Chromium. Playwright video needs its normal FFmpeg install, or the documented compatible system-encoder cache used in this environment. Normal testing does not send or deploy. A separate one-time authorized synthetic Formspree POST succeeded and the temporary live-send step was removed from CI.

The GitHub Actions workflow is test/artifact-only; a local pass is not a claim that CI has run successfully. [Direct-form setup](FORM-DELIVERY.md) · [Deployment and SEO preparation](deployment.md) · [Current handoff](HANDOFF.md). Existing marketing drafts are preserved, not a current workstream or release prerequisite.
