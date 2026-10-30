"""Capture real Chromium frames with their timestamps; encode a short review WebM."""
import argparse
import base64
import json
import math
import subprocess
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mobile', action='store_true')
args = parser.parse_args()
width, height = (390, 900) if args.mobile else (1440, 900)
stem = 'chromium-mobile-motion' if args.mobile else 'chromium-motion'
root = Path(__file__).resolve().parents[1]
out = root / 'docs/qa/issue-1-rework/emblem'
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='ncns-emblem-') as scratch, sync_playwright() as playwright:
    scratch = Path(scratch)
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width':width, 'height':height}, reduced_motion='no-preference', has_touch=args.mobile, is_mobile=args.mobile)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:8000', wait_until='networkidle')
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(1200)
    cdp = context.new_cdp_session(page)
    frames = []
    def frame(event):
        path = scratch / f'frame-{len(frames):05d}.jpg'
        path.write_bytes(base64.b64decode(event['data']))
        frames.append((path, event['metadata']['timestamp']))
        cdp.send('Page.screencastFrameAck', {'sessionId':event['sessionId']})
    cdp.on('Page.screencastFrame', frame)
    cdp.send('Page.startScreencast', {'format':'jpeg', 'quality':88, 'maxWidth':width, 'maxHeight':height, 'everyNthFrame':2})
    halo_start = page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime')
    # About 10 seconds of real elapsed page motion, including gentle pointer depth.
    for step in range(100):
        phase = step / 99 * math.tau
        if not args.mobile:
            page.mouse.move(970 + 110 * math.sin(phase), 260 + 70 * math.cos(phase))
        page.wait_for_timeout(85)
    cdp.send('Page.stopScreencast')
    halo_end = page.locator('.orbit-ring').evaluate('(e)=>e.getAnimations({subtree:true})[0].currentTime')
    assert not errors, errors
    assert len(frames) > 40, len(frames)
    assert halo_end > halo_start + 7000
    sequence = scratch / 'frames.ffconcat'
    lines = ['ffconcat version 1.0']
    for index, (path, timestamp) in enumerate(frames):
        duration = frames[index+1][1] - timestamp if index+1 < len(frames) else 1/30
        lines.extend([f"file '{path}'", f'duration {max(duration, 0.001):.6f}'])
    sequence.write_text('\n'.join(lines)+'\n')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-safe','0','-f','concat','-i',str(sequence),'-fps_mode','vfr','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','6','-crf','32','-b:v','0','-pix_fmt','yuv420p','-an',str(out/f'{stem}.webm')],check=True)
    (out/f'{stem}.json').write_text(json.dumps({'source':'actual Chromium CDP screencast; original frame timestamps preserved','viewport':[width,height],'frames':len(frames),'captured_seconds':frames[-1][1]-frames[0][1],'halo_elapsed_ms':halo_end-halo_start,'js_errors':errors,'reduced_motion':False},indent=2)+'\n')
    context.close()
    browser.close()
print('Saved actual Chromium recording and capture metadata.')
