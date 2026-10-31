"""Compare the conversion branch hero with approved origin/main in Chromium."""
import http.server,threading,tempfile,subprocess,tarfile,io,json,shutil
from pathlib import Path
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'docs/qa/first-clients';QA.mkdir(parents=True,exist_ok=True)
def server(root):
 class H(http.server.SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw):super().__init__(*a,directory=str(root),**kw)
  def log_message(self,*a):pass
 s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();return s
with tempfile.TemporaryDirectory() as tmp:
 with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','origin/main'],cwd=ROOT))) as t:t.extractall(tmp,filter='data')
 a,b=server(tmp),server(ROOT);results=[]
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path=shutil.which('chromium'))
   for width,height in [(1440,900),(1024,900),(768,1024),(390,844),(360,780)]:
    images=[]
    for s,label in [(a,'approved'),(b,'current')]:
     page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');page.goto(f'http://127.0.0.1:{s.server_port}',wait_until='networkidle');page.evaluate('document.fonts.ready');page.mouse.move(0,0)
     f=QA/f'hero-{label}-{width}.png';page.locator('#home').screenshot(path=str(f),animations='disabled');images.append(Image.open(f).convert('RGB'));page.close()
    diff=ImageChops.difference(*images);assert diff.getbbox() is None, (width,diff.getbbox())
    results.append({'width':width,'pixel_identical':True,'baseline':subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()})
    if width in (1440,390):
     sheet=Image.new('RGB',(images[0].width*2,images[0].height));sheet.paste(images[0],(0,0));sheet.paste(images[1],(images[0].width,0));sheet.save(QA/f'hero-approved-current-{width}.webp')
   browser.close()
 finally:a.shutdown();b.shutdown()
(QA/'hero-regression.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
