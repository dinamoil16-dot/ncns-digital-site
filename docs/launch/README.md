# Issue #13 — first-client readiness

**Decision: NO-GO for public launch.** The review build works locally; publication and inbound delivery have not been verified. No merge or deployment performed.

## Two review streams

- Existing PR #9 / `feat/growth-os-interactive-demo`: Growth OS runtime, data-driven flow, keyboard/pipeline fixes, five-width browser QA and genuine walkthroughs.
- `codex/issue-13-client-ready` from approved main: focused solution navigation, short qualification/contact interface, privacy disclosure, launch checklist and manual marketing pack. No Growth OS runtime copied into this branch. Its working demo link depends on PR #9 being approved/integrated first.

## Tested client journey

Homepage `#work` → `solutions/` → `work/growth-os/` → filters / sample operator queue / scenario / JSON → return to homepage `#work` → `#experience` → three-step requirements draft → use in project review → `#contact` → copy local brief. An owner-approved email configuration will enable a mailto draft. Instagram and WhatsApp Business are secondary configurable links; **no Telegram**. No invented recipient. Opening a composer never claims delivery.

Integration QA serves the PR #9 worktree through an explicitly documented local HTTP overlay. It does not merge branches, publish a preview or prove public availability. Plain standalone main-branch hosting cannot resolve Growth OS until that dependency is integrated. Do not release these links separately.

## GO / NO-GO

| Gate | Current evidence | Decision |
| --- | --- | --- |
| Approved homepage/emblem preserved | Original asset untouched; five-width pixel comparison against approved main in QA | Ready for review |
| One useful functional example | Growth OS filters, arithmetic, queue, opt-out, export and flow tested in Chromium | Ready for owner review, not yet accepted |
| Honest second example | Experience Lab is explicitly a requirements tool, not a full case study | Ready for review |
| Honest content | Synthetic-data labels, no real clients/ROI claims; other five demos in development | Ready for review |
| Mobile/navigation | 1440/1024/768/390/360 Chromium; native fallback and clipboard failure paths | Tested locally |
| Inbound contact | Owner selected email primary + Instagram + WhatsApp Business; exact values not provided | **P0 blocked: configuration and delivery test** |
| Legal/operator disclosure | Limited browser-local disclosure implemented; legal identity/retention/provider details remain unconfirmed | **Owner input required before public collection** |
| Working public URL | None deployed or verified; two-PR integration pending | **Blocked until review and authorized staging** |
| Canonical/SEO/share | Title/description/favicon/relative OG present; canonical origin, absolute share URL/image, robots and sitemap need actual domain | **Launch configuration pending** |
| Cross-browser / performance | Chromium and no-JS covered; actual Safari/iOS, Firefox and modest-device checks remain | **Release QA pending** |
| Traffic/CTA | Draft first-week pack, manual CTA and CRM mapping prepared | Not posted/sent; link only after accessible URL exists |
| Credentials/privacy | No new credentials, trackers or server submissions; config is public | Review before release |

## Owner-supplied contact setup

Edit public `contact-config.json`: `email`, `instagramUrl` (https://www.instagram.com/...), `whatsappUrl` (https://wa.me/...), and `ownerApproved: true` only after confirming account ownership. Do not add passwords, API keys or private tokens. Leave `deliveryVerified: false` until a controlled test email from an independent sender reaches the owner and a reply reaches that sender. Also test a manual Instagram DM and WhatsApp message with permission. No test messages were sent by this work.

Email is the primary brief path; Instagram and WhatsApp open the owner's confirmed account, without uploading form content. Mailto needs a configured email app. Copy/manual fallback stays available. A provider endpoint can be scoped later; no fake form backend.

## Reproduction / evidence

`node --check main.js` and `node --check contact.js`; `python3 tests/client_ready_browser.py` (set `NCNS_GROWTH_WORKTREE` to checked-out PR #9); `python3 tests/approved_hero_regression.py` (baseline `origin/main`, Pillow + Chromium). Screenshots, contact captures, local overlay results, original-vs-current hero comparisons and an Experience Lab recording live in `docs/qa/first-clients/`.

For this environment the system Chromium/FFmpeg were used. For Playwright video, either install its normal encoder with `python3 -m playwright install ffmpeg` or point `PLAYWRIGHT_BROWSERS_PATH` to a temporary cache containing `ffmpeg-1011/ffmpeg-linux` linked to the installed compatible system encoder. No production service is started by these tests.

[Deployment runbook](deployment.md) · [Manual marketing pack](marketing/README.md) · [Draft PR body](PR.md)
