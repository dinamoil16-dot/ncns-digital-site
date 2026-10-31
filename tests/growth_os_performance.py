"""Local Chromium lab measurements, not field CWV or real mobile hardware evidence."""
import http.server,threading,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];QA=ROOT/'docs/qa/milestone-c2/growth-os'
class H(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();results=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'))
  for width,height in [(1440,900),(390,844),(360,780)]:
   context=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce');page=context.new_page();cdp=context.new_cdp_session(page);cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
   page.add_init_script("window.qaCLS=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.qaCLS+=e.value}).observe({type:'layout-shift',buffered:true})")
   page.goto(f'http://127.0.0.1:{s.server_port}/work/growth-os/',wait_until='networkidle');page.locator('#overview').scroll_into_view_if_needed()
   latency=page.evaluate("""async()=>{const start=performance.now(),el=document.getElementById('channel');el.value='outbound';el.dispatchEvent(new Event('change',{bubbles:true}));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));return performance.now()-start}""")
   assert page.locator('#kpiLeads').inner_text()=='58'
   results.append(page.evaluate("""({width,latency})=>({width,cpu_throttle:4,filter_to_second_frame_ms:Math.round(latency*10)/10,local_document_dom_ready_ms:Math.round(performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd),observed_layout_shift_score:window.qaCLS,subresource_transfer_bytes:performance.getEntriesByType('resource').reduce((a,e)=>a+e.transferSize,0),scope:'local HTTP; no network throttling; synthetic CPU slowdown; not field CWV or real hardware'})""",{'width':width,'latency':latency}));context.close()
  b.close()
finally:s.shutdown()
(QA/'performance.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
