"""Compatibility entry point: standalone agency QA supersedes the retired demo overlay."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('agency_site_browser.py')), run_name='__main__')
