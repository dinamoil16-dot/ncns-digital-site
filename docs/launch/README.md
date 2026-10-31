# NCNS Digital — live release status
As of 31 October 2026.

## Confirmed
- Owner approved complete agency website: 12 service families, five pillars, Experience Lab, Build / Operate / Grow, responsive layouts, approved cinematic hero and original logo.
- **Live:** https://ncns.digital/ (Cloudflare Registrar + Cloudflare Pages, valid HTTPS) and https://ncns-digital-site.pages.dev/
- Formspree direct enquiry `https://formspree.io/f/mjyyagao` active. A labelled synthetic enquiry submitted from the **live custom domain** returned provider acceptance and the matching email arrived at `ncns.digital@gmail.com`.
- Public contact links: email, Instagram `@ncns.digital`, WhatsApp; icon-only links in Contact and footer. No public Telegram.
- Browser QA: Chromium five viewport sizes (1440, 1024, 768, 390, 360), approved hero regression, mocked form tests, public-bundle allowlist and genuine 404-page source. The public release excludes internal docs, tests and repository files.
- `https://ncns.digital/sitemap.xml`, `robots.txt`, canonical and OG metadata exist.

## GitHub release workflow
- PR #14 was reviewed, passed CI and **merged** as `0be2f474` into `main`. Cloudflare Pages must still switch production from `codex/issue-13-client-ready` to `main` manually. Merging alone will not change the Pages production branch.
- A GitHub Actions green check tests build and browser behavior; it does **not** verify actual iOS Safari, Firefox or live client email reply-to handling.
- `scripts/build_pages.py` builds public `dist` from the source without deploying internal documentation.
- Prior draft text claiming 'no domain' or 'no active form' is historical and superseded by this live release status.

## Incomplete tasks
1. Owner confirmed NCNS Digital is an **individual-operated, unregistered international freelance brand**, not a separate company. Privacy/Terms now state this transparently. Check the operator's actual legal/tax jurisdiction, mandatory legal identity/address disclosures and Formspree/Gmail retention before accepting paid engagements; the brand's international positioning does not remove legal obligations.
2. PR #14 merged into `main`; switch Pages Production branch to `main`, verify new production deployment and rollback ability.
3. **Completed:** `ncns.digital` verified in Google Search Console, `https://ncns.digital/sitemap.xml` submitted, owner requested indexing of homepage and services. Actual Google indexing is not yet confirmed.
4. **Owner confirmed:** the site works on iPhone and Android. **Owner confirmed a successful email reply to the self-addressed test.** An optional follow-up using a distinct external sender can additionally validate client Reply-To routing. Firefox review remains optional.
5. Optionally forward `www.ncns.digital` and `ncns-digital-site.pages.dev` to the canonical `https://ncns.digital`.

The six portfolio concept demos are separate and not prerequisites to receiving first paid enquiries. Marketing and outreach should link only to the live approved site.

[Detailed operations runbook](deployment.md) · [Contact receipt evidence](FORM-DELIVERY.md) · [Browser evidence](../qa/agency-site/README.md).
