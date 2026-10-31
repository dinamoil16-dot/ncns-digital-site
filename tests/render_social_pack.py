"""Render original draft carousel art; does not post to any account."""
import http.server,threading,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];M=ROOT/'docs/launch/marketing';out=M/'previews';out.mkdir(exist_ok=True)
class H(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'));page=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=1)
  page.goto(f'http://127.0.0.1:{s.server_port}/docs/launch/marketing/social-cards.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
  for slug in json.loads((M/'slides.json').read_text()):
   page.locator('#'+slug).screenshot(path=str(out/f'{slug}.png'))
  b.close()
finally:s.shutdown()
print('Rendered eleven original draft social cards at 1080×1350.')
