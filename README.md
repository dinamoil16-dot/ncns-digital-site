# NCNS Digital — approved cinematic direction (starter)

This is a **working static starter** built around the October 30, 2026 approved combined visual concept (Cinematic Luxury + Premium Minimalism).

## Run locally

Open `index.html` in Chrome/Edge, or serve this directory with `python -m http.server 8000`.

## Files
- `index.html` — semantic front-end prototype (not yet final production page)
- `styles.css` — original layout, atmospheric backdrop, responsive and reduced-motion styles
- `main.js` — real client-side interactions: navigation, workflow stage selector, reveal, progress bar, cursor parallax, copyable brief
- `assets/ncns-original-logo.webp` — owner-supplied authentic approved brand mark. **Do not redraw or replace without approval.**
- `reference/design-direction.md` — visual inspiration only; never use the whole screenshot as the website, because it contains baked-in UI and placeholder copy.
- `spec/CODEX_TASK.md` — engineering brief for Codex.

## Status and integrity
- This is an initial implementation, **not a launched site or finished product**.
- Portfolio contains no invented client case studies or fake numbers. Additional real demo projects will be added separately after the site direction is approved.
- Brief builder only copies text locally; no personal information is transmitted.
- Do not use fake client logos, reviews, '50+ projects', 'global clients', or claimed conversion increases without evidence.
- Contact email, domain, analytics, deployments and backend integrations are intentionally unconfigured.
- Real-world device visual QA, accessibility audit and Core Web Vitals remain open before publishing.

## Milestone A visual rework (issue #3)

The rejected CSS scenery and geometric service illustrations have been replaced with local generated photographic assets. The original NCNS emblem is unchanged. Typography uses locally packaged, licensed Michroma and Manrope; there are no external font requests or frontend build dependencies.

Serve the repository with `python3 -m http.server 8000 --bind 127.0.0.1`. Run `node --check main.js` and `python3 tests/browser_smoke.py` (Python Playwright and `/usr/bin/chromium` required). The app itself only needs a static file server.

The latest Chromium checks passed at 1440, 768, 390 and 360px. See [the visual review, screenshots and limitations](docs/qa/issue-1-rework/visual-comparison.md). Automated checks do not establish owner visual approval.

The exact approved screenshot is visible in the owner's conversation, but its downloadable source file was unavailable to the execution workspace. Its exact committed WebP and approved-versus-actual collage remain blocked; see [reference provenance](reference/README.md). Do not substitute generated scenery for that reference.

PR #2 must remain draft pending the missing reference gate and owner approval. No portfolio development, merge or deployment is authorized at this stage.
