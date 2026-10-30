import json
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parents[1] / 'docs/qa/issue-1'
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 results=[]
 for width in [1440,768,390,360]:
  context=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
  page=context.new_page(); errors=[]; failed=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('requestfailed',lambda r:failed.append(r.url))
  response=page.goto('http://127.0.0.1:8000',wait_until='networkidle')
  assert response.status==200
  assert page.title()=='NCNS Digital — Digital Solutions That Work'
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
  assert page.locator('.hero-mist').evaluate('(e)=>getComputedStyle(e).animationName')=='none'
  page.emulate_media(reduced_motion='no-preference')
  assert page.locator('.hero-mist').evaluate('(e)=>getComputedStyle(e).animationName')=='mistDrift'
  page.emulate_media(reduced_motion='reduce')
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
  results.append({'width':width,'http':response.status,'horizontal_overflow':overflow,'js_errors':errors,'failed_requests':failed,'interactions':'passed'})
  context.close()
 browser.close()
 (out / 'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
