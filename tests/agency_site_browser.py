"""Standalone agency QA for PR #14: no Growth OS, worktree overlay or portfolio dependency."""
from pathlib import Path
import http.server,threading,json,shutil,hashlib,subprocess,tarfile,io,tempfile
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'docs/qa/agency-site';QA.mkdir(parents=True,exist_ok=True)
class H(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
results=[];coverage=json.loads((ROOT/'docs/launch/service-coverage.json').read_text())
assert len(coverage)==12 and len({x['pillar'] for x in coverage})==5
assert hashlib.sha256((ROOT/'assets/ncns-original-logo.webp').read_bytes()).hexdigest()=='75b0a8357126199bae258710941d5b7dccdeb4492607e7a123787a59a327fd01'
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'))
  for width,height in [(1440,900),(1024,900),(768,1024),(390,844),(360,780)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',has_touch=width<=768)
   page=context.new_page();errors=[];bad=[];external=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('requestfailed',lambda r:bad.append(r.url))
   page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
   page.on('request',lambda r:external.append(r.url) if not r.url.startswith(base) or r.method!='GET' else None)
   assert page.goto(base,wait_until='networkidle').ok;page.evaluate('document.fonts.ready')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert page.locator('h1').count()==1
   assert page.locator('[data-family]').count()==12
   assert page.locator('.pillar-nav a').count()==5
   assert page.locator('a[href*="growth-os"], a[href*="/work/"], img[src*="previews/"]').count()==0
   assert page.locator('#instagramContact').get_attribute('href')=='https://www.instagram.com/ncns.digital/'
   assert page.locator('#emailBrief').is_visible() and page.locator('#whatsappContact').is_visible()
   assert page.locator('#whatsappContact').get_attribute('href')=='https://wa.me/79063231457'
   assert page.locator('.contact-channels .channel-icon-link').count()==3
   assert page.locator('.contact-channels .channel-icon-svg').count()==3
   assert page.locator('.contact-channels .channel-card').count()==0
   assert page.locator('#emailPending').text_content().strip()=='ncns.digital@gmail.com'
   assert page.locator('#emailBrief').get_attribute('href').startswith('mailto:ncns.digital@gmail.com')
   assert 'delivery has not been verified' in page.locator('#contactDelivery').inner_text()
   assert page.locator('#motionToggle').is_disabled()
   page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('e=>e===document.activeElement');page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='mainContent'
   if width<=800:
    page.locator('#menuToggle').click();assert page.locator('#menuToggle').get_attribute('aria-expanded')=='true';page.keyboard.press('Escape');assert page.locator('#menuToggle').get_attribute('aria-expanded')=='false'
    page.locator('#menuToggle').click();page.locator('#primaryNavigation a[href="#services"]').click();assert page.locator('#menuToggle').get_attribute('aria-expanded')=='false'
   for row in coverage:
    item=page.locator('#'+row['anchor']);item.locator('summary').click();assert item.get_attribute('open') is not None
    assert row['name'] in item.inner_text();assert 'what you receive' in item.inner_text().lower()
    item.locator('a[data-service]').click();assert page.locator('#projectType').input_value()==row['name']
    item.locator('summary').click()
   page.locator('#phase-tab-0').click();page.locator('#phase-tab-0').focus();page.keyboard.press('End');assert page.locator('#phase-tab-3').get_attribute('aria-selected')=='true';page.keyboard.press('Home');assert page.locator('#phase-tab-0').get_attribute('aria-selected')=='true'
   page.locator('.faq summary').first.click();assert page.locator('.faq').first.get_attribute('open') is not None;page.locator('.faq summary').first.click()
   page.locator('#labService').select_option('Business Process Automation');page.locator('#labNext').click();page.locator('#labNext').click();assert page.locator('[data-lab-step="1"]').is_visible()
   page.locator('#labGoal').fill('Reduce manual enquiry handoffs.');page.locator('#labNext').click();assert 'Business Process Automation' in page.locator('#labResult').input_value()
   page.locator('#labBack').click();page.locator('#labGoal').fill('Reduce manual enquiry handoffs with human review.');page.locator('#labNext').click();page.locator('#useLab').click()
   assert 'human review' in page.locator('#projectDetails').input_value();assert page.locator('#projectType').input_value()=='Business Process Automation'
   page.locator('#currentProcess').fill('Shared inbox and spreadsheet');page.locator('#replyChannel').fill('Owner review fixture / no message sent')
   page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('QA denied'))},configurable:true})")
   page.locator('#copyBrief').click();assert page.locator('#briefFallback').is_visible();assert 'Shared inbox' in page.locator('#briefFallback').input_value()
   page.locator('#contact').screenshot(path=str(QA/f'contact-{width}.png'),animations='disabled',style='.scroll-progress{visibility:hidden!important}')
   page.locator('#projectDetails').fill('   ');page.locator('#copyBrief').click();assert 'Please describe' in page.locator('#formStatus').inner_text()
   page.locator('#labRestart').click();assert page.locator('[data-lab-step="0"]').is_visible();assert page.locator('#labGoal').input_value()==''
   page.locator('#briefForm').evaluate('e=>e.reset()');page.locator('#briefFallback').evaluate('e=>e.hidden=true');page.locator('#formStatus').evaluate('e=>e.textContent=""');page.locator('#questions').focus();page.evaluate('scrollTo(0,0)')
   page.screenshot(path=str(QA/f'full-{width}.png'),full_page=True,animations='disabled',style='.scroll-progress{visibility:hidden!important}');page.locator('#home').screenshot(path=str(QA/f'hero-{width}.png'),animations='disabled',style='.scroll-progress{visibility:hidden!important}')
   for id in ['capabilities','work','process','about','questions']:
    page.locator('#'+id).screenshot(path=str(QA/f'{id}-{width}.png'),animations='disabled',style='.scroll-progress{visibility:hidden!important}')
   page.goto(base+'/solutions/',wait_until='networkidle');assert page.locator('.directory a').count()==5
   assert page.locator('a[href*="growth-os"]').count()==0
   assert page.request.get(base+'/index.html').ok
   page.screenshot(path=str(QA/f'directory-{width}.png'),full_page=True)
   # Crawl public internal routes and anchors without an overlay; do not visit external providers.
   for route in ['/','/solutions/','/privacy.html','/terms.html']:
    page.goto(base+route,wait_until='networkidle')
    for href in page.locator('a[href]').evaluate_all('(a)=>a.map(e=>e.href)'):
     if not href.startswith(base):continue
     path=href.split('#')[0];assert page.request.get(path).ok,href
     if '#' in href and path==page.url.split('#')[0]:assert page.locator('[id="'+href.split('#',1)[1]+'"]').count(),href
   assert not errors and not bad and not external,(errors,bad,external)
   results.append({'width':width,'passed':True,'service_families':12,'pillars':5,'js_errors':errors,'failed_resources':bad,'external_or_write_requests':external,'overflow':False,'runtime':'standalone agency; no portfolio overlay','email_delivery':'recipient configured / delivery unverified'})
   context.close()
  # Clipboard success and failure, malformed hash, direct family URL, no-JS native disclosure.
  page=browser.new_page();page.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>window.qaCopied=text},configurable:true})")
  page.goto(base+'/#family-12',wait_until='networkidle');assert page.locator('#family-12').get_attribute('open') is not None
  page.locator('#projectDetails').fill('A focused maintenance scope.');page.locator('#copyBrief').click();assert 'A focused maintenance scope.' in page.evaluate('window.qaCopied')
  page.goto(base+'/#%invalid',wait_until='networkidle');assert page.locator('#copyBrief').is_enabled();page.close()
  context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=context.new_page();page.goto(base)
  assert page.locator('#primaryNavigation').is_visible();assert not page.locator('.process-controls').is_visible()
  page.locator('#family-11 summary').click();assert page.locator('#family-11').get_attribute('open') is not None
  assert page.locator('#instagramContact').is_visible();assert page.locator('#emailBrief').is_hidden();page.screenshot(path=str(QA/'no-js.png'),full_page=True);context.close()
  # Realistic configured email/WhatsApp are test-only fixtures; no message or external page is opened.
  page=browser.new_page();page.route('**/contact-config.json',lambda r:r.fulfill(json={'email':'qa@example.test','ownerApproved':True,'deliveryVerified':False,'whatsappUrl':'https://wa.me/10000000000','instagramUrl':'https://www.instagram.com/ncns.digital/'}))
  page.goto(base,wait_until='networkidle');assert page.locator('#emailBrief').is_visible();assert page.locator('#whatsappContact').is_visible()
  page.locator('#emailBrief').click();assert 'Describe your business need' in page.locator('#contactDelivery').inner_text()
  page.locator('#projectDetails').fill('A&B — multilingual: привет');assert '%26' in page.locator('#emailBrief').get_attribute('href');assert '%D0' in page.locator('#emailBrief').get_attribute('href');page.close()
  page=browser.new_page();page.route('**/contact-config.json',lambda r:r.fulfill(status=503,body='unavailable'));page.goto(base,wait_until='networkidle');assert 'Automatic project-email preparation is unavailable' in page.locator('#contactDelivery').inner_text();assert page.locator('#instagramContact').is_visible();page.close()
  # Normal-motion review: pause/resume state survives background synchronization.
  page=browser.new_page(reduced_motion='no-preference');page.goto(base,wait_until='networkidle');page.locator('#motionToggle').click();assert page.locator('html').evaluate('e=>e.classList.contains("motion-paused")');page.evaluate("document.dispatchEvent(new Event('visibilitychange'))");assert page.locator('#motionToggle').get_attribute('aria-pressed')=='true';page.locator('#motionToggle').click();assert not page.locator('html').evaluate('e=>e.classList.contains("motion-paused")');page.close()
  browser.close()
finally:s.shutdown()
(QA/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
