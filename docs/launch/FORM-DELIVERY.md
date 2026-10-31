# NCNS Digital — automatic project enquiries into the business inbox

**Status:** The website contains a working Formspree AJAX submission workflow. **It is intentionally disabled until the owner creates and confirms a real Formspree form ID and verifies email delivery.** The current contact icons remain live; no domain purchase or public deployment has occurred.

## What is already implemented
- A form on the agency Contact section with name, required reply email, selected service, project description, optional existing workflow and preferred reply method.
- A required consent checkbox and hidden Formspree `_gotcha` anti-spam field.
- A clear **Send Project Request** button. Once configured, it sends the form data in the background through Formspree with a JSON-aware cross-origin request.
- Visible sending/success/rejection/rate-limit/timeout states. Prevent duplicate clicks; preserve text after an error and preserve it after success. A successful provider response means **accepted by the form service**, not guaranteed notification delivery to the owner.
- A separate Copy Project Brief and optional manual email-draft link as fallbacks.
- Email, Instagram and WhatsApp icons remain clickable. Hero, design, all service sections and deferred portfolio are untouched.
- No API secret or Gmail password is stored in the public site or GitHub.

## One-time setup the owner must do — no need to buy the domain first
1. Visit **https://formspree.io/** and create or log into the owner-managed account. Verify the account email.
2. In the dashboard, choose **New Form**, name it `NCNS Digital — Project Enquiries`, and select **ncns.digital@gmail.com** as the target notification email. Confirm/verify the destination address if Formspree requests it. Confirm email-notification workflow is enabled.
3. In **Integration**, copy the endpoint URL that looks like `https://formspree.io/f/xxxxxxxx`. **The ID is public form routing metadata**, not a secret API key, but still use the exact URL, not a made-up value.
4. Send the endpoint URL to the development assistant for a review. We will place it in `contact-config.json`:
   ```json
   {
     "formProvider": "formspree",
     "formEndpoint": "https://formspree.io/f/<actual-form-id>",
     "formEnabled": true,
     "formDeliveryVerified": false
   }
   ```
   Do not paste anything containing a personal password, API key, Gmail login, OAuth token, session cookie or 2FA code.
5. Test with a **controlled real submission** from the website preview: fill name, reply email, service and business need, consent, click **Send Project Request**, verify success status. Confirm the message exists in the Formspree submissions dashboard, then confirm actual receipt at `ncns.digital@gmail.com` (check Spam as needed) and that a reply reaches the sender.
6. Only **after a real end-to-end receipt/reply test**, mark `formDeliveryVerified: true` and update release readiness. Provider acceptance alone is insufficient. During testing, the site still must not be merged or published without the owner's separate approval.
7. After the custom domain is approved and deployed: configure Formspree domain restrictions for that public origin, review spam controls/reCAPTCHA and privacy terms, perform another real inbox test, and verify deliverability/response handling on desktop and mobile.

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
Browser tests mock the third-party endpoint and never submit a real message. A green browser test is **not** proof that an email landed in the owner's inbox.
