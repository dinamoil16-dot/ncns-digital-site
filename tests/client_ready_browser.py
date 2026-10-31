"""Issue 13: isolated integration QA. Growth OS served from PR #9 worktree, not copied into main."""
import http.server,json,threading,os,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
DEMO=Path(os.environ.get('NCNS_GROWTH_WORKTREE','/workspace/ncns-digital-site'))
QA=ROOT/'docs/qa/first-clients';QA.mkdir(parents=True,exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def translate_path(self,path):
  if path.split('?')[0].startswith('/work/growth-os/'):
   relative=path.split('?')[0].removeprefix('/work/growth-os/')
   candidate=(DEMO/'work/growth-os'/relative).resolve()
   if candidate.is_relative_to((DEMO/'work/growth-os').resolve()):return str(candidate)
  return super().translate_path(path)
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
results=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'))
  for width,height in [(1440,900),(1024,900),(768,1024),(390,844),(360,780)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce');page=context.new_page();errors=[];bad=[];writes=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
   page.on('request',lambda r:writes.append(r.url) if r.method!='GET' or not r.url.startswith(base) else None)
   page.goto(base,wait_until='networkidle');page.evaluate('document.fonts.ready');page.screenshot(path=str(QA/f'home-{width}.png'),full_page=True,animations='disabled')
   page.locator('#home').screenshot(path=str(QA/f'hero-{width}.png'),animations='disabled')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   page.locator('#work a[href="./solutions/"]').click();assert '/solutions/' in page.url
   page.screenshot(path=str(QA/f'solutions-{width}.png'),full_page=True)
   page.get_by_role('link',name='OPEN GROWTH OS').click();assert page.locator('#kpiLeads').inner_text()=='288'
   page.locator('.return').evaluate('(e)=>e.click()');page.wait_for_url('**/index.html#work')
   page.locator('#labNext').click();page.locator('#labNext').click();assert page.locator('[data-lab-step="1"]').is_visible()
   page.locator('#labGoal').fill('Reduce manual qualification and review missed follow-ups.');page.locator('#labNext').click()
   assert 'Reduce manual' in page.locator('#labResult').input_value();page.locator('#useLab').click()
   page.locator('#currentProcess').fill('Manual spreadsheet');page.locator('#replyChannel').fill('QA only / no recipient supplied')
   assert page.locator('#emailBrief').is_hidden();assert page.locator('#instagramContact').is_hidden();assert page.locator('#whatsappContact').is_hidden()
   assert 'not yet verified' in page.locator('#contactDelivery').inner_text()
   page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('QA'))},configurable:true})")
   page.locator('#copyBrief').click();assert page.locator('#briefFallback').is_visible();assert 'Manual spreadsheet' in page.locator('#briefFallback').input_value()
   page.locator('#contact').screenshot(path=str(QA/f'contact-{width}.png'),animations='disabled')
   assert not errors and not bad and not writes,(errors,bad,writes)
   results.append({'width':width,'passed':True,'errors':errors,'bad_resources':bad,'external_or_write_requests':writes,'integration':'PR9 worktree overlay; not merged','contact_delivery':'unconfigured, not tested'})
   context.close()
  # Configuration enables actual links but never claims a send or delivery.
  page=browser.new_page(viewport={'width':390,'height':844})
  page.route('**/contact-config.json',lambda r:r.fulfill(json={'email':'qa@example.test','ownerApproved':True,'deliveryVerified':False,'instagramUrl':'https://www.instagram.com/qa_fixture/','whatsappUrl':'https://wa.me/10000000000'}))
  page.goto(base,wait_until='networkidle');assert page.locator('#emailBrief').is_visible()
  page.locator('#emailBrief').click();assert 'Describe your business need' in page.locator('#contactDelivery').inner_text()
  page.locator('#projectDetails').fill('A&B / multilingual: привет');page.locator('#replyChannel').fill('QA only')
  href=page.locator('#emailBrief').get_attribute('href');assert href.startswith('mailto:qa@example.test?') and '%26' in href and '%D0' in href
  assert page.locator('#instagramContact').get_attribute('href')=='https://www.instagram.com/qa_fixture/'
  assert page.locator('#whatsappContact').is_visible();page.close()
  context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=context.new_page();page.goto(base);assert page.locator('#contactDelivery').is_visible();assert page.locator('#emailBrief').is_hidden();page.screenshot(path=str(QA/'no-js.png'),full_page=True);context.close()
  # Genuine mobile Experience Lab walkthrough, for manual social editing, no publication.
  context=browser.new_context(viewport={'width':390,'height':844},record_video_dir=str(QA/'recordings'),record_video_size={'width':390,'height':844})
  page=context.new_page();page.goto(base,wait_until='networkidle');page.locator('#experience').scroll_into_view_if_needed();page.wait_for_timeout(1500)
  page.locator('#labNext').click();page.wait_for_timeout(1200);page.locator('#labGoal').fill('Qualify enquiries before a sales conversation.');page.wait_for_timeout(1500);page.locator('#labNext').click();page.wait_for_timeout(2000);page.locator('#useLab').click();page.wait_for_timeout(2000);page.locator('#copyBrief').click();page.wait_for_timeout(1800)
  video=page.video;context.close();video.save_as(str(QA/'experience-lab-mobile.webm'));video.delete();browser.close()
finally:server.shutdown()
(QA/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
