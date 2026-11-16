"""House style figures from his own EEG analysis (eeg-demo/index.html data):
OpenNeuro ds005876, 29 listeners, MusicGen-large surprise, regression over all songs.
erp_svg(): EEG at the 11 frontocentral channels after high vs low surprise notes, SE band, cluster window.
topo_svg(): scalp maps of the extra response per +1 SD surprise at 0, 0.1, 0.2, 0.3 s."""
import json, os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
_t = open(os.path.join(HERE, '..', '..', 'eeg-demo', 'index.html')).read()
D = json.loads(re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>', _t, re.S).group(1))
INK, INK2, AXIS, ACC, LINE, TEAL = '#1F1E1B', '#5F5D50', '#ACA39A', '#F76902', '#7C878E', '#009CBD'
CL = D['cluster']

def erp_svg(W=700, H=380):
    L, R, T, B = 70, 20, 30, 60
    t = D['lags']; hi, lo, se = D['k_hi'], D['k_lo'], D['k_se']
    ymin = min(min(lo), min(h - s for h, s in zip(hi, se))) - 0.16
    ymax = max(max(hi), max(h + s for h, s in zip(hi, se))) + 0.05
    sx = lambda v: L + (v - t[0]) / (t[-1] - t[0]) * (W - L - R)
    sy = lambda v: T + (ymax - v) / (ymax - ymin) * (H - T - B)
    o = [f'<svg class="fig" viewBox="0 0 {W} {H}" style="width:{W}px">']
    o.append(f'<rect x="{sx(CL["t_from"]):.1f}" y="{T}" width="{sx(CL["t_to"])-sx(CL["t_from"]):.1f}" height="{H-T-B}" fill="#EFEBE5"/>')
    o.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{W-R}" y2="{sy(0):.1f}" stroke="{AXIS}"/>')
    o.append(f'<line x1="{sx(0):.1f}" y1="{T}" x2="{sx(0):.1f}" y2="{H-B}" stroke="{AXIS}" stroke-dasharray="3 4"/>')
    band = ' '.join(f'{sx(a):.1f},{sy(h+s):.1f}' for a, h, s in zip(t, hi, se)) + ' ' + ' '.join(f'{sx(a):.1f},{sy(h-s):.1f}' for a, h, s in reversed(list(zip(t, hi, se))))
    o.append(f'<polygon points="{band}" fill="#FAD6BA" opacity=".7"/>')
    o.append('<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>' % (LINE, ' '.join(f'{sx(a):.1f},{sy(v):.1f}' for a, v in zip(t, lo))))
    o.append('<polyline fill="none" stroke="%s" stroke-width="2.5" points="%s"/>' % (ACC, ' '.join(f'{sx(a):.1f},{sy(v):.1f}' for a, v in zip(t, hi))))
    for v in (0, 0.2, 0.4, 0.6):
        o.append(f'<text x="{sx(v):.1f}" y="{H-B+24}" font-size="17" fill="{INK2}" text-anchor="middle">{v:g}</text>')
    o.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-12}" font-size="18" fill="{INK2}" text-anchor="middle">seconds after the note starts</text>')
    o.append(f'<text x="{sx(0)+6:.1f}" y="{T+14}" font-size="16" fill="{INK2}">note</text>')
    o.append(f'<text x="{sx(CL["t_from"])+6:.1f}" y="{T+18}" font-size="16" fill="{INK2}">cluster, p = {CL["p"]:.4f}</text>')
    k = min(range(len(t)), key=lambda q: abs(t[q] - 0.37))
    o.append(f'<text x="{sx(t[k])+8:.1f}" y="{sy(hi[k])-14:.1f}" font-size="19" fill="{INK}">surprising notes</text>')
    j = min(range(len(t)), key=lambda q: lo[q] if 0.1 < t[q] < 0.35 else 9)
    o.append(f'<text x="{sx(0.13):.1f}" y="{sy(lo[j])+26:.1f}" font-size="19" fill="{INK2}">expected notes</text>')
    o.append(f'<text x="{L-10}" y="{sy(0)+5:.1f}" font-size="16" fill="{INK2}" text-anchor="end">0</text>')
    o.append(f'<text x="14" y="{T+10}" font-size="16" fill="{INK2}">EEG (SD)</text>')
    o.append('</svg>')
    return ''.join(o)

def _interp(vals, pos, x, y, p=2):
    num = den = 0.0
    for v, (a, b) in zip(vals, pos):
        d = (x - a) ** 2 + (y - b) ** 2
        if d < 1e-9: return v
        w = 1 / d ** (p / 2); num += w * v; den += w
    return num / den

def _col(v, lim):
    # diverging teal (negative) to orange (positive) through warm white
    x = max(-1, min(1, v / lim))
    a, n, b = (0, 156, 189), (251, 250, 247), (125, 85, 199)
    c = b if x > 0 else a; x = abs(x)
    return '#%02x%02x%02x' % tuple(int(n[k] + (c[k] - n[k]) * x) for k in range(3))

def topo_svg(times=(0.0, 0.1, 0.2, 0.3), size=74, gap=10, grid=22):
    t = D['lags']; ks = D['k_surp']; pos = D['pos']
    R = max(math.hypot(*p) for p in pos) * 1.08
    idx = [min(range(len(t)), key=lambda k: abs(t[k] - tt)) for tt in times]
    lim = max(abs(v) for i in idx for v in ks[i])
    W = len(times) * size + (len(times) - 1) * gap
    o = [f'<svg viewBox="0 0 {W} {size+34}" width="{W}" height="{size+34}" style="display:block">']
    hl = set(D['highlight'])
    for n, (i, tt) in enumerate(zip(idx, times)):
        ox = n * (size + gap); cx = ox + size / 2; cy = size / 2; r = size / 2 - 6
        o.append(f'<clipPath id="tc{n}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><g clip-path="url(#tc{n})">')
        cs = 2 * r / grid
        for gx in range(grid):
            for gy in range(grid):
                x = -R + (gx + .5) * 2 * R / grid; y = R - (gy + .5) * 2 * R / grid
                v = _interp(ks[i], pos, x, y)
                o.append(f'<rect x="{cx-r+gx*cs:.1f}" y="{cy-r+gy*cs:.1f}" width="{cs+.6:.1f}" height="{cs+.6:.1f}" fill="{_col(v, lim)}"/>')
        o.append('</g>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{AXIS}"/>')
        o.append(f'<path d="M{cx-7},{cy-r+1} L{cx},{cy-r-9} L{cx+7},{cy-r+1}" fill="none" stroke="{AXIS}"/>')
        for c, (a, b) in zip(D['ch'], pos):
            px, py = cx + a / R * r, cy - b / R * r
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{size/55 if c in hl else size/110:.1f}" fill="{INK if c in hl else INK2}"/>')
        o.append(f'<text x="{cx}" y="{size+26}" font-size="17" fill="{INK2}" text-anchor="middle">{"+" if tt else ""}{tt:g} s</text>')
    o.append('</svg>')
    return ''.join(o)

if __name__ == '__main__':
    print(CL, D['n_listeners'])
