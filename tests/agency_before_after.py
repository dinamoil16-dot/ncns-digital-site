"""Capture real standalone before/after journeys. The old missing demo is an expected historical 404."""
import http.server,threading,tempfile,subprocess,tarfile,io,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'docs/qa/agency-site'
def server(root):
 class H(http.server.SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw):super().__init__(*a,directory=str(root),**kw)
  def log_message(self,*a):pass
 s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();return s
with tempfile.TemporaryDirectory() as temp:
 with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','d6f4aac'],cwd=ROOT))) as t:t.extractall(temp,filter='data')
 old,new=server(temp),server(ROOT);results=[]
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path=shutil.which('chromium'))
   for width,height in [(1440,900),(390,844)]:
    images=[]
    for srv,label in [(old,'before'),(new,'after')]:
     page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');base=f'http://127.0.0.1:{srv.server_port}';page.goto(base,wait_until='networkidle');page.evaluate('document.fonts.ready')
     for section in ['work','capabilities']:
      file=QA/f'{label}-{section}-{width}.png';page.locator('#'+section).screenshot(path=str(file),animations='disabled',style='.scroll-progress{visibility:hidden!important}')
      if section=='work':images.append(Image.open(file).convert('RGB'))
     if label=='before':assert page.request.get(base+'/work/growth-os/').status==404
     else:assert page.locator('a[href*="growth-os"]').count()==0
     page.close()
    target=900 if width==1440 else 390
    resized=[im.resize((target,round(im.height*target/im.width)),Image.Resampling.LANCZOS) for im in images]
    sheet=Image.new('RGB',(target*2+48,max(im.height for im in resized)+72),'#03070c');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
    for i,(label,im) in enumerate(zip(['BEFORE: unavailable demo dependency','AFTER: standalone agency partnership'],resized)):
     x=16+i*(target+16);draw.text((x,20),label,fill='#eaf2fc',font=font);sheet.paste(im,(x,56))
    sheet.save(QA/f'journey-before-after-{width}.webp',quality=92)
    results.append({'width':width,'before_commit':'d6f4aac','before_unavailable_demo_http_status':404,'after_demo_links':0,'after_journey':'12 services / 5 pillars → selected scope → project brief; Build/Operate/Grow independent of portfolio'})
   b.close()
 finally:old.shutdown();new.shutdown()
(QA/'before-after.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
