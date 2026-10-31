# Agency release preparation — no portfolio prerequisite

No merge, publishing, hosting purchase or DNS edit is performed by this runbook or its preparation script. Owner reviews the finished main website first. Growth OS and other demos stay deferred in their own branches.

## Owner decisions still needed

- Canonical HTTPS domain/origin and www/apex preference: **UNSET**.
- Static hosting account/provider, staging access, budget and release approver: **UNSET**.
- Owner-confirmed public contact links: email `ncns.digital@gmail.com`, Instagram `https://www.instagram.com/ncns.digital/` and WhatsApp `https://wa.me/79063231457`. **Actual delivery remains unverified.**
- Legal/operating identity, necessary public contact/address, retention and host-log disclosures: **UNCONFIRMED**.

Do not invent values or publish with placeholders. A domain or provider cannot be called configured until verified.

## Contact configuration and actual delivery

Public `contact-config.json` holds only public values, not passwords. Email/Instagram/WhatsApp have been owner-confirmed and configured. Direct form submission uses Formspree but remains **disabled** until a verified endpoint is provided. The client-side script allows only `https://formspree.io/f/FORM_ID` URLs. Do not put a provider API key or Gmail password in browser code, GitHub or public JSON. [Owner setup and receipt test](FORM-DELIVERY.md). No Telegram.

The main contact form now has a real AJAX submission workflow, mandatory name/reply email/project description/privacy acceptance, provider statuses and fallback links. A provider 2xx response confirms acceptance, **not** inbox arrival. Separately, the manual `mailto:` action opens a draft for the visitor to send. When the owner gives a Formspree endpoint, set `formEnabled: true`, then run a genuine submission from staging and verify the Formspree dashboard plus receipt and reply in `ncns.digital@gmail.com`. Only mark `formDeliveryVerified` after independent proof; repeat checks on the final domain and test the owner-confirmed WhatsApp/Instagram links. Do not upload real private enquiry content to GitHub.

## Static artifact / SEO preparation

Source is plain HTML/CSS/JS. No framework build or server backend is needed. `site-config.json` deliberately leaves `canonicalOrigin` empty. Once the owner approves a real HTTPS origin, set it there and run:

```sh
python3 scripts/prepare_site.py --output /tmp/ncns-reviewed-static
```

Use a new output directory outside the repository. The script refuses an absent/invalid origin or existing output, copies a strict public allowlist, excludes `.git`, tests, internal docs/QA and marketing drafts, and writes actual canonical/og:url metadata, absolute social image URLs, robots and sitemap. It does not deploy or enable contact delivery. Includes only agency pages/assets; no Growth OS runtime required. Reserved QA-origin preparation was tested in a temporary directory, not published.

Source `robots.txt` has no invented sitemap URL. Prepared production sitemap lists home and service directory; privacy/terms remain noindex until legal review. Structured data lists real service capabilities, not fake clients, ratings or completed integrations. Recheck social-card crop and absolute URL from the real host.

## Staging and hosting

After explicit staging authorization, deploy only the prepared artifact to the chosen static host. Publish directory is artifact root; no build command. Preserve `/solutions/` directory indexes, relative assets and real 404s; do not use an SPA catch-all. No API keys belong in public JSON. Use TLS, least-privilege deploy credentials and a rollback artifact. Disable automatic production deploy-on-push until separately approved.

Use the provider's exact A/AAAA/CNAME values for the chosen hostname; no DNS values can be supplied before provider/domain decisions. Confirm propagation, TLS and one canonical redirect. Keep staging access-restricted and noindex at host level, then deliberately verify production indexing settings. Configure supported security headers (at minimum nosniff and a suitable referrer policy), and test any CSP against local fonts, images and existing inline-style motion before enforcing it.

## Final release acceptance

1. Review PR #14 screenshots and functional result. Growth OS PR #9 stays deferred; do not merge it as a release dependency.
2. Repeat all five-width Chromium tests and `python3 tests/contact_submission_browser.py` plus real Safari/iOS and Firefox checks, modest-device loading, keyboard, no-JS/font/clipboard/config failure paths and reduced motion. Browser mocks alone do NOT test inbox delivery; check no unavailable portfolio routes.
3. Confirm legal details and contact delivery privately. No production-ready claim before primary inbound is verified.
4. Open the authorized staging/public link on a separate device: home → service pillar → scope → project brief → actual contact. Verify metadata/social image/canonical/robots/sitemap and that internal docs/QA cannot be fetched from the artifact.
5. Present exact URL, evidence and remaining risks for final release approval. Only then discuss production publication. Never equate local testing or a staging URL with a public launch.
6. After an authorized release, verify contact delivery again and retain a rollback path. Resume portfolio and marketing production only after the owner approves the completed main site.
