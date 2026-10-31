"""Render original HTML share artwork; original emblem remains unchanged."""
from pathlib import Path
import http.server,threading,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class H(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'));page=b.new_page(viewport={'width':1200,'height':630});page.goto(f'http://127.0.0.1:{s.server_port}/docs/qa/agency-site/og-source.html',wait_until='networkidle');page.evaluate('document.fonts.ready');page.screenshot(path=str(ROOT/'assets/social/ncns-digital.png'));b.close()
finally:s.shutdown()
