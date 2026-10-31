"""Validate Cloudflare Pages release output. No network access or deployment."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
dist=ROOT/"dist"
assert not dist.exists(), "dist should be absent in a clean checkout"
try:
    subprocess.run([sys.executable,str(ROOT/"scripts/build_pages.py")],cwd=ROOT,check=True)
    assert dist.is_dir()
    expected={"index.html","styles.css","milestone-b.css","agency.css","main.js",
      "contact.js","contact-config.json","privacy.html","terms.html","solutions",
      "assets","robots.txt","sitemap.xml"}
    assert {p.name for p in dist.iterdir()}==expected
    assert (dist/"assets/ncns-original-logo.webp").is_file()
    assert (dist/"assets/social/ncns-digital.png").is_file()
    assert (dist/"solutions/index.html").is_file()
    assert not any((dist/x).exists() for x in ["README.md","AGENTS.md","docs",".github","tests","spec","reference","scripts","site-config.json"])
    homepage=(dist/"index.html").read_text()
    assert 'href="https://ncns.digital/"' in homepage
    assert 'content="https://ncns.digital/assets/social/ncns-digital.png"' in homepage
    assert 'href="mailto:ncns.digital@gmail.com"' in homepage
    assert 'href="https://www.instagram.com/ncns.digital/"' in homepage
    assert 'href="https://wa.me/79063231457"' in homepage
    assert homepage.count('class="footer-social-link"')==3
    assert "https://ncns.digital/sitemap.xml" in (dist/"robots.txt").read_text()
    assert "https://ncns.digital/solutions/" in (dist/"sitemap.xml").read_text()
    c=json.loads((dist/"contact-config.json").read_text())
    assert c["formEndpoint"]=="https://formspree.io/f/mjyyagao"
    assert c["formEnabled"] and c["formDeliveryVerified"]
    print("Cloudflare release bundle PASSED: canonical, safe allowlist, site services and Formspree config. Nothing deployed.")
finally:
    if dist.is_dir() and not dist.is_symlink():
        shutil.rmtree(dist)
