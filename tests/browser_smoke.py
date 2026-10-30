import json
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parents[1] / 'docs/qa/issue-1-rework'
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 results=[]
 for width in [1440,768,390,360]:
  context=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
  page=context.new_page(); errors=[]; failed=[]; bad_responses=[]
  page.add_init_script("""window.layoutShiftScore=0;new PerformanceObserver(list=>{
    for(const entry of list.getEntries()) if(!entry.hadRecentInput) window.layoutShiftScore+=entry.value;
  }).observe({type:'layout-shift',buffered:true});""")
  page.on('response',lambda response:bad_responses.append(response.url) if response.status>=400 else None)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('requestfailed',lambda r:failed.append(r.url))
  response=page.goto('http://127.0.0.1:8000',wait_until='networkidle')
  assert response.status==200
  assert page.title()=='NCNS Digital — Digital Solutions That Work'
  page.evaluate('document.fonts.ready')
  assert page.evaluate("document.fonts.check('16px Michroma') && document.fonts.check('16px Manrope')")
  assert page.locator('.brand img').first.evaluate('(e)=>e.complete && e.naturalWidth>0')
  assert page.locator('.hero-scene img').evaluate('(e)=>e.complete && e.naturalWidth>0')
  assert page.locator('.emblem-wrap img').evaluate('(e)=>e.complete && e.naturalWidth>0')
  overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
  if width<=800:
   page.locator('#menuToggle').click()
   assert page.locator('#menuToggle').get_attribute('aria-expanded')=='true'
   page.keyboard.press('Escape')
   assert page.locator('#menuToggle').get_attribute('aria-expanded')=='false'
   assert page.locator('#menuToggle').evaluate('(e)=>e===document.activeElement')
   page.locator('#menuToggle').click()
   page.locator('#primaryNavigation a[href="#services"]').click()
   assert page.evaluate('document.activeElement.id')=='services'
   assert page.locator('#menuToggle').get_attribute('aria-expanded')=='false'
  assert not overflow, f'Horizontal overflow at {width}'
  for card in page.locator('.service-card').all():
   card.click()
   assert page.evaluate('document.activeElement.id')=='contact'
  assert page.locator('.hero-mist').evaluate('(e)=>getComputedStyle(e).animationName')=='none'
  page.emulate_media(reduced_motion='no-preference')
  assert page.locator('.hero-mist').evaluate('(e)=>getComputedStyle(e).animationName')==('mistDrift' if width>800 else 'none')
  animation=page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0]?.currentTime')
  page.wait_for_timeout(100)
  assert page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0]?.currentTime')>animation
  page.evaluate('scrollTo(0,0)')
  page.wait_for_timeout(50)
  page.mouse.move(width/2,300)
  page.mouse.move(width*.7,350)
  page.wait_for_timeout(50)
  if width>800:
   assert page.locator('.hero').evaluate('(e)=>e.style.getPropertyValue("--scene-x")')!=''
  else:
   assert page.locator('.hero').evaluate('(e)=>e.style.getPropertyValue("--scene-x")')==''
  page.emulate_media(reduced_motion='reduce')
  assert page.locator('.hero-orbit').evaluate('(e)=>getComputedStyle(e).transform')=='none'
  assert page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true}).length')==0
  assert page.locator('a[href^="#"]').evaluate_all('(links)=>links.every(a=>document.querySelector(a.getAttribute("href")))')
  page.locator('#nextStep').click()
  assert page.locator('#workflowCount').inner_text()=='02 / 04'
  page.locator('[data-step="3"]').click()
  assert page.locator('#workflowCount').inner_text()=='04 / 04'
  page.locator('#projectDetails').fill('Onboarding browser check')
  page.evaluate("Object.defineProperty(navigator,'clipboard',{value:undefined,configurable:true})")
  page.locator('#briefForm button').click()
  assert 'Onboarding browser check' in page.locator('#formStatus textarea').input_value()
  page.locator('#projectDetails').fill('')
  page.locator('#formStatus').evaluate('(e)=>e.replaceChildren()')
  page.locator('[data-step="0"]').click()
  page.evaluate('document.activeElement.blur(); scrollTo(0,0)')
  page.wait_for_timeout(150)
  page.screenshot(path=str(out/f'hero-{width}.png'))
  page.screenshot(path=str(out/f'screenshot-{width}.png'),full_page=True)
  assert not errors,errors
  assert not failed,failed
  assert not bad_responses,bad_responses
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  if width==1440:
   page.screenshot(path=str(out/'after-1440.png'))
   services_end=page.locator('#services').evaluate('(e)=>e.getBoundingClientRect().bottom+scrollY')
   with Image.open(out/'screenshot-1440.png') as full_screenshot:
    full_screenshot.crop((0,0,1440,round(services_end))).save(out/'hero-services-1440.png')
  results.append({'width':width,'http':response.status,'horizontal_overflow':overflow,'js_errors':errors,'failed_requests':failed,'interactions':'passed','layout_shift_score':page.evaluate('window.layoutShiftScore'),'resource_bytes':page.evaluate('performance.getEntriesByType("resource").reduce((sum,r)=>sum+r.transferSize,0)')})
  context.close()
 # Font fallback remains usable without depending on any remote font service.
 for width in [1440,360]:
  fallback=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
  fallback.route('**/*.woff2',lambda route:route.abort())
  page=fallback.new_page();page.goto('http://127.0.0.1:8000',wait_until='networkidle')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  assert page.locator('h1').is_visible()
  page.screenshot(path=str(out/f'fallback-{width}.png'))
  fallback.close()
 # Content must stay available with JavaScript disabled.
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
 page=nojs.new_page();page.goto('http://127.0.0.1:8000',wait_until='networkidle')
 assert page.locator('.service-card').first.is_visible()
 assert page.locator('.service-card').first.evaluate('(e)=>getComputedStyle(e).opacity')=='1'
 nojs.close()
 browser.close()
 (out / 'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
