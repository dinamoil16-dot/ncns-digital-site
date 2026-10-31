"""Record actual normal-motion Chromium: hero, services, native scroll and requirements tool."""
import argparse
import base64
import json
import math
import subprocess
import tempfile
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mobile',action='store_true')
args=parser.parse_args()
width,height=(390,844) if args.mobile else (1440,900)
stem='mobile-preview' if args.mobile else 'desktop-preview'
root=Path(__file__).resolve().parents[1]
out=root/'docs/qa/milestone-b'
out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='ncns-milestone-b-') as tmp, sync_playwright() as p:
    tmp=Path(tmp)
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='no-preference',has_touch=args.mobile,is_mobile=args.mobile)
    context.grant_permissions(['clipboard-read','clipboard-write'])
    page=context.new_page();errors=[];writes=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:writes.append(r.url) if r.method!='GET' else None)
    page.goto('http://127.0.0.1:8000',wait_until='networkidle')
    page.evaluate('document.fonts.ready')
    cdp=context.new_cdp_session(page);frames=[]
    def frame(event):
        path=tmp/f'frame-{len(frames):05d}.jpg'
        path.write_bytes(base64.b64decode(event['data']))
        frames.append((path,event['metadata']['timestamp']))
        cdp.send('Page.screencastFrameAck',{'sessionId':event['sessionId']})
    cdp.on('Page.screencastFrame',frame)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':86,'maxWidth':width,'maxHeight':height,'everyNthFrame':2})
    start=time.monotonic()
    halo_start=page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime')
    page.wait_for_timeout(650)
    if not args.mobile:
        for index in range(24):
            page.mouse.move(900+160*math.sin(index/23*math.pi*2),240+60*math.cos(index/23*math.pi*2))
            page.wait_for_timeout(35)
        depth=page.locator('.hero').evaluate('(e)=>e.style.getPropertyValue("--scene-x")')
        assert depth
        assert page.locator('#heroOrbit').evaluate('(e)=>getComputedStyle(e).transform')=='none'
    page.wait_for_timeout(650)
    page.evaluate("document.querySelector('#services').scrollIntoView({behavior:'smooth'})")
    page.wait_for_timeout(750)
    if not args.mobile:
        page.locator('.service-web').hover(position={'x':80,'y':60})
        page.wait_for_timeout(500)
        page.locator('.service-brand').hover(position={'x':220,'y':130})
        page.wait_for_timeout(500)
    else:
        page.mouse.wheel(0,160);page.wait_for_timeout(500)
    page.evaluate("document.querySelector('#experience').scrollIntoView({behavior:'smooth'})")
    page.wait_for_timeout(850)
    page.evaluate("document.querySelector('#labForm').scrollIntoView({behavior:'smooth',block:'start'})")
    page.wait_for_timeout(600)
    page.locator('#labService').select_option('Websites & Web Development')
    page.locator('#labNext').click()
    page.locator('#labGoal').press_sequentially('A considered multilingual website for an independent studio.',delay=13)
    page.locator('#labTiming').select_option('Within 1–3 months')
    page.locator('input[value="Responsive implementation"]').check()
    page.wait_for_timeout(400)
    page.locator('#labNext').click()
    page.wait_for_timeout(750)
    page.locator('#copyLab').click()
    expect(page.locator('#labCopyStatus')).to_contain_text('Copied')
    page.wait_for_timeout(400)
    page.locator('#useLab').click()
    page.wait_for_timeout(850)
    assert 'A considered multilingual website' in page.locator('#projectDetails').input_value()
    page.wait_for_timeout(max(0,20000-(time.monotonic()-start)*1000))
    end_epoch=time.time()
    halo_end=page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime')
    cdp.send('Page.stopScreencast')
    assert not errors,errors
    assert not writes,writes
    assert len(frames)>40,len(frames)
    sequence=['ffconcat version 1.0']
    for i,(path,timestamp) in enumerate(frames):
        duration=frames[i+1][1]-timestamp if i+1<len(frames) else max(.033,end_epoch-timestamp)
        sequence += [f"file '{path}'",'option framerate 1000',f'duration {max(.001,duration):.6f}']
    sequence += [f"file '{frames[-1][0]}'",'option framerate 1000']
    (out/f'{stem}-timing.json').write_text(json.dumps({'timestamps':[stamp-frames[0][1] for _,stamp in frames],'capture_seconds':end_epoch-frames[0][1]},indent=2)+'\n')
    seq=tmp/'frames.ffconcat';seq.write_text('\n'.join(sequence)+'\n')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-safe','0','-f','concat','-i',str(seq),'-fps_mode','passthrough','-enc_time_base','1:1000','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','6','-crf','32','-b:v','0','-pix_fmt','yuv420p','-an',str(out/f'{stem}.webm')],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(out/f'{stem}.webm')]))
    encoded_seconds=float(probe['format']['duration'])
    assert abs(encoded_seconds-(end_epoch-frames[0][1]))<.75, (encoded_seconds,end_epoch-frames[0][1])
    metadata={'encoded_seconds':encoded_seconds,'source':'real Chromium CDP frames with original timestamps','viewport':[width,height],'frames':len(frames),'capture_seconds':end_epoch-frames[0][1],'halo_elapsed_ms':halo_end-halo_start,'reduced_motion':False,'js_errors':errors,'data_submissions':writes,'sequence':['normal-motion hero','scenery depth and service hover (desktop)','native scrolling','requirements builder','copy result','transfer to editable offline brief']}
    (out/f'{stem}.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metadata,indent=2))
    context.close();browser.close()
