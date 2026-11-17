"""Build koopman-eeg/2026-12-02-bibm/index.html from src/slides.html.
Placeholders:
  {{COVER}}                 animated real EEG lines for the cover
  {{EEG:name|w|h|mode}}     real CHB-MIT chb01 clip from clips.json (seizure, preictal, interictal)
  {{MAP:key}}               the two roads map, current stop in orange (sz1 sz2 sz3 kp1 kp2 kp3 kp4 ks)
  {{F1BARS}} {{ABL}}        results drawn from the paper tables
  {{PIPE}}                  running example pipeline
  {{CIRCLE}}                chb01 learned eigenvalues (digitized from the paper figure) with a band
  {{DEMO}}                  interactive spectrum demo
  {{PEOPLE:file|name|aff}}  a photo with name
Run: python3 -I src/build.py
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INK, INK2, LINE, AXIS, RULE, GROUP = '#1F1E1B', '#5F5D50', '#7C878E', '#ACA39A', '#D7D2CB', '#EFEBE5'
ACC, ACCT, PUR, PURT, TEAL, TEALT, FAIL = '#F76902', '#FAD6BA', '#7D55C7', '#DCD1EB', '#009CBD', '#BCE2E8', '#DA291C'
PRE, INTER = PUR, TEAL   # fixed for the whole talk: pre-ictal purple, inter-ictal teal

def T(x, y, s, size=22, fill=INK, anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

def head(x1, y1, x0, y0, col, L=12, Wd=5.5):
    a = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - L * math.cos(a), y1 - L * math.sin(a)
    px, py = -math.sin(a) * Wd, math.cos(a) * Wd
    return f'<path d="M{x1:.1f},{y1:.1f} L{bx+px:.1f},{by+py:.1f} L{bx-px:.1f},{by-py:.1f} z" fill="{col}"/>'

def arrow(x0, y0, x1, y1, col=LINE, w=1.5):
    a = math.atan2(y1 - y0, x1 - x0)
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1 - 10*math.cos(a):.1f}" y2="{y1 - 10*math.sin(a):.1f}" stroke="{col}" stroke-width="{w}"/>'
            + head(x1, y1, x0, y0, col))

CLIPS = json.load(open(os.path.join(HERE, 'clips.json')))

def traces(name, x0, y0, w, h, col=INK2, gain=None, every=1, sw=1.0):
    c = CLIPS[name]; rows = c['uV']; n = len(rows); dy = h / n
    g = gain or (dy * 0.45 / 80.0)
    s = []
    for k, r in enumerate(rows):
        r = r[::every]; m = sum(r) / len(r); dx = w / (len(r) - 1); yc = y0 + dy * (k + 0.5)
        pts = ' '.join(f'{x0 + i*dx:.1f},{yc - max(-dy*1.4, min(dy*1.4, (v - m) * g)):.1f}' for i, v in enumerate(r))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>')
    return ''.join(s)

def eeg(spec):
    name, w, h, mode = (spec.split('|') + ['', '', '', ''])[:4]
    w, h = int(w or 1100), int(h or 360)
    c = CLIPS[name]; lab_w = 92
    s = [f'<svg class="fig" viewBox="0 -10 {w + 20} {h + 60}" style="width:{w}px" data-id="eeg-{name}">']
    for k, ch in enumerate(c['channels']):
        s.append(T(lab_w - 12, (k + 0.5) * h / len(c['channels']) + 6, ch, 16, INK2, 'end'))
    col = {'preictal': PRE, 'interictal': INTER}.get(name, INK2) if mode != 'gray' else INK2
    s.append(traces(name, lab_w, 0, w - lab_w, h, col, every=1 if c['secs'] <= 10 else 2, sw=1.0))
    secs = c['secs']
    for t in range(0, secs + 1, 5 if secs > 10 else 2):
        x = lab_w + (w - lab_w) * t / secs
        s.append(f'<line x1="{x:.1f}" y1="{h + 16}" x2="{x:.1f}" y2="{h + 22}" stroke="{AXIS}"/>')
        s.append(T(x, h + 44, f'{t} s', 17, INK2, 'middle'))
    if name == 'seizure':
        x = lab_w + (w - lab_w) * 10 / secs
        s.append(f'<line x1="{x:.1f}" y1="-4" x2="{x:.1f}" y2="{h}" stroke="{FAIL}" stroke-width="2" stroke-dasharray="6 5"/>')
    s.append('</svg>')
    return ''.join(s)

def cover():
    w, h = 1152, 150
    s = [f'<svg class="cover-eeg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
         '<defs><clipPath id="cv"><rect class="cv-reveal" x="0" y="0" width="0" height="150"/></clipPath></defs>',
         f'<g clip-path="url(#cv)">' + traces('preictal', 0, 0, w, h, PRE, every=1, sw=1.0) + '</g></svg>']
    return ''.join(s)

# ---------------------------------------------------------------- map: two roads meet
STOPS = {
    'sz1': (150, 90, 'Hand features', '1970s to 2000s'),
    'sz2': (420, 90, 'Deep nets on raw EEG', '2017 to now'),
    'sz3': (690, 90, 'More sensors', 'previous talk: EEG, ECG, EMG'),
    'kp1': (150, 300, 'Koopman', '1931'),
    'kp2': (420, 300, 'Mode decomposition', 'fluids 2009, brains 2016'),
    'kp3': (690, 300, 'Deep Koopman', '2018'),
    'ks':  (940, 195, 'KSNet', 'predict from the spectrum'),
}
def road_map(at):
    s = [f'<svg class="fig map" viewBox="0 0 1152 400" data-id="roads">']
    s.append(T(0, 130, 'PREDICTING SEIZURES', 16, INK2, 'start', 'letter-spacing="2.5"'))
    s.append(T(0, 252, 'A LINEAR LENS ON NONLINEAR MOTION', 16, INK2, 'start', 'letter-spacing="2.5"'))
    def ln(a, b, dash=False):
        (x0, y0), (x1, y1) = STOPS[a][:2], STOPS[b][:2]
        d = ' stroke-dasharray="6 6"' if dash else ''
        if y0 == y1:
            return f'<line x1="{x0+10}" y1="{y0}" x2="{x1-10}" y2="{y1}" stroke="{AXIS}" stroke-width="2"{d}/>'
        return f'<path d="M{x0+10},{y0} C{x0+150},{y0} {x1-150},{y1} {x1-12},{y1}" fill="none" stroke="{AXIS}" stroke-width="2"{d}/>'
    s += [ln('sz1', 'sz2'), ln('sz2', 'sz3'), ln('sz3', 'ks'), ln('kp1', 'kp2'), ln('kp2', 'kp3'), ln('kp3', 'ks')]
    for k, (x, y, t, sub) in STOPS.items():
        on = k == at
        r = 11 if k == 'ks' else 8
        fill = ACC if on else (INK if k == 'ks' else LINE)
        s.append(f'<circle cx="{x}" cy="{y}" r="{r + (2 if on else 0)}" fill="{fill}" data-id="stop-{k}"/>')
        if k == 'ks': tx, ty, anchor = x + 24, y + 8, 'start'
        elif y < 185: tx, ty, anchor = x, y - 44, 'middle'
        else: tx, ty, anchor = x, y + 40, 'middle'
        s.append(T(tx, ty, t, 26 if (on or k == 'ks') else 22, INK if on or k == 'ks' else INK2, anchor, 'font-weight="600"' if on else ''))
        s.append(T(tx, ty + 24, sub, 17, INK2, anchor))
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- results (paper Table I, F1, mean over 5 folds)
F1 = [  # name, CHB-MIT, SIENA
    ('SVM', .53, .54), ('DNN', .57, .57), ('LSTM', .58, .61), ('EEGNet', .59, .65), ('EEG Conformer', .60, .66),
    ('CNN-LSTM', .61, .69), ('ST-GCN', .61, .63), ('ResNet', .65, .72), ('DeepConvNet', .66, .62),
    ('ShallowConvNet 2017', .73, .76), ('ShallowConvNet 2022', .74, .73), ('KSNet', .81, .82)]
def f1bars():
    W, top, rowh = 1152, 40, 29
    x0, bw = 250, 380
    acc = []
    s = [f'<svg class="fig" viewBox="0 0 {W} {top + rowh*len(F1) + 30}">']
    for j, (ds, xs) in enumerate([('CHB-MIT, 23 patients', x0), ('SIENA, 13 patients', x0 + bw + 70)]):
        s.append(T(xs, 22, ds, 20, INK2))
        lo = 0.4
        for i, row in enumerate(F1):
            v = row[1 + j]; y = top + i * rowh
            ours = row[0] == 'KSNet'
            L = (v - lo) / (0.9 - lo) * bw
            r = f'<rect x="{xs}" y="{y + 4}" width="{L:.1f}" height="{rowh - 9}" rx="2" fill="{ACC if ours else AXIS}"/>'
            (acc if ours else s).append(r)
            s.append(T(xs + L + 8, y + rowh - 8, f'{v:.2f}', 18, INK if ours else INK2, 'start', 'font-weight="600"' if ours else ''))
        s.append(f'<line x1="{xs}" y1="{top}" x2="{xs}" y2="{top + rowh*len(F1)}" stroke="{AXIS}"/>')
        s.append(T(xs, top + rowh*len(F1) + 24, 'F1, axis starts at 0.40', 16, INK2))
    for i, row in enumerate(F1):
        ours = row[0] == 'KSNet'
        if i == 0: s.append('<g data-accent="1">' + ''.join(acc) + '</g>')
        s.append(T(x0 - 14, top + i*rowh + rowh - 8, row[0], 19 if not ours else 21, INK if ours else INK2, 'end', 'font-weight="600"' if ours else ''))
    s.append('</svg>')
    return ''.join(s)

def ablation():
    # paper Fig. mode selection: F1 0.69 -> 0.81 (CHB-MIT), 0.72 -> 0.82 (SIENA); best baseline 0.74, 0.76
    W, H = 1152, 400
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}">']
    acc = []
    groups = [('CHB-MIT', .74, .69, .81, 60), ('SIENA', .76, .72, .82, 620)]
    lo, hi, base, ph = 0.6, 0.85, 300, 260
    def y(v): return base - (v - lo) / (hi - lo) * ph
    for name, bb, wo, wi, gx in groups:
        s.append(T(gx, 30, name, 22, INK2))
        bars = [('best baseline', bb, AXIS, ''), ('Koopman space, no selection', wo, LINE, 'class="fragment" data-fragment-index="2"'),
                ('with mode selection', wi, ACC, 'class="fragment" data-fragment-index="3"')]
        for k, (lab, v, col, frag) in enumerate(bars):
            x = gx + k * 160
            g = f'<g {frag}>'
            (acc if col == ACC else s).append(g + f'<rect x="{x}" y="{y(v):.1f}" width="110" height="{base - y(v):.1f}" rx="2" fill="{col}"/>'
                     + T(x + 55, y(v) - 10, f'{v:.2f}', 24, INK, 'middle') + '</g>')
            lines = {'best baseline': ['best', 'baseline'], 'Koopman space, no selection': ['Koopman space,', 'no selection'], 'with mode selection': ['with mode', 'selection']}[lab]
            s.append(f'<g {frag}>' + T(x + 55, base + 26, lines[0], 17, INK2, 'middle') + T(x + 55, base + 46, lines[1], 17, INK2, 'middle') + '</g>')
        s.append(f'<line x1="{gx - 10}" y1="{base}" x2="{gx + 440}" y2="{base}" stroke="{AXIS}"/>')
    # expected outcome sketch (fragment 1, removed at 2)
    s.append(f'<g class="fragment fade-out" data-fragment-index="2">' +
             ''.join(f'<rect x="{gx + 160}" y="{y(v):.1f}" width="110" height="{base - y(v):.1f}" rx="2" fill="none" stroke="{LINE}" stroke-dasharray="5 5"/>'
                     + T(gx + 215, y(v) - 10, 'your guess?', 18, INK2, 'middle') for _, _, _, v, gx in [(0, 0, 0, .78, 60), (0, 0, 0, .79, 620)]) + '</g>')
    s.append('<g data-accent="1">' + ''.join(acc) + '</g>')
    s.append(T(0, H - 2, 'F1, mean over 5 folds. Axis starts at 0.60.', 16, INK2))
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- running example pipeline
def pipe():
    W, H = 1152, 430
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}">']
    # clip
    s.append(T(0, 20, '10 s of patient chb01, 10 min before a seizure', 18, INK2))
    s.append(traces('preictal', 0, 34, 330, 170, PRE, every=2, sw=0.8))
    wx = 330 * 0.42
    s.append(f'<rect x="{wx:.0f}" y="30" width="8" height="178" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    s.append(T(wx + 4, 232, 'one snapshot, 1/8 s', 17, INK2, 'middle'))
    # encoder to latent
    s.append('<g class="fragment" data-fragment-index="1">')
    s.append(arrow(350, 120, 440, 120, LINE))
    s.append(T(395, 106, 'encode', 18, INK2, 'middle'))
    def latent(x, y, lab, col=GROUP, txt=INK):
        cells = ''.join(f'<rect x="{x + (i % 4) * 17}" y="{y + (i // 4) * 17}" width="14" height="14" rx="2" fill="{col}"/>' for i in range(16))
        return cells + T(x + 33, y + 92, lab, 20, txt, 'middle')
    s.append(latent(450, 86, 'now', PURT))
    s.append('</g><g class="fragment" data-fragment-index="2">')
    for k in range(3):
        x = 450 + (k + 1) * 170
        s.append(arrow(x - 96, 120, x - 14, 120, INK, 1.8))
        s.append(T(x - 55, 106, 'K', 22, INK, 'middle', 'font-style="italic"'))
        s.append(latent(x, 86, f'+{k + 1} step', GROUP, INK2))
    s.append(T(450, 30, 'one matrix K moves the state forward, three steps ahead', 20, INK))
    s.append('</g><g class="fragment" data-fragment-index="3">')
    for k in range(3):
        x = 450 + (k + 1) * 170 + 33
        s.append(arrow(x, 196, x, 262, LINE))
        s.append(f'<rect x="{x - 40}" y="270" width="80" height="54" rx="3" fill="{GROUP}"/>')
        s.append(T(x, 302, 'decoded', 16, INK2, 'middle'))
        s.append(f'<rect x="{x - 40}" y="340" width="80" height="54" rx="3" fill="none" stroke="{AXIS}"/>')
        s.append(T(x, 372, 'recorded', 16, INK2, 'middle'))
    s.append(T(560, 300, 'decode each step,', 21, INK, 'end'))
    s.append(T(560, 328, 'compare with what the', 21, INK, 'end'))
    s.append(T(560, 356, 'EEG actually did next', 21, INK, 'end'))
    s.append('</g></svg>')
    return ''.join(s)

# ---------------------------------------------------------------- learned spectrum of chb01 (fold 0), digitized from the paper figure
EIG = [(-0.158, 0.804), (0.497, 0.716), (0.831, 0.526), (-0.456, 0.242), (0.877, 0.226), (0.13, 0.16), (0.206, 0.0),
       (0.77, 0.0), (0.86, 0.0), (0.95, 0.0)]
def circle(band=(20, 45)):
    W, H, cx, cy, R = 600, 500, 270, 240, 190
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:600px">']
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{AXIS}" stroke-width="1.5"/>')
    s.append(f'<line x1="{cx - R - 20}" y1="{cy}" x2="{cx + R + 30}" y2="{cy}" stroke="{RULE}"/>')
    s.append(f'<line x1="{cx}" y1="{cy - R - 20}" x2="{cx}" y2="{cy + R + 20}" stroke="{RULE}"/>')
    fs = 256.0
    def ang(f): return f * 2 * math.pi / fs
    # band wedge (fragment)
    a0, a1 = ang(band[0]), ang(band[1])
    def wedge(sign):
        p0 = (cx + R * 1.08 * math.cos(a0), cy - sign * R * 1.08 * math.sin(a0)); p1 = (cx + R * 1.08 * math.cos(a1), cy - sign * R * 1.08 * math.sin(a1))
        sweep = 0 if sign > 0 else 1
        return f'<path d="M{cx},{cy} L{p0[0]:.1f},{p0[1]:.1f} A{R*1.08},{R*1.08} 0 0 {sweep} {p1[0]:.1f},{p1[1]:.1f} z" fill="{ACCT}" opacity="0.8"/>'
    s.append(f'<g class="fragment" data-fragment-index="2">{wedge(1)}{wedge(-1)}</g>')
    for f in (16, 32, 64, 96):
        a = ang(f)
        s.append(T(cx + (R + 34) * math.cos(a), cy - (R + 26) * math.sin(a) + 6, f'{f} Hz', 16, INK2, 'middle'))
        s.append(f'<line x1="{cx + R*0.97*math.cos(a):.1f}" y1="{cy - R*0.97*math.sin(a):.1f}" x2="{cx + R*1.03*math.cos(a):.1f}" y2="{cy - R*1.03*math.sin(a):.1f}" stroke="{AXIS}"/>')
    for re_, im_ in EIG:
        for sg in ([1, -1] if im_ else [1]):
            x, y = cx + re_ * R, cy - sg * im_ * R
            f = abs(math.atan2(im_, re_)) * fs / (2 * math.pi)
            inb = band[0] <= f <= band[1] and im_
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{PRE if not inb else PRE}" class="eig{" inb" if inb else ""}"/>')
    s.append(T(0, H - 4, 'Learned K of patient chb01, fold 0, read off the paper figure', 16, INK2))
    s.append('</svg>')
    return ''.join(s)

def lopo():
    W, H = 700, 400
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:640px">']
    lo, hi, base, ph = 0.3, 1.0, 300, 270
    def y(v): return base - (v - lo) / (hi - lo) * ph
    acc = []
    for gi, (name, seg, lp) in enumerate([('CHB-MIT', .87, .48), ('SIENA', .90, .57)]):
        gx = 30 + gi * 320
        s.append(T(gx + 120, base + 76, name, 24, INK, 'middle'))
        for k, (lab, v, col) in enumerate([('seen', seg, AXIS), ('new', lp, ACC)]):
            x = gx + k * 130
            r = f'<rect x="{x}" y="{y(v):.1f}" width="110" height="{base - y(v):.1f}" rx="2" fill="{col}"/>'
            (acc if col == ACC else s).append(r)
            s.append(T(x + 55, y(v) - 10, f'{v:.2f}', 26, INK, 'middle'))
            s.append(T(x + 55, base + 30, lab + (' patients' if k == 0 else ' patient'), 18, INK2, 'middle'))
        s.append(f'<line x1="{gx - 10}" y1="{base}" x2="{gx + 250}" y2="{base}" stroke="{AXIS}"/>')
    s.append('<g data-accent="1">' + ''.join(acc) + '</g>')
    s.append(f'<line x1="10" y1="{y(.5):.1f}" x2="696" y2="{y(.5):.1f}" stroke="{LINE}" stroke-dasharray="7 6" stroke-width="2"/>')
    s.append(T(698, y(.5) - 8, 'chance', 20, INK2, 'end'))
    s.append('</svg>')
    return ''.join(s)

def timeline(w=1100):
    s = [f'<svg class="fig" viewBox="0 0 {w} 90" style="width:{w}px">']
    # inter-ictal far away, gap, pre-ictal 30 min, onset
    s.append(f'<line x1="0" y1="40" x2="{w-20}" y2="40" stroke="{AXIS}" stroke-width="1.5"/>')
    s.append(f'<rect x="20" y="28" width="330" height="24" rx="2" fill="{TEALT}"/>' + T(185, 76, 'inter-ictal: at least 30 min from any seizure', 17, INK2, 'middle'))
    s.append(f'<rect x="700" y="28" width="330" height="24" rx="2" fill="{PURT}"/>' + T(865, 76, 'pre-ictal: the 30 min before onset', 17, INK2, 'middle'))
    s.append(f'<line x1="1032" y1="14" x2="1032" y2="62" stroke="{FAIL}" stroke-width="2" stroke-dasharray="5 4"/>' + T(1032, 10, 'onset', 16, INK2, 'end'))
    s.append(T(525, 22, 'task: tell the two apart from one 10 s clip', 18, INK, 'middle'))
    s.append('</svg>')
    return ''.join(s)


def kooptoy():
    W, H = 760, 440
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(T(0, 22, 'what we record', 19, INK2))
    m = [(0.93, 0.42, 1.0), (0.975, 0.11, 0.8)]
    pts = []
    for n in range(90):
        v = sum(a * r**n * math.cos(th * n) for r, th, a in m)
        pts.append(f'{n * 300 / 89:.1f},{140 - v * 60:.1f}')
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    s.append(T(0, 260, 'a tangle of rhythms', 19, INK2))
    s.append(arrow(320, 140, 400, 140, LINE))
    s.append(T(360, 124, 'lift', 19, INK2, 'middle'))
    s.append(T(430, 22, 'in the right coordinates', 19, INK2))
    for k, (r, th, a) in enumerate(m):
        cx, cy, R = 520 + k * 150, 140, 62
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RULE}"/>')
        dots = [(cx + R * r**n * math.cos(th * n * (1.6 if k == 0 else 3.5)), cy - R * r**n * math.sin(th * n * (1.6 if k == 0 else 3.5))) for n in range(0, 22)]
        s.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in dots)}" fill="none" stroke="{AXIS}" stroke-width="1"/>')
        for i, (x, y) in enumerate(dots[:12]):
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if i == 0 else 3.5}" fill="{PRE if k == 0 else TEAL}"/>')
        s.append(T(cx, cy + R + 30, f'rhythm {k + 1}', 18, INK2, 'middle'))
    s.append(T(430, 290, 'each rhythm turns a fixed angle per step', 20, INK))
    s.append(T(430, 316, 'and shrinks by a fixed factor per step', 20, INK))
    s.append(T(430, 360, 'angle = frequency', 20, INK2))
    s.append(T(430, 386, 'shrink = how fast it fades', 20, INK2))
    s.append(T(430, 412, 'together: one eigenvalue of one matrix K', 20, INK2))
    s.append('</svg>')
    return ''.join(s)

TAB = [('SVM','0.56 0.52 0.53 0.50','0.69 0.49 0.54 0.63'),('DNN','0.39 0.64 0.57 0.53','0.51 0.62 0.57 0.61'),
 ('LSTM','0.43 0.64 0.58 0.54','0.55 0.65 0.61 0.67'),('CNN-LSTM','0.52 0.65 0.61 0.61','0.60 0.75 0.69 0.77'),
 ('EEGNet','0.67 0.56 0.59 0.63','0.77 0.60 0.65 0.73'),('DeepConvNet','0.48 0.75 0.66 0.68','0.71 0.59 0.62 0.71'),
 ('ResNet','0.45 0.74 0.65 0.64','0.62 0.80 0.72 0.80'),('ShallowConvNet 2017','0.65 0.78 0.73 0.80','0.70 0.81 0.76 0.85'),
 ('ShallowConvNet 2022','0.65 0.78 0.74 0.80','0.71 0.76 0.73 0.82'),('ST-GCN','0.63 0.60 0.61 0.66','0.44 0.76 0.63 0.68'),
 ('EEG Conformer','0.58 0.60 0.60 0.65','0.61 0.70 0.66 0.73'),('KSNet*','0.73 0.83 0.79 0.86','0.76 0.84 0.80 0.90'),
 ('KSNet','0.74 0.85 0.81 0.87','0.78 0.86 0.82 0.90')]
def table():
    th = '<th></th>' + ''.join(f'<th>{m}</th>' for m in ['Spec', 'Recall', 'F1', 'AUC'] * 2)
    rows = ''.join('<tr' + (' class="ours"' if r[0] == 'KSNet' else '') + f'><td>{r[0]}</td>' + ''.join(f'<td>{v}</td>' for v in (r[1] + ' ' + r[2]).split()) + '</tr>' for r in TAB)
    return ('<table class="tab"><tr><th></th><th colspan="4">CHB-MIT</th><th colspan="4">SIENA</th></tr>'
            f'<tr>{th}</tr>{rows}</table>')


def territory():
    W, H = 1152, 470
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}">']
    s.append(T(0, 24, 'TODAY', 16, INK2, 'start', 'letter-spacing="2.5"'))
    c = CLIPS['seizure']['uV'][0]; pts = []
    for i in range(0, len(c), 4):
        pts.append(f'{i * 250 / len(c):.1f},{120 - max(-60, min(60, c[i] * 0.2)):.1f}')
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{PRE}" stroke-width="1"/>')
    s.append(T(0, 230, 'scalp EEG', 24, INK)); s.append(T(0, 260, 'before a seizure', 24, INK))
    s.append(f'<line x1="300" y1="10" x2="300" y2="{H - 10}" stroke="{RULE}"/>')
    s.append(T(340, 24, 'NOT YET: OTHER SIGNALS THAT DRIFT BEFORE THEY TIP', 16, INK2, 'start', 'letter-spacing="2.5"'))
    x0 = 340; pts = []
    for i in range(240):
        t = i / 240 * 5; ph = t % 1
        v = 55 if 0.30 < ph < 0.33 else (-15 if 0.33 <= ph < 0.36 else 7 * math.sin(ph * 6.28))
        pts.append(f'{x0 + i:.1f},{130 - v:.1f}')
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK2}" stroke-width="1.4"/>')
    s.append(T(x0, 230, 'heart rhythm before', 24, INK)); s.append(T(x0, 260, 'an arrhythmia', 24, INK))
    x1 = 640
    import random
    rnd = random.Random(3); v = 0
    for i in range(30):
        v = v * (0.3 + 0.65 * i / 30) + rnd.gauss(0, 1)
        s.append(f'<circle cx="{x1 + i * 8:.1f}" cy="{120 - v * 14:.1f}" r="4" fill="{INK2}"/>')
    s.append(T(x1, 230, 'daily mood before', 24, INK)); s.append(T(x1, 260, 'a depressive episode', 24, INK))
    x2 = 925
    for k, (b, a) in enumerate([(70, 9), (120, 7), (165, 5)]):
        pts = [f'{x2 + i * 2:.1f},{b - a * math.sin(i / 7 + k) * (1 + i / 60):.1f}' for i in range(112)]
        s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK2}" stroke-width="1.4"/>')
    s.append(T(x2, 230, 'ICU vital signs before', 24, INK)); s.append(T(x2, 260, 'a patient deteriorates', 24, INK))
    s.append(T(340, 360, 'Each drifts slowly, then switches suddenly.', 30, INK))
    s.append(T(340, 400, 'A learned spectrum could watch the drift.', 30, INK))
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- demo
def demo():
    return '''<div class="demo" style="display:flex;gap:36px;align-items:flex-start">
<svg id="dm-circle" viewBox="0 0 400 400" style="width:400px;height:400px"></svg>
<div style="flex:1">
<svg id="dm-sig" viewBox="0 0 640 300" style="width:640px;height:300px"></svg>
<div style="display:flex;align-items:center;gap:18px;margin-top:6px">
<span class="dm-l">far from the edge</span><input id="dm-r" type="range" min="0" max="100" value="0" style="width:300px"><span class="dm-l">near a tipping point</span>
</div>
<p class="key" id="dm-read" style="margin-top:18px">The orange rhythm needs about 0.4 s to settle</p>
</div></div>'''

DEMO_JS = r'''
(function(){
const C=document.getElementById('dm-circle'),S=document.getElementById('dm-sig'),R=document.getElementById('dm-r'),out=document.getElementById('dm-read');
if(!C)return;
const ns='http://www.w3.org/2000/svg';
function el(p,t,a){const e=document.createElementNS(ns,t);for(const k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
const cx=200,cy=200,rad=160;
el(C,'circle',{cx,cy,r:rad,fill:'none',stroke:'#ACA39A','stroke-width':1.5});
el(C,'line',{x1:20,y1:cy,x2:380,y2:cy,stroke:'#D7D2CB'});el(C,'line',{x1:cx,y1:20,x2:cx,y2:380,stroke:'#D7D2CB'});
const t1=el(C,'text',{x:200,y:398,'font-size':17,fill:'#5F5D50','text-anchor':'middle'});t1.textContent='each dot: a rhythm and how fast it fades';
const modes=[{r:0.80,th:0.55,a:0.9,c:'#7C878E'},{r:0.70,th:1.6,a:0.6,c:'#7C878E'},{r:0.95,th:0.22,a:1.0,c:'#F76902'}];
const ga=el(C,'g',{'data-accent':'1'});const dots=[];modes.forEach(m=>{const p=m.c==='#F76902'?ga:C;dots.push([el(p,'circle',{r:8,fill:m.c}),el(p,'circle',{r:8,fill:m.c})]);});
el(S,'line',{x1:0,y1:150,x2:640,y2:150,stroke:'#D7D2CB'});
const path=el(S,'path',{fill:'none',stroke:'#1F1E1B','stroke-width':1.6});
const k1=el(S,'text',{x:0,y:290,'font-size':17,fill:'#5F5D50'});k1.textContent='response to one kick, 2 s';
function draw(){const u=R.value/100;modes[2].r=0.95+u*(0.995-0.95);
 modes.forEach((m,i)=>{const x=cx+m.r*rad*Math.cos(m.th),y=cy-m.r*rad*Math.sin(m.th);dots[i][0].setAttribute('cx',x);dots[i][0].setAttribute('cy',y);dots[i][1].setAttribute('cx',x);dots[i][1].setAttribute('cy',2*cy-y);});
 let d='';const N=320;for(let n=0;n<N;n++){let v=0;modes.forEach(m=>{v+=m.a*Math.pow(m.r,n)*Math.cos(m.th*n);});d+=(n?'L':'M')+(n*640/N).toFixed(1)+','+(150-v*48).toFixed(1);}
 path.setAttribute('d',d);
 const steps=Math.log(0.05)/Math.log(modes[2].r);const secs=steps*2/N;out.textContent='The orange rhythm needs about '+secs.toFixed(1)+' s to settle';}
R.addEventListener('input',draw);draw();
})();
'''

def people(spec):
    f, name, aff = spec.split('|')
    return (f'<figure><img src="../figs/people/{f}" alt="{name}"><figcaption>{name}<span>{aff}</span></figcaption></figure>')

def build():
    src = open(os.path.join(HERE, 'slides.html')).read()
    src = src.replace('{{COVER}}', cover()).replace('{{F1BARS}}', f1bars()).replace('{{ABL}}', ablation())
    src = src.replace('{{PIPE}}', pipe()).replace('{{CIRCLE}}', circle()).replace('{{DEMO}}', demo()).replace('{{DEMO_JS}}', DEMO_JS).replace('{{LOPO}}', lopo()).replace('{{TIMELINE}}', timeline()).replace('{{KOOPTOY}}', kooptoy()).replace('{{TERRITORY}}', territory()).replace('{{TABLE}}', table())
    src = re.sub(r'\{\{EEG:([^}]+)\}\}', lambda m: eeg(m.group(1)), src)
    src = re.sub(r'\{\{MAP:([^}]+)\}\}', lambda m: road_map(m.group(1)), src)
    src = re.sub(r'\{\{PEOPLE:([^}]+)\}\}', lambda m: people(m.group(1)), src)
    # style gate: no em dash, en dash or semicolon in visible text (scripts, styles and entities excluded)
    vis = re.sub(r'<script.*?</script>|<style.*?</style>|&[#a-zA-Z0-9]+;', '', src, flags=re.S)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    bad = sorted(set(re.findall(r'.{0,25}[–—;].{0,25}', vis)))
    # time ledger
    total = 0; n_main = 0
    for m in re.finditer(r'<section([^>]*)>', src):
        a = m.group(1)
        if 'data-backup' in a: continue
        sec = re.search(r'data-sec="(\d+)"', a)
        if sec: total += int(sec.group(1)); n_main += 1
    missing = [p for p in re.findall(r'src="(\.\./[^"]+)"', src) if not os.path.exists(os.path.normpath(os.path.join(ROOT, p)))]
    open(os.path.join(ROOT, 'index.html'), 'w').write(src)
    print(f'slides: {src.count("<section")}  main: {n_main}  time: {total // 60} min {total % 60} s')
    print('style violations:', bad or 'none')
    print('missing images:', missing or 'none')
    if total > 20 * 60: print('OVER BUDGET')

if __name__ == '__main__':
    build()
