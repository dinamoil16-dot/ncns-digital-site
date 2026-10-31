"""Static launch-readiness checks. No network, no actual Formspree submission."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text(encoding="utf-8")

home = read("index.html")
privacy = read("privacy.html")
terms = read("terms.html")
not_found = read("404.html")
config = json.loads(read("contact-config.json"))
origin = json.loads(read("site-config.json"))["canonicalOrigin"]

assert origin == "https://ncns.digital"
assert config["formProvider"] == "formspree"
assert config["formEndpoint"] == "https://formspree.io/f/mjyyagao"
assert config["formEnabled"] is True
assert config["formDeliveryVerified"] is True
assert "ncns.digital@gmail.com" in privacy
assert "Cloudflare Pages" in privacy
assert "independent freelance digital-services provider" in privacy
assert "not a separately incorporated company" in privacy
assert "country of incorporation" in privacy
assert "independent freelance digital-services provider" in terms
assert "not a separately incorporated company" in terms
assert "Formspree" in privacy and "Gmail" in privacy
assert "deletion" in privacy.lower()
assert "under owner review" not in privacy.lower()
assert "before public launch" not in privacy.lower()
assert "when the provider has been configured" not in privacy.lower()
assert "real inbox receipt was verified with a controlled test" not in privacy.lower()
assert "written" in terms and "Formspree" in terms
assert "before public launch" not in terms.lower()
assert "one synthetic formspree notification" not in terms.lower()
assert '<meta name="robots" content="noindex,follow"' in not_found
assert "Page not found" in not_found and 'href="/"' in not_found
assert "404.html" in read("scripts/prepare_site.py")
assert "_headers" in read("scripts/prepare_site.py")
assert "X-Robots-Tag: noindex" in read("_headers")
assert "https://ncns-digital-site.pages.dev/*" in read("_headers")
assert "404.html" in read("scripts/build_pages.py")
assert "404.html" in read("tests/site_release_build.py")
assert 'href="./privacy.html"' in home
assert 'href="./terms.html"' in home
assert 'id="briefForm"' in home
assert 'id="privacyConsent"' in home
assert home.count('class="footer-social-link"') == 3
print("NCNS live content readiness PASSED: privacy, terms, form, canonical, public 404 and links.")
