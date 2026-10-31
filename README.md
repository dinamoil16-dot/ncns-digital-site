# NCNS Digital — agency website

**Live website:** https://ncns.digital/

An independent, international-facing AI and digital agency website. The owner approved the cinematic dark/chrome hero and its original NCNS emblem. The site contains 12 service families in five pillars, Build → Operate → Grow, a browser-only Experience Lab, a project enquiry form and public contact links.

## Hosting and delivery

- Hosting: **Cloudflare Pages**, project `ncns-digital-site`; secondary URL https://ncns-digital-site.pages.dev/
- GitHub: `dinamoil16-dot/ncns-digital-site`. PR #14 has been merged into stable `main` (squash commit `0be2f474`). **Cloudflare Pages remains configured to deploy `codex/issue-13-client-ready` until the owner changes its Production branch to `main`.** Do **not** assume production follows `main` until Pages settings are changed.
- Build command: `python3 scripts/build_pages.py`, output directory `dist`, no framework.
- `scripts/prepare_site.py` generates the safe public allowlist, canonical metadata `https://ncns.digital/`, `robots.txt`, `sitemap.xml` and a branded `404.html`; source docs, CI files and internal tests must never be included in the deployment directory.
- Cloudflare Pages automatically deploys selected production-branch commits when Git integration is enabled. Review the build result after each intended deployment.

## Enquiries

The live contact form submits via Formspree `https://formspree.io/f/mjyyagao` to `ncns.digital@gmail.com`. A controlled browser submission **from the live `ncns.digital` site** was accepted and the corresponding notification appeared in that Gmail inbox on 31 October 2026. This verifies one end-to-end inbound message; it is not a guarantee of universal delivery. The Reply-To round-trip is still to be checked with a distinct test sender.

Contact icons in both Contact and footer link to email, Instagram `@ncns.digital` and WhatsApp. The Experience Lab is a local draft builder, **not an AI agent, CRM or a submitted enquiry**.

## Development and checks

Run locally from repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

On Windows double-click `REVIEW-SITE-WINDOWS.bat` (requires Python). Neither method makes a production deployment.

```sh
node --check main.js && node --check contact.js
python3 tests/site_release_build.py
python3 tests/agency_site_browser.py
python3 tests/contact_submission_browser.py
python3 tests/approved_hero_regression.py
python3 tests/agency_before_after.py
```

Browser tests use mock Formspree responses and never send a real enquiry. `tests/site_release_build.py` builds a temporary release and verifies only public files are included. Do not publish the repo root.

## Remaining owner tasks

1. Confirm the individual/legal entity and business jurisdiction responsible for the site, and align the live privacy disclosure, form processor retention and contractual terms with applicable law. Privacy contact: `ncns.digital@gmail.com`.
2. GitHub PR #14 is already integrated into `main`. Now change Cloudflare Pages **production branch** to `main`, verify deployment and monitor its status. Keep tests before releases. GitHub merger alone does not switch the Pages branch.
3. Configure Google Search Console for Domain property `ncns.digital` via Cloudflare DNS TXT verification. Submit `https://ncns.digital/sitemap.xml`, inspect `https://ncns.digital/` and `https://ncns.digital/solutions/`.
4. Check actual mobile Safari, Android and Firefox; confirm delivery/replies; optionally redirect `www.ncns.digital` and `ncns-digital-site.pages.dev` to the canonical host.

No fabricated portfolio, client logos, revenue claims or completed customer cases appear on the site. Portfolio concepts and marketing launch are separate future work.

Full operational detail: [deployment runbook](docs/launch/deployment.md) · [contact delivery QA](docs/launch/FORM-DELIVERY.md).
