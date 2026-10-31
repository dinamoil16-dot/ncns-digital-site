"""Actual normal-motion Chromium review, standalone agency only. No posts, messages or deployment."""
import http.server,threading,shutil,subprocess,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'docs/qa/agency-site';(QA/'recordings').mkdir(parents=True,exist_ok=True)
class H(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';results=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'))
  for width,height in [(1440,900),(390,844)]:
   context=b.new_context(viewport={'width':width,'height':height},has_touch=width<800,record_video_dir=str(QA/'recordings'),record_video_size={'width':width,'height':height},reduced_motion='no-preference')
   page=context.new_page();errors=[];writes=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:writes.append(r.url) if r.method!='GET' or not r.url.startswith(base) else None)
   page.goto(base,wait_until='networkidle');page.evaluate('document.fonts.ready');page.wait_for_timeout(1800)
   if width<800:
    page.locator('#menuToggle').click();page.wait_for_timeout(700);page.locator('#primaryNavigation a[href="#services"]').click()
   else:page.locator('#primaryNavigation a[href="#services"]').click()
   page.wait_for_timeout(1200);page.locator('.pillar-nav').scroll_into_view_if_needed();page.wait_for_timeout(900)
   page.locator('.pillar-nav a[href="#service-ai"]').click();page.wait_for_timeout(900);page.locator('#family-3 summary').click();page.wait_for_timeout(1400)
   page.locator('#work').scroll_into_view_if_needed();page.wait_for_timeout(1600)
   page.locator('#experience').scroll_into_view_if_needed();page.wait_for_timeout(1100);page.locator('#labService').select_option('Business Process Automation');page.locator('#labNext').click();page.wait_for_timeout(700);page.locator('#labGoal').fill('Make enquiry handoffs clearer, with a person reviewing exceptions.');page.wait_for_timeout(1000);page.locator('#labNext').click();page.wait_for_timeout(1200)
   page.locator('#useLab').click();page.wait_for_timeout(1300);page.locator('.contact-channels').scroll_into_view_if_needed();page.wait_for_timeout(1300)
   page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('QA fallback'))},configurable:true})");page.locator('#copyBrief').click();page.wait_for_timeout(1400)
   assert not errors and not writes
   video=page.video;context.close();webm=QA/f'walkthrough-{width}.webm';video.save_as(str(webm));video.delete()
   mp4=QA/f'walkthrough-{width}.mp4';subprocess.run(['ffmpeg','-y','-i',str(webm),'-an','-c:v','libx264','-crf','23','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
   duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(mp4)],text=True));results.append({'width':width,'duration_seconds':duration,'file':mp4.name,'source':webm.name,'real_browser':True,'js_errors':errors,'external_or_write_requests':writes,'journey':'approved hero → service pillars → automation detail → Build/Operate/Grow → Experience Lab → local brief/copy; no send'})
  b.close()
finally:s.shutdown()
(QA/'recordings.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
