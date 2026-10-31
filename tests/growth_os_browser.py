#!/usr/bin/env python3
"""Chromium smoke test for the separate Growth OS demo. No production deployment."""
from __future__ import annotations
import http.server
import json
from pathlib import Path
import threading
import shutil
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
        browser = playwright.chromium.launch(headless=True, executable_path=shutil.which("chromium"))
        for width, height in ((1440, 900), (1024, 900), (768, 1024), (390, 844), (360, 780)):
            page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce", accept_downloads=True)
            errors, bad_requests, external, writes = [], [], [], []
            page.on("request", lambda r: external.append(r.url) if not r.url.startswith(url.split("/work/")[0]) else None)
            page.on("request", lambda r: writes.append(r.url) if r.method != "GET" else None)
            page.on("response", lambda r: bad_requests.append(r.url) if r.status >= 400 else None)
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.on("requestfailed", lambda req: bad_requests.append(req.url))
            resp = page.goto(url, wait_until="networkidle")
            assert resp and resp.ok, "Page must return HTTP success"
            assert page.title().startswith("Growth OS")
            assert page.locator("#kpiLeads").inner_text() == "288"
            assert page.locator("#kpiQualified").inner_text() == "86"
            assert page.locator("#kpiWon").inner_text() == "20"
            assert page.locator("#kpiRevenue").inner_text() == "$31,800"
            assert page.locator("#flowLeads").inner_text() == "288"
            page.locator('[data-flow="2"]').click()
            assert page.locator("#flowTarget").get_attribute("href") == "#pipeline"
            assert "20 won / 86" in page.locator("#flowDetail").inner_text()
            assert page.locator("#pauseFlow").get_attribute("aria-pressed") == "true"
            page.locator("#pauseFlow").click()
            assert page.locator("#pauseFlow").get_attribute("aria-pressed") == "false"
            page.locator("#pauseFlow").click()
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
            assert page.locator("#forecastRevenue").inner_text() == "$31,596"
            assert page.locator("#forecastContribution").inner_text() == "$5,039"
            blocked=page.locator("tr").filter(has_text="Sample Supply D")
            assert blocked.get_by_role("button").count()==0
            stage=page.get_by_label("Stage for Sample Engineering B")
            stage.select_option("Won")
            assert page.locator("#followupCount").inner_text().startswith("1")
            stage.select_option("Proposal")
            assert page.locator("#followupCount").inner_text().startswith("2")
            assert stage.evaluate("e=>e===document.activeElement")
            page.locator("#resetPipeline").click()
            # Force the clipboard failure path rather than assuming OS clipboard access.
            page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('QA denied'))},configurable:true})")
            page.locator("#copyPlan").click()
            assert page.locator("#manualPlan").is_visible()
            assert "FICTIONAL DATA" in page.locator("#manualPlan").input_value()
            page.locator("#qualifiedRate").focus()
            page.keyboard.press("ArrowRight")
            assert page.locator("#qualifiedValue").inner_text()=="31%"
            page.locator("#resetScenario").click()
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
            assert data["scenario"]["averageRevenue"] == 1590
            assert data["sampleOpenOpportunities"][0]["followUpCompleted"]
            assert data["sampleOpenOpportunities"][3]["policy"]=="Opted out"
            assert not external and not writes
            page.locator("#resetPipeline").click()
            page.locator("#manualPlan").evaluate("e=>e.hidden=true")
            page.evaluate("scrollTo(0,0)")
            page.screenshot(path=str(QA / f"opening-{width}.png"),animations="disabled")
            page.screenshot(path=str(QA / "full-{}.png".format(width)), full_page=True, animations="disabled")
            for section in ["journey","overview","pipeline","scenario","plan"]:
                page.locator(".journey" if section=="journey" else "#"+section).screenshot(path=str(QA/f"{section}-{width}.png"),animations="disabled")
            overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            assert not overflow, "{}px viewport overflow".format(width)
            assert not errors, "JS errors: {}".format(errors)
            assert not bad_requests, "failed network requests: {}".format(bad_requests)
            results.append({"width": width, "height": height, "passed": True, "js_errors": errors, "bad_requests": bad_requests, "overflow": overflow})
            page.close()
        context=browser.new_context(java_script_enabled=False,viewport={"width":390,"height":844})
        page=context.new_page();page.goto(url)
        assert page.locator(".fallback").is_visible()
        assert not page.locator(".journey").is_visible()
        page.screenshot(path=str(QA/"no-js.png"),full_page=True)
        context.close()
        for width,height in [(1440,900),(390,844)]:
            context=browser.new_context(viewport={"width":width,"height":height},record_video_dir=str(QA/"recordings"),record_video_size={"width":width,"height":height})
            page=context.new_page();page.goto(url,wait_until="networkidle")
            for i in range(4):
                page.locator(f'[data-flow="{i}"]').click();page.wait_for_timeout(1100)
            page.locator("#channel").select_option("outbound");page.wait_for_timeout(1300)
            page.locator("#channel").select_option("all")
            page.locator("#flowTarget").click();page.wait_for_timeout(1300)
            page.locator("#qualifiedRate").scroll_into_view_if_needed();page.locator("#qualifiedRate").focus();page.keyboard.press("ArrowRight");page.wait_for_timeout(1300)
            page.locator("#resetScenario").click();page.wait_for_timeout(1100)
            page.get_by_role("button",name="Mark follow-up completed for Sample Atelier A").click();page.wait_for_timeout(1500)
            page.locator("#copyPlan").click();page.wait_for_timeout(1700)
            page.wait_for_timeout(2500)
            video=page.video;context.close();video.save_as(str(QA/f"walkthrough-{width}.webm"));video.delete()
        browser.close()
finally:
    server.shutdown()
(QA / "results.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
