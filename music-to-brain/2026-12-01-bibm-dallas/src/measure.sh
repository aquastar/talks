#!/bin/bash
# Build, dump, render and gate one version for RSI review. Usage: measure.sh OUTDIR
# Exits 1 if the build gate or the layout gate fails (sheets are still written).
OUT=$1; mkdir -p $OUT; D=$(cd "$(dirname "$0")" && pwd); RC=0
python3 -I $D/build.py > $OUT/build.txt || RC=1
grep -q "OVER BUDGET\|^gate:\|violations: \[" $OUT/build.txt && RC=1
python3 -I $D/dump.py $D/../index.html $OUT/version.md
OUT=$OUT node $D/shoot.js > $OUT/overflow.txt 2>&1 || RC=1
python3 -I - "$OUT" <<'PY' >> $OUT/overflow.txt
import glob, sys, json, colorsys
from PIL import Image
o = sys.argv[1]
fs = sorted(glob.glob(o + '/s[0-9][0-9].png'))
for k in range(0, len(fs), 6):
    ims = [Image.open(f).resize((800, 450)) for f in fs[k:k+6]]
    sh = Image.new('RGB', (1600, 450 * ((len(ims) + 1) // 2)), 'white')
    for j, im in enumerate(ims): sh.paste(im, ((j % 2) * 800, (j // 2) * 450))
    sh.save(f'{o}/sheet_{k:02d}-{min(k+5, len(fs)-1):02d}.png')
# palette check on non exempt raster images
boxes = json.load(open(o + '/imgboxes.json'))
OK = [(20, 35), (255, 275), (185, 195)]
for i, bl in boxes.items():
    for b in bl:
        if b['exempt'] or b['w'] < 40: continue
        im = Image.open(f'{o}/s{int(i):02d}.png').convert('RGB').crop((int(b['x']), int(b['y']), int(b['x'] + b['w']), int(b['y'] + b['h']))).resize((120, 80))
        px = list(im.getdata()); sat = off = 0
        for r, g, bb in px:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, bb / 255)
            if s > 0.45 and v > 0.25:
                sat += 1
                if not any(a <= h * 360 <= z for a, z in OK): off += 1
        if off / len(px) > 0.02: print(f'off palette: slide {i}, {b["src"].split("/")[-1]} ({100*off/len(px):.0f} percent)')
PY
cat $OUT/build.txt $OUT/overflow.txt
exit $RC
