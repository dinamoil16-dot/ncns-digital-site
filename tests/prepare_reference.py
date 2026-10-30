"""Encode the actual owner-supplied reference and assemble the review collage."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
qa = root / 'docs/qa/issue-1-rework'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path, help='The exact owner-supplied reference, never generated scenery')
args = parser.parse_args()
with Image.open(args.source) as source:
    reference = source.convert('RGB')
    reference.save(root / 'reference/approved-concept.webp', quality=92, method=6)
    reference.save(qa / 'approved-target.webp', quality=92, method=6)
with Image.open(qa / 'after-1440.png') as screenshot:
    actual = screenshot.convert('RGB')
width = 1000
images = [reference, actual]
images = [im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS) for im in images]
canvas = Image.new('RGB', (width * 2 + 48, max(im.height for im in images) + 80), '#080d13')
draw = ImageDraw.Draw(canvas)
for x, label, image in zip([16, width + 32], ['APPROVED REFERENCE (full composition)', 'REAL CHROMIUM — 1440 x 900'], images):
    draw.text((x, 22), label, fill='#eaf2fc')
    canvas.paste(image, (x, 60))
canvas.save(qa / 'approved-vs-actual.webp', quality=92, method=6)
print('Saved exact reference encoding, QA target and approved-vs-actual.webp; visual review is still required.')
