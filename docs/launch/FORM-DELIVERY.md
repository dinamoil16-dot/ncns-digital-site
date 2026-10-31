# NCNS Digital — automatic project enquiries into the business inbox

**Status as of 2026-10-31:** The owner supplied `https://formspree.io/f/mjyyagao`; `formEnabled: true`. **Real Formspree-to-Gmail delivery is VERIFIED.** Exactly one synthetic test POST from CI returned **HTTP 200** and `{"next":"/thanks","ok":true}`. Its uniquely marked Formspree notification reached the connected **`ncns.digital@gmail.com`** mailbox at **2026-10-31 16:54 UTC**. The temporary real-send CI step was immediately removed and is not included in subsequent tests. `formDeliveryVerified: true`, `formReplyVerified: false` (the reply-to flow was not independently tested). This verifies **form processing and inbox arrival**, not Safari/production domain behavior or ongoing guaranteed delivery. **No domain purchased, PR merged or site published.**

## What is already implemented
- A form on the agency Contact section with name, required reply email, selected service, project description, optional existing workflow and preferred reply method.
- A required consent checkbox and hidden Formspree `_gotcha` anti-spam field.
- A clear **Send Project Request** button. Once configured, it sends the form data in the background through Formspree with a JSON-aware cross-origin request.
- Visible sending/success/rejection/rate-limit/timeout states. Prevent duplicate clicks; preserve text after an error and preserve it after success. A successful provider response means **accepted by the form service**, not guaranteed notification delivery to the owner.
- A separate Copy Project Brief and optional manual email-draft link as fallbacks.
- Email, Instagram and WhatsApp icons remain clickable. Hero, design, all service sections and deferred portfolio are untouched.
- No API secret or Gmail password is stored in the public site or GitHub.

## Owner account checks and one-time live delivery test — no domain purchase required
1. Sign in at **https://formspree.io/** using the account that created the form. Confirm the recipient/notification destination for this form is **`ncns.digital@gmail.com`**, and complete any email verification it requires.
2. Current public client configuration (already committed):
   ```json
   {
     "formProvider": "formspree",
     "formEndpoint": "https://formspree.io/f/mjyyagao",
     "formEnabled": true,
     "formDeliveryVerified": true,
    "formReplyVerified": false
   }
   ```
   This URL is public routing metadata, not a secret API key. Never paste a Gmail password, API key, session cookie, OAuth token or 2FA code into GitHub or this chat.
3. **Completed one provider delivery test:** the verified owner endpoint accepted a synthetic POST and the Formspree notification arrived in Gmail. The code path was called directly from temporary CI (not a deployed page). The on-site browser form still has mocked integration QA only. After domain/staging are available, perform a real browser submission from the final site and reconfirm receipt.
4. **Still outstanding:** verify the reply-to path with an external test sender, and retest a real browser submission once a staging/production origin exists. Mark `formReplyVerified: true` only after checking the reply arrives. The current `formDeliveryVerified: true` documents the confirmed incoming notification, not the untested reply.
5. After final domain approval and publication, confirm allowed origins, spam controls, policy/retention and real end-to-end mail delivery on desktop and mobile again. No host deployment, PR merge, or domain purchase is authorized at this stage.

### Provider facts and trade-offs
Formspree is a third-party service that processes and stores form content and forwards the notification to the chosen email. Its **free tier currently advertises 50 submissions/month**, basic spam filtering, CAPTCHA and AJAX submissions; check the live dashboard before depending on limits or retention. Formspree sends notifications from its service email; custom branded sending may require a paid tier/verified domain. The site does not need a dedicated backend or a custom domain solely to run an owner-verified Formspree endpoint.

Sources:
- https://help.formspree.io/articles/building-your-form/building-an-html-form
- https://help.formspree.io/articles/building-your-form/submit-forms-with-javascript-ajax
- https://help.formspree.io/articles/troubleshooting/how-to-prevent-spam/
- https://formspree.io/plans

## Security and privacy review
- Do not connect forms until the owner has reviewed the form processor's privacy requirements and published an accurate privacy/contact notice and legal operator details.
- Do not promise irreversible security guarantees, zero spam or 100% delivery.
- Server-side spam/validation/rate limiting relies on the form provider, not just browser checks. The public endpoint may receive spam; use provider dashboard controls.
- Do not submit real prospect/customer records while doing development QA. Browser tests use mocked Formspree responses only.
- Contact details are shown publicly as the owner approved. No Telegram public contact is included.
- The mailto link is a **manual alternative**, not an automatic submission.
- Domain, hosting, legal disclosures, and production email receipt verification remain explicit launch blockers.

## Reproducible QA
```sh
node --check contact.js
python3 tests/contact_submission_browser.py
python3 tests/agency_site_browser.py
```
Normal browser tests mock the third-party endpoint and never submit a real message. One temporary **separately identified** synthetic POST was sent for actual delivery verification and then removed from CI. Ordinary tests must never contact the real endpoint. A green browser test is **not** proof that an email landed in the owner's inbox.
