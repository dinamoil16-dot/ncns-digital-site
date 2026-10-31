# Growth OS — real browser verification for existing PR #9

The original prototype now has a user-selected, animated acquisition → qualification → won → action-plan mechanism linked to the real selected sample data. Inspect Sell to enter the separate operator queue. Motion can be paused and respects reduced motion. No decorative 3D, forced intro or external calls.

Fixed a real mobile min-content grid overflow, invalid default range step (1590 now fits step 10), loss of keyboard focus on stage rerenders and stale closed-task state when a deal is reopened. A reset restores the fictional queue. Added favicon and a visible no-JavaScript explanation; runtime controls require JS. The original agency homepage and emblem are untouched.

## Verification

`node --check work/growth-os/app.js`

`python3 tests/growth_os_browser.py`

Playwright uses installed Chromium when present, otherwise its bundled Chromium. Install its video encoder with `python3 -m playwright install ffmpeg`; this environment instead used compatible system FFmpeg through a temporary `/tmp/ncns-playwright/ffmpeg-1011/ffmpeg-linux` symlink and `PLAYWRIGHT_BROWSERS_PATH=/tmp/ncns-playwright`. The normal CI workflow installs the bundled browser/encoder. No deployment is part of testing.

[Results](results.json): 1440, 1024, 768, 390 and 360 px. Initial 288 leads / 86 qualified / 20 won / $31,800 sample revenue; channel/period switching; keyboard range adjustment; default scenario $31,596 revenue / $5,039 contribution (not profit); stage close/reopen; focus retention; two due tasks; completion/reset; opted-out row has no follow-up action; forced clipboard-failure manual copy; parsed local JSON content; no horizontal overflow, JS errors, failed resources, external requests or non-GET operations. No-JS capture included. These are local Chromium checks, not an asserted GitHub Actions run, Safari certification or real-world performance/ROI evidence.

## Real visual evidence

- `opening-1440.png`, `opening-390.png`, `opening-360.png`: opening frame.
- `full-<width>.png`: complete page at all five widths.
- `journey-<width>.png`, `overview-<width>.png`, `pipeline-<width>.png`, `scenario-<width>.png`, `plan-<width>.png`: inspectable customer/operator states.
- [Desktop walkthrough](walkthrough-1440.webm), [mobile walkthrough](walkthrough-390.webm): genuine normal-motion Chromium recordings, approximately 16 seconds each. They show stage selection, filtering, scenario change, local task completion and plan copying; never a sent message. Frames were inspected, not generated.
- `download-<width>.json`: synthetic exported sample plans. No genuine leads or contacts.

## Readiness and commercial meaning

For an owner/revenue operations team, the paid scope would be connected sources, agreed qualification rules, a CRM/operator workflow, measurement plan and handover. Optional Operate care covers agreed integration/rule reliability; Grow means measured experiments. Client retains data access. The local prototype demonstrates these mechanisms, not completed production integrations.

NO-GO for public launch: owner must review/accept this demo; separate Issue #13 conversion integration, contact values and delivery verification, domain/hosting choices and release QA remain. No real CRM, AI, messaging, tracking, deployment or merge. The other five complete demos are deferred until MVP launch readiness.
