"""Own house style redraws of paper figures that do not read at slide size.
Values marked APPROX are read off the published figure by eye (stated in the slide notes and reference).
Placeholders: {{FIG:dl_gain}} {{FIG:dl_memory}} {{FIG:denk_acc}} {{FIG:nh_schematic}} {{FIG:knob_orders}}
{{FIG:design_strip}} {{FIG:turned}} {{FIG:pernote}}"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
INK, INK2, AXIS, RULE, GROUP, ACC, ACCT, LINE, MUS, MUST, LANG, LANGT = ('#1F1E1B', '#5F5D50', '#ACA39A', '#D7D2CB', '#EFEBE5',
    '#F76902', '#FAD6BA', '#7C878E', '#7D55C7', '#DCD1EB', '#009CBD', '#BCE2E8')
def T(x, y, s, size=20, fill=INK, anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

def hbars(rows, W=640, label_w=250, vmax=1.0, ref=None, ref_label='', fmt='{:.2f}', H_row=64, title=''):
    """rows: (label, value, highlight). Horizontal bars, value at bar end, one orange bar."""
    H = 40 + H_row * len(rows) + (40 if ref is not None else 10)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    if title: s.append(T(0, 22, title, 20, INK2))
    x0, x1 = label_w, W - 70
    sx = lambda v: x0 + v / vmax * (x1 - x0)
    for i, (lab, v, hi) in enumerate(rows):
        y = 40 + i * H_row
        s.append(T(0, y + 30, lab, 24))
        s.append(('<g data-accent="1">' if hi else '<g>') + f'<rect x="{x0}" y="{y+6}" width="{sx(v)-x0:.1f}" height="34" fill="{ACC if hi else AXIS}"/>' + T(sx(v) + 8, y + 30, fmt.format(v), 23, INK) + '</g>')
    if ref is not None:
        yb = 40 + H_row * len(rows)
        s.append(f'<line x1="{sx(ref):.1f}" y1="30" x2="{sx(ref):.1f}" y2="{yb}" stroke="{INK2}" stroke-dasharray="5 5"/>')
        s.append(T(sx(ref), yb + 26, ref_label, 18, INK2, 'middle'))
    s.append('</svg>')
    return ''.join(s)

def dl_gain():
    # Di Liberto 2020 Fig 2A, mean prediction correlation over 20 listeners, APPROX
    return hbars([('sound only', 0.073, False), ('sound plus surprise', 0.078, True)], W=700, vmax=0.09,
                 fmt='{:.3f}', title='EEG prediction correlation, mean of 20 listeners', H_row=150)

def dl_memory():
    # Di Liberto 2020 Fig 2C, median gain (AM minus A) by IDyOM short term memory length in bars, APPROX
    xs = ['1', '2', '4', '8', '16', '32', 'all']
    ys = [0.0012, 0.0012, 0.0025, 0.0037, 0.0040, 0.0058, 0.0049]
    W, H, L, B = 700, 440, 90, 70
    sx = lambda i: L + 30 + i * (W - L - 60) / (len(xs) - 1)
    sy = lambda v: 30 + (0.0065 - v) / 0.0065 * (H - B - 30)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{W-20}" y2="{sy(0):.1f}" stroke="{AXIS}"/>')
    s.append('<polyline fill="none" stroke="%s" stroke-width="1.5" points="%s"/>' % (LINE, ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i, v in enumerate(ys))))
    for i, (x, v) in enumerate(zip(xs, ys)):
        s.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="8" fill="{MUS}"/>')
        s.append(T(sx(i), H - B + 28, x, 19, INK2, 'middle'))
    s.append(T((L + W) / 2, H - 12, 'bars of the piece the listener model may remember', 20, INK2, 'middle'))
    s.append(T(L - 12, sy(0) + 6, '0', 17, INK2, 'end'))
    s.append(T(L - 12, sy(0.005) + 6, '0.005', 17, INK2, 'end'))
    s.append(T(0, 20, 'EEG gain from surprise (median)', 20, INK2))
    s.append('</svg>')
    return ''.join(s)

def denk_acc():
    # Denk, Takagi et al. 2025 Fig 1a, identification accuracy of generated clips (MusicLM), medians over 5 scanned listeners,
    # with the oracle ceiling of each space as a gray tick, APPROX
    rows = [('judged in the music embedding (MuLan)', 0.85, 1.0, True), ('judged in a low level audio space', 0.66, 0.79, False)]
    W, L = 1100, 470; x0, x1 = L, W - 90
    sx = lambda v: x0 + (v - 0.4) / 0.6 * (x1 - x0)
    H = 300
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(T(0, 22, 'how often the generated clip is closer to the heard clip than to another clip', 20, INK2))
    for i, (lab, v, ceil, hi) in enumerate(rows):
        y = 60 + i * 100
        s.append(T(0, y + 30, lab, 24))
        s.append(('<g data-accent="1">' if hi else '<g>') + f'<rect x="{x0}" y="{y+6}" width="{sx(v)-x0:.1f}" height="34" fill="{ACC if hi else AXIS}"/>' + T(sx(v) + 10, y + 30, f'{v:.0%}', 23) + '</g>')
        s.append(f'<line x1="{sx(ceil):.1f}" y1="{y-2}" x2="{sx(ceil):.1f}" y2="{y+48}" stroke="{INK2}" stroke-width="2"/>')
        s.append(T(sx(ceil), y + 72, f'best possible {ceil:.0%}', 18, INK2, 'middle'))
    s.append(f'<line x1="{sx(0.5):.1f}" y1="44" x2="{sx(0.5):.1f}" y2="{H-20}" stroke="{INK2}" stroke-dasharray="5 5"/>')
    s.append(T(sx(0.5), H - 2, 'chance 50%', 18, INK2, 'middle'))
    s.append('</svg>')
    return ''.join(s)

def nh_schematic():
    # Norman-Haignere et al. 2022 Fig 2A as a schematic: which sound categories drive three components
    cats = ['speech', 'instrumental music', 'music with singing', 'other sounds']
    comps = [('speech selective', [1.0, 0.1, 0.45, 0.1]), ('music selective', [0.1, 0.9, 0.8, 0.15]), ('song selective', [0.15, 0.2, 1.0, 0.05])]
    W, H = 900, 300
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    for j, c in enumerate(cats):
        s.append(T(0, 70 + j * 52, c, 23))
    for k, (name, vals) in enumerate(comps):
        x0 = 230 + k * 220
        s.append(T(x0, 30, name, 21, INK if k == 2 else INK2, 'start', 'font-weight="600"' if k == 2 else ''))
        for j, v in enumerate(vals):
            s.append((('<g data-accent="1">') if (k == 2 and j == 2) else '<g>') + f'<rect x="{x0}" y="{50 + j*52}" width="{v*180:.0f}" height="28" fill="{ACC if (k == 2 and j == 2) else (MUS if j in (1, 2) else AXIS)}"/></g>')
    s.append(T(0, H - 12, 'schematic of the component responses, 165 natural sounds', 19, INK2))
    s.append('</svg>')
    return ''.join(s)

FE = json.load(open(os.path.join(HERE, 'fe_surprise.json')))
SEMI = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
def _midi(n): return SEMI[n[:-1]] + 12 * (int(n[-1]) + 1)
def _dots(mel, x, y, w, h, n=16, col=MUS):
    mel = mel[:n]; lo, hi = 57, 76
    out = []
    for i, m in enumerate(mel):
        out.append(f'<circle cx="{x + i * w / (n - 1):.1f}" cy="{y + (hi - _midi(m)) * h / (hi - lo):.1f}" r="3.2" fill="{col}"/>')
    return ''.join(out)

def chain_sample(order, n=35, seed=29):
    import random
    mel = FE['melody']; rng = random.Random(seed)
    table = {}
    for i in range(len(mel) - order):
        table.setdefault(tuple(mel[i:i + order]), []).append(mel[i + order])
    out = mel[:order]
    while len(out) < n:
        nxt = table.get(tuple(out[-order:]))
        if not nxt: out += mel[:order]; continue
        out.append(rng.choice(nxt))
    return out[:n]

def knob_orders():
    conds = [('order 0', FE['shuffled']), ('order 1', FE['order1']), ('order 4', chain_sample(4)), ('the real piece', FE['melody'])]
    pred = [0.15, 0.5, 0.8, 0.88]
    W, H, L = 1000, 440, 140
    sx = lambda i: L + 90 + i * 210
    sy = lambda v: 50 + (1 - v) * 220
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<line x1="{L}" y1="{sy(0)}" x2="{W-40}" y2="{sy(0)}" stroke="{AXIS}"/><line x1="{L}" y1="{sy(0)}" x2="{L}" y2="40" stroke="{AXIS}"/>')
    s.append(T(L - 12, 60, 'how strongly', 18, INK2, 'end')); s.append(T(L - 12, 82, 'EEG tracks', 18, INK2, 'end')); s.append(T(L - 12, 104, 'surprise', 18, INK2, 'end'))
    s.append(T(L + 16, 46, 'PREDICTION, NO DATA YET', 17, INK2, 'start', 'letter-spacing="2"'))
    g = '<g data-accent="1">' + f'<path d="M{sx(0)},{sy(pred[0])} ' + ' '.join(f'L{sx(i)},{sy(v)}' for i, v in enumerate(pred)) + f'" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="7 6"/>'
    for i, v in enumerate(pred):
        g += f'<circle cx="{sx(i)}" cy="{sy(v)}" r="8" fill="#FBFAF7" stroke="{ACC}" stroke-width="2"/>'
    s.append(g + '</g>')
    for i, (lab, mel) in enumerate(conds):
        s.append(T(sx(i), sy(0) + 32, lab, 22, INK, 'middle'))
        s.append(_dots(mel, sx(i) - 80, sy(0) + 52, 160, 70))
    s.append('</svg>')
    return ''.join(s)

def design_strip():
    W, H = 1150, 316
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    conds = [('order 0', FE['shuffled']), ('order 1', FE['order1']), ('order 4', chain_sample(4)), ('real, unfamiliar', None)]
    s.append(T(0, 24, 'Stimuli: chains trained on a melody corpus, 20 s each, same timbre, settings logged', 20, INK2))
    for i, (lab, mel) in enumerate(conds):
        x = i * 200
        s.append(f'<rect x="{x}" y="38" width="185" height="100" rx="3" fill="{MUST if mel is None else GROUP}"/>')
        s.append(T(x + 12, 64, lab, 21))
        if mel: s.append(_dots(mel, x + 16, 78, 150, 46))
        else: s.append(T(x + 12, 104, 'held out melodies,', 18, INK2)); s.append(T(x + 12, 126, 'familiarity rated', 18, INK2))
    s.append(f'<path d="M810,88 L860,88" stroke="{LINE}" stroke-width="1.5"/><path d="M860,82 L870,88 L860,94 z" fill="{LINE}"/>')
    s.append(f'<rect x="880" y="38" width="270" height="100" rx="3" fill="{GROUP}"/>')
    s.append(T(895, 66, '24 young, 24 older', 21)); s.append(T(895, 94, 'hearing screened', 19, INK2)); s.append(T(895, 120, '64 channel EEG, 40 min', 19, INK2))
    s.append(T(0, 186, 'Outcome', 19, INK2))
    s.append(T(0, 216, 'surprise gain in a TRF over envelope, onsets and interval size', 23))
    s.append(T(0, 260, 'Test and decision rule, set before recording', 19, INK2))
    s.append('<g data-accent="1">' + f'<text x="0" y="292" font-size="23" fill="{INK}">a linear trend across order 0, 1, 4 in both groups</text>' + f'<line x1="0" y1="302" x2="520" y2="302" stroke="{ACC}" stroke-width="3"/></g>')
    s.append('</svg>')
    return ''.join(s)

def turned():
    W_, H_ = 1150, 400
    rows = [('Koelsch 2000', 'the last chord of a cadence', 'EEG: an early negativity (ERAN)'),
            ('Quiroga-Martinez 2019', 'how uncertain a melody is', 'EEG: a smaller mismatch response'),
            ('Rhythmic stimulation', 'the tempo of a beat', 'gait: faster walking after stroke'),
            ('Generators', 'chosen properties, whole pieces', 'the next step')]
    W, H = 1150, 400
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(T(0, 24, 'study', 20, INK2)); s.append(T(330, 24, 'the stimulus knob', 20, INK2)); s.append(T(720, 24, 'what moved', 20, INK2))
    for i, (a, b, c) in enumerate(rows):
        y = 50 + i * 86
        last = i == 3
        s.append(f'<rect x="0" y="{y}" width="1150" height="70" rx="3" fill="{ACCT if last else GROUP}"/>')
        s.append(T(16, y + 44, a, 26))
        s.append(T(330, y + 44, b, 24, INK if last else INK2))
        s.append(T(720, y + 44, c, 24, INK if last else INK2))
    s.append('</svg>')
    return ''.join(s)

def pernote():
    d = json.load(open(os.path.join(HERE, 'eeg_pernote.json')))
    return d

def mischler_curves():
    # Mischler et al. 2025 Fig 3a, normalized iEEG prediction correlation by layer, two of three clusters, APPROX
    early = [0.42, 0.63, 0.69, 0.73, 0.57, 0.50, 0.37, 0.28, 0.25, 0.26, 0.32, 0.27, 0.37]
    late = [0.08, 0.23, 0.20, 0.23, 0.32, 0.45, 0.66, 0.69, 0.81, 0.86, 0.91, 0.88, 0.87]
    mid = [0.02, 0.23, 0.57, 0.63, 0.66, 0.75, 0.75, 0.79, 0.84, 0.86, 0.92, 0.89, 0.87]
    W, H, L, B = 560, 420, 70, 60
    sx = lambda i: L + i * (W - L - 130) / 12
    sy = lambda v: 34 + (1 - v) * (H - B - 40)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<line x1="{L}" y1="{sy(0)}" x2="{W-120}" y2="{sy(0)}" stroke="{AXIS}"/>')
    for v in (0, 0.5, 1): s.append(T(L - 10, sy(v) + 6, f'{v:g}', 18, INK2, 'end'))
    for i in (0, 4, 8, 12): s.append(T(sx(i), sy(0) + 26, str(i), 18, INK2, 'middle'))
    s.append(T((L + W - 120) / 2, H - 10, 'model layer', 20, INK2, 'middle'))
    s.append('<polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/>' % (LANG, ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i, v in enumerate(early))))
    s.append('<polyline fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="6 5" points="%s"/>' % (AXIS, ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i, v in enumerate(mid))))
    s.append('<polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/>' % (MUS, ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i, v in enumerate(late))))
    s.append(T(sx(12) + 8, sy(late[-1]) + 6, 'far sites', 20, INK)); s.append(T(sx(12) + 8, sy(early[-1]) + 6, 'early sites', 20, INK2)); s.append(T(W - 10, 14, 'redrawn, approximate', 16, INK2, 'end'))
    s.append(T(L + 10, 14, 'fit, normalized', 18, INK2))
    s.append('</svg>')
    return ''.join(s)

def pepino_subset():
    # Pepino et al. 2025 Fig 6, NH2015 voxel regression R2 vs downstream score, labeled models only, APPROX
    pts = [('DCASE2020', -2.9, 0.083), ('MetricGAN', -2.0, 0.123), ('DeepSpeech', -1.3, 0.192), ('ZeroSpeech', -0.85, 0.178),
           ('SepFormer', -1.05, 0.25), ('Wav2Vec2', -0.5, 0.278), ('VGGish', -0.45, 0.363), ('SpectroTemporal', -0.05, 0.235), ('best models', 0.7, 0.39)]
    W, H, L, B = 640, 420, 80, 60
    sx = lambda v: L + (v + 3.2) / 4.2 * (W - L - 20)
    sy = lambda v: 20 + (0.42 - v) / 0.36 * (H - B - 20)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<line x1="{L}" y1="{sy(0.06)}" x2="{W-10}" y2="{sy(0.06)}" stroke="{AXIS}"/><line x1="{L}" y1="{sy(0.06)}" x2="{L}" y2="20" stroke="{AXIS}"/>')
    s.append('<g data-accent="1">' + f'<line x1="{sx(-2.9)}" y1="{sy(0.083)}" x2="{sx(0.85)}" y2="{sy(0.40)}" stroke="{ACC}" stroke-width="2.5"/></g>')
    for n, x, y in pts:
        s.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="{9 if n == "best models" else 6}" fill="{LINE if n != "best models" else INK2}"/>')
    for n in ('DCASE2020', 'DeepSpeech', 'VGGish', 'best models'):
        x, y = [(a, b) for m, a, b in pts if m == n][0]
        s.append(T(sx(x) + (12 if n != 'best models' else -12), sy(y) - 10, n, 19, INK, 'start' if n != 'best models' else 'end'))
    s.append(T((L + W) / 2, H - 12, 'better at audio tasks', 20, INK2, 'middle'))
    s.append(T(L + 8, 28, 'fit to auditory cortex', 20, INK2))
    s.append('</svg>')
    return ''.join(s)

def order_accuracy():
    # his own result (accuracy_by_order.png, pitch class panel), APPROX, in preparation
    xs = ['0', '1', '2', '3', 'variable']
    lik = [27, 62, 72, 72, 73]; lr = [None, 70, 78, None, None]
    W, H, L, B = 620, 420, 80, 60
    sx = lambda i: L + 40 + i * (W - L - 100) / 4
    sy = lambda v: 20 + (90 - v) / 75 * (H - B - 20)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<line x1="{L}" y1="{sy(15)}" x2="{W-10}" y2="{sy(15)}" stroke="{AXIS}"/>')
    s.append(f'<line x1="{L}" y1="{sy(21)}" x2="{W-10}" y2="{sy(21)}" stroke="{AXIS}" stroke-dasharray="4 5"/>')
    s.append(T(W - 12, sy(21) - 8, 'majority class 21%', 18, INK2, 'end'))
    for v in (20, 50, 80): s.append(T(L - 10, sy(v) + 6, f'{v}%', 18, INK2, 'end'))
    s.append('<polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/>' % (MUS, ' '.join(f'{sx(i):.1f},{sy(v):.1f}' for i, v in enumerate(lik))))
    for i, v in enumerate(lik): s.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="7" fill="{MUS}"/>')
    s.append('<g data-accent="1">' + f'<circle cx="{sx(1):.1f}" cy="{sy(70):.1f}" r="8" fill="{ACC}"/>' + T(sx(1) - 14, sy(70) - 14, '70.2%', 22, INK, 'end') + '</g>')
    for i, x in enumerate(xs): s.append(T(sx(i), sy(15) + 28, x, 19, INK2, 'middle'))
    s.append(T((L + W) / 2, H - 10, 'Markov order (notes remembered)', 20, INK2, 'middle'))
    s.append(T(sx(4), sy(73) - 14, 'likelihood', 19, INK2, 'middle'))
    s.append('</svg>')
    return ''.join(s)

def null_hist():
    d = pernote(); null = d['null_r']
    W, H, L, B = 1000, 300, 40, 60
    lo, hi = -0.35, 0.35; nb = 35
    cnt = [0] * nb
    for v in null:
        k = min(nb - 1, max(0, int((v - lo) / (hi - lo) * nb))); cnt[k] += 1
    mx = max(cnt)
    sx = lambda v: L + (v - lo) / (hi - lo) * (W - 2 * L)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    for k, c in enumerate(cnt):
        x = sx(lo + k * (hi - lo) / nb); w = (W - 2 * L) / nb - 2; h = c / mx * (H - B - 40)
        s.append(f'<rect x="{x:.1f}" y="{H-B-h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{GROUP}"/>')
    s.append(f'<line x1="{L}" y1="{H-B}" x2="{W-L}" y2="{H-B}" stroke="{AXIS}"/>')
    for v in (-0.3, 0, 0.3): s.append(T(sx(v), H - B + 26, f'{v:g}', 18, INK2, 'middle'))
    s.append(T(W / 2, H - 6, 'r when surprise and response are shuffled, 2000 times', 19, INK2, 'middle'))
    r1, r2 = d['r_musicgen'], d['r_random_model']
    s.append(f'<line x1="{sx(r2):.1f}" y1="30" x2="{sx(r2):.1f}" y2="{H-B}" stroke="{LINE}" stroke-width="2.5" stroke-dasharray="6 5"/>')
    s.append(T(sx(r2) + 8, 46, f'untrained model {r2}', 20, INK2))
    s.append('<g data-accent="1">' + f'<line x1="{sx(r1):.1f}" y1="14" x2="{sx(r1):.1f}" y2="{H-B}" stroke="{ACC}" stroke-width="2.5"/>' + T(sx(r1) - 8, 28, f'MusicGen {r1}', 20, INK, 'end') + '</g>')
    s.append('</svg>')
    return ''.join(s)

def kern_context(brain_only=False):
    # Kern et al. 2022 Fig 3C, Music Transformer context length: MEG fit gain and next note accuracy, APPROX
    xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 100, 150, 200, 250, 300, 400]
    meg = [1.35, 2.7, 2.9, 3.2, 3.3, 3.4, 3.5, 3.6, 3.55, 3.5, 3.1, 3.0, 2.9, 2.7, 2.5, 2.1, 2.1, 2.1]
    acc = [10, 18, 21, 24, 26, 27, 28, 29, 28, 30, 33, 43, 43, 42, 44, 53, 54, 54]
    W = 1000; L = 150; PH = 150 if not brain_only else 260
    H = (PH + 70) * (1 if brain_only else 2) + 40
    GAP = 40
    px = lambda i: L + i * (W - L - 40 - GAP) / (len(xs) - 1) + (GAP if i >= 10 else 0)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    def panel(y0, vals, lo, hi, title, col, peak):
        sy = lambda v: y0 + (hi - v) / (hi - lo) * PH
        out = [T(0, y0 + 20, title[0], 21, INK), T(0, y0 + 44, title[1], 18, INK2)]
        bx = (px(9) + px(10)) / 2
        out.append(f'<line x1="{L}" y1="{y0+PH}" x2="{bx-8}" y2="{y0+PH}" stroke="{AXIS}"/><line x1="{bx+8}" y1="{y0+PH}" x2="{W-40}" y2="{y0+PH}" stroke="{AXIS}"/>')
        out.append(f'<path d="M{bx-12},{y0+PH+6} L{bx-4},{y0+PH-6} M{bx+4},{y0+PH+6} L{bx+12},{y0+PH-6}" stroke="{INK2}" stroke-width="1.5"/>')
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/>' % (col, ' '.join(f'{px(i):.1f},{sy(v):.1f}' for i, v in enumerate(vals[:10]))))
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/>' % (col, ' '.join(f'{px(i):.1f},{sy(v):.1f}' for i, v in enumerate(vals) if i >= 10)))
        out.append(f'<line x1="{px(9):.1f}" y1="{sy(vals[9]):.1f}" x2="{px(10):.1f}" y2="{sy(vals[10]):.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        if peak:
            k = vals.index(max(vals))
            out.append('<g data-accent="1">' + f'<circle cx="{px(k):.1f}" cy="{sy(vals[k]):.1f}" r="8" fill="{ACC}"/>' + T(px(k) + 12, sy(vals[k]) - 10, 'peak at 8 notes', 20, INK) + '</g>')
        return out
    s += panel(30, meg, 1.0, 3.8, ('fit to the brain', 'MEG, gain from surprise'), MUS, True)
    if not brain_only:
        s += panel(30 + PH + 70, acc, 5, 58, ('model at music', 'next note accuracy'), LINE, False)
    yb = H - 14
    for i, x in enumerate(xs):
        if x in (1, 5, 10, 25, 100, 400): s.append(T(px(i), yb - 14, str(x), 18, INK2, 'middle'))
    s.append(T((L + W) / 2, yb + 10, 'notes of context the model may use', 19, INK2, 'middle'))
    s.append('</svg>')
    return ''.join(s)

def downgrade():
    rows = [('risk of bias', 'no blinding, open allocation'), ('imprecision', 'small samples'), ('inconsistency', 'different controls and outcomes'), ('and the music is rarely described', 'which piece, how loud, how long')]
    W, H = 1100, 360
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(T(0, 22, 'GRADE reasons for lower certainty (rows 1 to 3) and a reporting gap reviews name (row 4)', 20, INK2))
    for i, (a, b) in enumerate(rows):
        y = 44 + i * 76; last = i == 3
        s.append(f'<rect x="0" y="{y}" width="{W}" height="62" rx="3" fill="{GROUP}"/>')
        s.append(T(20, y + 40, a, 26)); s.append(T(560, y + 40, b, 22, INK2))
        if last: s.append('<g data-accent="1">' + f'<rect x="0" y="{y}" width="6" height="62" fill="{ACC}"/>' + '</g>' + T(W - 20, y + 40, 'the one a lab can fix', 22, INK, 'end'))
    s.append('</svg>')
    return ''.join(s)

def closed_loop():
    W, H = 1150, 430
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    box = lambda x, y, w, h, t, sub, fill: [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>', T(x + 20, y + 44, t, 28), T(x + 20, y + 76, sub, 19, INK2)]
    s += box(0, 40, 300, 110, 'Generator', 'sets predictability, style, tempo', MUST)
    s += box(425, 40, 300, 110, 'Listener', 'hears this piece, now', GROUP)
    s += box(850, 40, 300, 110, 'EEG', 'surprise response, 0.1 to 0.35 s', GROUP)
    s += box(425, 270, 300, 110, 'Model of the brain', 'which setting to try next', GROUP)
    def arr(d, col=LINE, w=1.5):
        nums = [float(v) for v in __import__('re').findall(r'-?\d+\.?\d*', d)]
        import math
        x1, y1, x0, y0 = nums[-2], nums[-1], nums[-4], nums[-3]
        a = math.atan2(y1 - y0, x1 - x0); bx, by = x1 - 13 * math.cos(a), y1 - 13 * math.sin(a); px, py = -math.sin(a) * 6, math.cos(a) * 6
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"/><path d="M{x1:.1f},{y1:.1f} L{bx+px:.1f},{by+py:.1f} L{bx-px:.1f},{by-py:.1f} z" fill="{col}"/>'
    s.append(arr('M305,95 L420,95')); s.append(arr('M730,95 L845,95'))
    s.append(arr('M1000,155 C1000,300 900,325 730,325'))
    s.append('<g data-accent="1">' + arr('M420,325 C200,325 150,290 150,155', ACC, 2.5) + '</g>')
    s.append(T(190, 372, 'the next bar adapts', 22, INK))
    s.append('</svg>')
    return ''.join(s)

def prescription():
    W, H = 760, 400
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="6" fill="#FFFFFF" stroke="{AXIS}"/>')
    s.append(T(30, 56, 'Rx', 44, INK, 'start', 'font-style="italic"'))
    s.append(T(110, 52, 'Music dose, week 3', 26)); s.append(T(110, 80, 'example: a listener, 81, moderate dementia', 19, INK2))
    s.append(f'<line x1="30" y1="104" x2="{W-30}" y2="104" stroke="{RULE}"/>')
    rows = [('length', '20 min, after lunch'), ('predictability', 'order 2, familiar contour'), ('tempo', '72 bpm, steady beat'), ('timbre', 'piano and voice'), ('adjust', 'by her response, weekly')]
    for i, (a, b) in enumerate(rows):
        y = 146 + i * 46
        s.append(T(30, y, a, 22, INK2)); s.append(T(260, y, b, 24))
    s.append('<g data-accent="1">' + f'<line x1="260" y1="{146 + 4*46 + 10}" x2="560" y2="{146 + 4*46 + 10}" stroke="{ACC}" stroke-width="3"/></g>')
    s.append('</svg>')
    return ''.join(s)

def mg_dial():
    E = json.load(open(os.path.join(HERE, 'mg_env.json')))
    rows = [('slow', '60 bpm asked', 59), ('medium', '100 bpm asked', 100), ('fast', '160 bpm asked', 158)]
    W, H, L = 1150, 360, 260
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    for i, (k, lab, bpm) in enumerate(rows):
        y = 20 + i * 110; e = E[k]; n = len(e)
        pts = ' '.join(f'{L + j * (W - L - 10) / (n - 1):.1f},{y + 80 - v * 70:.1f}' for j, v in enumerate(e))
        col = ACC if k == 'fast' else MUS
        g = '<g data-accent="1">' if k == 'fast' else '<g>'
        s.append(g + f'<polyline fill="none" stroke="{col}" stroke-width="1.6" points="{pts}"/></g>')
        s.append(T(0, y + 44, lab, 23)); s.append(T(0, y + 72, f'measured {bpm} bpm', 19, INK2))
    s.append(T(L, H - 4, 'loudness over 8 seconds', 18, INK2))
    s.append('</svg>')
    return ''.join(s)

def eran():
    import math
    W, H, L = 620, 330, 70
    sx = lambda ms: L + ms / 600 * (W - L - 20)
    sy = lambda v: 150 - v * 90
    reg = [(t, 0.3 * math.exp(-((t - 100) / 40) ** 2) - 0.35 * math.exp(-((t - 300) / 80) ** 2)) for t in range(0, 601, 10)]
    odd = [(t, v - 1.0 * math.exp(-((t - 180) / 45) ** 2)) for t, v in reg]
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<rect x="{sx(130):.1f}" y="30" width="{sx(230)-sx(130):.1f}" height="230" fill="{GROUP}"/>')
    s.append(f'<line x1="{L}" y1="{sy(0)}" x2="{W-20}" y2="{sy(0)}" stroke="{AXIS}"/>')
    s.append('<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>' % (LINE, ' '.join(f'{sx(t):.1f},{sy(v):.1f}' for t, v in reg)))
    s.append('<g data-accent="1"><polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/></g>' % (ACC, ' '.join(f'{sx(t):.1f},{sy(v):.1f}' for t, v in odd)))
    s.append(T(sx(185), 50, 'ERAN', 22, INK, 'middle'))
    s.append(T(sx(420), sy(-0.1) - 12, 'regular chord', 19, INK2)); s.append(T(sx(240), sy(-0.95) + 8, 'odd chord', 19, INK))
    for ms in (0, 200, 400, 600): s.append(T(sx(ms), 290, str(ms), 18, INK2, 'middle'))
    s.append(T((L + W) / 2, 318, 'ms after the last chord, right frontal', 18, INK2, 'middle'))
    s.append(T(L - 10, sy(-1) + 5, 'neg', 16, INK2, 'end'))
    s.append(T(W - 20, 18, 'schematic, not data', 16, INK2, 'end'))
    s.append('</svg>')
    return ''.join(s)

def turned_small():
    rows = [('Koelsch 2000', 'last chord of a cadence', 'ERAN in EEG'),
            ('Quiroga-Martinez 2019', 'melody uncertainty', 'smaller mismatch response'),
            ('Rhythmic stimulation', 'tempo of a beat', 'faster walking after stroke'),
            ('Generators', 'chosen properties, whole pieces', 'the next step')]
    W, H = 1150, 230
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(T(0, 20, 'study', 18, INK2)); s.append(T(330, 20, 'the stimulus knob', 18, INK2)); s.append(T(760, 20, 'what moved in the brain', 18, INK2))
    for i, (a, b, c) in enumerate(rows):
        y = 32 + i * 48; last = i == 3
        s.append(f'<rect x="0" y="{y}" width="{W}" height="42" rx="3" fill="{ACCT if last else GROUP}"/>')
        s.append(T(14, y + 28, a, 21)); s.append(T(330, y + 28, b, 20, INK if last else INK2)); s.append(T(760, y + 28, c, 20, INK if last else INK2))
    s.append('</svg>')
    return ''.join(s)

def noz():
    W, H, L = 700, 420, 160
    sx = lambda f: L + f / 3.0 * (W - L - 20)
    rows = [('beat only', [2.4], None), ('imagine a march', [2.4, 1.2], 1.2), ('imagine a waltz', [2.4, 0.8, 1.6], 0.8)]
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    for i, (lab, peaks, new) in enumerate(rows):
        y0 = 40 + i * 120
        s.append(T(0, y0 + 60, lab, 22))
        s.append(f'<line x1="{L}" y1="{y0+80}" x2="{W-20}" y2="{y0+80}" stroke="{AXIS}"/>')
        for f in peaks:
            hi = (f == new)
            col = ACC if (hi and i == 1) else (MUS if hi else LINE)
            g = '<g data-accent="1">' if (hi and i == 1) else '<g>'
            s.append(g + f'<line x1="{sx(f):.1f}" y1="{y0+80}" x2="{sx(f):.1f}" y2="{y0+10}" stroke="{col}" stroke-width="4"/>' + T(sx(f), y0 + 4, f'{f} Hz', 17, INK if hi else INK2, 'middle') + '</g>')
            if f == 1.6 and i == 2: s.append(f'<line x1="{sx(f):.1f}" y1="{y0+80}" x2="{sx(f):.1f}" y2="{y0+30}" stroke="{MUS}" stroke-width="4"/>')
    s.append(T((L + W) / 2, H - 4, 'EEG frequency, schematic of the paper\'s finding', 18, INK2, 'middle'))
    s.append('</svg>')
    return ''.join(s)

def dial():
    import math
    W, H = 560, 380; cx, cy, r = 280, 300, 220
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    s.append(f'<path d="M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r},{cy}" fill="none" stroke="{AXIS}" stroke-width="10"/>')
    labs = [('order 0', 160), ('order 1', 90), ('Beethoven', 20)]
    for lab, deg in labs:
        a = math.radians(deg); x, y = cx + (r + 34) * math.cos(a), cy - (r + 34) * math.sin(a)
        s.append(T(x, y, lab, 22, INK, 'middle'))
    g = ['<g data-accent="1">']
    for k, (lab, deg) in enumerate(labs):
        a = math.radians(deg); x, y = cx + (r - 30) * math.cos(a), cy - (r - 30) * math.sin(a)
        cls = 'fragment fade-in-then-out' if k < 2 else 'fragment'
        g.append(f'<g class="{cls}" data-fragment-index="{k+1}"><line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{ACC}" stroke-width="5"/><circle cx="{cx}" cy="{cy}" r="12" fill="{ACC}"/></g>')
    g.append('</g>')
    s += g
    s.append(T(cx, cy + 50, 'staged mock up: the dial follows a script, not EEG', 18, INK2, 'middle'))
    s.append('</svg>')
    return ''.join(s)

FIGS = {'dial': dial, 'eran': eran, 'turned_small': turned_small, 'noz': noz, 'mg_dial': mg_dial, 'prescription': prescription, 'closed_loop': closed_loop, 'kern_context': kern_context, 'kern_brain': lambda: kern_context(True), 'downgrade': downgrade, 'mischler_curves': mischler_curves, 'pepino_subset': pepino_subset, 'order_accuracy': order_accuracy, 'null_hist': null_hist, 'dl_gain': dl_gain, 'dl_memory': dl_memory, 'denk_acc': denk_acc, 'nh_schematic': nh_schematic,
        'knob_orders': knob_orders, 'design_strip': design_strip, 'turned': turned}
