"""Prepare a static review artifact after an owner supplies the canonical origin. Never deploys."""
import argparse,json,re,shutil
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--origin',help='Owner-approved HTTPS origin; defaults to site-config.json');a=p.parse_args()
origin=(a.origin or json.loads((ROOT/'site-config.json').read_text()).get('canonicalOrigin','')).rstrip('/')
u=urlsplit(origin)
valid_host=bool(u.hostname and re.fullmatch(r'(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z][a-zA-Z0-9-]{1,62}',u.hostname))
if not valid_host or not origin or u.scheme!='https' or not u.hostname or u.username or u.password or u.port or u.path or u.query or u.fragment:p.error('Set an owner-approved HTTPS canonical origin (no path, credentials, query or port). Domain is currently unconfirmed; nothing was built.')
out=a.output.resolve()
if out==ROOT or ROOT.is_relative_to(out) or out.is_relative_to(ROOT) or out.exists():p.error('Use a new output directory, outside the source repository, not an existing directory.')
out.mkdir(parents=True)
for name in ['index.html','styles.css','milestone-b.css','agency.css','main.js','contact.js','contact-config.json','privacy.html','terms.html','solutions','assets']:
 src=ROOT/name;dst=out/name
 if src.is_dir():shutil.copytree(src,dst)
 else:shutil.copy2(src,dst)
for path,url in [('index.html',origin+'/'),('solutions/index.html',origin+'/solutions/'),('privacy.html',origin+'/privacy.html'),('terms.html',origin+'/terms.html')]:
 f=out/path;s=f.read_text();s=re.sub(r'<link rel="canonical"[^>]*>\s*','',s)
 s=s.replace('</head>',f'<link rel="canonical" href="{url}" />\n<meta property="og:url" content="{url}" />\n</head>')
 s=s.replace('content="./assets/social/ncns-digital.png"',f'content="{origin}/assets/social/ncns-digital.png"').replace('content="../assets/social/ncns-digital.png"',f'content="{origin}/assets/social/ncns-digital.png"')
 if path=='index.html':
  match=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
  schema=json.loads(match.group(1));schema.update(url=origin+'/',logo=origin+'/assets/ncns-original-logo.webp')
  s=s[:match.start(1)]+json.dumps(schema,separators=(',',':'))+s[match.end(1):]
 f.write_text(s)
(out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\n')
(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+origin+'/</loc></url><url><loc>'+origin+'/solutions/</loc></url></urlset>\n')
print(json.dumps({'artifact':str(out),'canonicalOrigin':origin,'status':'prepared locally; NOT deployed','contactDeliveryVerified':json.loads((ROOT/'contact-config.json').read_text()).get('deliveryVerified',False)},indent=2))
