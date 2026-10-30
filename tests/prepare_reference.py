"""Encode the actual owner-supplied reference and assemble the review collage."""
import argparse
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
qa = root / 'docs/qa/issue-1-rework'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path, help='The exact owner-supplied reference, never generated scenery')
args = parser.parse_args()
with Image.open(args.source) as source:
    reference = source.convert('RGB')
    if args.source.suffix.lower() == '.webp':
        if args.source.resolve() != (root / 'reference/approved-concept.webp').resolve():
            shutil.copyfile(args.source, root / 'reference/approved-concept.webp')
    else:
        reference.save(root / 'reference/approved-concept.webp', quality=92, method=6)
    shutil.copyfile(root / 'reference/approved-concept.webp', qa / 'approved-target.webp')
with Image.open(qa / 'after-1440.png') as screenshot:
    actual = screenshot.convert('RGB')
width = 1000
images = [reference, actual]
images = [im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS) for im in images]
canvas = Image.new('RGB', (width * 2 + 48, max(im.height for im in images) + 80), '#080d13')
draw = ImageDraw.Draw(canvas)
for x, label, image in zip([16, width + 32], ['APPROVED REFERENCE (full composition)', 'REAL CHROMIUM - 1440 x 900'], images):
    draw.text((x, 22), label, fill='#eaf2fc', font=ImageFont.load_default(size=18))
    canvas.paste(image, (x, 60))
canvas.save(qa / 'approved-vs-actual.webp', quality=92, method=6)
# Equal-width focus comparison covers only the authorized hero/services scope.
with Image.open(qa / 'hero-services-1440.png') as screenshot:
    actual_focus = screenshot.convert('RGB')
reference_focus = reference.crop((0, 0, reference.width, round(reference.height * 838 / 1286)))
panels = [reference_focus, actual_focus]
panels = [im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS) for im in panels]
focus = Image.new('RGB', (width * 2 + 48, max(im.height for im in panels) + 80), '#080d13')
draw = ImageDraw.Draw(focus)
for x, label, im in zip([16, width + 32], ['APPROVED - HERO / SERVICES', 'ACTUAL CHROMIUM - HERO / SERVICES'], panels):
    draw.text((x, 22), label, fill='#eaf2fc', font=ImageFont.load_default(size=18))
    focus.paste(im, (x, 60))
focus.save(qa / 'approved-vs-actual-focus.webp', quality=92, method=6)
print('Saved original reference, QA copy, full-reference / 1440 viewport comparison, and hero/services focus comparison.')
