"""KSNet talk, IEEE BIBM 2026, Session S3, Wed Dec 2 10:40. Builds ../index.html.

usage: python3 -I src/build.py   (from the deck folder)
Slides are inline SVG on a 1180 by 470 drawing, house style v2 (warm neutrals, RIT orange as the only accent, ET Book).
Numbers: paper Table I and II (published PDF), and our follow up runs in aquastar/zhiqian-knowledge-base
(papers/ksnet-talk-findings.md, which points to every run folder).
"""
import os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.dirname(HERE)
URL = 'https://aquastar.github.io/talks/koopman-seizure/2026-12-02-bibm-dallas/'

BG = '#FBFAF7'; INK = '#1F1E1B'; INK2 = '#5F5D50'; LINE = '#7C878E'; AXIS = '#ACA39A'; RULE = '#D7D2CB'; GROUP = '#F1EDE7'
ACC = '#F76902'; ACC_T = '#C45200'; TINT = '#FAD6BA'; SLATE = '#4C5B66'; FAIL = '#DA291C'; KEYBG = '#FDEFE3'; REF = '#A39E93'
FONT = 'et-book,Georgia,serif'

# ---------------- svg helpers ----------------
def esc(s):
    return html.escape(str(s), quote=False)

def T(x, y, s, size=18, w=400, fill=INK, a='start', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{a}" {extra}>{s}</text>'

def R(x, y, w, h, fill=GROUP, rx=3, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'

def L(x1, y1, x2, y2, col=AXIS, sw=1, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}" {extra}/>'

def C(x, y, r, fill=INK2, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'

def P(d, col=INK2, sw=1.5, fill='none', extra=''):
    return f'<path d="{d}" stroke="{col}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'

def F(i, inner):
    """one fragment step"""
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
    return f'<tspan font-weight="600" fill="{ACC_T}">{s}</tspan>'

def keybox(x, y, w, text, size=21):
    """his fixed style for a key statement: light orange box, thick orange bar on the left, key words bold orange"""
    return R(x, y, w, 48, KEYBG, 3) + R(x, y, 7, 48, ACC, 0) + T(x + 24, y + 31, text, size, 400, INK)

def bignum(x, y, num, line1, line2=''):
    out = T(x, y, num, 40, 400, INK) + L(x, y + 10, x + 26 * len(num) * 0.62 + 10, y + 10, ACC, 3)
    out += T(x, y + 38, line1, 16, 400, INK2)
    if line2:
        out += T(x, y + 59, line2, 16, 400, INK2)
    return out

def hbar(x, y, label, v, vmin, vmax, w, col, bold=False, note='', lw=330, h=26, val=None):
    bw = ((val if val is not None else v) - vmin) / (vmax - vmin) * w
    out = T(x + lw - 14, y + h * 0.72, label, 17, 600 if bold else 400, INK, 'end')
    out += R(x + lw, y, max(bw, 2), h, col, 2)
    out += T(x + lw + bw + 10, y + h * 0.72, f'{v:.2f}' if isinstance(v, float) else str(v), 17, 600 if bold else 400, INK)
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

def chance_line(x0, y_top, y_bot, vmin, vmax, w, v=0.5):
    tx = x0 + (v - vmin) / (vmax - vmin) * w
    return L(tx, y_top, tx, y_bot, LINE, 1.2, 'stroke-dasharray="4 4"') + T(tx, y_top - 8, 'chance', 14, 400, INK2, 'middle')

# ---------------- section ----------------
SLIDES = []
STATUS = {'pub': 'Published, BIBM 2026', 'prog': 'In progress', 'pre': 'Exploratory, post hoc'}

def slide(title, svg, mark='', status='', ref='', notes='', cls='', backup=None):
    st = f'<span class="status">Our work · {STATUS[status]}</span>' if status else ''
    mk = f'<span class="mark">{mark}</span>' if mark else ''
    rf = f'<div class="ref">{ref}</div>' if ref else ''
    nt = f'<aside class="notes">{notes}</aside>' if notes else ''
    c = f' class="{cls}"' if cls else ''
    body = f'<section{c}>{mk}<h2>{title}</h2>{st}{svg}{rf}{nt}</section>'
    if backup:
        body = '<section>' + body + ''.join(backup) + '</section>'
    SLIDES.append(body)

def bslide(title, svg, ref='', notes='', status=''):
    st = f'<span class="status">Our work · {STATUS[status]}</span>' if status else ''
    rf = f'<div class="ref">{ref}</div>' if ref else ''
    nt = f'<aside class="notes">{notes}</aside>' if notes else ''
    return f'<section><span class="mark">Backup</span><h2>{title}</h2>{st}{svg}{rf}{nt}</section>'

# =====================================================================
# 1. cover
cover_fig = ''
# unit circle with eigenvalues, a light motif on the right
cx, cy, r = 930, 300, 190
cover_fig += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RULE}" stroke-width="1.5"/>'
cover_fig += L(cx - r - 30, cy, cx + r + 30, cy, RULE, 1) + L(cx, cy - r - 30, cx, cy + r + 30, RULE, 1)
import math
pts = [(0.97, 0.10), (0.93, 0.32), (0.84, 0.55), (0.62, 0.95), (0.70, 1.55), (0.45, 2.3), (0.88, 0.0)]
for k, (m, a) in enumerate(pts):
    for sgn in (1, -1):
        x = cx + r * m * math.cos(a); y = cy - sgn * r * m * math.sin(a)
        col = ACC if k == 0 else INK2
        cover_fig += C(round(x, 1), round(y, 1), 7 if k == 0 else 5.5, col, f'class="eig" style="animation-delay:{k * 0.35:.2f}s"')
cover_fig += T(cx + r + 10, cy + 26, 'Re', 14, 400, INK2) + T(cx + 10, cy - r - 12, 'Im', 14, 400, INK2)
cover = f'''<section class="cover">
  <div class="cv-left">
    <div class="cv-kicker">IEEE BIBM 2026 · Session S3, Biomedical Signal Analysis</div>
    <h1><span class="cv-small">KSNet: Learning Interpretable</span><span class="cv-big">Koopman</span><span class="cv-small">Spectral Representations for EEG Seizure Prediction</span></h1>
    <div class="cv-rule"></div>
    <div class="cv-author"><b>Siji Chen, Yanshen Sun, Zhiqian Chen, Chang-Tien Lu</b><br>Virginia Tech · Rochester Institute of Technology<br>Presented by Zhiqian Chen</div>
  </div>
  <svg class="cv-fig" viewBox="700 60 480 480" width="480" height="480" font-family="{FONT}">{cover_fig}</svg>
  <aside class="notes">Good morning. One line on the picture: these dots are eigenvalues of a linear operator learned from EEG, and the whole talk is about what such a spectrum can and cannot tell us before a seizure. Casey Nguyen just showed wearable prediction with three signals. I will stay with EEG and ask a harder question about how we test these models.</aside>
</section>'''
SLIDES.append(cover)

# 2. the question, with the dataset's own numbers
g = ''
# a 24 hour strip with seizures, a 30 minute window before each one
x0, x1, yb = 60, 1120, 210
g += T(60, 40, 'One child in CHB-MIT, chb01: about 40 hours of scalp EEG, 7 seizures (positions schematic)', 19, 400, INK)
g += L(x0, yb, x1, yb, AXIS, 1.5)
hours = 40.5
sz = [3.0, 4.1, 7.4, 21.2, 25.7, 26.4, 29.3]  # illustrative positions, see notes
for k, h in enumerate(sz):
    x = x0 + h / hours * (x1 - x0)
    pre = 0.5 / hours * (x1 - x0)
    g += F(1, R(round(x - pre, 1), yb - 46, round(pre, 1), 40, TINT, 2)) if k < 7 else ''
    g += L(round(x, 1), yb - 60, round(x, 1), yb + 8, ACC, 2.5)
for hh in range(0, 41, 8):
    x = x0 + hh / hours * (x1 - x0)
    g += L(x, yb, x, yb + 6, AXIS, 1) + T(x, yb + 28, f'{hh} h', 14.5, 400, INK2, 'middle')
g += T(x0, yb - 72, 'seizure onsets', 15, 400, ACC_T)
g += F(1, T(x0 + 330, yb - 72, 'shaded: the 30 minutes before each onset', 15, 400, INK2))
g += F(2, keybox(60, 300, 900, f'Can a model tell the {kw("30 minutes before")} a seizure from the rest of the day?'))
g += F(3, T(60, 400, 'A yes would give patients a warning, and devices time to act.', 20, 400, INK2))
slide('Seizure prediction asks whether the half hour before a seizure looks different', SVG(g), mark='Problem',
      ref='Shoeb, PhD thesis, MIT 2009 | Goldberger et al., PhysioNet, Circulation 2000',
      notes='CHB-MIT is the most used dataset for this task. Patient chb01 has 7 seizures in about 40 hours of recording. The positions on the strip are drawn to show the idea, not the exact file times. Click: the 30 minute windows before each onset, the pre-ictal phase. Everything else, far from seizures, is inter-ictal. Click: the question. Click: why it matters. A reliable warning would let a patient sit down, take a rescue dose, or let a device stimulate. Keep this picture in mind: a few short orange windows on a long day. It comes back.')

# 3. Koopman idea
g = ''
g += T(60, 40, 'Nonlinear dynamics', 20, 600, INK) + T(60, 66, 'hard to analyze', 16, 400, INK2)
# a nonlinear trajectory
g += P('M80,250 C140,120 260,120 300,210 S420,330 470,200', INK2, 2)
for (x, y) in [(80, 250), (190, 150), (300, 210), (400, 300), (470, 200)]:
    g += C(x, y, 5, INK2)
g += T(80, 290, 'x', 18, 400, INK, extra='font-style="italic"') + T(92, 296, 't', 13, 400, INK, extra='font-style="italic"')
g += F(1, arrow(510, 210, 640, 210, INK2, 1.5) + T(575, 196, 'lift with φ', 17, 400, INK2, 'middle'))
g += F(1, T(680, 40, 'Linear dynamics in a lifted space', 20, 600, INK) + T(680, 66, 'one matrix K moves every state forward', 16, 400, INK2)
       + R(680, 150, 90, 70, GROUP) + T(725, 192, 'z', 22, 400, INK, 'middle', 'font-style="italic"')
       + arrow(772, 185, 878, 185) + T(825, 172, 'K', 20, 400, INK, 'middle', 'font-style="italic"')
       + R(880, 150, 110, 70, GROUP) + T(935, 192, 'Kz', 22, 400, INK, 'middle', 'font-style="italic"')
       + arrow(992, 185, 1088, 185) + T(1040, 172, 'K', 20, 400, INK, 'middle', 'font-style="italic"')
       + R(1090, 150, 80, 70, GROUP) + T(1130, 192, 'K²z', 20, 400, INK, 'middle', 'font-style="italic"'))
# spectrum read out
g += F(2, T(680, 285, 'Each eigenvalue λ of K is one mode:', 18, 400, INK)
       + T(700, 318, 'angle of λ', 18, 600, INK) + T(820, 318, 'how fast it oscillates', 18, 400, INK2)
       + T(700, 348, 'size of λ', 18, 600, INK) + T(820, 348, 'how fast it fades', 18, 400, INK2))
g += F(3, keybox(60, 400, 1060, f'The spectrum of K is a {kw("readable summary")} of the dynamics: frequencies and decay rates.'))
slide('Koopman theory turns nonlinear dynamics into a linear map you can read', SVG(g), mark='Idea',
      ref='Koopman, PNAS 1931 | Lusch, Kutz, Brunton, Nat. Commun. 2018',
      notes='Brain dynamics are nonlinear. Koopman showed in 1931 that if you look at the right functions of the state, observables, the evolution becomes linear. Click: we lift the state with a map phi, and then one matrix K moves it forward step by step. Lusch, Kutz and Brunton made phi a neural network. Click: the payoff is the spectrum. Every eigenvalue is a mode. Its angle says how fast it oscillates, its size says how fast it fades. Click: so the spectrum is a readable summary of the dynamics. That is why we chose it for seizure prediction: the hope is that the dynamics before a seizure have a different spectrum.')

# 4. KSNet
g = ''
bx = [(60, 'EEG segment', '10 s, all channels'), (290, 'encoder φ', 'snapshots to latent z'), (520, 'Koopman K', 'full real matrix'),
      (750, 'mode selection', 'by mode frequency'), (980, 'classifier', 'ShallowConvNet')]
for k, (x, a, b) in enumerate(bx):
    fill = TINT if k in (2, 3) else GROUP
    g += R(x, 120, 190, 86, fill) + T(x + 95, 158, a, 19, 600, INK, 'middle') + T(x + 95, 184, b, 15, 400, INK2, 'middle')
    if k < 4:
        g += arrow(x + 192, 163, x + 228, 163)
g += T(1075, 240, 'pre-ictal or inter-ictal', 15, 400, INK2, 'middle')
# rollout loop
g += F(1, P('M615,208 C615,290 370,290 385,212', INK2, 1.5, extra='marker-end="url(#ah)" stroke-dasharray="5 4"')
       + T(500, 312, 'decoder ψ checks z, Kz, K²z, K³z against the next snapshots', 15.5, 400, INK2, 'middle')
       + T(500, 334, 'multi step rollout, H = 3', 15.5, 600, INK, 'middle'))
# band
g += F(2, L(770, 300, 920, 300, AXIS, 1) + P('M770,296 L795,296 C805,296 805,262 815,262 L875,262 C885,262 885,296 895,296 L920,296', ACC, 2.5)
       + T(845, 330, 'learned frequency band', 15.5, 400, INK2, 'middle') + T(845, 352, 'keeps modes inside it', 15.5, 400, INK2, 'middle'))
g += F(3, keybox(60, 400, 1060, f'Loss = reconstruction + {kw("multi step prediction")} + classification, trained end to end'))
slide('KSNet learns K from EEG, then classifies with the modes it selects', SVG(g), mark='Method', status='pub',
      ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026',
      notes='KSNet in one row. A 10 second segment of all channels is cut into overlapping snapshots. The encoder phi maps each to a latent state. One full real matrix K, not diagonal, so modes can couple and rotate. Click: K must predict three steps ahead, the decoder psi checks the predicted states against the real next snapshots. That keeps the latent dynamics consistent in time. Click: mode selection. Each eigenvalue has a frequency. A soft band with learnable edges weights the modes, and the weighted modal representation goes to a ShallowConvNet style classifier. Click: everything is trained jointly. Siji Chen and Yanshen Sun, the co-first authors, built this.')

# 5. paper results
g = ''
def panel(x, name, rows, best):
    out = T(x, 30, name, 19, 600, INK)
    for k, (lab, v) in enumerate(rows):
        bold = lab.startswith('KSNet')
        col = ACC if bold else AXIS
        out += hbar(x - 120, 56 + k * 44, lab, v, 0.4, 1.0, 270, col, bold, lw=300)
    out += axis_ticks(x + 180, 56 + len(rows) * 44 + 6, 270, 0.4, 1.0, [0.4, 0.6, 0.8, 1.0], label='AUC, higher is better')
    return out
rows_c = [('SVM', 0.50), ('EEG Conformer', 0.65), ('EEGNet', 0.63), ('DeepConvNet', 0.68), ('ShallowConvNet', 0.80), ('KSNet', 0.87)]
rows_s = [('SVM', 0.63), ('EEG Conformer', 0.73), ('EEGNet', 0.73), ('DeepConvNet', 0.71), ('ShallowConvNet', 0.85), ('KSNet', 0.90)]
g += panel(120, 'CHB-MIT, 23 patients', rows_c, 0.80)
g += panel(700, 'SIENA, 13 patients', rows_s, 0.85)
g += F(1, keybox(60, 400, 1060, f'Mode selection alone: F1 {kw("0.69 to 0.81")} on CHB-MIT, 0.72 to 0.82 on SIENA'))
slide('Under segment level cross validation, KSNet beats eleven baselines on both datasets', SVG(g), mark='Results', status='pub',
      ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Table I and Fig. 4',
      notes='These are the published numbers, 5 fold cross validation over segments, 50 pre-ictal and 50 inter-ictal segments per patient. KSNet reaches AUC 0.87 on CHB-MIT and 0.90 on SIENA. The strongest baseline is ShallowConvNet, 0.80 and 0.85. I show 5 of the 11 baselines, the rest are in the paper and all lower. Click: the ablation. Without mode selection the encoder output goes straight to the classifier. With it, F1 goes from 0.69 to 0.81 on CHB-MIT. So the spectral part carries real weight.')

# 6. spectra differ (redrawn from Fig. 3 CHB-MIT)
g = ''
fq = [4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124]
pre = [-93, -17, -4, -15, -31, -10, -65, -38, -12, -2, -8, -13, -19, -24, -30, -35]
inter = [-59, -8, -5, -58, -35, -18, -55, -30, -6, -17, -120, -170, -222, -226, -229, -232]
X0, Y0, W, H = 140, 40, 760, 300
def px(f): return X0 + (f - 4) / 120 * W
def py(v): return Y0 + (0 - v) / 250 * H
for v in (0, -100, -200):
    g += L(X0, py(v), X0 + W, py(v), RULE, 1) + T(X0 - 12, py(v) + 5, str(v), 14.5, 400, INK2, 'end')
for f in (4, 28, 52, 76, 100, 124):
    g += T(px(f), Y0 + H + 26, f'{f}', 14.5, 400, INK2, 'middle')
g += T(X0 + W / 2, Y0 + H + 52, 'mode frequency (Hz)', 15, 400, INK2, 'middle')
g += T(X0 - 12, Y0 - 14, 'decay rate, lower fades faster', 15, 400, INK2, 'start')
g += P('M' + ' L'.join(f'{px(f):.1f},{py(v):.1f}' for f, v in zip(fq, inter)), INK2, 2)
g += T(px(124) + 10, py(-232) + 5, 'model trained on inter-ictal', 15, 400, INK2)
g += P('M' + ' L'.join(f'{px(f):.1f},{py(v):.1f}' for f, v in zip(fq, pre)), ACC, 2.5)
g += T(px(124) + 10, py(-35) + 5, 'model trained on pre-ictal', 15, 600, ACC_T)
g += F(1, R(px(76), Y0, px(124) - px(76), H, '#000', 0, 'fill-opacity="0.04"') + T(px(100), py(-110), 'largest gap', 15, 400, INK2, 'middle') + T(px(100), py(-110) + 20, 'above 76 Hz', 15, 400, INK2, 'middle'))
slide('Trained on each phase alone, the two models learn different spectra', SVG(g), mark='Results', status='pub',
      ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Fig. 3 (CHB-MIT, curves redrawn from the figure)',
      notes='The interpretability result. We trained one KSNet only on pre-ictal segments and another only on inter-ictal segments, six folds each, and pooled the eigenvalues. Each curve is the mean decay rate per 8 Hz bin of mode frequency. The curves are redrawn from Figure 3, values read from the figure. Click: on CHB-MIT the two phases separate above about 76 Hz, inter-ictal modes there fade much faster. On SIENA the gaps sit below 28 Hz and around 76 to 92 Hz. So the latent dynamics differ by phase. That was the end of the paper.')

# 7. the turn
g = ''
g += T(60, 30, 'Same labels, same random split. One model sees EEG, one sees only the clock.', 18, 400, INK2)
rows = [('time of day + position in file, no EEG', 0.981, ACC, True), ('KSNet as published (its own sample)', 0.87, SLATE, False),
        ('Koopman clip summary, EEG', 0.836, AXIS, False), ('band power, EEG', 0.787, AXIS, False)]
for k, (lab, v, col, b) in enumerate(rows):
    inner = hbar(60, 62 + k * 46, lab, v, 0.4, 1.0, 420, col, b, lw=420)
    g += F(1, inner) if k == 0 else inner
g += axis_ticks(480, 62 + 4 * 46 + 4, 420, 0.4, 1.0, [0.4, 0.6, 0.8, 1.0], label='AUC on CHB-MIT, random split')
g += F(2, T(60, 352, 'SIENA: the clock alone gets 0.883. Leave one patient out, KSNet gets 0.48 and 0.57.', 18, 400, INK))
g += F(3, keybox(60, 400, 1060, f'A random split rewards knowing {kw("when")} a segment was recorded, not knowing the {kw("brain")}'))
slide('Then we asked a rude question: what if the model never sees the EEG?', SVG(g), mark='After the paper',
      ref='Our follow up, all 10 s clips every 30 s, 17 CHB-MIT and 12 SIENA patients, details in backup',
      notes='After acceptance we asked what a model can get without any EEG. The three gray and slate bars use EEG. Click: the orange bar uses two numbers per segment, the time of day and the position inside the recording file. Under a random split it reaches 0.98 on CHB-MIT, higher than every EEG model, including our own published 0.87. To be fair, KSNet used its own sample of 100 segments per patient, our rerun uses every clip. Click: SIENA is the same story, 0.88 for the clock. And our own paper already had the hint: leave one patient out, KSNet drops to 0.48 and 0.57. Click: the lesson.')

# 8. why: neighbors in time
g = ''
g += T(60, 30, 'Pre-ictal segments sit next to each other in time', 18, 400, INK2)
yy = 70
for k in range(30):
    x = 60 + k * 34
    pre_ = 18 <= k <= 23
    col = TINT if pre_ else GROUP
    g += R(x, yy, 30, 30, col, 2)
g += L(60 + 24 * 34 + 2, yy - 10, 60 + 24 * 34 + 2, yy + 40, ACC, 2.5) + T(60 + 24 * 34 + 8, yy - 14, 'seizure', 15, 400, ACC_T)
# random split marks
import random
rnd = random.Random(3)
test = sorted(rnd.sample(range(30), 6))
g += F(1, ''.join(T(60 + k * 34 + 15, yy + 56, 'test', 13.5, 400, INK2, 'middle') for k in test)
       + T(60, yy + 92, 'random split: every test segment has a training neighbor a few seconds away', 17, 400, INK))
# ladder slope chart
X = [180, 480, 780]
labs = ['random split', 'leave one seizure out', 'walk forward in time']
def ly(v): return 420 - (v - 0.4) / 0.6 * 200
for k, x in enumerate(X):
    g += F(2, L(x, 210, x, 420, RULE, 1) + T(x, 445, labs[k], 15.5, 400, INK2, 'middle'))
series = [('no EEG', [0.981, 0.582, 0.564], ACC, 2.5), ('Koopman clips', [0.836, 0.588, 0.536], SLATE, 2), ('band power', [0.787, 0.544, 0.508], AXIS, 2)]
for name, vals, col, sw in series:
    d = 'M' + ' L'.join(f'{x},{ly(v):.1f}' for x, v in zip(X, vals))
    lab_y = ly(vals[-1]) + (-10 if name == 'no EEG' else 6 if name == 'Koopman clips' else 22)
    g += F(2, P(d, col, sw) + ''.join(C(x, round(ly(v), 1), 4.5, col) for x, v in zip(X, vals))
           + T(X[-1] + 14, round(lab_y, 1), f'{name} {vals[-1]:.2f}', 15.5, 600 if name == 'no EEG' else 400, ACC_T if name == 'no EEG' else INK2))
g += F(2, T(X[0] - 16, ly(0.981) + 5, '0.98', 15.5, 400, INK2, 'end') + T(980, 300, 'Every EEG method loses', 16, 400, INK) + T(980, 322, '0.28 to 0.53 AUC', 16, 400, INK))
slide('Labels come in blocks, so a random split lets the model copy its neighbor', SVG(g), mark='After the paper',
      ref='Mormann et al., Brain 2007 | our follow up on CHB-MIT, 8 to 17 patients per level',
      notes='Why does the clock win? Labels are not scattered. All pre-ictal segments of one seizure sit in one block of 30 minutes. Click: a random split puts test segments right next to training segments from the same block. Anything that changes slowly, time, electrode impedance, the recording file, identifies the block. The model does not need the brain. Click: the audit ladder. Make the split stricter step by step. Leave out a whole seizure, then train only on the past. The no EEG model falls from 0.98 to 0.56. Every EEG method falls too, by 0.28 to 0.53. Mormann and colleagues warned about this in 2007. We still fell into it, and so does much of the deep learning literature on these two datasets.')

# 9. the strict protocol and what it caught
g = ''
steps_ = [('Train on the past only', 'refit after each seizure'), ('Seizures 4 h apart', 'warn 5 to 35 min ahead'),
          ('Held out calibration', 'past data never trained on'), ('Fake seizure times', 'onsets moved by whole days')]
for k, (a, b) in enumerate(steps_):
    x = 60 + k * 270
    g += R(x, 30, 250, 84, GROUP) + T(x + 16, 64, a, 18, 600, INK) + T(x + 16, 92, b, 14.5, 400, INK2)
g += T(60, 160, 'What it caught, all from methods that looked fine before', 18, 400, INK2)
cards = [('Daily rhythm', 'SWEC, cycle model', '0.556', 'on fake seizures', '0.563'), ('Recording structure', 'SeizeIT2, no EEG', '0.659', 'on fake seizures', '0.666'),
         ('In sample calibration', 'CHB-MIT, our own baseline', '0.667', 'held out calibration', '0.589')]
for k, (a, b, v1, lab2, v2) in enumerate(cards):
    x = 60 + k * 360
    inner = (R(x, 180, 340, 170, GROUP) + T(x + 18, 214, a, 19, 600, INK) + T(x + 18, 240, b, 15, 400, INK2)
             + T(x + 18, 290, v1, 34, 400, INK) + T(x + 18, 316, 'real seizures' if k < 2 else 'as reported', 14.5, 400, INK2)
             + T(x + 180, 290, v2, 34, 400, FAIL if k < 2 else INK) + T(x + 180, 316, lab2, 14.5, 400, INK2))
    g += F(k + 1, inner)
g += F(3, T(60, 395, 'A real signal must beat its own fake seizures. These did not.', 19, 400, INK))
slide('A strict test with fake seizure times caught three shortcuts we had trusted', SVG(g), mark='A stricter test', status='prog',
      ref='Andrzejak et al., Phys. Rev. E 2003 | Burrello et al. 2019 (SWEC) | SeizeIT2, OpenNeuro ds005873',
      notes='So we rebuilt the evaluation. Four rules. Train only on the past. Count only seizures at least 4 hours after the previous one, and warn 5 to 35 minutes ahead. Calibrate scores on held out past data. And the key one, from Andrzejak 2003: move the seizure times by whole days, keeping the clock, and require the method to do worse on those fake times. Click: a cycle model on SWEC intracranial data looked good, 0.556, but it scores 0.563 on fake seizures. It learned the daily rhythm. Click: on SeizeIT2 a model with no EEG reached 0.659, and 0.666 on fake seizures. It learned how sessions were recorded. Click: our own baseline on CHB-MIT dropped from 0.667 to 0.589 once calibration used held out data.')

# 10. honest level
g = ''
cols_ = ['band power', 'CNN', 'foundation model', 'Koopman']
dsets = [('SeizeIT2', '73 patients, behind the ear', [0.613, 0.560, 0.562, 0.621]), ('SWEC', '13 patients, intracranial', [0.523, 0.636, 0.578, 0.533]),
         ('CHB-MIT', '7 patients, scalp', [0.589, 0.483, 0.486, 0.590])]
CX = [520, 690, 860, 1030]
g += R(CX[3] - 70, 22, 140, 306, TINT, 3, 'fill-opacity="0.45"')
for j, c in enumerate(cols_):
    g += T(CX[j], 52, c, 18, 600, INK, 'middle')
g += L(60, 70, 1110, 70, INK, 1.5)
for k, (name, sub, vals) in enumerate(dsets):
    y = 120 + k * 80
    g += T(60, y, name, 20, 600, INK) + T(60, y + 24, sub, 15, 400, INK2)
    best = max(range(4), key=lambda j: vals[j]) if k < 2 else -1
    for j, v in enumerate(vals):
        g += T(CX[j], y + 6, f'{v:.2f}', 24, 600 if j == best else 400, INK if j == best else INK2, 'middle')
    if k < 2:
        g += L(60, y + 44, 1110, y + 44, RULE, 1)
g += L(60, 330, 1110, 330, INK, 1.5)
g += T(60, 360, 'Calibrated AUC, 0.5 is chance. Bold: best per dataset. On CHB-MIT only the CNN passes the fake seizure gate, so no winner.', 16, 400, INK2)
g += F(1, keybox(60, 400, 1060, f'No method wins everywhere, and the {kw("foundation model")} does not rescue it'))
slide('Under the strict test, every method sits between 0.48 and 0.64, deep models included', SVG(g), mark='A stricter test', status='prog',
      ref='Wang et al., CBraMod, ICLR 2025 | our round 11, held out calibration, shared windows and fake seizures',
      notes='This is the honest level. Three datasets, four kinds of model, all under the same strict test. Calibrated AUC, 0.5 is chance. On SeizeIT2, 73 patients with two channels behind the ear, the Koopman feature is best at 0.62. On SWEC intracranial, the CNN is best at 0.64. On CHB-MIT nothing is reliably above chance, and only the CNN passes the fake seizure gate. No method wins everywhere, and the foundation model does not rescue it. Our paper listed comparison with foundation models as future work. Here it is.')

# 11. Koopman as a plug-in
g = ''
g += T(60, 30, 'SeizeIT2, 73 patients. Each system averages three calibrated scores, no fitted weights.', 18, 400, INK2)
rows = [('CNN alone', 0.560, AXIS, False), ('CNN + foundation model + control feature', 0.571, AXIS, False),
        ('CNN + foundation model + band power', 0.587, AXIS, False), ('CNN + foundation model + Koopman', 0.594, ACC, True)]
for k, (lab, v, col, b) in enumerate(rows):
    inner = hbar(60, 70 + k * 50, lab, f'{v:.3f}', 0.45, 0.65, 380, col, b, lw=470, val=v)
    g += F(1, inner) if k == 3 else inner
g += axis_ticks(530, 70 + 4 * 50 + 4, 380, 0.45, 0.65, [0.45, 0.5, 0.55, 0.6, 0.65], label='calibrated AUC')
g += F(2, bignum(1000, 110, '+0.023', 'Koopman over the same', 'feature without Koopman'))
g += F(2, T(1000, 220, '90% CI +0.004 to +0.041', 14.5, 400, INK2) + T(1000, 242, 'Holm p 0.046, preregistered', 14.5, 400, INK2))
g += F(3, keybox(60, 400, 1060, f'Koopman does not need to win alone: it {kw("adds")} to CNN and foundation model'))
slide('Plugged into a CNN and a foundation model, the Koopman feature still adds', SVG(g), mark='Where Koopman helps', status='prog',
      ref='Our round 11, preregistered, development set (these patients were seen in earlier rounds)',
      notes='So where does Koopman help? We stopped asking it to win alone. Each system averages calibrated scores, no weights to fit, so nothing can overfit. The Koopman feature is the leading eigenvalue of a DMD on band power, measured against the same patient two hours earlier. Click: adding it to CNN plus foundation model gives 0.594. Click: the preregistered test compares it with the identical feature built without Koopman, plus 0.023, confidence interval above zero, Holm corrected p 0.046. It also beats the CNN alone by 0.034. Honest caveat: these patients were used in earlier rounds, so this is development evidence. Click.')

# 12. few labels
g = ''
grp = [('only 1 seizure to learn from', 41, [0.571, 0.467, 0.461, 0.519]), ('2 or more seizures', 44, [0.595, 0.557, 0.565, 0.600])]
nm = ['Koopman', 'CNN', 'control feature', 'band power']
for gi, (name, n, vals) in enumerate(grp):
    x = 60 + gi * 560
    inner = T(x, 40, f'{name}, {n} patients', 19, 600, INK)
    for j, v in enumerate(vals):
        inner += hbar(x - 40, 66 + j * 44, nm[j], v, 0.4, 0.65, 240, ACC if j == 0 else AXIS, j == 0, lw=200)
    inner += axis_ticks(x + 160, 66 + 4 * 44 + 4, 240, 0.4, 0.65, [0.4, 0.5, 0.6])
    g += F(1, inner) if gi == 1 else inner
g += F(2, keybox(60, 330, 1060, f'With one seizure to learn from, Koopman leads the CNN by {kw("0.10")}'))
g += F(3, T(60, 420, 'Why it fits: an eigenvalue has no units and needs almost no labels to mean something.', 18, 400, INK2))
slide('The fewer seizures a patient has, the more the Koopman feature helps', SVG(g), mark='Where Koopman helps', status='pre',
      ref='Our analysis of round 11 scores, split after the fact. Confirmation on HUP Phase II (ieeg.org) is being set up',
      notes='The most interesting pattern, and I flag it as exploratory. Split the SeizeIT2 patients by how much the model could learn from. Left: only one seizure before testing, 41 patients. Koopman 0.57, the CNN 0.47, below chance. Click: with two or more seizures the gap closes. Click: one seizure is the common clinical case, a new patient on the unit. Click: why it makes sense. A leading eigenvalue relative to the same patient two hours ago has no units. It needs almost no labels to mean something, while a CNN needs examples. We split this after seeing the data, so it is a hypothesis. We are now testing it on the HUP Phase II intracranial data on ieeg.org, 42 patients with at least two well separated seizures.')

# 13. critical slowing
g = ''
g += T(60, 30, 'If seizures were a tipping point, the leading eigenvalue should creep toward 1 before onset', 18, 400, INK2)
# simple tipping diagram: eigenvalue magnitude vs time to onset, expected vs found
X0, Y0, W, H = 100, 70, 460, 250
g += L(X0, Y0 + H, X0 + W, Y0 + H, AXIS, 1) + L(X0, Y0, X0, Y0 + H, AXIS, 1)
g += T(X0 + W, Y0 + H + 24, 'onset', 14.5, 400, INK2, 'end') + T(X0, Y0 + H + 24, '4 h before', 14.5, 400, INK2)
g += T(X0 - 10, Y0 + 6, 'closer to 1', 14.5, 400, INK2, 'end')
g += F(1, P(f'M{X0},{Y0 + H - 40} C{X0 + 250},{Y0 + H - 45} {X0 + 380},{Y0 + H - 90} {X0 + W - 10},{Y0 + 20}', LINE, 2, extra='stroke-dasharray="6 5"')
       + T(X0 + W - 150, Y0 + 30, 'expected', 15.5, 400, INK2))
g += F(2, P(f'M{X0},{Y0 + H - 40} L{X0 + 120},{Y0 + H - 36} L{X0 + 240},{Y0 + H - 44} L{X0 + 360},{Y0 + H - 38} L{X0 + W - 10},{Y0 + H - 46}', ACC, 2.5)
       + T(X0 + 250, Y0 + H - 60, 'found, SeizeIT2', 15.5, 600, ACC_T))
g += F(2, T(640, 100, '120 patients, scalp', 18, 600, INK) + T(640, 128, 'last 10 min: z = −0.13', 17, 400, INK) + T(640, 154, 'fake seizures: z = −0.10', 17, 400, INK2))
g += F(3, T(640, 220, '13 patients, intracranial', 18, 600, INK) + T(640, 248, 'it does move before onset', 17, 400, INK) + T(640, 274, 'but up in only 31% of patients', 17, 400, INK2))
g += F(3, keybox(60, 400, 1060, f'No common tipping point. Changes are {kw("patient specific")}, and visible only inside the skull'))
slide('The spectrum does not tip toward instability before seizures, at least not for everyone', SVG(g), mark='What the spectrum says',
      ref='Maturana et al., Nat. Commun. 2020 | Wilkat, Rings, Lehnertz, Chaos 2019 | Scheffer et al., Nature 2009',
      notes='Back to the spectrum. A popular idea from tipping points, Scheffer 2009: before a critical transition, the system recovers slowly, critical slowing down, so the leading eigenvalue should creep toward the unit circle. Click: that is the expected curve. Maturana 2020 found signs of it in long intracranial recordings. Click: on 120 scalp patients we see nothing beyond what fake seizure times give, z minus 0.13 against minus 0.10. That agrees with Wilkat, Rings and Lehnertz 2019. Click: inside the skull, SWEC, the eigenvalue does move before onset, but up in only 31 percent of patients, down in the rest. So the debate may have two sides that are both right: changes exist, they are individual. That fits the one seizure result: a feature measured against the patient\'s own recent past.')

# 14. one family
g = ''
fam = [('DMD', 'identity observables', 'fluid dynamics, 2010'), ('Neural fragility', 'windowed DMD on iEEG', 'finds the seizure onset zone, 2021'),
       ('KSNet', 'learned observables', 'seizure prediction, 2026')]
for k, (a, b, c) in enumerate(fam):
    x = 60 + k * 370
    g += R(x, 40, 330, 110, TINT if k == 2 else GROUP) + T(x + 20, 80, a, 22, 600, INK) + T(x + 20, 108, b, 16, 400, INK) + T(x + 20, 132, c, 15, 400, INK2)
    if k < 2:
        g += arrow(x + 334, 95, x + 366, 95)
g += T(60, 190, 'One operator family. We rebuilt neural fragility in the open (its code was not released) and tested richer observables.', 17, 400, INK2)
rows = [('line length, classic baseline', 0.790, 0.714), ('neural fragility, our rebuild', 0.806, 0.719), ('Koopman, delay embedding', 0.809, 0.729)]
g += T(560, 234, 'HUP, 56 patients', 15.5, 600, INK, 'middle') + T(860, 234, 'external, 29 patients', 15.5, 600, INK, 'middle')
for k, (lab, a, b) in enumerate(rows):
    y = 262 + k * 40
    g += T(400, y + 18, lab, 17, 400, INK, 'end')
    g += F(1 if k < 2 else 2, T(560, y + 18, f'{a:.2f}', 18, 600 if k == 2 else 400, INK, 'middle') + T(860, y + 18, f'{b:.2f}', 18, 600 if k == 2 else 400, INK, 'middle'))
g += T(1000, 280, 'electrode level AUC', 14.5, 400, INK2) + T(1000, 300, 'for the onset zone', 14.5, 400, INK2)
g += F(3, keybox(60, 400, 1060, f'Richer observables {kw("tie")} with fragility: the operator matters more than the lift'))
slide('KSNet, neural fragility and DMD are one family, and that helps beyond prediction', SVG(g), mark='What the spectrum says',
      ref='Schmid, J. Fluid Mech. 2010 | Li et al., Nat. Neurosci. 2021 | OpenNeuro ds004100, ds003029',
      notes='One more connection that I find useful. Dynamic mode decomposition from fluid dynamics fits a linear operator with the identity as observables. Neural fragility, Li and colleagues 2021, is windowed DMD on intracranial EEG: how small a change makes a channel unstable. It localizes the seizure onset zone. KSNet is the same operator with learned observables. Fragility code was never released, so we rebuilt it in the open. Click: on HUP, 56 patients, fragility reaches 0.81 for finding onset zone electrodes, line length 0.79. On an external set of 29 patients, 0.72 against 0.71. Click: replacing the identity with a delay embedding, a richer Koopman lift, gives 0.81 and 0.73, a tie within our preregistered margin. Click: the lesson for Koopman methods: the operator does most of the work.')

# 15. close: open territory + QR
import importlib.util
qr_svg = ''
try:
    import segno
    q = segno.make(URL, error='m')
    qr_svg = q.svg_inline(scale=5, dark=INK, light=BG, border=2)
except Exception:
    qr_svg = f'<div style="width:190px;height:190px;border:1px dashed {AXIS}"></div>'
g = ''
cols = [('What this talk covered', ['a learned Koopman model for prediction', 'a test that random splits cannot pass', 'where Koopman helps: as a plug-in, with few labels']),
        ('Open, and where the same idea applies', ['confirm the one seizure result on 42 new patients', 'operators that amplify before they decay, invisible to eigenvalues', 'closed loop devices that read the spectrum online'])]
for k, (h, items) in enumerate(cols):
    x = 60 + k * 420
    g += T(x, 40, h, 20, 600, INK)
    for j, it in enumerate(items):
        g += C(x + 6, 82 + j * 56, 4, ACC if k == 1 else AXIS) + T(x + 22, 88 + j * 56, it if len(it) < 44 else it[:it.rfind(' ', 0, 44)], 17, 400, INK)
        if len(it) >= 44:
            g += T(x + 22, 110 + j * 56, it[it.rfind(' ', 0, 44) + 1:], 17, 400, INK)
g += T(60, 300, 'Talk to us: intracranial cohorts with long recordings, and anyone running seizure forecasting trials.', 18, 400, INK2)
close = f'''<section class="close"><span class="mark">Close</span>
  <h2>Koopman spectra help most where labels are scarce, if the test is honest</h2>
  {SVG(g)}
  <div class="qr">{qr_svg}<div class="qr-cap">Slides: scan, or zhiqian.ai, then Talks</div></div>
  <div class="ref">Trefethen et al., Science 1993 | Liang et al., IEEE JBHI 2023 | Cook et al., Lancet Neurol. 2013</div>
  <aside class="notes">Three things to take home. A learned Koopman model gives a readable spectrum. A random split cannot tell us whether it predicts seizures, and the strict test can. Under that test, Koopman features help as a plug-in and most of all when a patient has few seizures. Open territory on the right. First, the one seizure result needs confirmation, and we have 42 new intracranial patients for it. Second, Trefethen showed in 1993 that a linear operator can amplify a disturbance for a while even when every eigenvalue decays. An eigenvalue only feature cannot see that, and a seizure may start exactly that way. Third, Liang and colleagues already use an online Koopman model for closed loop stimulation. Cook 2013 showed an implanted advisory device can work in people. A spectrum read online is a natural input. If you have long intracranial cohorts, or run forecasting trials, please come and talk. The QR code has these slides.</aside>
</section>'''
SLIDES.append(close)

# ---------------- backups under the relevant main slides ----------------
B_LADDER = bslide('The audit ladder in numbers', SVG(
    T(60, 40, 'Mean AUC, CHB-MIT core patients (n per level 17, 10, 8, 6)', 17, 400, INK2) +
    ''.join(T(60 + j * 210 + (0 if j == 0 else 160), 80, h, 16, 600, INK, 'start' if j == 0 else 'middle') for j, h in enumerate(['method', 'random split', 'leave one seizure out', 'walk forward', 'walk forward, clock matched'])) +
    ''.join(T(60, 116 + i * 36, r[0], 17, 400, INK) + ''.join(T(60 + (j + 1) * 210 + 160, 116 + i * 36, f'{v:.3f}', 17, 400, INK, 'middle') for j, v in enumerate(r[1:]))
            for i, r in enumerate([('time + position, no EEG', 0.981, 0.582, 0.564, 0.547), ('band power median', 0.787, 0.544, 0.508, 0.402), ('all 138 band powers', 0.968, 0.497, 0.435, 0.312),
                                   ('Koopman clip summary', 0.836, 0.588, 0.536, 0.415), ('slow scale Koopman', 0.893, 0.653, 0.600, 0.595)])) +
    T(60, 330, 'SIENA, 12 patients: no EEG 0.883 random, 0.837 with whole files held out (files are cut around seizures).', 17, 400, INK2) +
    T(60, 360, 'Two seizure free files of the same patient separate at 0.72, close to pre vs inter at 0.75.', 17, 400, INK2)),
    ref='Our follow up, run 2026-11-17, preregistered predictions A1 to A3 all held')
B_SPEC = bslide('The paper figure for both datasets', f'<img class="figimg" src="figs/paper/pre_inter_chbmit_new.png" style="left:60px;width:560px"><img class="figimg" src="figs/paper/pre_inter_siena_new.png" style="left:640px;width:560px">',
    ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Fig. 3', status='pub')
B_ARCH = bslide('The full KSNet architecture', '<img class="figimg" src="figs/paper/flow_chart.png" style="left:90px;width:1100px">',
    ref='Chen, Sun, Chen, Lu, KSNet, IEEE BIBM 2026, Fig. 2', status='pub')
B_HUP = bslide('Confirmation set: HUP Phase II on ieeg.org', SVG(
    T(60, 40, '151 patients, about 35,600 hours of intracranial EEG, median 128 channels', 19, 400, INK) +
    T(60, 80, 'Seizures from annotations of type Seizure, end and uncertain marks removed, merged within 5 min', 17, 400, INK2) +
    ''.join(hbar(60, 110 + k * 38, f'{lab} lead seizures', v, 0, 80, 500, ACC if lab in ('2', '3', '4', '5+') else AXIS, False, lw=230) for k, (lab, v) in enumerate([('0', 79), ('1', 30), ('2', 19), ('3', 9), ('4', 8), ('5+', 6)])) +
    T(60, 360, '42 patients with 2 or more lead seizures (4 h apart), 23 with 3 or more. Stimulation sessions are still to be excluded.', 17, 400, INK2)),
    ref='Our scan 2026-11-25, metadata only, prereg amendment pending', status='prog')

# attach backups as vertical stacks
def attach(idx, *bs):
    SLIDES[idx] = '<section>' + SLIDES[idx] + ''.join(bs) + '</section>'
attach(3, B_ARCH)
attach(5, B_SPEC)
attach(7, B_LADDER)
attach(11, B_HUP)

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
.reveal img.figimg{{position:absolute;top:170px;margin:0;border:0;box-shadow:none}}
/* cover */
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
/* close */
.reveal section.close .qr{{position:absolute;right:50px;top:190px;width:230px;text-align:center}}
.reveal section.close .qr svg{{width:210px;height:210px}}
.reveal section.close .qr-cap{{font:400 17px/1.3 {FONT};color:{INK2};margin-top:8px}}
'''

def linkify(ref):
    parts = [p.strip() for p in ref.split('|')]
    out = []
    for p in parts:
        if p.lower().startswith('our'):
            out.append(esc(p))
        else:
            q = re.sub(r'\s+', '+', re.sub(r'[^\w\s.,]', ' ', p))
            out.append(f'<a href="https://scholar.google.com/scholar?q={q}" target="_blank" title="{esc(p)}">{esc(p)}</a>')
    return '<span class="rsep" aria-hidden="true"></span>'.join(out)

body = '\n'.join(SLIDES)
body = re.sub(r'<div class="ref">(.*?)</div>', lambda m: f'<div class="ref">{linkify(m.group(1))}</div>', body)

# ---------------- gates ----------------
visible = re.sub(r'<aside class="notes">.*?</aside>', ' ', body, flags=re.S)
everything = body
for bad, name in (('—', 'em dash'), ('–', 'en dash')):
    assert bad not in everything, f'{name} found'
txt_only = re.sub(r'<[^>]+>', ' ', everything)
txt_only = re.sub(r'&[a-z]+;|&#\d+;', ' ', txt_only)
assert ';' not in txt_only, 'semicolon in visible text or notes: ' + txt_only[max(0, txt_only.find(';') - 60):txt_only.find(';') + 20]
for sec_ in re.findall(r'<section[^>]*>(?:(?!<section).)*?</section>', body, re.S):
    n = len(set(re.findall(r'data-fragment-index="(\d+)"', sec_)))
    assert n <= 4, 'more than 4 fragment steps'

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>KSNet: Koopman Spectra for Seizure Prediction</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/theme/white.min.css">
<style>{CSS}</style></head>
<body><div class="reveal"><div class="slides">
{body}
</div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/reveal.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.1.0/plugin/notes/notes.min.js"></script>
<script>Reveal.initialize({{hash:true,center:false,width:1280,height:720,margin:0.03,transition:'fade',transitionSpeed:'fast',backgroundTransition:'fade',plugins:[RevealNotes]}});</script>
</body></html>
'''
open(os.path.join(DECK, 'index.html'), 'w').write(page)
n_main = len(SLIDES)
print('main slides', n_main, 'bytes', len(page))
