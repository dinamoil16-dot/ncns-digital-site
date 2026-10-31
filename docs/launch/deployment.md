# Agency release preparation — no portfolio prerequisite

No merge, publishing, hosting purchase or DNS edit is performed by this runbook or its preparation script. Owner reviews the finished main website first. Growth OS and other demos stay deferred in their own branches.

## Owner decisions still needed

- Selected canonical origin: **`https://ncns.digital`**, configured in `site-config.json` solely for build preparation. **Domain NOT purchased or activated**; real registry availability and final purchase price are confirmed again at checkout. Prefer apex domain with optional `www` redirect.
- Chosen hosting provider: **Cloudflare Pages (Git integration)**, pending owner's Cloudflare account registration, project configuration, authorization and final launch approval. No hosting project exists yet.
- Owner-confirmed public contact links: email `ncns.digital@gmail.com`, Instagram `https://www.instagram.com/ncns.digital/` and WhatsApp `https://wa.me/79063231457`. **One Formspree test notification successfully reached Gmail; direct mailto and reply-to remain untested.**
- Legal/operating identity, necessary public contact/address, retention and host-log disclosures: **UNCONFIRMED**.

Do not invent values or publish with placeholders. A domain or provider cannot be called configured until verified.

## Contact configuration and actual delivery

Public `contact-config.json` holds only public values, not passwords. Email/Instagram/WhatsApp have been owner-confirmed and configured. Direct form submission uses the **owner-provided Formspree endpoint** `https://formspree.io/f/mjyyagao` and is enabled in the website preview. The client-side script allows only `https://formspree.io/f/FORM_ID` URLs. Do not put a provider API key or Gmail password in browser code, GitHub or public JSON. [Owner setup and receipt test](FORM-DELIVERY.md). No Telegram.

The main contact form now has a real AJAX submission workflow, mandatory name/reply email/project description/privacy acceptance, provider statuses and fallback links. A provider 2xx response confirms acceptance, **not** inbox arrival. Separately, the manual `mailto:` action opens a draft for the visitor to send. The owner supplied a Formspree endpoint, and one uniquely marked synthetic POST was accepted by Formspree and independently observed as a notification at `ncns.digital@gmail.com` (2026-10-31 16:54 UTC). `formDeliveryVerified: true` documents that **inbound notification**. The real on-site browser test after deployment and Reply-To round-trip remain outstanding (`formReplyVerified: false`). Repeat checks on the final domain and test owner-approved WhatsApp/Instagram links. Do not upload real private enquiry content to GitHub.

## Static artifact / SEO preparation

Source is plain HTML/CSS/JS. No framework build or server backend is needed. `site-config.json` deliberately leaves `canonicalOrigin` empty. Once the owner approves a real HTTPS origin, set it there and run:

```sh
python3 scripts/prepare_site.py --output /tmp/ncns-reviewed-static
```

Use a new output directory outside the repository. The script refuses an absent/invalid origin or existing output, copies a strict public allowlist, excludes `.git`, tests, internal docs/QA and marketing drafts, and writes actual canonical/og:url metadata, absolute social image URLs, robots and sitemap. It does not deploy or enable contact delivery. Includes only agency pages/assets; no Growth OS runtime required. Reserved QA-origin preparation was tested in a temporary directory, not published.

Source `robots.txt` has no invented sitemap URL. Prepared production sitemap lists home and service directory; privacy/terms remain noindex until legal review. Structured data lists real service capabilities, not fake clients, ratings or completed integrations. Recheck social-card crop and absolute URL from the real host.

## Recommended Cloudflare Pages Git-based launch (after domain purchase and final approval)

Cloudflare Registrar public domain search showed `ncns.digital` available as a standard registration at USD $32.20 for the first year and annual renewal (as of 2026-10-31); a definitive availability and billing check occurs in Cloudflare checkout. This repository has **not** registered the domain, created a Pages project, updated DNS, or deployed.

**First purchase:** in the owner's Cloudflare account, Domains > Register domains > Search `ncns.digital` > Purchase. Choose one year, verify the final price and premium status, supply legitimate registrant contact and payment details privately, enable 2FA, and verify both Cloudflare and ICANN registrant emails. Domain auto-renew is enabled by default unless the owner changes it. No credentials are needed by the development team.

**Then Git deployment:**
1. Ensure PR #14 is up to date with latest main and all tests pass. **Do not use stale `main`**; the approved complete website and Formspree configuration currently reside in the draft PR branch `codex/issue-13-client-ready`. Merge only after the owner approves this explicit release step.
2. Cloudflare dashboard > **Workers & Pages > Create application > Pages > Connect to Git**. Grant GitHub access narrowly to `dinamoil16-dot/ncns-digital-site`.
3. Production branch **`main` only after the approved site is merged**. Framework preset: **None**; root directory: repository root; build command: `python3 scripts/build_pages.py`; build output directory: `dist`. No extra frontend package manager or credentials. This command creates only an allowlisted public build, with `index.html`, styles, app JS, contact configuration, assets, sitemap, privacy and terms. The source tree, docs, internal QA, Git and CI data must NOT be deployed.
4. Before first public deployment, examine the GitHub commit and staging settings. Git integration deploys automatically by default; disable automatic production deployments as required until the owner's explicit authorization. After approval, deploy and obtain the provider-generated `*.pages.dev` URL; verify it and check no internal files such as `/docs/` or `/AGENTS.md` are available.
5. In Pages project **Custom domains > Set up a domain**, enter `ncns.digital`. Cloudflare Registrar manages its own authoritative nameservers and Cloudflare Pages can add the required zone/CNAME. **Do not invent any A, AAAA or CNAME values** or manually add a duplicate record. Check that `https://ncns.digital` serves the expected homepage with valid TLS. Add an owner-approved `www` alias/redirect separately.
6. Verify the domain-specific canonical/OG/robots/sitemap from the prepared build. Perform a real browser contact form submission to the owner-approved Formspree endpoint `https://formspree.io/f/mjyyagao`, independently observe the email at `ncns.digital@gmail.com`, and verify a reply to the sender. Existing one-time Formspree-to-Gmail receipt verification **does not replace production-origin testing**.
7. Confirm legally accurate operator details and Formspree/hosting retention handling, and test desktop, iPhone Safari, Android and Firefox. Owner authorizes public launch only after those gates.

The app build helper is `scripts/build_pages.py`, which invokes the strict external-temp allowlist in `scripts/prepare_site.py`. `tests/site_release_build.py` tests it and deletes the temporary local `dist` output; no network or deployment occurs. Cloudflare's `dist` directory is ignored by Git. No scripts require Gmail passwords or account tokens.

Official references: https://developers.cloudflare.com/registrar/get-started/register-domain/ ; https://developers.cloudflare.com/pages/get-started/git-integration/ ; https://developers.cloudflare.com/pages/configuration/custom-domains/

## Staging and hosting

After explicit staging authorization, deploy only the prepared artifact to the chosen static host. Publish directory is artifact root; no build command. Preserve `/solutions/` directory indexes, relative assets and real 404s; do not use an SPA catch-all. No API keys belong in public JSON. Use TLS, least-privilege deploy credentials and a rollback artifact. Disable automatic production deploy-on-push until separately approved.

Use the provider's exact A/AAAA/CNAME values for the chosen hostname; no DNS values can be supplied before provider/domain decisions. Confirm propagation, TLS and one canonical redirect. Keep staging access-restricted and noindex at host level, then deliberately verify production indexing settings. Configure supported security headers (at minimum nosniff and a suitable referrer policy), and test any CSP against local fonts, images and existing inline-style motion before enforcing it.

## Final release acceptance

1. Review PR #14 screenshots and functional result. Growth OS PR #9 stays deferred; do not merge it as a release dependency.
2. Repeat all five-width Chromium tests and `python3 tests/contact_submission_browser.py` plus real Safari/iOS and Firefox checks, modest-device loading, keyboard, no-JS/font/clipboard/config failure paths and reduced motion. Browser mocks alone do NOT test inbox delivery; check no unavailable portfolio routes.
3. Primary Formspree inbox delivery was tested once; reconfirm via live website browser on real hosting and test the Reply-To flow. Confirm legal details and provider retention before release.
4. Open the authorized staging/public link on a separate device: home → service pillar → scope → project brief → actual contact. Verify metadata/social image/canonical/robots/sitemap and that internal docs/QA cannot be fetched from the artifact.
5. Present exact URL, evidence and remaining risks for final release approval. Only then discuss production publication. Never equate local testing or a staging URL with a public launch.
6. After an authorized release, verify contact delivery again and retain a rollback path. Resume portfolio and marketing production only after the owner approves the completed main site.
