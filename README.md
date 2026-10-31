# NCNS Digital — agency website

**Live website:** https://ncns.digital/

An independent, international-facing AI and digital agency website. The owner approved the cinematic dark/chrome hero and its original NCNS emblem. The site contains 12 service families in five pillars, Build → Operate → Grow, a browser-only Experience Lab, a project enquiry form and public contact links.

## Hosting and delivery

- Hosting: **Cloudflare Pages**, project `ncns-digital-site`; secondary URL https://ncns-digital-site.pages.dev/
- GitHub: `dinamoil16-dot/ncns-digital-site`. PR #14 has been merged into stable `main` (squash commit `0be2f474`). **Cloudflare Pages production deployment from `main` is verified:** a unique, temporary change to generated `robots.txt` appeared at `https://ncns.digital/` and then disappeared following its removal from `main`. The current published site follows `main`.
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

1. **Operator status confirmed:** NCNS Digital is an independent, unregistered freelance service brand operated by an individual; it is not a separate incorporated company. Privacy and Terms reflect this without inventing a country or company. **Still required:** assess the individual's actual tax/registration obligations and any mandatory legal name/address disclosures for relevant jurisdictions, plus Formspree/Gmail data retention. Privacy contact: `ncns.digital@gmail.com`.
2. **Completed:** PR #14 integrated into `main`; production deployment from `main` confirmed with a harmless public marker that was then removed. Keep branch review, green CI and rollback checks for future releases.
3. **Domain verified in Google Search Console**; `https://ncns.digital/sitemap.xml` submitted on 31 October 2026 (Google displayed “Sitemap sent”). At submission time its status was “Not received” / 0 indexed pages while Google had not processed it. **The owner subsequently requested indexing of both** `https://ncns.digital/` and `https://ncns.digital/solutions/` in Search Console. Actual indexing is not yet confirmed.
4. **Owner checked Android and iPhone:** site renders and functions normally. Further optional Firefox review and Reply-To test with an external email remain; redirects for `www.ncns.digital` and `pages.dev` are optional.

No fabricated portfolio, client logos, revenue claims or completed customer cases appear on the site. Portfolio concepts and marketing launch are separate future work.

Full operational detail: [deployment runbook](docs/launch/deployment.md) · [contact delivery QA](docs/launch/FORM-DELIVERY.md).
