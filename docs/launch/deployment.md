# NCNS Digital — live operations and release checklist
Updated 31 October 2026. **Site is already public:** https://ncns.digital/ and https://ncns-digital-site.pages.dev/

## Confirmed production facts
- The owner purchased `ncns.digital` via Cloudflare Registrar and connected it to Cloudflare Pages `ncns-digital-site`. The origin is served on HTTPS.
- Cloudflare Pages Git integration builds from `dinamoil16-dot/ncns-digital-site`, currently deploying branch `codex/issue-13-client-ready` although the approved code was merged into `main` as `0be2f474`.
- Framework: None; Build command: `python3 scripts/build_pages.py`; Build output directory: `dist` (repository root). Public build contains only approved site assets, pages, scripts, contact configuration, SEO and a real `404.html`; internal code-review and QA artifacts are excluded.
- Real Formspree endpoint: `https://formspree.io/f/mjyyagao`. On 31 October 2026 a single synthetic browser submission from `https://ncns.digital/` was accepted; the matching notification reached `ncns.digital@gmail.com`. Both the earlier direct provider POST and this live-site test are documented in PR #14. This is not a guarantee of future receipt. Owner later confirmed a successful self-addressed reply test. A separate external Reply-To round trip is optional for stronger validation of replies to real prospects.
- Google-compatible canonical origin: `https://ncns.digital/`; `robots.txt` and `sitemap.xml` are publicly accessible. `www.ncns.digital` redirect and Google Search Console verification are not yet confirmed.
- The approved hero, logo, site sections and 12-service structure must remain unchanged unless the owner requests a change.

## 1 — Legal and privacy handoff

The public Privacy & Contact page now explains the live Cloudflare Pages host, Formspree submissions, Gmail notification, purpose of replies, correction/deletion contact and absence of advertising trackers. Terms explain that the website is not a binding quote or service contract.

**Remaining owner input before asserting compliance:** identify the responsible legal person or registered company, applicable business country/jurisdiction, and whether any legally mandated registration/contact details must be published. This cannot safely be inferred from the domain registrar's address or the owner's temporary physical location. Obtain local legal advice if serving regulated markets.

Verify in Formspree and Gmail the actual retention/deletion settings and choose a defensible retention policy. Do not claim an automatic deletion period without implementing it. Confirm third-party policies/processor obligations where applicable.

## 2 — Bring GitHub and Cloudflare production under one stable branch

1. **Completed:** PR #14 passed CI and was merged into `main` as `0be2f474`. **Do not delete the old `codex/issue-13-client-ready` branch before Cloudflare is switched**.
2. In [Cloudflare Dashboard](https://dash.cloudflare.com/) > Workers & Pages > `ncns-digital-site` > **Settings > Builds & deployments > Production branch** (or Build > Branch control in the current UI), select **`main`** and save. Cloudflare's production branch is not changed merely by merging a PR.
3. Use Cloudflare Deployments to confirm the expected `main` commit was deployed to production, or manually trigger a production deployment if the branch switch does not deploy immediately. Avoid a blank `main` deployment: first ensure `scripts/build_pages.py`, `site-config.json` and all assets exist there.
4. Verify `https://ncns.digital` and the `*.pages.dev` alias, Contact and footer icons, 12 services, consent, form, and `/404-ncns-test-url` returning a genuine 404.
5. Consider disabling automatic production deployment on pushes until the review process is established, or require reviews / CI status checks on protected main. Keep rollback capability and use PR preview deployments for later changes.
6. Preview branches or subsequent work on separate modules must not affect this site's production.

Cloudflare documentation: https://developers.cloudflare.com/pages/configuration/branch-build-controls/ ; https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/

## 3 — SEO / indexing / mobile

Site build already generates:
- `https://ncns.digital/robots.txt` with reference to `https://ncns.digital/sitemap.xml`
- Sitemap listing `https://ncns.digital/` and `https://ncns.digital/solutions/`
- Canonical metadata, Open Graph card, service structured data and brand logo
- A real 404 page so unknown URLs are no longer silently served the homepage by Cloudflare Pages' default SPA fallback.

Owner-assisted Google Search Console:
1. Open https://search.google.com/search-console/ and sign in to the Google account that will manage the business.
2. **Add property > Domain**, enter `ncns.digital` (no https). Google provides a unique `google-site-verification=...` TXT token; it is **not** a password.
3. Cloudflare Dashboard > `ncns.digital` domain > DNS > Records > Add record: **TXT**, Name `@`, Content **the exact value Google gives you**, TTL Auto. Do not modify existing CNAME records or guess a token.
4. Back in Search Console > Verify; then **Sitemaps**, submit `https://ncns.digital/sitemap.xml` (or `sitemap.xml` if the UI prefixes the property). Use URL Inspection for homepage and service index; request indexing once if eligible.
5. Google crawling/indexing may take days or weeks and is never guaranteed. Check reports later for actual results.

Test live on iPhone Safari, Android Chrome and Firefox in addition to the automated Chromium five-width checks (1440 / 1024 / 768 / 390 / 360). Confirm keyboard navigation, contact icons, form error states, reduced-motion, and no unexpected overflow. Keep test enquiries synthetic, clearly labelled and infrequent.

Optional tidy-up: configure a 301 `www.ncns.digital` → `https://ncns.digital` with Cloudflare redirect rule + its required DNS entry, then verify HTTPS/certificates. The canonical address is already the apex; the alias is not mandatory for current function.

## Rollback and limitations
- The Pages output `dist` contains public site content only; never deploy the repository root or paste credentials into browser-visible JSON.
- GitHub and Cloudflare are separate services. Updating the repository or merging a PR changes live content **only** when the configured production branch deploys successfully.
- Production form submission was verified on 31 October 2026; a live third-party service may still reject or delay individual submissions. Check Formspree dashboard, Gmail Spam and quota if a visitor reports a problem.
- Never promise measured ROI, real clients, integrated customer AI, or an already configured CRМ based solely on this agency website.
- Keep privacy notice and terms accurate as account/legal details are finalized.

Reference sources: https://support.google.com/webmasters/answer/9008080 ; https://support.google.com/webmasters/answer/7451001 ; https://developers.cloudflare.com/pages/configuration/serving-pages/ ; https://developers.cloudflare.com/pages/how-to/www-redirect/
