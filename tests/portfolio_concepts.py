"""C1 visual proposal renders only: no complete portfolio flow is implemented."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
out=root/'docs/portfolio/concepts/screenshots'
out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for slug in ['asterwake','kern9','auven']:
  for width,height in [(1440,1000),(390,844),(360,780)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   page=context.new_page();errors=[];failed=[];bad=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('requestfailed',lambda r:failed.append(r.url))
   page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
   assert page.goto(f'http://127.0.0.1:8000/docs/portfolio/concepts/boards/{slug}.html',wait_until='networkidle').status==200
   page.evaluate('document.fonts.ready')
   assert page.locator('h1').is_visible()
   assert page.locator('.hero-photo').evaluate('(e)=>e.complete&&e.naturalWidth>0')
   assert page.locator('.review-bar').inner_text().find('FICTIONAL')>=0
   assert page.locator('.module-notice').inner_text().lower().find('visual')>=0
   assert page.locator('button').evaluate_all('(buttons)=>buttons.every(b=>b.disabled)')
   assert page.locator('script').count()==0
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(slug,width)
   page.screenshot(path=str(out/f'{slug}-{width}.png'),full_page=True)
   page.screenshot(path=str(out/f'{slug}-hero-{width}.png'))
   box=page.locator('#module').evaluate('(e)=>{const r=e.getBoundingClientRect();return [Math.floor(r.left),Math.floor(r.top),Math.ceil(r.right),Math.ceil(r.bottom)]}')
   with Image.open(out/f'{slug}-{width}.png') as full:full.crop(tuple(box)).save(out/f'{slug}-module-{width}.png')
   page.locator('.hero-copy a[href="#module"]').click()
   assert page.evaluate('location.hash')=='#module'
   assert page.locator('.module-notice').is_visible()
   assert not errors and not failed and not bad,(errors,failed,bad)
   results.append({'concept':slug,'viewport':[width,height],'js_errors':errors,'failed_resources':failed,'bad_http':bad,'overflow':False,'stage':'visual board only, all proposed action controls disabled','resource_bytes':page.evaluate('performance.getEntriesByType("resource").reduce((n,r)=>n+r.transferSize,0)')})
   context.close()
 for width in [1440,390]:
  context=browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=False)
  page=context.new_page();page.goto('http://127.0.0.1:8000/docs/portfolio/concepts/',wait_until='networkidle')
  assert page.locator('.card').count()==3
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  page.screenshot(path=str(out/f'index-{width}.png'),full_page=True)
  page.locator('a[href="boards/kern9.html"]').click()
  assert page.title().startswith('Kern/9')
  page.locator('.review-bar a').click()
  assert page.title().startswith('NCNS')
  context.close()
 browser.close()
# A visual selection sheet. Native-resolution full boards remain the primary deliverables.
canvas=Image.new('RGB',(1496,920),'#071019');draw=ImageDraw.Draw(canvas)
for x,slug,label in [(16,'asterwake','01 / ASTERWAKE - MARINE'),(512,'kern9','02 / KERN/9 - INDUSTRIAL'),(1008,'auven','03 / AUVEN - CONSUMER')]:
 draw.text((x,16),label,fill='#eaf2fc',font=ImageFont.load_default(size=16))
 with Image.open(out/f'{slug}-1440.png') as full:
  hero=full.crop((0,0,1440,710)).convert('RGB').resize((480,237),Image.Resampling.LANCZOS)
  canvas.paste(hero,(x,54))
 with Image.open(out/f'{slug}-390.png') as mobile:
  thumb=mobile.convert('RGB').resize((210,round(mobile.height*210/mobile.width)),Image.Resampling.LANCZOS)
  canvas.paste(thumb.crop((0,0,210,min(thumb.height,590))),(x+135,310))
canvas.save(out/'three-directions.webp',quality=93,method=6)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
