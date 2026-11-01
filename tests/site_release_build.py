"""Validate Cloudflare Pages release output. No network access or deployment."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
dist=ROOT/"dist"
assert not dist.exists(), "dist should be absent in a clean checkout"
try:
    subprocess.run([sys.executable,str(ROOT/"scripts/build_pages.py")],cwd=ROOT,check=True)
    assert dist.is_dir()
    expected={"index.html","404.html","_headers","styles.css","milestone-b.css","agency.css","main.js",
      "contact.js","contact-config.json","privacy.html","terms.html","solutions",
      "assets","robots.txt","sitemap.xml"}
    assert {p.name for p in dist.iterdir()}==expected
    assert (dist/"assets/ncns-original-logo.webp").is_file()
    assert (dist/"assets/social/ncns-digital.png").is_file()
    assert (dist/"solutions/index.html").is_file()
    missing=(dist/"404.html").read_text(encoding="utf-8")
    assert "Page not found" in missing and 'content="noindex,follow"' in missing
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
    # Search discovery: unique, descriptive pages and crawlable internal navigation.
    assert "<title>Web Development &amp; AI Automation Agency | NCNS Digital</title>" in homepage
    assert 'name="description" content="NCNS Digital builds custom websites' in homepage
    assert '<nav class="footer-links" aria-label="Footer"><a href="./solutions/">Services</a>' in homepage
    services = (dist / "solutions/index.html").read_text(encoding="utf-8")
    assert "<title>Websites, AI Agents &amp; Business Automation | NCNS Digital</title>" in services
    assert 'name="description" content="Explore web development, e-commerce, AI agents' in services
    assert "AI agents, website chatbots" in services and "SEO, website optimization" in services
    assert 'href="https://ncns.digital/solutions/"' in services
    assert 'content="https://ncns.digital/solutions/"' in services
    assert "https://ncns.digital/solutions/" in (dist / "sitemap.xml").read_text()
    print("Cloudflare release bundle PASSED: canonical, SEO titles/descriptions, safe allowlist, services and Formspree config. Nothing deployed.")
finally:
    if dist.is_dir() and not dist.is_symlink():
        shutil.rmtree(dist)
