#!/usr/bin/env python3
"""Chromium smoke test for the separate Growth OS demo. No production deployment."""
from __future__ import annotations
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "docs" / "qa" / "milestone-c2" / "growth-os"
QA.mkdir(parents=True, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
url = "http://127.0.0.1:{}/work/growth-os/".format(server.server_address[1])
results = []

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for width, height in ((1440, 900), (390, 844), (360, 780)):
            page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce", accept_downloads=True)
            errors, bad_requests = [], []
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.on("requestfailed", lambda req: bad_requests.append(req.url))
            resp = page.goto(url, wait_until="networkidle")
            assert resp and resp.ok, "Page must return HTTP success"
            assert page.title().startswith("Growth OS")
            assert page.locator("#kpiLeads").inner_text() == "288"
            assert page.locator("#kpiQualified").inner_text() == "86"
            assert page.locator("#kpiWon").inner_text() == "20"
            assert page.locator("#kpiRevenue").inner_text() == "$31,800"
            assert page.locator(".funnel-step").count() == 3
            assert page.locator("tr").count() == 6
            assert page.locator("#followupCount").inner_text().startswith("2")
            page.locator("#channel").select_option("outbound")
            assert page.locator("#kpiLeads").inner_text() == "58"
            page.locator("#channel").select_option("all")
            page.locator("#period").select_option("previous")
            assert page.locator("#kpiLeads").inner_text() == "236"
            page.locator("#period").select_option("current")
            before = page.locator("#forecastRevenue").inner_text()
            page.locator("#qualifiedRate").evaluate("(el) => { el.value = '44'; el.dispatchEvent(new Event('input', { bubbles: true })); }")
            assert page.locator("#qualifiedValue").inner_text() == "44%"
            assert page.locator("#forecastRevenue").inner_text() != before
            page.locator("#resetScenario").click()
            assert page.locator("#qualifiedValue").inner_text() == "30%"
            page.get_by_role("button", name="Mark follow-up completed for Sample Atelier A").click()
            assert page.locator("#followupCount").inner_text().startswith("1")
            with page.expect_download() as obj:
                page.locator("#downloadPlan").click()
            download = obj.value
            assert download.suggested_filename == "ncns-growth-os-demo-plan.json"
            path = QA / ("download-{}.json".format(width))
            download.save_as(str(path))
            data = json.loads(path.read_text())
            assert data["demo"] and data["syntheticData"]
            assert data["metrics"]["leads"] == 288
            page.screenshot(path=str(QA / "full-{}.png".format(width)), full_page=True, animations="disabled")
            overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            assert not overflow, "{}px viewport overflow".format(width)
            assert not errors, "JS errors: {}".format(errors)
            assert not bad_requests, "failed network requests: {}".format(bad_requests)
            results.append({"width": width, "height": height, "passed": True, "js_errors": errors, "bad_requests": bad_requests, "overflow": overflow})
            page.close()
        browser.close()
finally:
    server.shutdown()
(QA / "results.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
