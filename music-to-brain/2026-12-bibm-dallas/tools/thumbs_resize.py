"""Shrink thumbs/*.png to 400 px wide after tools/thumbs.js."""
import glob, os
from PIL import Image
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'thumbs')
for f in glob.glob(os.path.join(d, '*.png')):
    im = Image.open(f).convert('RGB')
    im.resize((400, round(400 * im.height / im.width)), Image.LANCZOS).save(f, optimize=True)
