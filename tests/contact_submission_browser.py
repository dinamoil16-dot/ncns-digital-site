"""NCNS agency Contact: direct Formspree submissions with no real external sends.

Chromium tests mock both contact configuration and provider endpoint, including
success, 429 and failures. This tests UI/client integration, NOT real inbox delivery.
"""
from pathlib import Path
import http.server
import threading
import shutil
import json

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class LocalServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *_args):
        pass


httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), LocalServer)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
origin = f"http://127.0.0.1:{httpd.server_port}"
endpoint = "https://formspree.io/f/xncnsdemo1"
config = json.loads((ROOT / "contact-config.json").read_text())
results = []


def fields(page):
    page.locator("#visitorName").fill("Example Company")
    page.locator("#visitorEmail").fill("test@example.com")
    page.locator("#projectDetails").fill("Need a quote request portal with managed follow-ups.")
    page.locator("#currentProcess").fill("Spreadsheets and email")
    page.locator("#replyChannel").fill("Reply by email")
    page.locator("#privacyConsent").check()


def configured(page, **overrides):
    sample = dict(config, formProvider="formspree", formEndpoint=endpoint, formEnabled=True, formDeliveryVerified=False)
    sample.update(overrides)
    page.route("**/contact-config.json", lambda route: route.fulfill(json=sample))


def provider(route, status=200):
    route.fulfill(
        status=status,
        headers={"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
        body=json.dumps({"ok": status == 200, "errors": [] if status == 200 else [{"message": "Try again"}]})
    )


try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which("chromium"))
        for width, height in [(1440, 900), (390, 844), (360, 780)]:
            context = browser.new_context(viewport={"width": width, "height": height})
            page = context.new_page()
            assert page.goto(origin, wait_until="networkidle").ok
            assert page.locator("#submitEnquiry").is_disabled()
            assert page.locator("#emailContact").get_attribute("href") == "mailto:ncns.digital@gmail.com"
            assert page.locator("#instagramContact").get_attribute("href") == "https://www.instagram.com/ncns.digital/"
            assert page.locator("#whatsappContact").get_attribute("href") == "https://wa.me/79063231457"
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
            assert "not connected" in page.locator("#sendStatus").inner_text()
            assert page.locator("#copyBrief").is_enabled()
            results.append({"width": width, "disabled_without_endpoint": True, "no_overflow": True})
            context.close()

        # Realistic configured path with a mocked provider, inspected multipart fields.
        context = browser.new_context()
        page = context.new_page()
        configured(page)
        sent = []
        def success(route):
            sent.append(route.request.post_data or "")
            provider(route)
        page.route(endpoint, success)
        page.goto(origin, wait_until="networkidle")
        assert page.locator("#submitEnquiry").is_enabled()
        page.locator("#visitorName").fill("Example Company")
        page.locator("#visitorEmail").fill("not-an-email")
        page.locator("#projectDetails").fill("Need enquiry routing.")
        assert page.locator("#visitorEmail").evaluate("(el) => el.validity.typeMismatch")
        page.locator("#visitorEmail").fill("test@example.com")
        assert not page.locator("#briefForm").evaluate("(el) => el.checkValidity()")
        assert not sent
        fields(page)
        page.locator("#submitEnquiry").click()
        assert "Request accepted" in page.locator("#sendStatus").inner_text(timeout=10000)
        assert page.locator("#submitEnquiry").is_disabled()
        assert len(sent) == 1
        for expected in ["test@example.com", "Example Company", "Need a quote request portal", "Spreadsheets and email", "contact_permission"]:
            assert expected in sent[0], expected
        assert page.locator("#visitorEmail").input_value() == "test@example.com"
        assert page.locator("#projectDetails").input_value().startswith("Need a quote")
        assert page.locator("#briefForm").get_attribute("action") is None
        assert "Formspree" in page.request.get(origin + "/privacy.html").text()
        context.close()
        results.append({"status": "mocked_200", "posts": len(sent), "success_state": True, "privacy": True})

        # Provider rate limit: no false success, original text retained and retry possible.
        context = browser.new_context()
        page = context.new_page()
        configured(page)
        counter = []
        def throttled(route):
            counter.append(1)
            provider(route, 429 if len(counter) == 1 else 200)
        page.route(endpoint, throttled)
        page.goto(origin, wait_until="networkidle")
        fields(page)
        page.locator("#submitEnquiry").click()
        assert "Too many requests" in page.locator("#sendStatus").inner_text(timeout=10000)
        assert page.locator("#submitEnquiry").is_enabled()
        assert "Need a quote" in page.locator("#projectDetails").input_value()
        page.locator("#submitEnquiry").click()
        assert "Request accepted" in page.locator("#sendStatus").inner_text(timeout=10000)
        assert len(counter) == 2
        context.close()
        results.append({"status": "mocked_429_then_200", "retries": len(counter)})

        # Unsafe and missing endpoints are never called.
        for invalid in ["", "http://formspree.io/f/xncnsdemo1", "https://evil.example/collect",
                        "https://formspree.io/api/0/forms/abc/submissions"]:
            context = browser.new_context()
            page = context.new_page()
            configured(page, formEndpoint=invalid)
            page.goto(origin, wait_until="networkidle")
            assert page.locator("#submitEnquiry").is_disabled(), invalid
            assert "not connected" in page.locator("#sendStatus").inner_text(), invalid
            context.close()
        results.append({"status": "untrusted_endpoints_rejected", "count": 4})

        browser.close()
finally:
    httpd.shutdown()

print(json.dumps(results, indent=2))
