"""Build the reviewed NCNS public website for Cloudflare Pages.

Cloudflare Pages settings:
  Build command: python3 scripts/build_pages.py
  Build output directory: dist
  Root directory: repository root

The source repository contains review assets and internal tests that MUST NOT be
published. This script delegates the strict allowlist to prepare_site.py and
only copies that safe result into the Pages upload directory. No deployment,
domain registration, account access, or external request is made.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"

def build():
    if OUT.is_symlink() or OUT.exists():
        raise SystemExit("Refusing to overwrite dist. Build from a clean checkout, or remove a previously generated dist after reviewing it.")
    with tempfile.TemporaryDirectory(prefix="ncns-pages-") as temp:
        target = Path(temp) / "public-site"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "prepare_site.py"), "--output", str(target)],
            cwd=ROOT, check=True
        )
        expected = {
            "index.html", "styles.css", "milestone-b.css", "agency.css",
            "main.js", "contact.js", "contact-config.json",
            "privacy.html", "terms.html", "solutions", "assets",
            "robots.txt", "sitemap.xml"
        }
        names = {p.name for p in target.iterdir()}
        if names != expected:
            raise SystemExit("Release allowlist mismatch; refusing to publish unreviewed files.")
        settings = json.loads((target / "contact-config.json").read_text())
        if settings.get("formEnabled") is not True or settings.get("formEndpoint") != "https://formspree.io/f/mjyyagao":
            raise SystemExit("Direct enquiry form is not configured to the confirmed NCNS endpoint.")
        if "https://ncns.digital" not in (target / "index.html").read_text():
            raise SystemExit("Canonical domain missing. Do not deploy.")
        shutil.copytree(target, OUT)
    print("Prepared static site in dist/ for Cloudflare Pages. Not deployed.")

if __name__ == "__main__":
    build()
