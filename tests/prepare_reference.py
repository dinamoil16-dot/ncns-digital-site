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
# Keep the emblem review crops reproducible from real, identically scoped captures.
emblem = qa / 'emblem'
if (emblem / 'before-1440.png').exists():
    box = (700, 12, 1280, 590)
    for name, source in [('before-closeup.png', emblem / 'before-1440.png'), ('after-closeup.png', qa / 'after-1440.png')]:
        with Image.open(source) as shot:
            shot.crop(box).save(emblem / name)
    canvas = Image.new('RGB', (1208, 650), '#080d13')
    draw = ImageDraw.Draw(canvas)
    for x, label, name in [(16, 'BEFORE - OPAQUE DISC', 'before-closeup.png'), (612, 'AFTER - SCENE INTEGRATION', 'after-closeup.png')]:
        draw.text((x, 18), label, fill='#eaf2fc', font=ImageFont.load_default(size=18))
        with Image.open(emblem / name) as shot:
            canvas.paste(shot, (x, 58))
    canvas.save(emblem / 'before-after-closeup.webp', quality=94, method=6)
    scale = reference.width / 1440
    target_crop = reference.crop(tuple(round(value * scale) for value in box)).resize((580, 578), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (1208, 650), '#080d13')
    draw = ImageDraw.Draw(canvas)
    for x, label in [(16, 'APPROVED REFERENCE'), (612, 'UPDATED CHROMIUM - 1440 PX')]:
        draw.text((x, 18), label, fill='#eaf2fc', font=ImageFont.load_default(size=18))
    canvas.paste(target_crop, (16, 58))
    with Image.open(emblem / 'after-closeup.png') as shot:
        canvas.paste(shot, (612, 58))
    canvas.save(emblem / 'reference-actual-closeup.webp', quality=94, method=6)
if (qa / 'before-1440.png').exists():
    canvas = Image.new('RGB', (1968, 660), '#080d13')
    draw = ImageDraw.Draw(canvas)
    for x, label, name in [(16, 'REJECTED IMPLEMENTATION - BEFORE', 'before-1440.png'), (992, 'FINAL REWORK - ACTUAL CHROMIUM', 'after-1440.png')]:
        draw.text((x, 16), label, fill='#eaf2fc', font=ImageFont.load_default(size=18))
        with Image.open(qa / name) as shot:
            canvas.paste(shot.convert('RGB').resize((960, 600), Image.Resampling.LANCZOS), (x, 48))
    canvas.save(qa / 'before-vs-after.webp', quality=92, method=6)
