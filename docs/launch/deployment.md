# Agency release preparation — no portfolio prerequisite

No merge, publishing, hosting purchase or DNS edit is performed by this runbook or its preparation script. Owner reviews the finished main website first. Growth OS and other demos stay deferred in their own branches.

## Owner decisions still needed

- Canonical HTTPS domain/origin and www/apex preference: **UNSET**.
- Static hosting account/provider, staging access, budget and release approver: **UNSET**.
- Primary business email and WhatsApp Business URL: **UNSET**. Instagram is owner-confirmed `https://www.instagram.com/ncns.digital/`.
- Legal/operating identity, necessary public contact/address, retention and host-log disclosures: **UNCONFIRMED**.

Do not invent values or publish with placeholders. A domain or provider cannot be called configured until verified.

## Contact configuration and actual delivery

Public `contact-config.json` holds only public values, never credentials. `ownerApproved: false` keeps primary email and WhatsApp disabled. Instagram has its own `instagramApproved: true` from the latest owner instruction. Set real `email` and `whatsappUrl` only after owner confirmation; then set the appropriate approval flag (`ownerApproved` or `whatsappApproved`) deliberately. Allowed WhatsApp links are HTTPS `wa.me` paths, with no embedded credentials or custom port. Do not invent numbers or add Telegram.

The email action opens a local email draft; the client must review/send in their email application. The page says it cannot confirm delivery and retains a copy fallback. Test from an independent desktop and phone: compose → send → owner confirms inbox receipt → owner replies → sender confirms reply. Repeat for the owner-approved WhatsApp and a controlled Instagram DM. Record results privately, not private message contents in git. Only mark `deliveryVerified` after actual evidence. No delivery test was performed here.

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
2. Repeat all five-width Chromium tests plus real Safari/iOS and Firefox checks, modest-device loading, keyboard, no-JS/font/clipboard/config failure paths and reduced motion. Verify primary contact button on actual devices; check no hidden/unavailable portfolio routes.
3. Confirm legal details and contact delivery privately. No production-ready claim before primary inbound is verified.
4. Open the authorized staging/public link on a separate device: home → service pillar → scope → project brief → actual contact. Verify metadata/social image/canonical/robots/sitemap and that internal docs/QA cannot be fetched from the artifact.
5. Present exact URL, evidence and remaining risks for final release approval. Only then discuss production publication. Never equate local testing or a staging URL with a public launch.
6. After an authorized release, verify contact delivery again and retain a rollback path. Resume portfolio and marketing production only after the owner approves the completed main site.
