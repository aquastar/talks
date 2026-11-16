"""Build bibm26-keynote/index.html from src/slides.html.
Placeholders in slides.html:
  {{MAP:all|encode|decode|compare|treat|control}}  recurring field map, current arrow in orange
  {{FE_SURPRISE}}         running example: Fur Elise notes with per note surprise
  {{FE_STRIP:id}}         running example as a pitch strip (dots), id for auto animate
  {{FOREST_FULL}} {{FOREST_PREVIEW}}  Cochrane 2025 dementia, real SMDs and CIs
  {{COVER_MELODY}}        animated melody dots for the cover
Run: python3 -I src/build.py
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INK, INK2, LINE, AXIS, RULE, GROUP = '#1F1E1B', '#5F5D50', '#7C878E', '#ACA39A', '#D7D2CB', '#EFEBE5'
ACC, ACCT, MUS, MUST, LANG, LANGT, FAIL = '#F76902', '#FAD6BA', '#7D55C7', '#DCD1EB', '#009CBD', '#BCE2E8', '#DA291C'

def T(x, y, s, size=22, fill=INK, anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

def arrowhead(id_, color):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')

# ---------------------------------------------------------------- map
EDGES = {
    # key: (path, label lines, label x, y, number)
    'encode':  ('M300,150 C420,60 560,60 660,140', ['1  Encode', 'predict the brain from the music'], 480, 52),
    'decode':  ('M660,210 C560,290 420,290 300,215', ['2  Decode', 'play the music back from the brain'], 480, 300),
    'compare': ('M770,250 C770,360 730,392 650,392', ['3  Compare', 'does a model resemble the brain?'], 800, 420),
    'treat':   ('M880,180 L955,180', ['4  Treat', 'does music help patients?'], 960, 270),
    'control': ('M440,392 C260,392 190,330 190,240', ['5  Control', 'set the music, one knob at a time'], 40, 440),
}
BOXES = [  # x, y, w, h, title, sub, fill
    (80, 130, 220, 100, 'Music', 'songs, scores, sound', MUST),
    (660, 130, 220, 100, 'Brain', 'EEG, MEG, fMRI, ECoG', GROUP),
    (440, 350, 200, 84, 'Models', 'audio and music AI', GROUP),
    (960, 130, 170, 100, 'Patients', 'therapy outcomes', GROUP),
]

import math as _m
def _head(d, col):
    # explicit arrowhead from the last control point to the end point of a path
    nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', d)]
    x1, y1, x0, y0 = nums[-2], nums[-1], nums[-4], nums[-3]
    ang = _m.atan2(y1 - y0, x1 - x0); L, Wd = 13, 6
    bx, by = x1 - L * _m.cos(ang), y1 - L * _m.sin(ang)
    px, py = -_m.sin(ang) * Wd, _m.cos(ang) * Wd
    return f'<path d="M{x1:.1f},{y1:.1f} L{bx+px:.1f},{by+py:.1f} L{bx-px:.1f},{by-py:.1f} z" fill="{col}"/>'

def field_map(spec):
    at, _, landmark = spec.partition('|')
    dy = 40 if landmark else 0
    s = [f'<svg class="fig map" viewBox="0 {-dy} 1152 {470+dy}" data-id="fieldmap">']
    if landmark:
        s.append(T(0, -12, landmark, 24, INK2))
    for x, y, w, h, t, sub, fill in BOXES:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>')
        s.append(T(x + 20, y + 44, t, 28))
        s.append(T(x + 20, y + 74, sub, 18, INK2))
    for k, (d, lab, lx, ly) in EDGES.items():
        on = (k == at)
        gap = (k == 'control' and at != 'control')
        col = ACC if on else AXIS
        dash = ' stroke-dasharray="6 6"' if gap else ''
        grp = '<g data-accent="1">' if on else '<g>'
        s.append(grp + f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{2.5 if on else 1.5}"{dash}/>' + _head(d, col) + '</g>')
        anchor = 'middle' if k in ('encode', 'decode') else 'start'
        s.append(T(lx, ly, lab[0], 22 if on else 20, INK if (on or at == 'all') else INK2, anchor, 'font-weight="600"' if on else ''))
        s.append(T(lx, ly + 24, lab[1], 18, INK if on else INK2, anchor))
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- running example
FE = json.load(open(os.path.join(HERE, 'fe_surprise.json')))
SEMI = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
def midi(n): return SEMI[n[:-1]] + 12 * (int(n[-1]) + 1)

def fe_surprise(n=18):
    mel, sur = FE['melody'][:n], FE['surprise'][:n]
    W, x0, dx = 1152, 40, 60
    s = [f'<svg class="fig" viewBox="0 0 {W} 420" data-id="fe">']
    lo, hi = min(map(midi, mel)), max(map(midi, mel))
    for i, (m, v) in enumerate(zip(mel, sur)):
        x = x0 + i * dx
        y = 40 + (hi - midi(m)) * 7
        s.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{MUS}" data-id="fe{i}"/>')
        s.append(T(x, 200, m.replace('#', '&#9839;'), 17, INK2, 'middle'))
        if v is not None:
            h = v * 60
            top = v == max(x_ for x_ in sur if x_ is not None)
            s.append(f'<rect class="fragment" data-fragment-index="1" x="{x-12}" y="{380-h}" width="24" height="{max(h,1.5)}" fill="{ACC if top else (MUS if v >= 2 else AXIS)}"/>')
    s.append(f'<line x1="20" y1="380" x2="{x0+(n-1)*dx+30}" y2="380" stroke="{AXIS}"/>')
    s.append(f'<g class="fragment" data-fragment-index="1">{T(20, 236, "surprise of each note given the one before (bits)", 19, INK2)}</g>')
    s.append('</svg>')
    return ''.join(s)

def fe_strip(id_, notes=None, color=MUS, w=1100, h=120, r=6):
    mel = FE[notes] if notes else FE['melody']
    lo, hi = min(map(midi, FE['melody'])), max(map(midi, FE['melody']))
    dx = (w - 40) / (len(mel) - 1)
    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" data-id="{id_}" style="display:block">']
    for i, m in enumerate(mel):
        y = 14 + (hi - midi(m)) * (h - 28) / (hi - lo)
        s.append(f'<circle cx="{20 + i*dx:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>')
    s.append('</svg>')
    return ''.join(s)

def cover_melody():
    mel = FE['melody']
    lo, hi = min(map(midi, mel)), max(map(midi, mel))
    w, h = 1150, 120
    dx = (w - 40) / (len(mel) - 1)
    s = [f'<svg class="cover-mel" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for i, m in enumerate(mel):
        y = 14 + (hi - midi(m)) * (h - 28) / (hi - lo)
        s.append(f'<circle cx="{20 + i*dx:.1f}" cy="{y:.1f}" r="6" fill="{MUS}" style="animation-delay:{i*0.16:.2f}s"/>')
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- Cochrane 2025 dementia forest
# van der Steen et al. 2025, music vs usual care, end of treatment. SMD, 95% CI, certainty.
# Sign flipped where lower is better so that right always means "music helped".
FOREST = [
    ('Depressive symptoms', 0.23, 0.04, 0.42, 'moderate', 'probably improves slightly'),
    ('Overall behavior problems', 0.31, 0.02, 0.60, 'low', 'may improve'),
    ('Agitation, aggression', 0.05, -0.17, 0.27, 'moderate', 'probably no effect'),
    ('Anxiety', 0.15, -0.09, 0.39, 'low to very low', 'unclear'),
    ('Cognition', 0.19, -0.02, 0.41, 'low to very low', 'unclear'),
]
def forest(rows, preview=False, foot=''):
    W = 1152; X0, X1, V0, V1 = 420, 860, -0.4, 0.8
    sx = lambda v: X0 + (v - V0) / (V1 - V0) * (X1 - X0)
    rh = 66 if not preview else 140
    H = 80 + rh * len(rows) + (50 if foot else 10)
    s = [f'<svg class="fig" viewBox="0 0 {W} {H}">']
    s.append(f'<line x1="{sx(0)}" y1="44" x2="{sx(0)}" y2="{80 + rh*len(rows) - rh//2}" stroke="{AXIS}"/>')
    s.append(T(sx(0) - 10, 30, 'music worse', 18, INK2, 'end'))
    s.append(T(sx(0) + 10, 30, 'music better', 18, INK2))
    s.append(T(900, 30, 'outcome' if preview else 'certainty', 18, INK2))
    for i, (name, m, lo, hi, cert, verdict) in enumerate(rows):
        y = 80 + i * rh
        clear = lo > 0
        star = clear and cert == 'moderate'
        col = ACC if star else (INK2 if clear else LINE)
        g = '<g data-accent="1">' if star else '<g>'
        s.append(T(0, y + 8, name, 26 if preview else 23))
        s.append(g + f'<line x1="{sx(lo):.1f}" y1="{y}" x2="{sx(hi):.1f}" y2="{y}" stroke="{col}" stroke-width="2.5"/>')
        if clear:
            s.append(f'<circle cx="{sx(m):.1f}" cy="{y}" r="8" fill="{col}"/></g>')
        else:
            s.append(f'<circle cx="{sx(m):.1f}" cy="{y}" r="7" fill="#FBFAF7" stroke="{col}" stroke-width="2"/></g>')
        s.append(T(900, y + 8, verdict if preview else cert, 24 if preview else 21, INK2))
    if foot:
        s.append(T(0, H - 14, foot, 21, INK2))
    s.append('</svg>')
    return ''.join(s)

PREVIEW_ROWS = [FOREST[0], FOREST[4]]

ORIG = open(os.path.join(HERE, 'original.html')).read()
def old_svg(key):
    # first <svg class="fig"> of the section in original.html whose h2 contains key
    for sec in re.findall(r'<section.*?</section>', ORIG, flags=re.S):
        h = re.search(r'<h2[^>]*>(.*?)</h2>', sec, flags=re.S)
        if h and key in h.group(1):
            m = re.search(r'<svg class="fig"[^>]*>(.*?)</svg>', sec, flags=re.S)
            assert m, key
            inner = m.group(1)
            if key.startswith('Music releases dopamine'):
                inner = re.sub(r'font-size="(\d+)"', lambda q: f'font-size="{int(q.group(1)) + 3}"', inner)
            return m.group(0).split('>', 1)[0] + '><g data-accent="1">' + inner + '</g></svg>'
    raise KeyError(key)

import glob
FIGS = os.path.join(ROOT, '..', 'shared', 'figs')
MISSING = []
def find(sub, key):
    hits = sorted(glob.glob(os.path.join(FIGS, sub, key + '*.*')))
    hits = [h for h in hits if h.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    if not hits:
        MISSING.append(sub + '/' + key)
        return None
    return '../shared/figs/' + sub + '/' + os.path.basename(hits[0])

def people(spec):
    # spec: key|Name|affiliation ; key2|Name2|affiliation2   (';' only inside the placeholder)
    out = []
    for item in spec.split(' ; '):
        key, name, aff = [x.strip() for x in item.split('|')]
        f = find('people', key)
        if f:
            out.append(f'<figure><img src="{f}" alt="{name}"><figcaption>{name}<span>{aff}</span></figcaption></figure>')
    return '<div class="people">' + ''.join(out) + '</div>' if out else ''

def photo(spec):
    key, alt = [x.strip() for x in spec.split('|')]
    f = find('photos', key)
    return f'<img class="ph" src="{f}" alt="{alt}">' if f else f'<div style="height:230px;background:#EFEBE5"></div>'

def build():
    src = open(os.path.join(HERE, 'slides.html')).read()
    src = re.sub(r'\{\{PEOPLE:([^}]+)\}\}', lambda m: people(m.group(1)), src)
    src = re.sub(r'\{\{PHOTO:([^}]+)\}\}', lambda m: photo(m.group(1)), src)
    src = re.sub(r'\{\{OLD:([^}]+)\}\}', lambda m: old_svg(m.group(1)), src)
    src = re.sub(r'\{\{MAP:([^}]+)\}\}', lambda m: field_map(m.group(1)), src)
    src = src.replace('{{FE_SURPRISE}}', fe_surprise())
    src = re.sub(r'\{\{FE_STRIP:(\w+)(?::(\w+))?(?::(\d+))?\}\}', lambda m: fe_strip(m.group(1), m.group(2), w=int(m.group(3) or 1100), h=90 if m.group(3) else 120, r=5 if m.group(3) else 6), src)
    src = src.replace('{{FOREST_FULL}}', forest([FOREST[0], FOREST[2], FOREST[4]], foot='Filled: interval excludes zero (orange: moderate certainty). Four weeks after treatment, no clear effect.'))
    src = src.replace('{{FOREST_PREVIEW}}', forest(PREVIEW_ROWS, preview=True))
    src = src.replace('{{COVER_MELODY}}', cover_melody())
    import redraw
    src = re.sub(r'\{\{FIG:(\w+)\}\}', lambda m: redraw.FIGS[m.group(1)](), src)
    PN = redraw.pernote()
    src = re.sub(r'\{\{PERNOTE:(\w+)\}\}', lambda m: str(PN[m.group(1)]), src)
    if '{{EEG_' in src:
        import eeg_figs
        src = src.replace('{{EEG_ERP}}', eeg_figs.erp_svg()).replace('{{EEG_TOPO}}', eeg_figs.topo_svg())
    left = re.findall(r'\{\{[^}]*\}\}', src)
    assert not left, left
    open(os.path.join(ROOT, 'index.html'), 'w').write(src)
    # style gate: no em dash, en dash or semicolon in visible text
    vis = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', src, flags=re.S)
    vis = re.sub(r'<aside class="notes">.*?</aside>', '', vis, flags=re.S)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    vis = re.sub(r'&[#\w]+;', ' ', vis)
    bad = [c for c in ('—', '–', ';') if c in vis]
    # time ledger (data-sec per slide, backup excluded), minute stamps in notes, word gate
    t = 0; acts = {}; over = []; words = []; out = []; pos = 0; LASTACT = ['0']
    total = sum(int(re.search(r'data-sec="(\d+)"', m.group(1)).group(1)) for m in re.finditer(r'<section([^>]*)>', src) if 'data-backup' not in m.group(1) and 'data-sec' in m.group(1))
    def stamp(m):
        nonlocal t
        a, body = m.group(1), m.group(2)
        if 'data-backup' in a: return m.group(0)
        sec = re.search(r'data-sec="(\d+)"', a)
        if not sec: over.append('slide without data-sec'); return m.group(0)
        mk = re.search(r'<span class="mark">(\d)', body)
        if mk and mk.group(1) not in acts: acts[mk.group(1)] = round(t / 60, 1)
        if mk:
            if mk.group(1) < LASTACT[0]: over.append(f'act order: act {mk.group(1)} after act {LASTACT[0]} at slide {len(words)}')
            LASTACT[0] = max(LASTACT[0], mk.group(1))
        nt = re.search(r'<aside class="notes">(.*?)</aside>', body, flags=re.S)
        if nt:
            sents = [x.strip() for x in re.split(r'(?<=[.])\s+', nt.group(1)) if len(x.strip()) > 30]
            if len(sents) != len(set(sents)): over.append(f'repeated sentence in notes at slide {len(words)}')
        if 'class="thesis"' in body and 'stimulus' in body: acts['thesis'] = round(t / 60, 1)
        body = body.replace('<aside class="notes">', f'<aside class="notes">[minute {t/60:.1f} of {total/60:.0f}] ', 1)
        # word gate: visible body words outside headline, mark, svg, ref, notes
        v = re.sub(r'<(svg|aside|h2|script)[^>]*>.*?</\1>', ' ', body, flags=re.S)
        v = re.sub(r'<div class="ref">.*?</div>', ' ', v, flags=re.S)
        v = re.sub(r'<span class="(mark|status)[^"]*">.*?</span>', ' ', v, flags=re.S)
        v = re.sub(r'<button[^>]*>.*?</button>', ' ', v, flags=re.S)
        v = re.sub(r'<figcaption>.*?</figcaption>', ' ', v, flags=re.S)
        n = len(re.sub(r'<[^>]+>', ' ', v).split()); nli = len(re.findall(r'<li[ >]', body))
        idx = len(words)
        words.append(n)
        if (n > 30 or nli > 3) and 'data-gate' not in a: over.append(f'slide {idx}: {n} words, {nli} items')
        t += int(sec.group(1))
        return f'<section{a}>{body}</section>'
    src = re.sub(r'<section([^>]*)>(.*?)</section>', stamp, src, flags=re.S)
    open(os.path.join(ROOT, 'index.html'), 'w').write(src)
    print(f'ledger: {t} s = {t/60:.1f} min (window 1750 to 2150 s)', 'OVER BUDGET' if (t > 2150 or t < 1750) else 'ok', '| act starts (min):', acts)
    if over: print('gate:', '; '.join(over))
    for bad in ('the listener model', 'the music model'):
        k = src.find('Change one chord, and the brain answers')
        if k >= 0 and bad in src[k:src.find('</section>', k)]: over.append(f'knob slide still lists {bad}')
    if MISSING: print('missing images:', ', '.join(sorted(set(MISSING))))
    print('slides:', src.count('<section'), ' style violations:', bad or 'none')

if __name__ == '__main__':
    build()
