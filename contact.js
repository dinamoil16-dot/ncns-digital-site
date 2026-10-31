/* NCNS Digital — direct contact and owner-approved form delivery.
   Public config contains no credentials; only Formspree endpoints are accepted.
   Form success means accepted by the provider, NOT confirmed inbox delivery. */
(() => {
  "use strict";

  const $ = id => document.getElementById(id);
  const form = $("briefForm");
  const emailBrief = $("emailBrief");
  const deliveryStatus = $("contactDelivery");
  const submitButton = $("submitEnquiry");
  const sendStatus = $("sendStatus");

  if (!form || !emailBrief || !deliveryStatus || !submitButton || !sendStatus) return;

  const state = { endpoint: "", sending: false, sent: false };
  const emailPattern = /^[a-zA-Z0-9.!#$%&'*+/=?^`{|}~-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  const formspreeEndpoint = /^https:\/\/formspree\.io\/f\/[A-Za-z0-9_-]{5,80}$/;

  function setSendState(message, kind) {
    sendStatus.textContent = message;
    if (kind) sendStatus.dataset.state = kind;
    else delete sendStatus.dataset.state;
  }

  function allowContactLink(config, key, id, pending, host, approvedFlag) {
    if (config.ownerApproved !== true && config[approvedFlag] !== true) return;
    try {
      const url = new URL(config[key]);
      if (url.protocol !== "https:" || url.hostname !== host || url.username ||
          url.password || url.port || url.pathname === "/") return;
      const el = $(id);
      if (!el) return;
      el.href = url.href;
      el.hidden = false;
      if ($(pending)) $(pending).hidden = true;
    } catch (_) { /* Keep original safe link or pending display. */ }
  }

  function updateEmailDraft(email) {
    const body = [
      "NCNS Digital — project review request",
      "Name: " + $("visitorName").value.trim(),
      "Email: " + $("visitorEmail").value.trim(),
      "Need: " + $("projectType").value,
      "Outcome: " + $("projectDetails").value.trim(),
      "Current website/process: " + $("currentProcess").value.trim(),
      "Preferred reply: " + $("replyChannel").value.trim()
    ].join("\n");
    emailBrief.href = "mailto:" + email +
      "?subject=" + encodeURIComponent("NCNS project review request") +
      "&body=" + encodeURIComponent(body);
  }

  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (state.sending || state.sent) return;
    if (!state.endpoint) {
      setSendState("Online submissions are not connected yet. Please email us or use Instagram or WhatsApp.", "error");
      return;
    }
    if (!form.checkValidity()) {
      form.reportValidity();
      setSendState("Please complete your name, a valid email, project details and the privacy checkbox.", "error");
      return;
    }

    const name = $("visitorName").value.trim();
    const email = $("visitorEmail").value.trim();
    const message = $("projectDetails").value.trim();
    if (name.length < 2 || !emailPattern.test(email) || !message) {
      setSendState("Please provide your name, a valid email address and a short description of your project.", "error");
      (name.length < 2 ? $("visitorName") : !emailPattern.test(email) ? $("visitorEmail") : $("projectDetails")).focus();
      return;
    }
    if ($("contactWebsite").value.trim()) {
      setSendState("Your request could not be processed. Contact us directly by email.", "error");
      return;
    }

    const data = new FormData();
    data.set("name", name);
    data.set("email", email);
    data.set("service", $("projectType").value);
    data.set("message", message);
    data.set("existing_process", $("currentProcess").value.trim());
    data.set("preferred_reply", $("replyChannel").value.trim());
    data.set("contact_permission", $("privacyConsent").value);
    data.set("_subject", "New NCNS Digital project enquiry");
    data.set("_gotcha", "");

    state.sending = true;
    submitButton.disabled = true;
    submitButton.textContent = "SENDING…";
    setSendState("Sending your request securely…");

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(state.endpoint, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
        credentials: "omit",
        signal: controller.signal
      });
      if (!response.ok) {
        if (response.status === 429) throw new Error("rate_limited");
        throw new Error("provider_rejected");
      }
      state.sent = true;
      setSendState("Request accepted. Thank you — we will review your project and reply to your email. If you do not hear back, you can contact us directly using the icons above.", "success");
      submitButton.textContent = "REQUEST SUBMITTED ✓";
      // Preserve the filled brief so the visitor does not lose their work.
    } catch (error) {
      const message = error && error.message === "rate_limited"
        ? "Too many requests. Please wait and try again, or email us directly."
        : error && error.name === "AbortError"
          ? "The request timed out. Please check before retrying to avoid a duplicate, or contact us directly."
          : "We could not confirm your submission. Your details are still here; please try again or use an icon above.";
      setSendState(message, "error");
    } finally {
      clearTimeout(timeout);
      state.sending = false;
      if (!state.sent) {
        submitButton.disabled = !state.endpoint;
        submitButton.textContent = "SEND PROJECT REQUEST →";
      }
    }
  });

  fetch("./contact-config.json", { cache: "no-store" })
    .then(r => { if (!r.ok) throw new Error("Configuration unavailable"); return r.json(); })
    .then(config => {
      allowContactLink(config, "instagramUrl", "instagramContact", "instagramPending", "www.instagram.com", "instagramApproved");
      allowContactLink(config, "whatsappUrl", "whatsappContact", "whatsappPending", "wa.me", "whatsappApproved");

      const email = typeof config.email === "string" ? config.email.trim() : "";
      if (config.ownerApproved === true && emailPattern.test(email)) {
        emailBrief.hidden = false;
        if ($("emailPending")) $("emailPending").textContent = email;
        const directEmail = $("emailContact");
        if (directEmail) {
          directEmail.href = "mailto:" + email;
          directEmail.setAttribute("aria-label", "Email NCNS Digital at " + email);
        }
        form.addEventListener("input", () => updateEmailDraft(email));
        emailBrief.addEventListener("click", event => {
          if (!$("projectDetails").value.trim()) {
            event.preventDefault();
            deliveryStatus.textContent = "Describe your business need and desired outcome first.";
            $("projectDetails").focus();
            return;
          }
          updateEmailDraft(email);
          deliveryStatus.textContent = "Opening your email application. Review and send the message there; this page cannot confirm mail delivery.";
        });
        updateEmailDraft(email);
        deliveryStatus.textContent = config.deliveryVerified === true
          ? "For a manual email, open the draft and press Send in your mail app."
          : "This email recipient is available, but delivery has not been verified. You can also copy your brief.";
      }

      const endpoint = typeof config.formEndpoint === "string" ? config.formEndpoint.trim() : "";
      if (config.formProvider === "formspree" && config.formEnabled === true && formspreeEndpoint.test(endpoint)) {
        state.endpoint = endpoint;
        submitButton.disabled = false;
        setSendState("Send the form directly to NCNS Digital. Your project details will be processed by Formspree and forwarded to our work inbox.");
      } else {
        submitButton.disabled = true;
        setSendState("Direct form sending is not connected yet. Use the email, Instagram or WhatsApp icons above.");
      }

      const note = document.querySelector(".contact-note");
      if (note) note.textContent = state.endpoint
        ? "Tell us about your project and press Send Project Request — no email application required. Or choose a direct-contact icon below."
        : "Online project enquiries are being connected. In the meantime use email, Instagram or WhatsApp, or prepare and copy your project brief.";
    })
    .catch(() => {
      submitButton.disabled = true;
      setSendState("Form service configuration is unavailable. Use the email, Instagram or WhatsApp icons instead.", "error");
      deliveryStatus.textContent = "Automatic project-email preparation is unavailable. Use the direct email, Instagram or WhatsApp links, or copy your brief. No message has been sent.";
    });
})();
