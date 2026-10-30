"""Compatibility entry point: run the current Milestone B browser acceptance suite."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('milestone_b_browser.py')), run_name='__main__')
