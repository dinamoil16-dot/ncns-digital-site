"""Encode genuine recordings for manual editorial review. Never posts or synthesizes UI actions."""
import os,subprocess,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEMO=Path(os.environ.get('NCNS_GROWTH_WORKTREE','/workspace/ncns-digital-site'))
OUT=ROOT/'docs/launch/marketing/reels';OUT.mkdir(exist_ok=True)
sources=[(DEMO/'docs/qa/milestone-c2/growth-os/walkthrough-390.webm','growth-os','INTERACTIVE DEMO / FICTIONAL DATA','Local plan. No messages sent.'),(ROOT/'docs/qa/first-clients/experience-lab-mobile.webm','experience-lab','BROWSER-LOCAL REQUIREMENTS TOOL','Draft only. No enquiry sent.')]
manifest=[]
for source,slug,title,footer in sources:
 output=OUT/f'{slug}.mp4'
 filters=f"scale=900:1660:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x03070c,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='{title}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=48,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='{footer}':fontcolor=white:fontsize=31:x=(w-text_w)/2:y=1830"
 subprocess.run(['ffmpeg','-y','-i',str(source),'-vf',filters,'-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(output)],text=True))
 manifest.append({'file':output.name,'source':str(source.relative_to(DEMO if slug=='growth-os' else ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'duration_seconds':duration,'dimensions':[1080,1920],'status':'DRAFT for manual owner review; not posted','processing':'scale/pad only; constant truthful labels; original actions and timing retained; silent'})
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
