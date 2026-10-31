"""Real Chromium acceptance and review artifacts for Milestone B; serve on :8000."""
import hashlib
import io
import json
import os
import shutil
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright, expect

root = Path(__file__).resolve().parents[1]
out = Path(os.environ.get('NCNS_QA_OUTPUT', str(root / 'docs/qa/milestone-b')))
base_url = os.environ.get('NCNS_TEST_URL', 'http://127.0.0.1:8000')
out.mkdir(parents=True, exist_ok=True)
if not (out/'approved-a-1440.png').exists(): shutil.copy2(root/'docs/qa/milestone-b/approved-a-1440.png', out/'approved-a-1440.png')
assert hashlib.sha256((root/'assets/ncns-original-logo.webp').read_bytes()).hexdigest() == '75b0a8357126199bae258710941d5b7dccdeb4492607e7a123787a59a327fd01'
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width, height in [(1440,900),(1024,768),(768,900),(390,844),(360,780)]:
        context = browser.new_context(viewport={'width':width,'height':height}, reduced_motion='reduce', has_touch=width<=768)
        context.grant_permissions(['clipboard-read','clipboard-write'])
        page = context.new_page()
        errors, failed, bad, writes = [], [], [], []
        page.on('pageerror', lambda e:errors.append(str(e)))
        page.on('requestfailed', lambda r:failed.append(r.url))
        page.on('response', lambda r:bad.append(r.url) if r.status>=400 else None)
        page.on('request', lambda r:writes.append(r.url) if r.method!='GET' else None)
        page.add_init_script("""window.cls=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.cls+=e.value}).observe({type:'layout-shift',buffered:true});""")
        assert page.goto(base_url, wait_until='networkidle').status == 200
        page.evaluate('document.fonts.ready')
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'), width
        assert page.locator('.emblem-wrap img').evaluate('(e)=>e.complete&&e.naturalWidth===480')
        assert page.evaluate("document.fonts.check('16px Michroma') && document.fonts.check('16px Manrope')")
        assert page.locator('a[href^="#"]').evaluate_all('(links)=>links.every(a=>document.querySelector(a.hash))')
        page.screenshot(path=str(out/f'hero-{width}.png'))
        page.screenshot(path=str(out/f'full-{width}.png'), full_page=True)
        for name in ['services','experience','contact']:
            box=page.locator(f'#{name}').evaluate('(e)=>{const r=e.getBoundingClientRect();return [Math.floor(r.left+scrollX),Math.floor(r.top+scrollY),Math.ceil(r.right+scrollX),Math.ceil(r.bottom+scrollY)]}')
            with Image.open(out/f'full-{width}.png') as full:
                full.crop(tuple(box)).save(out/f'{name}-{width}.png')
        page.evaluate('scrollTo(0,0);document.activeElement.blur()')
        page.keyboard.press('Tab')
        assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
        page.keyboard.press('Enter')
        assert page.evaluate('document.activeElement.id') == 'mainContent'
        if width<=768:
            page.evaluate('scrollTo(0,0)')
            page.locator('#menuToggle').tap()
            assert page.locator('#menuToggle').get_attribute('aria-expanded') == 'true'
            page.screenshot(path=str(out/f'menu-{width}.png'))
            page.keyboard.press('Escape')
            assert page.locator('#menuToggle').get_attribute('aria-expanded') == 'false'
            assert page.evaluate('document.activeElement.id') == 'menuToggle'
            page.locator('#menuToggle').tap()
            page.locator('#primaryNavigation a[href="#services"]').tap()
            assert page.evaluate('document.activeElement.id') == 'services'
        page.locator('.service-brand').click()
        assert page.locator('#service-brand [data-family]').count() == 2
        assert page.evaluate('document.activeElement.id') == 'service-brand'
        page.locator('#phase-tab-0').focus()
        page.keyboard.press('ArrowRight')
        assert page.locator('#phase-tab-1').get_attribute('aria-selected') == 'true'
        assert page.locator('#phase-1').is_visible()
        page.keyboard.press('ArrowLeft')
        assert page.locator('#phase-0').is_visible()
        page.keyboard.press('End')
        assert page.locator('#phase-3').is_visible()
        page.keyboard.press('Home')
        assert page.locator('#phase-0').is_visible()
        page.locator('#labService').select_option('Websites & Web Development')
        page.locator('#labNext').click()
        goal_top=page.locator('#labGoal').evaluate('(e)=>e.getBoundingClientRect().top')
        assert 0<=goal_top<height
        page.locator('#labNext').click()
        assert page.locator('#labGoal').is_visible() # Missing goal cannot advance.
        assert page.evaluate('document.activeElement.id') == 'labGoal'
        goal = 'A multilingual website for an independent studio — қазақша / Русский.'
        page.locator('#labGoal').fill(goal)
        page.locator('#labTiming').select_option('Within 1–3 months')
        page.locator('input[value="Responsive implementation"]').check()
        page.locator('#labNext').click()
        page.locator('#labBack').click()
        assert page.locator('#labGoal').input_value() == goal
        assert page.locator('input[value="Responsive implementation"]').is_checked()
        page.locator('#labNext').click()
        draft = page.locator('#labResult').input_value()
        assert goal in draft and 'Responsive implementation' in draft and 'not a quotation' in draft
        page.evaluate('scrollTo(0,0)')
        page.wait_for_timeout(50)
        box=page.locator('#experience').evaluate('(e)=>{const r=e.getBoundingClientRect();return [Math.floor(r.left),Math.floor(r.top+scrollY),Math.ceil(r.right),Math.ceil(r.bottom+scrollY)]}')
        with Image.open(io.BytesIO(page.screenshot(full_page=True))) as full:
            full.crop(tuple(box)).save(out/f'experience-result-{width}.png')
        page.locator('#copyLab').click()
        assert page.evaluate('navigator.clipboard.readText()') == draft
        page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined})")
        page.locator('#copyLab').click()
        assert 'Automatic copy is unavailable' in page.locator('#labCopyStatus').inner_text()
        assert page.locator('#labResult').evaluate('(e)=>e.selectionStart===0&&e.selectionEnd===e.value.length')
        page.locator('#useLab').click()
        assert page.locator('#projectDetails').input_value() == draft
        assert page.evaluate('document.activeElement.id') == 'projectDetails'
        page.locator('#copyBrief').click()
        assert draft in page.locator('#briefFallback').input_value()
        assert page.locator('#briefFallback').get_attribute('readonly') is not None
        page.locator('#projectDetails').fill('')
        page.locator('#copyBrief').click()
        assert 'Please describe' in page.locator('#formStatus').inner_text()
        page.locator('#labRestart').click()
        assert page.locator('#labService').is_visible() and page.locator('#labGoal').input_value() == ''
        # Normal motion: halo clock, scene pointer depth, card movement, and immutable lettering.
        page.emulate_media(reduced_motion='no-preference')
        page.evaluate('scrollTo(0,0)')
        page.wait_for_timeout(100)
        clock = page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime')
        page.wait_for_timeout(120)
        assert page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime') > clock
        page.mouse.move(width*.4,200);page.mouse.move(width*.7,250);page.wait_for_timeout(70)
        if width>800:
            assert page.locator('.hero').evaluate('(e)=>!!e.style.getPropertyValue("--scene-x")')
            page.locator('.service-web').hover(position={'x':100,'y':60});page.wait_for_timeout(70)
            assert page.locator('.service-web').evaluate('(e)=>!!e.style.getPropertyValue("--tilt-x")')
        else:
            assert not page.locator('.hero').evaluate('(e)=>!!e.style.getPropertyValue("--scene-x")')
        assert page.locator('#heroOrbit').evaluate('(e)=>getComputedStyle(e).transform') == 'none'
        # Exercise hidden-tab guards through the standard visibility event with a controlled state.
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
        assert page.locator('html').get_attribute('class').find('motion-paused')>=0
        paused = page.locator('.orbit-ring').evaluate('async(e)=>{const a=e.getAnimations({subtree:true})[0];await a.ready;return a.currentTime}')
        page.wait_for_timeout(100)
        assert page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime') == paused
        page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
        page.emulate_media(reduced_motion='reduce')
        assert page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true}).length') == 0
        assert not page.locator('.hero').evaluate('(e)=>!!e.style.getPropertyValue("--scene-x")')
        assert not page.locator('.service-web').evaluate('(e)=>!!e.style.getPropertyValue("--tilt-x")')
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
        assert not errors, errors
        assert not failed, failed
        assert not bad, bad
        assert not writes, writes
        results.append({'viewport':[width,height],'js_errors':errors,'failed_requests':failed,'bad_http':bad,'data_submissions':writes,'overflow':False,'functional_and_motion_checks':'passed','bytes':page.evaluate('performance.getEntriesByType("resource").reduce((sum,e)=>sum+e.transferSize,0)'),'layout_shift':page.evaluate('window.cls')})
        context.close()
    for width,height in [(1440,900),(390,844)]:
        context=browser.new_context(viewport={'width':width,'height':height},java_script_enabled=False)
        page=context.new_page();page.goto(base_url,wait_until='networkidle')
        assert page.locator('.service-web').is_visible()
        assert page.locator('#phase-3').is_visible()
        assert page.locator('#copyBrief').is_disabled()
        if width==390:
            assert page.locator('#primaryNavigation a[href="#contact"]').first.is_visible()
            page.locator('#primaryNavigation a[href="#contact"]').first.click()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
        page.screenshot(path=str(out/f'no-js-{width}.png'))
        context.close()
        context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
        context.route('**/*.woff2',lambda route:route.abort())
        page=context.new_page();page.goto(base_url,wait_until='networkidle')
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
        assert page.locator('h1').is_visible()
        page.screenshot(path=str(out/f'fallback-{width}.png'))
        context.close()
    normal=browser.new_context(viewport={'width':1440,'height':900},reduced_motion='no-preference')
    page=normal.new_page();page.goto(base_url,wait_until='networkidle')
    for selector in ['#capabilities .section-heading','#experience .lab-layout','#process .process-explorer','#about .about-heading','#contact .brief']:
        element=page.locator(selector)
        element.scroll_into_view_if_needed()
        expect(element).to_have_css('opacity','1')
    normal.close()
    browser.close()
# Compare only the approved hero, at identical size with reduced motion.
with Image.open(out/'approved-a-1440.png') as a, Image.open(out/'hero-1440.png') as b:
    a=a.convert('RGB').crop((0,0,1440,604));b=b.convert('RGB').crop((0,0,1440,604))
    difference=ImageChops.difference(a,b)
    changed=sum(1 for value in difference.get_flattened_data() if max(value)>2)
    regression={'hero_crop':[1440,604],'changed_pixels_above_2_255':changed,'total_pixels':1440*604}
    canvas=Image.new('RGB',(1968,467),'#080d13');draw=ImageDraw.Draw(canvas)
    for x,label,im in [(16,'APPROVED MILESTONE A',a),(992,'MILESTONE B - SAME HERO',b)]:
        draw.text((x,16),label,fill='#eaf2fc',font=ImageFont.load_default(size=18))
        canvas.paste(im.resize((960,403),Image.Resampling.LANCZOS),(x,50))
    canvas.save(out/'hero-before-after.webp',quality=94,method=6)
(out/'results.json').write_text(json.dumps({'viewports':results,'no_js_and_font_fallback':'passed at 1440 and 390','normal_first_load_reveals':'passed for new sections','hero_comparison':regression},indent=2)+'\n')
print(json.dumps({'results':results,'hero_comparison':regression},indent=2))
