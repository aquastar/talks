"""Dump the built deck to markdown for reviewers: one block per slide with mark, headline,
visible text, images, audio, status labels, references and speaker notes.
Usage: python3 -I dump.py ../index.html out.md"""
import re, sys, html
src = open(sys.argv[1]).read()
secs = re.findall(r'<section(.*?)>(.*?)</section>', src, flags=re.S)
out = []
def txt(s):
    s = re.sub(r'<svg.*?</svg>', lambda m: ' [svg: ' + ' / '.join(t.strip() for t in re.findall(r'>([^<>]{2,})<', m.group(0)) if t.strip()) + '] ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()
for i, (attr, body) in enumerate(secs):
    notes = re.search(r'<aside class="notes">(.*?)</aside>', body, flags=re.S)
    ref = re.search(r'<div class="ref">(.*?)</div>', body, flags=re.S)
    b = re.sub(r'<aside class="notes">.*?</aside>', '', body, flags=re.S)
    b = re.sub(r'<div class="ref">.*?</div>', '', b, flags=re.S)
    imgs = [x.split('/')[-1] for x in re.findall(r'<img[^>]*src="([^"]+)"', b)]
    aud = [x.split('/')[-1] for x in re.findall(r'data-audio="([^"]+)"', b)]
    frames = re.findall(r'data-src="([^"]+)"', b)
    out.append(f'## Slide {i}' + (' (auto-animate)' if 'auto-animate' in attr else ''))
    out.append('Text: ' + txt(b))
    if imgs: out.append('Images: ' + ', '.join(imgs))
    if aud: out.append('Audio buttons: ' + ', '.join(aud))
    if frames: out.append('Embedded animation: ' + ', '.join(frames))
    if ref: out.append('Reference: ' + txt(ref.group(1)))
    if notes: out.append('Notes: ' + txt(notes.group(1)))
    out.append('')
open(sys.argv[2], 'w').write('\n'.join(out))
print(len(secs), 'slides')
