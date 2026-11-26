"""KSNet talk, IEEE BIBM 2026, Session S3, Wed Dec 2 10:40. Builds ../index.html.

usage: ~/venvs/slides/bin/python -I src/build.py   (from the deck folder)
v2 (2026-11-26): real EEG, found photos, covers and paper pages, verified quotes (src/quotes.json),
live canvas demos (demos.js). Slides are inline SVG on a 1180 by 470 drawing, house style v2.
Numbers: paper Table I and II, and our follow up runs in aquastar/zhiqian-knowledge-base
(papers/ksnet-talk-findings.md points to every run folder). Image credits: figs/ASSETS.md.
"""
import os, re, html, json, math, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.dirname(HERE)
URL = 'https://aquastar.github.io/talks/koopman-seizure/2026-12-02-bibm-dallas/'

BG = '#FBFAF7'; INK = '#1F1E1B'; INK2 = '#5F5D50'; LINE = '#7C878E'; AXIS = '#ACA39A'; RULE = '#D7D2CB'; GROUP = '#F1EDE7'
ACC = '#F76902'; ACC_T = '#C45200'; TINT = '#FAD6BA'; SLATE = '#4C5B66'; FAIL = '#DA291C'; KEYBG = '#FDEFE3'; REF = '#A39E93'
FONT = 'et-book,Georgia,serif'
Q = json.load(open(os.path.join(HERE, 'quotes.json')))
MISSING = []

# ---------------- svg helpers ----------------
def esc(s):
    return html.escape(str(s), quote=False)

def T(x, y, s, size=18, w=400, fill=INK, a='start', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{a}" {extra}>{s}</text>'

def TI(x, y, s, size=18, fill=INK, a='start'):
    return T(x, y, s, size, 400, fill, a, 'font-style="italic"')

def R(x, y, w, h, fill=GROUP, rx=3, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'

def L(x1, y1, x2, y2, col=AXIS, sw=1, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}" {extra}/>'

def C(x, y, r, fill=INK2, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'

def P(d, col=INK2, sw=1.5, fill='none', extra=''):
    return f'<path d="{d}" stroke="{col}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'

def F(i, inner):
    return f'<g class="fragment" data-fragment-index="{i}">{inner}</g>'

def arrow(x1, y1, x2, y2, col=INK2, sw=1.5, mk='ah'):
    return L(x1, y1, x2, y2, col, sw, f'marker-end="url(#{mk})"')

DEFS = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker>'
        f'<marker id="aho" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker></defs>')

def SVG(inner, h=470):
    return f'<svg class="fig" viewBox="0 0 1180 {h}" width="1180" height="{h}" font-family="{FONT}">{DEFS}{inner}</svg>'

def kw(s):
    return f'<tspan font-weight="600" fill="{ACC_T}" font-style="normal">{s}</tspan>'

def keybox(x, y, w, text, size=21):
    return R(x, y, w, 48, KEYBG, 3) + R(x, y, 7, 48, ACC, 0) + T(x + 24, y + 31, text, size, 400, INK)

def bignum(x, y, num, line1, line2='', size=44, col=INK):
    out = T(x, y, num, size, 400, col) + L(x, y + 10, x + size * len(num) * 0.42, y + 10, ACC, 3)
    out += T(x, y + 36, line1, 16, 400, INK2)
    if line2:
        out += T(x, y + 56, line2, 16, 400, INK2)
    return out

_clip = [0]
def IMG(x, y, w, h, src, rx=3, frame=True, align='xMidYMid', fit='slice'):
    if not os.path.exists(os.path.join(DECK, src)):
        MISSING.append(src)
        return R(x, y, w, h, GROUP, rx) + T(x + w / 2, y + h / 2 + 4, os.path.basename(src), 11, 400, INK2, 'middle')
    _clip[0] += 1
    cid = f'clp{_clip[0]}'
    out = (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
           f'<image href="{src}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{align} {fit}" clip-path="url(#{cid})"/>')
    if frame:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{RULE}" stroke-width="1"/>'
    return out

def has(src):
    return os.path.exists(os.path.join(DECK, src))

def person(x, y, d, src, name, line2='', a='start'):
    """photo with a two line caption to its right"""
    return IMG(x, y, d, d, src, 4) + T(x + d + 12, y + d / 2 - 2, name, 16, 600, INK) + (T(x + d + 12, y + d / 2 + 18, line2, 14, 400, INK2) if line2 else '')

def quote(x, y, lines, who, size=21, lh=None, col=INK):
    """lines: list of strings, may contain kw() spans. Opening mark hangs in the margin."""
    lh = lh or size * 1.32
    out = T(x - 6, y + size * 0.55, '“', size * 2.2, 400, ACC, 'end', 'opacity="0.55"')
    for k, s in enumerate(lines):
        out += T(x, y + k * lh, s, size, 400, col, 'start', 'font-style="italic"')
    out += T(x, y + len(lines) * lh + 4, who, 14.5, 400, INK2)
    return out

def hbar(x, y, label, v, vmin, vmax, w, col, bold=False, note='', lw=330, h=26, val=None, size=17):
    bw = ((val if val is not None else v) - vmin) / (vmax - vmin) * w
    out = T(x + lw - 14, y + h * 0.72, label, size, 600 if bold else 400, INK, 'end')
    out += R(x + lw, y, max(bw, 2), h, col, 2)
    out += T(x + lw + bw + 10, y + h * 0.72, f'{v:.2f}' if isinstance(v, float) else str(v), size, 600 if bold else 400, INK)
    if note:
        out += T(x + lw + bw + 62, y + h * 0.72, note, 14.5, 400, INK2)
    return out

def axis_ticks(x0, y0, w, vmin, vmax, ticks, h=0, label=''):
    out = L(x0, y0, x0 + w, y0, AXIS, 1)
    for t in ticks:
        tx = x0 + (t - vmin) / (vmax - vmin) * w
        out += L(tx, y0, tx, y0 + 5, AXIS, 1) + T(tx, y0 + 22, f'{t:g}', 14.5, 400, INK2, 'middle')
        if h:
            out += L(tx, y0 - h, tx, y0, RULE, 1)
    if label:
        out += T(x0 + w, y0 + 44, label, 14.5, 400, INK2, 'end')
    return out

def demo(name, x, y, w, h):
    """live canvas, positioned in drawing coordinates (svg origin is at 50,168 on the slide)"""
    return f'<div class="demo" data-demo="{name}" style="left:{50 + x}px;top:{168 + y}px;width:{w}px;height:{h}px"></div>'

def steps(n):
    return ''.join(f'<span class="fragment stepper" data-fragment-index="{i}"></span>' for i in range(n))

# ---------------- section ----------------
SLIDES = []
STATUS = {'pub': 'Published, BIBM 2026', 'prog': 'In progress', 'pre': 'Exploratory, post hoc'}

def slide(title, svg, mark='', status='', ref='', notes='', cls='', html_=''):
    st = f'<span class="status">Our work · {STATUS[status]}</span>' if status else ''
    mk = f'<span class="mark">{mark}</span>' if mark else ''
    rf = f'<div class="ref">{ref}</div>' if ref else ''
    nt = f'<aside class="notes">{notes}</aside>' if notes else ''
    c = f' class="{cls}"' if cls else ''
    SLIDES.append(f'<section{c}>{mk}<h2>{title}</h2>{st}{svg}{html_}{rf}{nt}</section>')

def bslide(title, svg, ref='', notes='', status=''):
    st = f'<span class="status">Our work · {STATUS[status]}</span>' if status else ''
    rf = f'<div class="ref">{ref}</div>' if ref else ''
    nt = f'<aside class="notes">{notes}</aside>' if notes else ''
    return f'<section><span class="mark">Backup</span><h2>{title}</h2>{st}{svg}{rf}{nt}</section>'

# =====================================================================
# 1. cover
cover_fig = ''
cx, cy, r = 930, 300, 190
cover_fig += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RULE}" stroke-width="1.5"/>'
cover_fig += L(cx - r - 30, cy, cx + r + 30, cy, RULE, 1) + L(cx, cy - r - 30, cx, cy + r + 30, RULE, 1)
pts = [(0.97, 0.10), (0.93, 0.32), (0.84, 0.55), (0.62, 0.95), (0.70, 1.55), (0.45, 2.3), (0.88, 0.0)]
for k, (m, a) in enumerate(pts):
    for sgn in (1, -1):
        x = cx + r * m * math.cos(a); y = cy - sgn * r * m * math.sin(a)
        cover_fig += C(round(x, 1), round(y, 1), 7 if k == 0 else 5.5, ACC if k == 0 else INK2, f'class="eig" style="animation-delay:{k * 0.35:.2f}s"')
cover_fig += T(cx + r + 10, cy + 26, 'Re', 14, 400, INK2) + T(cx + 10, cy - r - 12, 'Im', 14, 400, INK2)
SLIDES.append(f'''<section class="cover">
  <div class="cv-left">
    <div class="cv-kicker">IEEE BIBM 2026 · Session S3, Biomedical Signal Analysis</div>
    <h1><span class="cv-small">KSNet: Learning Interpretable</span><span class="cv-big">Koopman</span><span class="cv-small">Spectral Representations for EEG Seizure Prediction</span></h1>
    <div class="cv-rule"></div>
    <div class="cv-author"><b>Siji Chen, Yanshen Sun, Zhiqian Chen, Chang-Tien Lu</b><br>Virginia Tech · Rochester Institute of Technology<br>Presented by Zhiqian Chen</div>
  </div>
  <svg class="cv-fig" viewBox="700 60 480 480" width="480" height="480" font-family="{FONT}">{cover_fig}</svg>
  <aside class="notes">Good morning. These dots are eigenvalues of a linear operator learned from EEG. The talk is about what such a spectrum can and cannot tell us before a seizure. Casey just showed prediction from wearables. I stay with EEG and ask a harder question: how do we know a predictor works?</aside>
</section>''')

# 2. the problem, on real data
E = json.load(open(os.path.join(HERE, 'chb01_03_onset.json')))
FILES = json.load(open(os.path.join(HERE, 'chb01_files.json')))
g = ''
tx0, tx1, y0, rowh = 70, 720, 22, 28
chs = E['chs']; n = len(E['uV'][chs[0]])
g += T(tx0, 6, 'Real scalp EEG, chb01 file 03, one minute around a seizure', 15, 400, INK2)
for i, c in enumerate(chs):
    yc = y0 + i * rowh + 14
    g += T(tx0 - 8, yc + 4, c.replace('-0', '').replace('-', ' to '), 11.5, 400, INK2, 'end')
    pts_ = ' '.join(f'{tx0 + j / (n - 1) * (tx1 - tx0):.1f},{yc - max(-240, min(240, v)) * 0.06:.1f}' for j, v in enumerate(E['uV'][c]))
    g += f'<polyline points="{pts_}" fill="none" stroke="{INK2}" stroke-width="0.6"/>'
xo = tx0 + 0.5 * (tx1 - tx0)
g += L(xo, y0 - 2, xo, y0 + 8 * rowh + 4, ACC, 2) + T(xo + 6, y0 + 8 * rowh + 22, 'onset, marked by clinicians', 14, 600, ACC_T)
g += T(tx0, y0 + 8 * rowh + 22, '−30 s', 14, 400, INK2) + T(tx1, y0 + 8 * rowh + 22, '+30 s', 14, 400, INK2, 'end')
# real recording timeline
H0 = FILES['t0']; span = FILES['span_h']
def hx(h): return tx0 + h / span * (tx1 - tx0)
ty = 330
g += T(tx0, ty - 26, f'The whole stay: {FILES["rec_h"]:.1f} h recorded over {span:.1f} h, 7 seizures at their real times', 15, 400, INK2)
for a, b in FILES['cov']:
    g += R(round(hx(a), 1), ty, round(max(hx(b) - hx(a) - 0.6, 0.6), 1), 16, '#E2DDD5', 0)
g += F(1, ''.join(R(round(hx(s - 0.5), 1), ty, round(hx(s) - hx(s - 0.5), 1), 16, ACC, 0) for s in FILES['sz']))
for s in FILES['sz']:
    g += L(round(hx(s), 1), ty - 8, round(hx(s), 1), ty + 24, INK, 1.6)
for hh in range(0, 46, 6):
    g += T(round(hx(hh), 1), ty + 40, f'{hh} h', 13.5, 400, INK2, 'middle')
g += F(1, T(tx0, ty + 62, 'orange: the 30 min before each seizure, the only windows a predictor should flag', 15, 600, ACC_T))
# right column: why it matters
rx = 790
g += bignum(rx, 40, Q['who']['num'], Q['who']['l1'], Q['who']['l2'])
g += IMG(rx, 136, 64, 64, Q['burden']['img'], 4) + quote(rx + 16, 236, Q['burden']['lines'], Q['burden']['who'], 18)
g += F(2, keybox(0, 410, 1120, f'Can a model tell the {kw("30 minutes before")} a seizure from the rest of the day?'))
slide('A seizure is obvious once it starts. The hard part is the half hour before.', SVG(g), mark='Problem',
      ref=Q['who']['ref'] + ' | ' + Q['burden']['ref'] + ' | Shoeb, PhD thesis, MIT 2009 | Goldberger et al., PhysioNet, Circulation 2000',
      notes='This is real EEG from CHB-MIT, a child, patient chb01. The orange line is where clinicians marked the onset. After it, nobody needs a model. Below is the whole stay, every file, gaps included, and the seven seizures at their real times. Click: the orange slivers are the half hours before each seizure. That is the target, a few thin windows in two days. Why bother: for patients the worst part is often not the seizure but not knowing when. Click: so the question is whether a model can recognize those windows from the rest of the day.')

# 3. the field: claims and tests
g = ''
cards = [('2003', 'figs/people/klaus-lehnertz.jpg', None, 'Andrzejak, ..., Lehnertz', 'Phys. Rev. E', ['Beat fake seizure', 'times before you', 'claim a warning']),
         ('2007', 'figs/people/florian-mormann.jpg', None, 'Mormann et al.', 'Brain', ['Review: early', 'claims did not', 'replicate']),
         ('2013', None, '11 of 15', 'Cook et al.', 'Lancet Neurol.', ['patients met the', 'criteria of an', 'implanted advisor']),
         ('2016', None, '478', 'Kaggle contest', 'Kuhlmann et al., Brain 2018', ['teams, 10,000', 'algorithms, best', 'AUC 0.81'])]
for k, (yr, img, big, who, where, ls) in enumerate(cards):
    x = k * 285
    inner = T(x, 26, yr, 30, 400, ACC_T) + T(x + 82, 12, who, 14.5, 600, INK) + T(x + 82, 31, where, 13.5, 400, INK2)
    if img:
        inner += IMG(x, 50, 120, 120, img, 4)
    else:
        inner += T(x, 118, big, 44 if len(big) < 5 else 30, 400, INK) + L(x, 130, x + 110, 130, ACC, 3)
    inner += ''.join(T(x + 136, 82 + j * 22, s_, 16, 400, INK) for j, s_ in enumerate(ls))
    g += inner if k < 2 else F(k - 1, inner)
g += L(0, 200, 1120, 200, RULE, 1)
g += F(3, quote(28, 270, Q['mormann']['lines'], Q['mormann']['who'], 21))
slide('Seizure prediction kept making claims until the field learned to test them against chance', SVG(g), mark='The field',
      ref='Andrzejak et al., Phys. Rev. E 2003 | Mormann et al., Brain 2007 | Cook et al., Lancet Neurol. 2013 | Kuhlmann et al., Brain 2018',
      notes='Photos: Klaus Lehnertz, senior author of both Bonn papers, and Florian Mormann. A short history, because it is the backbone of this talk. In 2003 Andrzejak and colleagues proposed a simple discipline: before you claim a pre-seizure state, show that your method does worse on fake seizure times. In 2007 Mormann reviewed the field: many early claims did not hold up. Click: in 2013 Cook and colleagues implanted a seizure advisory device in 15 people, and in 11 it met its performance criteria. Click: in 2016 a Kaggle contest drew 478 teams and over 10,000 algorithms, best AUC 0.81 on long intracranial recordings. Click: the lesson Mormann drew. Keep it in mind, it returns in ten minutes.')

# 4. Koopman 1931
g = ''
g += T(0, 40, '1931', 54, 400, ACC_T) + T(0, 72, 'B. O. Koopman, PNAS', 16, 600, INK) + T(0, 94, 'follow functions of the state,', 15, 400, INK2) + T(0, 113, 'not the state itself', 15, 400, INK2)
g += person(0, 140, 60, 'figs/people/igor-mezic.jpg', 'Igor Mezić', '2005: Koopman for data')
g += person(0, 214, 60, 'figs/people/peter-schmid.jpg', 'Peter Schmid', '2010: dynamic mode decomp.')
ix = 330
g += T(ix, 22, 'Nonlinear state', 17, 600, INK) + P(f'M{ix},120 C{ix + 40},40 {ix + 110},40 {ix + 130},100 S{ix + 190},170 {ix + 220},90', INK2, 2)
g += arrow(ix + 236, 100, ix + 296, 100) + T(ix + 266, 88, 'lift', 15, 400, INK2, 'middle')
g += T(ix + 312, 22, 'Linear in the lifted space', 17, 600, INK)
for j, s_ in enumerate(['z', 'Kz', 'K²z']):
    g += R(ix + 312 + j * 92, 76, 64, 48, GROUP) + T(ix + 344 + j * 92, 107, s_, 20, 400, INK, 'middle', 'font-style="italic"')
    if j < 2:
        g += arrow(ix + 378 + j * 92, 100, ix + 402 + j * 92, 100)
g += F(1, C(ix + 70, 250, 58, 'none', f'stroke="{AXIS}" stroke-width="1.5"') + L(ix, 250, ix + 140, 250, RULE) + L(ix + 70, 180, ix + 70, 320, RULE)
       + C(ix + 70 + 52 * math.cos(0.6), 250 - 52 * math.sin(0.6), 6, ACC) + C(ix + 70 + 52 * math.cos(0.6), 250 + 52 * math.sin(0.6), 6, ACC)
       + T(ix + 160, 220, 'Each eigenvalue λ of K is one mode', 17, 600, INK)
       + T(ix + 160, 246, 'angle: how fast it oscillates', 16, 400, INK2) + T(ix + 160, 270, 'radius: how fast it fades', 16, 400, INK2)
       + T(ix + 160, 294, 'on the circle: it neither grows nor fades', 16, 400, INK2))
bx = 930
g += F(2, IMG(bx, 0, 90, 132, Q['books']['dmd'], 2) + IMG(bx + 100, 0, 90, 132, Q['books']['ddse'], 2)
       + IMG(bx, 150, 60, 60, 'figs/people/steven-brunton.jpg', 4) + IMG(bx + 68, 150, 60, 60, 'figs/people/nathan-kutz.jpg', 4)
       + T(bx, 232, 'Brunton and Kutz:', 14.5, 600, INK) + T(bx, 250, 'DMD and deep Koopman', 14.5, 400, INK2) + T(bx, 268, 'made it practical', 14.5, 400, INK2))
g += F(3, quote(28, 372, Q['brunton']['lines'], Q['brunton']['who'], 20))
slide('In 1931 Koopman traded a nonlinear system for a linear one you can read', SVG(g), mark='Idea',
      ref='Koopman, PNAS 1931 | Mezić, Nonlinear Dyn. 2005 | Schmid, J. Fluid Mech. 2010 | ' + Q['brunton']['ref'] + ' | ' + Q['books']['ref'],
      notes='Bernard Koopman, 1931, a short paper in PNAS. The trick: do not follow the state, follow functions of the state. Then the dynamics become linear, one operator K moves everything forward. Click: and a linear operator has a spectrum. Each eigenvalue is a mode: its angle is a frequency, its radius says how fast it fades. For decades this stayed theory. Mezić brought it to data in 2005, Schmid introduced dynamic mode decomposition in 2010. Click: Brunton and Kutz wrote the books and the deep Koopman networks that made it practical. Click: in their words, read the quote. This is why we picked it for EEG.')

# 5. live demo on real EEG
g = F(0, T(0, 452, 'The spectrum sees the seizure. Before onset it looks like any other minute. That is the hard part.', 18, 600, ACC_T))
slide('Watch the operator’s eigenvalues on real EEG as a seizure begins', SVG(g), mark='Idea, live',
      html_=demo('dmd', 0, 0, 1130, 420) + '',
      ref='CHB-MIT chb01 file 03, channel T8 to P8, 4 s windows, delay embedded DMD of order 10 computed live in your browser',
      notes='This runs live in the browser. Top left is one channel of the recording you just saw, 50 seconds before onset and 40 after. The orange window slides along. For every window we fit a linear operator by dynamic mode decomposition, and the right side shows its eigenvalues on the unit circle. The large orange pair is the strongest rhythm. Watch what happens at onset: the rhythm locks in and the eigenvalues move toward the circle. Click: but before onset, nothing special. The spectrum sees the seizure. The real question is the half hour before. I can click the trace to jump.')

# 6. KSNet on the paper figure
sc = 760 / 2514
fx, fy = 0, 6
g = IMG(fx, fy, 760, round(1050 * sc), 'figs/paper/flow_chart.png', 0, frame=False, fit='meet')
def badge(x, y, k): return C(fx + x * sc, fy + y * sc, 15, ACC) + T(fx + x * sc, fy + y * sc + 6, str(k), 17, 700, '#fff', 'middle')
call = [(450, 470, 'Encoder φ lifts a 10 s, 23 channel segment'), (1080, 600, 'One full matrix K, rolled out H = 3 steps,'),
        (450, 905, 'Soft band over mode frequencies selects modes'), (1700, 1000, 'A ShallowConvNet style head classifies')]
sub = ['to a latent state', 'decoder ψ checks every step', 'edges are learned', 'pre-ictal or inter-ictal']
for k, (x, y, s) in enumerate(call):
    inner = badge(x, y, k + 1) + C(800, 40 + k * 84, 13, ACC) + T(800, 46 + k * 84, str(k + 1), 15, 700, '#fff', 'middle') + T(824, 46 + k * 84, s if len(s) < 34 else s[:s.rfind(' ', 0, 34)], 16.5, 600, INK)
    rest = s[s.rfind(' ', 0, 34) + 1:] if len(s) >= 34 else ''
    inner += (T(824, 67 + k * 84, rest, 16.5, 600, INK) if rest else '') + T(824, (88 if rest else 67) + k * 84, sub[k], 15, 400, INK2)
    g += inner if k == 0 else F(k, inner)
g += IMG(0, 360, 64, 64, 'figs/people/steven-brunton.jpg', 4) + IMG(72, 360, 64, 64, 'figs/people/nathan-kutz.jpg', 4)
g += T(152, 386, 'Builds on deep Koopman networks', 16, 600, INK) + T(152, 408, 'Lusch, Kutz and Brunton, Nature Communications 2018', 14.5, 400, INK2)
g += F(3, keybox(560, 372, 560, f'Loss = reconstruction + {kw("multi step")} + classification', 19))
slide('KSNet learns K from EEG, then classifies with the modes it keeps', SVG(g), mark='Method', status='pub',
      ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Fig. 2 | Lusch, Kutz, Brunton, Nat. Commun. 2018',
      notes='This is the figure from our paper. One: the encoder lifts a ten second, 23 channel segment into a latent state. Click two: one full real matrix K, not diagonal, so modes can couple. It must predict three steps ahead and the decoder checks each step. Click three: every eigenvalue has a frequency, and a soft band with learned edges keeps some modes. Click four: a small convolutional head classifies. All trained jointly. Siji Chen and Yanshen Sun built it, on the deep Koopman networks of Lusch, Kutz and Brunton.')

# 7. results and spectra (one slide)
g = ''
rows_c = [('SVM', 0.50, 0.63), ('EEG Conformer', 0.65, 0.73), ('EEGNet', 0.63, 0.73), ('DeepConvNet', 0.68, 0.71), ('ShallowConvNet', 0.80, 0.85), ('KSNet', 0.87, 0.90)]
g += T(0, 14, 'AUC, 5 fold cross validation over segments', 15, 400, INK2)
g += T(270, 40, 'CHB-MIT', 15, 600, INK, 'middle') + T(420, 40, 'SIENA', 15, 600, INK, 'middle')
for k, (lab, a, b) in enumerate(rows_c):
    y = 56 + k * 40; ks = lab == 'KSNet'
    g += T(180, y + 19, lab, 16.5, 600 if ks else 400, INK, 'end')
    for j, v in enumerate((a, b)):
        bw = (v - 0.4) / 0.6 * 120
        g += R(200 + j * 150, y + 2, bw, 24, ACC if ks else AXIS, 2) + T(206 + j * 150 + bw, y + 20, f'{v:.2f}', 15, 600 if ks else 400, INK)
g += T(0, 332, 'Mode selection on, F1: 0.69 to 0.81 (CHB-MIT), 0.72 to 0.82 (SIENA)', 15, 400, INK)
# spectra redrawn
fq = [4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124]
pre = [-93, -17, -4, -15, -31, -10, -65, -38, -12, -2, -8, -13, -19, -24, -30, -35]
inter = [-59, -8, -5, -58, -35, -18, -55, -30, -6, -17, -120, -170, -222, -226, -229, -232]
X0, Y0, W, H = 600, 50, 390, 260
def px_(f): return X0 + (f - 4) / 120 * W
def py_(v): return Y0 + (0 - v) / 250 * H
sp = T(X0 - 40, 14, 'Learned spectra, trained on one phase only (CHB-MIT)', 15, 400, INK2)
for v in (0, -100, -200):
    sp += L(X0, py_(v), X0 + W, py_(v), RULE, 1) + T(X0 - 10, py_(v) + 5, str(v), 13.5, 400, INK2, 'end')
for f in (4, 28, 52, 76, 100, 124):
    sp += T(px_(f), Y0 + H + 22, f'{f}', 13.5, 400, INK2, 'middle')
sp += T(X0 + W / 2, Y0 + H + 44, 'mode frequency (Hz)', 14, 400, INK2, 'middle') + T(X0 - 40, Y0 - 12, 'decay rate, lower fades faster', 13.5, 400, INK2)
sp += R(px_(76), Y0, px_(124) - px_(76), H, '#000', 0, 'fill-opacity="0.04"')
sp += P('M' + ' L'.join(f'{px_(f):.1f},{py_(v):.1f}' for f, v in zip(fq, inter)), INK2, 2) + T(px_(124) + 8, py_(-232) + 5, 'inter-ictal', 15, 400, INK2)
sp += P('M' + ' L'.join(f'{px_(f):.1f},{py_(v):.1f}' for f, v in zip(fq, pre)), ACC, 2.5) + T(px_(124) + 8, py_(-35) + 5, 'pre-ictal', 15, 600, ACC_T)
sp += T(px_(100), py_(-80), 'gap above 76 Hz', 14, 400, INK2, 'middle')
g += F(1, sp)
g += F(2, keybox(0, 400, 1120, f'Best of 11 baselines on both datasets, and a spectrum that {kw("differs by phase")}. That was the paper.'))
slide('In the paper, KSNet beat eleven baselines and learned phase specific spectra', SVG(g), mark='Results', status='pub',
      ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Table I, Fig. 3 (curves redrawn from the figure) and Fig. 4',
      notes='The published results. Segment level five fold cross validation, 23 CHB-MIT and 13 SIENA patients. KSNet 0.87 and 0.90, the best baseline ShallowConvNet 0.80 and 0.85, five of eleven baselines shown. Mode selection raises F1 from 0.69 to 0.81 on CHB-MIT. Click: interpretability. One model trained only on pre-ictal segments, one only on inter-ictal. Their spectra differ, most above 76 Hz, where inter-ictal modes fade much faster. Click: that was the end of the paper. Then we got curious.')

# 8. live demo: a clock that never sees EEG
g = ''
g += F(3, keybox(0, 410, 1120, f'A predictor must beat its own {kw("fake seizure times")}. A clock cannot.'))
slide('A model that sees only the clock can look like a seizure predictor', SVG(g), mark='After the paper, live',
      html_=demo('leak', 0, 0, 1130, 395) + steps(3),
      ref='Simulation computed live: 4 days of 5 min segments, 8 seizures mostly at night, a nearest neighbor model on time only',
      notes='A thought experiment, computed live. Four days of recording cut into five minute segments, eight seizures, most at night. The model never sees EEG, only when each segment was recorded. Click: shuffle the segments at random into train and test, the usual practice. AUC about 1.0, because every test segment has training neighbors from the same seizure. Click: train only on the past. It collapses to chance. Click: give it the hour of the day instead. Now 0.61, it looks like a weak predictor. Click: move every seizure by a whole day. It scores the same. That is a shortcut, not a predictor.')

# 9. the real numbers
g = ''
g += T(0, 14, 'CHB-MIT, same labels, every 10 s clip. One model has no EEG at all.', 15, 400, INK2)
rows = [('time of day + place in file, no EEG', 0.981, ACC, True), ('KSNet as published', 0.87, SLATE, False),
        ('Koopman clip summary', 0.836, AXIS, False), ('band power', 0.787, AXIS, False)]
for k, (lab, v, col, b) in enumerate(rows):
    g += hbar(0, 34 + k * 42, lab, v, 0.4, 1.0, 230, col, b, lw=290, size=16)
g += axis_ticks(290, 34 + 4 * 42 + 2, 230, 0.4, 1.0, [0.4, 0.6, 0.8, 1.0], label='AUC, random split')
g += T(0, 290, 'SIENA: no EEG 0.883. Our own paper, leave one patient out: 0.48 and 0.57.', 15.5, 400, INK)
XL = [700, 850, 1000]
labs_ = [('random', 'split'), ('leave one', 'seizure out'), ('train on', 'the past')]
def ly(v): return 330 - (v - 0.4) / 0.6 * 290
lad = ''
for k, x in enumerate(XL):
    lad += L(x, 40, x, 330, RULE, 1) + T(x, 352, labs_[k][0], 14.5, 400, INK2, 'middle') + T(x, 370, labs_[k][1], 14.5, 400, INK2, 'middle')
series = [('no EEG', [0.981, 0.582, 0.564], ACC, 2.5, -8), ('Koopman', [0.836, 0.588, 0.536], SLATE, 2, 8), ('band power', [0.787, 0.544, 0.508], AXIS, 2, 26)]
for name, vals, col, sw, off in series:
    lad += P('M' + ' L'.join(f'{x},{ly(v):.1f}' for x, v in zip(XL, vals)), col, sw) + ''.join(C(x, round(ly(v), 1), 4.5, col) for x, v in zip(XL, vals))
    lad += T(XL[-1] + 12, round(ly(vals[-1]) + off, 1), f'{name} {vals[-1]:.2f}', 15, 600 if name == 'no EEG' else 400, ACC_T if name == 'no EEG' else INK2)
    lad += T(XL[0] - 12, round(ly(vals[0]) + 5, 1), f'{vals[0]:.2f}', 14, 400, INK2, 'end')
g += F(1, lad + T(660, 14, 'Make the split stricter, step by step', 15, 400, INK2))
g += F(2, keybox(0, 400, 1120, f'Every EEG method loses {kw("0.28 to 0.53")} AUC. A random split measures neighbors in time.'))
slide('On real data, a model with no EEG scores 0.98 under a random split', SVG(g), mark='After the paper',
      ref='Our follow up, 17 CHB-MIT and 12 SIENA patients, preregistered predictions A1 to A3 all held, details in backup',
      notes='Now the real data, not a simulation. Same CHB-MIT labels, every clip. Two numbers per segment, time of day and position in the recording file, and no EEG at all: 0.98. Higher than every EEG model, including our published 0.87, which used its own sample. SIENA, 0.88. And our paper had the hint already: leave one patient out, 0.48 and 0.57. Click: make the split stricter. Leave out whole seizures, then train only on the past. The no EEG model falls to 0.56. Click: so do all EEG methods, by 0.28 to 0.53. The random split was measuring neighbors in time.')

# 10. the strict test and what it caught
g = ''
steps_ = [('Train on the past only', 'refit after each seizure'), ('Seizures 4 h apart', 'warn 5 to 35 min ahead'),
          ('Held out calibration', 'never trained on'), ('Fake seizure times', 'onsets moved by whole days')]
for k, (a, b) in enumerate(steps_):
    x = k * 285
    g += R(x, 0, 268, 76, GROUP) + R(x, 0, 5, 76, ACC if k == 3 else AXIS, 0) + T(x + 18, 32, a, 17.5, 600, INK) + T(x + 18, 58, b, 14.5, 400, INK2)
g += T(0, 112, 'What it caught, all from methods that looked fine before', 16, 400, INK2)
cards = [('Daily rhythm', 'SWEC, cycle model, intracranial', '0.556', 'real seizures', '0.563', 'fake seizures'),
         ('Recording structure', 'SeizeIT2, a model with no EEG', '0.659', 'real seizures', '0.666', 'fake seizures'),
         ('Calibration leak', 'CHB-MIT, our own baseline', '0.667', 'as first reported', '0.589', 'held out calibration')]
for k, (a, b, v1, l1, v2, l2) in enumerate(cards):
    x = k * 380
    g += F(k, R(x, 128, 360, 158, GROUP) + T(x + 18, 160, a, 18.5, 600, INK) + T(x + 18, 184, b, 14.5, 400, INK2)
           + T(x + 18, 240, v1, 36, 400, INK) + T(x + 18, 266, l1, 14, 400, INK2)
           + T(x + 190, 240, v2, 36, 400, FAIL if k < 2 else INK) + T(x + 190, 266, l2, 14, 400, INK2))
g += F(3, quote(28, 336, Q['andrzejak']['lines'], Q['andrzejak']['who'], 19))
slide('With fake seizure times as a control, the strict test caught three shortcuts we had trusted', SVG(g), mark='A stricter test', status='prog',
      ref='Andrzejak et al., Phys. Rev. E 2003 | Burrello et al. 2019 (SWEC) | SeizeIT2, OpenNeuro ds005873',
      notes='So we rebuilt the test. Train on the past only. Count seizures at least four hours apart and warn five to 35 minutes ahead. Calibrate on held out data. And Andrzejak 2003: move seizure times by whole days and demand the method does worse. Click: a cycle model on SWEC looked fine at 0.556, but scores 0.563 on fake seizures. Daily rhythm. Click: on SeizeIT2 a model with no EEG reached 0.659, 0.666 on fakes. Recording structure. Click: our own CHB-MIT baseline fell from 0.667 to 0.589 with honest calibration. Click: the rule from 2003, still the right one.')

# 11. honest level
g = ''
cols_ = ['band power', 'CNN', 'foundation model', 'Koopman']
dsets = [('SeizeIT2', '73 patients, behind the ear', [0.613, 0.560, 0.562, 0.621]), ('SWEC', '13 patients, intracranial', [0.523, 0.636, 0.578, 0.533]),
         ('CHB-MIT', '7 patients, scalp', [0.589, 0.483, 0.486, 0.590])]
CX = [470, 640, 810, 980]
g += R(CX[3] - 70, 0, 140, 300, TINT, 3, 'fill-opacity="0.45"')
for j, c in enumerate(cols_):
    g += T(CX[j], 34, c, 17, 600, INK, 'middle')
g += T(CX[2], 56, 'CBraMod, ICLR 2025', 13.5, 400, INK2, 'middle') + T(CX[3], 56, 'DMD eigenvalue', 13.5, 400, INK2, 'middle')
g += L(0, 70, 1110, 70, INK, 1.5)
for k, (name, sub_, vals) in enumerate(dsets):
    y = 112 + k * 72
    g += T(0, y, name, 20, 600, INK) + T(0, y + 22, sub_, 14.5, 400, INK2)
    best = max(range(4), key=lambda j: vals[j]) if k < 2 else -1
    for j, v in enumerate(vals):
        g += T(CX[j], y + 6, f'{v:.2f}', 26, 600 if j == best else 400, INK if j == best else INK2, 'middle')
    if k < 2:
        g += L(0, y + 38, 1110, y + 38, RULE, 1)
g += L(0, 300, 1110, 300, INK, 1.5)
g += T(0, 330, 'Calibrated AUC, 0.5 is chance. Bold: best per dataset. On CHB-MIT only the CNN passes the fake seizure gate, so no winner.', 15.5, 400, INK2)
g += F(1, keybox(0, 400, 1120, f'No method wins everywhere, and the {kw("foundation model")} does not rescue it'))
slide('Under the strict test, every method sits between 0.48 and 0.64, deep models included', SVG(g), mark='A stricter test', status='prog',
      ref='Wang et al., CBraMod, ICLR 2025 | our round 11, held out calibration, shared windows and fake seizures',
      notes='The honest level. Three datasets, four kinds of model, one strict test. On SeizeIT2, 73 patients with two channels behind the ear, the Koopman feature is best at 0.62. On SWEC intracranial, the CNN at 0.64. On CHB-MIT nothing is reliably above chance. Click: no method wins everywhere. And the EEG foundation model, which our paper listed as future work, does not rescue it.')

# 12. Koopman as a plug-in
g = ''
g += T(0, 14, 'SeizeIT2, 73 patients. Each system averages calibrated scores, no fitted weights.', 15, 400, INK2)
rows = [('CNN alone', 0.560, AXIS, False), ('CNN + foundation model + control feature', 0.571, AXIS, False),
        ('CNN + foundation model + band power', 0.587, AXIS, False), ('CNN + foundation model + Koopman', 0.594, ACC, True)]
for k, (lab, v, col, b) in enumerate(rows):
    inner = hbar(0, 40 + k * 50, lab, f'{v:.3f}', 0.45, 0.65, 330, col, b, lw=420, val=v)
    g += F(1, inner) if k == 3 else inner
g += axis_ticks(420, 40 + 4 * 50 + 4, 330, 0.45, 0.65, [0.45, 0.5, 0.55, 0.6, 0.65], label='calibrated AUC')
g += F(2, bignum(890, 80, '+0.023', 'over the identical feature', 'built without Koopman'))
g += F(2, T(890, 176, '90% CI +0.004 to +0.041', 14.5, 400, INK2) + T(890, 198, 'Holm p 0.046, preregistered', 14.5, 400, INK2)
       + T(890, 220, 'on fake seizures: −0.020', 14.5, 400, INK2))
g += F(3, keybox(0, 400, 1120, f'Koopman does not need to win alone: it {kw("adds")} to a CNN and a foundation model'))
slide('Plugged into a CNN and a foundation model, the Koopman feature still adds', SVG(g), mark='Where Koopman helps', status='prog',
      ref='Our round 11, preregistered, development set (these patients were seen in earlier rounds)',
      notes='So we stopped asking Koopman to win alone. Each system averages calibrated scores, nothing to fit. The Koopman feature is the leading DMD eigenvalue of band power, relative to the same patient two hours earlier. Click: added to CNN plus foundation model, 0.594. Click: against the identical feature without Koopman, plus 0.023, interval above zero, Holm p 0.046, preregistered, and it does worse on fake seizures, as it should. Caveat: these patients were seen in earlier rounds. Click.')

# 13. few labels
g = ''
grp = [('only 1 seizure to learn from', 41, [0.571, 0.467, 0.461, 0.519]), ('2 or more seizures', 44, [0.595, 0.557, 0.565, 0.600])]
nm = ['Koopman', 'CNN', 'control feature', 'band power']
for gi, (name, n_, vals) in enumerate(grp):
    x = gi * 570
    inner = T(x, 14, f'{name}, {n_} patients', 18, 600, INK)
    for j, v in enumerate(vals):
        inner += hbar(x - 40, 36 + j * 44, nm[j], v, 0.4, 0.65, 240, ACC if j == 0 else AXIS, j == 0, lw=200)
    inner += axis_ticks(x + 160, 36 + 4 * 44 + 4, 240, 0.4, 0.65, [0.4, 0.5, 0.6])
    g += F(1, inner) if gi == 1 else inner
g += F(2, keybox(0, 300, 1120, f'With one seizure to learn from, Koopman leads the CNN by {kw("0.10")}'))
g += F(3, T(0, 392, 'Why it fits: an eigenvalue relative to the same patient two hours ago has no units and needs almost no labels.', 17, 400, INK)
       + T(0, 420, 'Split after the fact, 11 SWEC patients do not repeat it. Confirmation: HUP Phase II, 42 patients with 2 or more lead seizures.', 15, 400, INK2))
slide('The fewer seizures a patient has, the more the Koopman feature helps', SVG(g), mark='Where Koopman helps', status='pre',
      ref='Our analysis of round 11 scores, split after the fact. Confirmation on HUP Phase II (ieeg.org) is being set up',
      notes='The most interesting pattern, flagged as exploratory. Split SeizeIT2 patients by how much the model could learn from. One seizure before testing, 41 patients: Koopman 0.57, the CNN 0.47, below chance. Click: with two or more, the gap closes. Click: one seizure is the common clinical case, a new patient. Click: why it makes sense. An eigenvalue relative to the patient two hours ago has no units and needs almost no labels. We split after seeing the data, so it is a hypothesis, now under test on 42 HUP intracranial patients.')

# 14. critical slowing
g = ''
g += IMG(0, 0, 76, 76, 'figs/people/marten-scheffer.jpg', 4) + (IMG(88, 0, 52, 76, Q['books']['scheffer'], 2) if Q['books'].get('scheffer') else '')
g += quote(176, 22, Q['scheffer']['lines'], Q['scheffer']['who'], 17.5)
g += F(0, quote(712, 128, Q['maturana']['lines'], Q['maturana']['who'], 17) + quote(712, 190, Q['wilkat']['lines'], Q['wilkat']['who'], 17))
g += F(1, L(700, 250, 1120, 250, RULE) + T(700, 276, 'Ours, 120 scalp patients (SeizeIT2)', 16.5, 600, INK) + T(700, 298, 'last 10 min z = −0.13, fake seizures −0.10', 15.5, 400, INK))
g += F(2, T(700, 334, 'Ours, 13 intracranial patients (SWEC)', 16.5, 600, INK) + T(700, 356, 'moves before onset, +0.27, but up', 15.5, 400, INK) + T(700, 376, 'in only 31% of patients', 15.5, 400, INK))
g += F(3, keybox(0, 410, 1120, f'No common tipping point. Changes are {kw("patient specific")}, and visible only inside the skull.'))
slide('Before seizures the spectrum does not tip toward instability, at least not for everyone', SVG(g), mark='What the spectrum says',
      html_=demo('tip', 0, 100, 660, 300),
      ref=Q['scheffer']['ref'] + ' | Maturana et al., Nat. Commun. 2020 | Wilkat, Rings, Lehnertz, Chaos 2019',
      notes='Back to the demo from the start, where nothing happened before onset. There is a famous reason to expect something. Scheffer and colleagues: before a tipping point, a system recovers slowly from small kicks. Watch the ball. Click: the valley flattens, kicks linger, and the leading eigenvalue creeps toward one. Maturana 2020 found it a reliable indicator in long intracranial recordings, Wilkat, Rings and Lehnertz found no evidence before 105 seizures. Click: in 120 scalp patients we see nothing beyond fake seizure times. Click: inside the skull the eigenvalue does move, but up in only a third of patients. Click: both camps may be right. Changes exist, they are individual.')

# 15. one family
g = ''
fam = [('figs/papers/schmid2010-p1.png', 'DMD', 'identity observables', 'fluid dynamics, Schmid 2010'),
       ('figs/papers/li2021-p1.png', 'Neural fragility', 'windowed DMD on iEEG', 'onset zone, Li et al. 2021'),
       ('figs/paper/flow_chart.png', 'KSNet', 'learned observables', 'prediction, ours 2026')]
for k, (src, a, b, c) in enumerate(fam):
    x = k * 380
    g += IMG(x, 0, 104, 134, src, 2, align='xMidYMin' if k < 2 else 'xMinYMid') + T(x + 120, 34, a, 21, 600, INK) + T(x + 120, 60, b, 15.5, 400, INK) + T(x + 120, 84, c, 14.5, 400, INK2)
    if k < 2:
        g += arrow(x + 300, 70, x + 366, 70)
g += quote(28, 176, Q['li']['lines'], Q['li']['who'], 16.5)
rows = [('line length, classic baseline', 0.790, 0.714), ('neural fragility, our rebuild', 0.806, 0.719), ('Koopman, delay embedding', 0.809, 0.729)]
g += T(0, 262, 'Fragility code was not released. Our open rebuild:', 15, 400, INK2) + T(560, 262, 'HUP, 56 patients', 15.5, 600, INK, 'middle') + T(820, 262, 'external, 29 patients', 15.5, 600, INK, 'middle')
for k, (lab, a, b) in enumerate(rows):
    y = 278 + k * 36
    g += T(400, y + 18, lab, 17, 400, INK, 'end')
    g += F(0 if k < 2 else 1, T(560, y + 18, f'{a:.2f}', 19, 600 if k == 2 else 400, INK, 'middle') + T(820, y + 18, f'{b:.2f}', 19, 600 if k == 2 else 400, INK, 'middle'))
g += T(960, 300, 'electrode level AUC', 14.5, 400, INK2) + T(960, 320, 'for the onset zone', 14.5, 400, INK2)
g += F(2, keybox(0, 400, 1120, f'Richer lifts {kw("tie")} with fragility: the operator matters more than the observables'))
slide('KSNet, neural fragility and DMD are one operator family, useful beyond prediction', SVG(g), mark='What the spectrum says',
      ref='Schmid, J. Fluid Mech. 2010 | Li et al., Nat. Neurosci. 2021 | OpenNeuro ds004100, ds003029',
      notes='One connection I find useful. Dynamic mode decomposition, from fluid dynamics, fits a linear operator with the identity as observables. Neural fragility, Li and colleagues 2021, is windowed DMD on intracranial EEG and it localizes the seizure onset zone, in their data better than clinicians at predicting surgical failure. KSNet is the same operator with learned observables. Click: our open rebuild of fragility, 0.81 on 56 HUP patients against 0.79 for line length, and 0.72 on 29 external patients. Click: a richer Koopman lift, 0.81 and 0.73, a tie. Click: the operator does most of the work.')

# 16. Trefethen: what eigenvalues miss
g = ''
g += IMG(0, 0, 76, 76, 'figs/people/lloyd-trefethen.jpg', 4) + (IMG(88, 0, 52, 76, Q['books']['trefethen'], 2) if Q['books'].get('trefethen') else '')
g += quote(176, 18, Q['trefethen']['lines'], Q['trefethen']['who'], 16.5)
g += F(0, T(700, 150, 'Both eigenvalues stay inside the circle.', 17, 600, INK) + T(700, 174, 'Couple the two modes and a kick', 16, 400, INK2)
       + T(700, 196, 'first grows several times, then decays.', 16, 400, INK2))
g += F(1, T(700, 250, 'An eigenvalue only feature, ours included,', 17, 600, INK) + T(700, 274, 'cannot see this. A seizure may start', 16, 400, INK2)
       + T(700, 296, 'exactly this way.', 16, 400, INK2))
g += F(2, keybox(0, 410, 1120, f'Open problem: features that see {kw("transient growth")}, not only eigenvalues'))
slide('Every eigenvalue can decay while the signal still grows first', SVG(g), mark='Open',
      html_=demo('nonnormal', 0, 100, 660, 300),
      ref=Q['trefethen']['ref'] + ' | ' + Q['books'].get('tref_ref', 'Trefethen and Embree, Spectra and Pseudospectra, Princeton 2005'),
      notes='One open problem I want to leave you with. Trefethen and colleagues showed in 1993 that eigenvalues can mislead. Here are two modes, both decaying, eigenvalues 0.92 and 0.85. Click: couple them, the eigenvalues do not move, yet a small kick first grows about five times and only then decays. Click: an eigenvalue only feature, including ours, is blind to this, and a seizure might start exactly this way. You can drag the slider. Click: features that see transient growth are open territory.')

# 17. close
qr_svg = ''
try:
    import segno
    qr_svg = segno.make(URL, error='m').svg_inline(scale=5, dark=INK, light=BG, border=2)
except Exception:
    qr_svg = f'<div style="width:190px;height:190px;border:1px dashed {AXIS}"></div>'
g = ''
cols = [('What this talk showed', ['a learned Koopman model gives a readable spectrum', 'random splits reward the clock, fake seizure times catch it', 'Koopman helps as a plug-in, most with few seizures']),
        ('Open, and where we want partners', ['confirm the one seizure result on 42 new patients', 'features that see transient growth, not only eigenvalues', 'spectra read online in closed loop devices'])]
for k, (h, items) in enumerate(cols):
    x = k * 430
    g += T(x, 30, h, 20, 600, INK)
    for j, it in enumerate(items):
        cut = it.rfind(' ', 0, 40) if len(it) > 40 else len(it)
        g += C(x + 6, 72 + j * 62, 4.5, ACC if k == 1 else AXIS) + T(x + 22, 78 + j * 62, it[:cut], 17, 400, INK)
        if cut < len(it):
            g += T(x + 22, 100 + j * 62, it[cut + 1:], 17, 400, INK)
g += T(0, 300, 'Talk to us: long intracranial cohorts, and anyone running seizure forecasting trials.', 18, 400, INK2)
SLIDES.append(f'''<section class="close"><span class="mark">Close</span>
  <h2>Koopman spectra help most where labels are scarce, if the test is honest</h2>
  {SVG(g)}
  <div class="qr">{qr_svg}<div class="qr-cap">Slides: scan, or zhiqian.ai, then Talks</div></div>
  <div class="ref">Andrzejak et al., Phys. Rev. E 2003 | Trefethen et al., Science 1993 | Liang et al., IEEE JBHI 2023 | Cook et al., Lancet Neurol. 2013</div>
  <aside class="notes">Three things. A learned Koopman model gives a readable spectrum. A random split rewards the clock, and fake seizure times catch it. Under the honest test Koopman helps as a plug-in, most when a patient has few seizures. Open: confirm that on 42 new intracranial patients, build features that see transient growth, and read spectra online in closed loop devices, as Liang and colleagues began. If you have long intracranial cohorts or run forecasting trials, come and talk. The QR code has the slides.</aside>
</section>''')

# ---------------- backups ----------------
B_LADDER = bslide('The audit ladder in numbers', SVG(
    T(0, 20, 'Mean AUC, CHB-MIT core patients (n per level 17, 10, 8, 6)', 17, 400, INK2) +
    ''.join(T(j * 210 + (0 if j == 0 else 160), 60, h, 16, 600, INK, 'start' if j == 0 else 'middle') for j, h in enumerate(['method', 'random split', 'leave one seizure out', 'walk forward', 'walk forward, clock matched'])) +
    ''.join(T(0, 96 + i * 36, r[0], 17, 400, INK) + ''.join(T((j + 1) * 210 + 160, 96 + i * 36, f'{v:.3f}', 17, 400, INK, 'middle') for j, v in enumerate(r[1:]))
            for i, r in enumerate([('time + position, no EEG', 0.981, 0.582, 0.564, 0.547), ('band power median', 0.787, 0.544, 0.508, 0.402), ('all 138 band powers', 0.968, 0.497, 0.435, 0.312),
                                   ('Koopman clip summary', 0.836, 0.588, 0.536, 0.415), ('slow scale Koopman', 0.893, 0.653, 0.600, 0.595)])) +
    T(0, 310, 'SIENA, 12 patients: no EEG 0.883 random, 0.837 with whole files held out (files are cut around seizures).', 17, 400, INK2) +
    T(0, 340, 'Two seizure free files of the same patient separate at 0.72, close to pre vs inter at 0.75.', 17, 400, INK2)),
    ref='Our follow up, run 2026-11-17, preregistered predictions A1 to A3 all held')
B_SPEC = bslide('The paper figure for both datasets', f'<img class="figimg" src="figs/paper/pre_inter_chbmit_new.png" style="left:60px;width:560px"><img class="figimg" src="figs/paper/pre_inter_siena_new.png" style="left:640px;width:560px">',
    ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Fig. 3', status='pub')
B_MODES = bslide('Mode selection ablation, paper figure', '<img class="figimg" src="figs/paper/modes_selection_chbmit_mod.png" style="left:140px;width:1000px">',
    ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Fig. 4', status='pub')
B_HUP = bslide('Confirmation set: HUP Phase II on ieeg.org', SVG(
    T(0, 20, '151 patients, about 35,600 hours of intracranial EEG, median 128 channels', 19, 400, INK) +
    T(0, 56, 'Seizures from annotations of type Seizure, end and uncertain marks removed, merged within 5 min', 17, 400, INK2) +
    ''.join(hbar(0, 86 + k * 38, f'{lab} lead seizures', v, 0, 80, 500, ACC if lab in ('2', '3', '4', '5+') else AXIS, False, lw=230) for k, (lab, v) in enumerate([('0', 79), ('1', 30), ('2', 19), ('3', 9), ('4', 8), ('5+', 6)])) +
    T(0, 340, '42 patients with 2 or more lead seizures (4 h apart), 23 with 3 or more. Stimulation sessions are still to be excluded.', 17, 400, INK2)),
    ref='Our scan 2026-11-25, metadata only, prereg amendment pending', status='prog')

def attach(idx, *bs):
    SLIDES[idx] = '<section>' + SLIDES[idx] + ''.join(bs) + '</section>'
attach(5, B_SPEC + B_MODES)  # KSNet method: paper figures below it
attach(8, B_LADDER)
attach(12, B_HUP)

# ---------------- page ----------------
FONTS = ''.join(f'@font-face{{font-family:"et-book";src:url(figs/fonts/{f}) format("woff");font-weight:{w};font-style:{s};font-display:swap}}'
                for f, w, s in [('etbook-roman-lf.woff', 400, 'normal'), ('etbook-bold-lf.woff', '600 800', 'normal'), ('etbook-italic.woff', 400, 'italic')])
CSS = FONTS + f'''
html,body,.reveal-viewport{{background:{BG} !important}}
.reveal{{font-family:{FONT};color:{INK}}}
.reveal .controls,.reveal .progress,.reveal .slide-number{{display:none !important}}
.reveal .slides{{text-align:left}}
.reveal .slides section{{padding:0 !important;height:720px;box-sizing:border-box}}
.reveal .slides>section,.reveal .slides>section>section{{top:0 !important}}
.reveal h2{{position:absolute;top:46px;left:64px;right:250px;margin:0 !important;font-family:{FONT} !important;font-weight:400 !important;font-size:40px !important;
  line-height:1.12;color:{INK} !important;text-transform:none !important;letter-spacing:0 !important}}
.reveal .mark{{position:absolute;top:18px;left:66px;font:400 13px/1 {FONT};color:{INK2};text-transform:uppercase;letter-spacing:.14em}}
.reveal .status{{position:absolute;top:14px;right:44px;background:{ACC};color:#fff;border-radius:4px;padding:6px 12px;font:700 14px/1 {FONT};text-transform:uppercase;letter-spacing:.1em}}
.reveal svg.fig{{position:absolute;top:168px;left:50px;width:1180px;height:470px;overflow:visible}}
.reveal .ref{{position:absolute;bottom:22px;right:64px;max-width:80%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font:400 13.5px/1.3 {FONT};color:{REF};text-align:right}}
.reveal .ref a{{color:inherit;text-decoration:none}} .reveal .ref a:hover{{text-decoration:underline}}
.reveal .ref .rsep{{display:inline-block;width:1px;height:.85em;background:{AXIS};margin:0 .65em;vertical-align:-.1em}}
.reveal .fragment{{transition:opacity 250ms ease}}
.reveal .fragment.stepper{{position:absolute;width:0;height:0;overflow:hidden}}
.reveal img.figimg{{position:absolute;top:170px;margin:0;border:0;box-shadow:none}}
.reveal .demo{{position:absolute}}
.reveal .demo canvas{{display:block;margin:0}}
.reveal .demo-btn{{font:400 14px/1 {FONT};color:{INK2};background:{GROUP};border:0;border-radius:3px;padding:6px 12px;cursor:pointer}}
.reveal .demo-range{{accent-color:{ACC}}}
.reveal section.cover .cv-left{{position:absolute;top:96px;left:64px;width:700px}}
.reveal section.cover .cv-kicker{{font:400 14px/1 {FONT};color:{INK2};text-transform:uppercase;letter-spacing:.16em;margin-bottom:28px}}
.reveal section.cover h1{{font-family:{FONT};font-weight:400;margin:0;text-transform:none;color:{INK};text-align:left;letter-spacing:0}}
.reveal section.cover .cv-small{{display:block;font-size:36px;line-height:1.2;color:{INK}}}
.reveal section.cover .cv-big{{display:block;font-size:150px;line-height:1;color:{ACC};margin:6px 0 10px -6px}}
.reveal section.cover .cv-rule{{width:120px;height:3px;background:{ACC};margin:30px 0 22px}}
.reveal section.cover .cv-author{{font:400 21px/1.45 {FONT};color:{INK2}}}
.reveal section.cover .cv-author b{{color:{INK};font-weight:600}}
.reveal section.cover .cv-fig{{position:absolute;right:30px;top:120px;width:480px;height:480px}}
.reveal section.cover.present .eig{{animation:eigp 3.2s ease-in-out infinite}}
@keyframes eigp{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.reveal section.cover .eig{{animation:none !important}}}}
.reveal section.close .qr{{position:absolute;right:50px;top:190px;width:230px;text-align:center}}
.reveal section.close .qr svg{{width:210px;height:210px}}
.reveal section.close .qr-cap{{font:400 17px/1.3 {FONT};color:{INK2};margin-top:8px}}
'''

def linkify(ref):
    parts = [p.strip() for p in ref.split('|')]
    out = []
    for p in parts:
        if p.lower().startswith(('our', 'simulation', 'chb-mit chb01')):
            out.append(esc(p))
        else:
            q = re.sub(r'\s+', '+', re.sub(r'[^\w\s.,]', ' ', p))
            out.append(f'<a href="https://scholar.google.com/scholar?q={q}" target="_blank" title="{esc(p)}">{esc(p)}</a>')
    return '<span class="rsep" aria-hidden="true"></span>'.join(out)

body = '\n'.join(SLIDES)
body = re.sub(r'<div class="ref">(.*?)</div>', lambda m: f'<div class="ref">{linkify(m.group(1))}</div>', body)

# ---------------- gates ----------------
for bad, name in (('—', 'em dash'), ('–', 'en dash')):
    assert bad not in body, f'{name} found'
txt_only = re.sub(r'<[^>]+>', ' ', body)
txt_only = re.sub(r'&[a-z]+;|&#\d+;', ' ', txt_only)
txt_only = re.sub(r'<polyline[^>]*>', ' ', txt_only)
assert ';' not in txt_only, 'semicolon: ' + txt_only[max(0, txt_only.find(';') - 60):txt_only.find(';') + 20]
for sec_ in re.findall(r'<section[^>]*>(?:(?!<section).)*?</section>', body, re.S):
    nf = len(set(re.findall(r'data-fragment-index="(\d+)"', sec_)))
    assert nf <= 4, 'more than 4 fragment steps'

DATA = json.load(open(os.path.join(HERE, 'chb01_03_t8p8.json')))
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>KSNet: Koopman Spectra for Seizure Prediction</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/theme/white.min.css">
<style>{CSS}</style></head>
<body><div class="reveal"><div class="slides">
{body}
</div></div>
<script>window.CHB01_T8P8={json.dumps(DATA, separators=(',', ':'))}</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/plugin/notes/notes.min.js"></script>
<script src="demos.js"></script>
<script>Reveal.initialize({{hash:true,center:false,width:1280,height:720,margin:0.03,transition:'fade',transitionSpeed:'fast',backgroundTransition:'fade',plugins:[RevealNotes]}}).then(function(){{DEMOS.init();DEMOS.sync();}});
['slidechanged','fragmentshown','fragmenthidden'].forEach(function(ev){{Reveal.on(ev,function(){{DEMOS.sync();}});}});</script>
</body></html>
'''
open(os.path.join(DECK, 'index.html'), 'w').write(page)
print('main slides', len(SLIDES), 'bytes', len(page))
if MISSING:
    print('MISSING images:', sorted(set(MISSING)))
