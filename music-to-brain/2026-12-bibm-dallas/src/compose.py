# Draft 1 of the BIBM 2026 keynote "The Music That Plays the Brain".
# Starts from the RIT CS colloquium deck (graph-inside/2026-11-19-cs-colloquium): its head, CSS, scripts
# and the music slides are reused as built, new slides are written here in the same markup.
# Run: python3 -I src/compose.py  (writes index.html next to src/)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from secs import top_sections, title

COL = os.path.join(DECK, '..', '..', 'graph-inside', '2026-11-19-cs-colloquium', 'index.html')
src = open(COL).read()
i0 = src.find('<div class="slides">') + len('<div class="slides">')
i1 = src.find('<div id="rail">')
head, tail = src[:i0], src[i1:]

head = re.sub(r'<title>.*?</title>', '<title>The Music That Plays the Brain</title>', head, count=1, flags=re.S)
tail = tail.replace("var CH=[['0','Overview'],['1','1 Language'],['2','2 Music'],['4','Close']];",
                    "var CH=[['0','Opening'],['1','Why now'],['2','Read'],['3','Model'],['4','Write'],['5','Close']];")
tail = re.sub(r"var NAMES=\{[^}]*\}", "var NAMES={'0':'Opening','1':'Why now','2':'Read','3':'Model','4':'Write','5':'Close'}", tail, count=1)

# ---------- pick slides from the colloquium, flattening its vertical stacks ----------
flat = []
for t in top_sections(src):
    if t.count('<section') > 1:
        inner = t[t.find('>') + 1:]
        flat += top_sections('<div class="slides">' + inner)
    else:
        flat.append(t)
def pick(start, ch, notes_add=''):
    hits = [x for x in flat if title(x).startswith(start)]
    assert len(hits) >= 1, start
    x = hits[0]
    x = re.sub(r'class="backup\s*', 'class="', x, count=1)
    x = x.replace('<span class="status plan">Backup</span>', '')
    x = re.sub(r'data-ch="[^"]*"', f'data-ch="{ch}"', x, count=1) if 'data-ch=' in x[:200] else x.replace('<section', f'<section data-ch="{ch}"', 1)
    if notes_add:
        x = x.replace('</aside>', ' ' + notes_add + '</aside>', 1) if '</aside>' in x else x.replace('</section>', f'  <aside class="notes">{notes_add}</aside>\n</section>', 1)
    return x
def demo_slide():
    x = [t for t in flat if 'fulldemo' in t[:200]][0]
    return re.sub(r'data-ch="[^"]*"', 'data-ch="3"', x, count=1)

# ---------- helpers for new slides, same look as the colloquium ----------
INK, MUT, LINE, TINT, SLATE = '#1F1E1B', '#5F5D50', '#D7D2CB', '#F1EDE7', '#4C5B66'
def kw(t): return f'<b style="color:#C45200;font-weight:700">{t}</b>'
def keybox(html, idx=None, top='.5em'):
    fr = f' class="fragment" data-fragment-index="{idx}"' if idx is not None else ''
    return (f'<p{fr} style="text-align:center;margin:{top} 1.1em 0"><span style="display:inline-block;background:#FDEFE3;border-left:7px solid #F76902;border-radius:3px;'
            f'padding:.32em 1em;font-family:et-book,Georgia,serif;font-size:.84em;color:{INK};line-height:1.35">{html}</span></p>')
def status(kind):
    cls = {'In progress': 'prog', 'Vision': 'open', 'Published': 'published', 'Under review': 'review'}[kind]
    return f'<span class="status {cls}">{kind}</span>'
def ref(*items):
    return '<div class="ref">' + '<span class="rsep" aria-hidden="true"></span>'.join(items) + '</div>' if items else ''
def a(text, url): return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
def btn(label, audio, clip):
    return (f'<button class="playclip" data-clip="{clip}" data-audio="figs/audio/{audio}" style="min-width:200px;height:40px;border-radius:3px;border:2px solid {MUT};'
            f'background:#fff;color:{MUT};font:600 15px et-book,sans-serif;cursor:pointer;margin:4px 6px">&#9654; {label}</button>')
def card(head, big, sub, frag=None, w=250, dim=False):
    fr = f' class="fragment" data-fragment-index="{frag}"' if frag is not None else ''
    col = MUT if dim else INK
    return (f'<div{fr} style="flex:1 1 {w}px;max-width:{w + 40}px;background:{TINT};border-radius:4px;padding:20px 22px;margin:8px;text-align:left">'
            f'<div style="font:600 15px Fira Sans,sans-serif;letter-spacing:.04em;color:{SLATE};text-transform:uppercase">{head}</div>'
            f'<div style="font-family:et-book,Georgia,serif;font-size:46px;line-height:1.1;color:{col};margin:10px 0 8px">{big}</div>'
            f'<div style="font-family:et-book,Georgia,serif;font-size:21px;line-height:1.3;color:{MUT}">{sub}</div></div>')
def row(*cards, top=40):
    return f'<div style="display:flex;justify-content:center;flex-wrap:wrap;margin:{top}px 30px 0">{"".join(cards)}</div>'
def two(left, right, lw=560):
    return (f'<div style="display:flex;gap:34px;align-items:center;justify-content:center;margin:14px 40px 0">'
            f'<div style="flex:0 0 {lw}px">{left}</div><div style="flex:1 1 auto;text-align:left">{right}</div></div>')
def line(t, size=22, col=INK, top=10):
    return f'<p style="font-family:et-book,Georgia,serif;font-size:{size}px;line-height:1.35;color:{col};margin:{top}px 0 0;text-align:left">{t}</p>'
def img(src, w, alt=''):
    return f'<img src="figs/{src}" alt="{alt}" style="width:{w}px;max-width:100%;max-height:340px;object-fit:cover;border-radius:3px;display:block">'
def sec(ch, h, body, refs='', notes='', st=None, cls=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<section data-ch="{ch}"{c}>\n  <h2>{h}</h2>{status(st) if st else ""}\n  {body}\n  {refs}\n'
            f'  <aside class="notes">{notes}</aside>\n</section>')


# ---------- slides from the earlier keynote draft (2026-12-01-bibm-dallas), kept with their own look ----------
OLDHTML = open(os.path.join(DECK, '..', '2026-12-01-bibm-dallas', 'index.html')).read()
OLDS = top_sections(OLDHTML)
_css = open(os.path.join(DECK, '..', 'shared', 'style.css')).read()
_keep = ('.mark', '.ink2', '.cols', '.big', '.thesis', '.fp', '.key', '.tldr', '.p ', '.cap', '.photos', '.audio-row', '.people', '.illus', 'svg.fig', 'button.play', 'p,.reveal li', 'b{')
KSCSS = ['.reveal section.ks{--bg:#FBFAF7;--ink:#1F1E1B;--ink2:#5F5D50;--line:#7C878E;--axis:#ACA39A;--rule:#D7D2CB;--group:#EFEBE5;--accent:#F76902;--accent-tint:#FAD6BA;--accent-text:#C45200;--lang:#4C5B66;--music:#4C5B66;--music-tint:#E4E7E9;--fail:#DA291C;--refc:#A39E93}',
         '.reveal section.ks .ksw{zoom:.84;text-align:left}', '.reveal section.ks .mark{display:none}']
for rule in re.findall(r'\.reveal [^{]+\{[^}]*\}', _css):
    sel = rule[:rule.index('{')]
    if any(k in sel for k in _keep) and 'section.cover' not in sel and '.forecast' not in sel:
        KSCSS.append(re.sub(r'\.reveal ', '.reveal section.ks ', rule))
def padvb(t, d=22):
    def f(m):
        a, b, w, h = [float(v) for v in m.group(1).split()]
        return f'<svg class="fig" viewBox="{a - d:g} {b - d:g} {w + 2 * d:g} {h + 2 * d:g}"'
    return re.sub(r'<svg class="fig[^"]*" viewBox="([^"]+)"', f, t)
_n = [0]
def oldk(start, ch):
    t = [x for x in OLDS if title(x).startswith(start)][0]
    t = re.sub(r'<section[^>]*>', f'<section data-ch="{ch}" class="ks">', t, count=1)
    t = re.sub(r'\s*<span class="mark">.*?</span>', '', t, count=1, flags=re.S)
    t = t.replace('class="status prog"', 'class="status prog"').replace('class="status rev"', 'class="status review"')
    def _btn(m):
        _n[0] += 1
        return f'<button class="playclip" data-clip="ok{_n[0]}" data-audio="{m.group(1)}" style="min-width:90px;height:36px;border-radius:3px;border:2px solid {MUT};background:#fff;color:{MUT};font:600 15px et-book,sans-serif;cursor:pointer;margin-right:8px">&#9654; play</button>'
    t = re.sub(r'<button class="play" data-audio="([^"]+)">play</button>', _btn, t)
    t = t.replace('class="embed" data-src=', 'class="fe-frame" data-src=')
    for c0, c1 in (('#7D55C7', SLATE), ('#7d55c7', SLATE), ('#DCD1EB', '#E4E7E9'), ('#dcd1eb', '#E4E7E9'), ('#009CBD', SLATE)):
        t = t.replace(c0, c1)
    # move a status label out of the h2, wrap the body so it fits the 660 px slide
    st = re.search(r'\s*(<span class="status[^"]*">[^<]*</span>)', t[:t.find('</h2>') + 5])
    if st:
        t = t.replace(st.group(0), '', 1)
        t = t.replace('</h2>', '</h2>' + st.group(1), 1)
    h_end = t.find('</h2>') + 5
    if st: h_end = t.find(st.group(1)) + len(st.group(1))
    r_at = t.find('<div class="ref">'); a_at = t.find('<aside')
    cut = min(x for x in (r_at, a_at, t.rfind('</section>')) if x > 0)
    t = padvb(t)
    return t[:h_end] + '\n  <div class="ksw">' + t[h_end:cut] + '</div>\n  ' + t[cut:]
def colk(start, ch, add=''):
    x = pick(start, ch, add)
    return re.sub(r'(<span class="status [^"]*">)Backup, ', r'\1', x)

# ---------- figures drawn for this deck ----------
BRAIN = open(os.path.join(DECK, 'figs', 'brain-lateral-inner.svgfrag')).read()
def T(x, y, s, size=18, col=INK, anchor='start', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}" font-family="et-book,Georgia,serif">{s}</text>'
def svgfig(w, h, inner, width=None):
    return (f'<svg class="fig" viewBox="0 0 {w} {h}" style="width:{width or w}px;max-width:100%;height:auto;display:block;margin:4px auto 0">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#4C5B66"/></marker>'
            '<marker id="aho" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#F76902"/></marker></defs>'
            + inner + '</svg>')
ACC = '#F76902'
def mapfig(active=None, notes3=False):
    """Music on the left, the brain on the right. Model goes over the top, Read under the bottom, Write is the dial on the music."""
    c = lambda k: ACC if active == k else SLATE
    m = lambda k: 'aho' if active == k else 'ah'
    g = ''
    g += f'<rect x="90" y="110" width="250" height="150" rx="6" fill="{TINT}"/>' + T(215, 170, 'Music', 26, INK, 'middle') + T(215, 205, 'notes, sound, a song', 18, MUT, 'middle')
    g += f'<g transform="translate(640,92) scale(.29)">{BRAIN}</g>' + T(770, 300, 'Brain', 26, INK, 'middle') + T(770, 326, 'EEG, MEG, fMRI, ECoG', 18, MUT, 'middle')
    g += f'<path d="M340,165 C470,105 560,105 650,145" fill="none" stroke="{c("model")}" stroke-width="3" marker-end="url(#{m("model")})"/>' + T(495, 72, 'Model', 22, c('model'), 'middle', 600) + T(495, 96, 'predict the brain from the music', 17, MUT, 'middle')
    g += f'<path d="M660,270 C560,340 450,340 340,240" fill="none" stroke="{c("read")}" stroke-width="3" marker-end="url(#{m("read")})"/>' + T(500, 352, 'Read', 22, c('read'), 'middle', 600) + T(500, 376, 'decode the music from the brain', 17, MUT, 'middle')
    wc = c('write'); dash = '' if active == 'write' else ' stroke-dasharray="7 6"'
    g += f'<circle cx="215" cy="62" r="26" fill="#fff" stroke="{wc}" stroke-width="3"{dash}/><line x1="215" y1="62" x2="232" y2="44" stroke="{wc}" stroke-width="3"/>'
    g += f'<path d="M246,56 C320,20 600,10 690,95" fill="none" stroke="{wc}" stroke-width="2.5"{dash} marker-start="url(#{m("write")})"/>'
    g += T(60, 40, 'Write', 22, wc, 'start', 600) + T(60, 64, 'set the dial for a', 17, MUT) + T(60, 86, 'brain response', 17, MUT)
    if notes3:
        g += f'<g class="fragment" data-fragment-index="1">{T(965, 150, "1. Sound moves the brain,", 19, INK)}{T(965, 174, "but the music was never set", 19, MUT)}</g>'
        g += f'<g class="fragment" data-fragment-index="2">{T(965, 220, "2. A small graph of notes", 19, INK)}{T(965, 244, "tracks the listening brain", 19, MUT)}</g>'
        g += f'<g class="fragment" data-fragment-index="3">{T(965, 290, "3. A dial, and the brain", 19, INK)}{T(965, 314, "as the judge", 19, MUT)}</g>'
    return svgfig(1240 if notes3 else 1000, 400, g, 1120 if notes3 else 900)
def hbars(rows, maxv, w=620, lab_w=330, bh=34, gap=16, unit='', top=10, chance=None, size=19):
    """rows: (label, value, highlight, value text)"""
    g = ''; y = top
    for lab, v, hi, vt in rows:
        L = max(3, v / maxv * w)
        g += T(lab_w - 12, y + bh * .68, lab, size, INK if hi else MUT, 'end')
        g += f'<rect x="{lab_w}" y="{y}" width="{L:.1f}" height="{bh}" rx="2" fill="{ACC if hi else "#ACA39A"}"/>'
        g += T(lab_w + L + 10, y + bh * .68, vt, size, INK if hi else MUT, 'start', 600 if hi else 400)
        y += bh + gap
    if chance is not None:
        x = lab_w + chance / maxv * w
        g += f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{y - gap + 6}" stroke="#1F1E1B" stroke-width="1.5" stroke-dasharray="5 5"/>' + T(x, y + 14, 'chance', 16, MUT, 'middle')
    return g, y + 24
def dots(n, k, x0, y0, cols=10, r=11, gap=27, col=None):
    g = ''
    for i in range(n):
        x = x0 + (i % cols) * gap; y = y0 + (i // cols) * gap
        g += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{(col or SLATE) if i < k else "#fff"}" stroke="{col or SLATE}" stroke-width="2"/>'
    return g

def stack(main, *backs):
    ch = re.search(r'data-ch="([^"]*)"', main).group(1)
    bk = [re.sub(r'<section([^>]*)>', lambda m: '<section' + (m.group(1).replace('class="', 'class="backup ') if 'class="' in m.group(1) else m.group(1) + ' class="backup"') + '>', b, count=1) for b in backs]
    return f'<section data-ch="{ch}">\n' + main + '\n' + '\n'.join(bk) + '\n</section>'
def table(cols, rows, widths, top=36, rh=62, size=17):
    g = ''; x = 10; xs = []
    for w_ in widths: xs.append(x); x += w_
    for c, h in enumerate(cols): g += T(xs[c], top - 10, h, 16, MUT, 'start', 600)
    g += f'<line x1="10" y1="{top}" x2="{x}" y2="{top}" stroke="#ACA39A" stroke-width="1.2"/>'
    for r, row in enumerate(rows):
        y = top + 26 + r * rh
        for c, cell in enumerate(row):
            for k, ln in enumerate(cell if isinstance(cell, list) else [cell]):
                g += T(xs[c], y + k * 22, ln, size, INK if (c == 0 or k == 0) else MUT, 'start', 600 if c == 0 else 400)
        g += f'<line x1="10" y1="{y + rh - 26}" x2="{x}" y2="{y + rh - 26}" stroke="#E4E0D9" stroke-width="1"/>'
    return g, top + 26 + len(rows) * rh - 10, x + 10
def landmark(ch, step, h, question, notes):
    return sec(ch, h, mapfig(step) + keybox(question, None, '.2em'), '', notes)

# ---------- the slides ----------
S = []
S.append(f'''<section class="title full" data-ch="0" data-background-color="#FBFAF7">
  <div style="display:flex;align-items:center;margin:100px 60px 0">
  <div style="flex:1 1 auto;text-align:left">
    <p style="font:600 15px Fira Sans,sans-serif;letter-spacing:.12em;color:{MUT};text-transform:uppercase;margin:0">Keynote · AI4BioSig Workshop · IEEE BIBM 2026 · Dallas</p>
    <h1 style="font-family:et-book,Georgia,serif;font-weight:400;font-size:86px;line-height:1.05;color:{INK};margin:26px 0 0;text-transform:none">The Music That<br>Plays the <span style="color:#F76902">Brain</span></h1>
    <div style="width:120px;height:3px;background:#F76902;margin:34px 0 26px"></div>
    <p style="font-family:et-book,Georgia,serif;font-size:26px;color:{INK};margin:0">Zhiqian Chen</p>
    <p style="font-family:et-book,Georgia,serif;font-size:20px;color:{MUT};margin:4px 0 0">Department of Computer Science, Rochester Institute of Technology</p>
  </div>
  <div style="flex:0 0 440px">{svgfig(420, 330, f'<g transform="translate(30,30) scale(.38)">{BRAIN}</g>', 420)}</div>
  </div>
  <aside class="notes">Open with sound, not with me. Go straight to the next slide. Brain drawing: Gray, Anatomy of the Human Body, public domain, recolored.</aside>
</section>''')


S.append(sec(0, 'Many people with advanced dementia can still sing the hymns of their youth',
    two(img('older_adults_choir.jpg', 520, 'Older adults singing together'),
        line('Music reaches a brain that has lost almost everything else.', 26, INK, 0)
        + line('What if we could choose the song for one of them, and watch her brain answer?', 26, MUT, 26)),
    ref(a('Jacobsen et al., Brain 2015', 'https://doi.org/10.1093/brain/awv135')),
    'Musical memory is among the last to go in Alzheimer disease, Jacobsen 2015 shows the regions that hold it are among the least affected. Pose the question and leave it open: what if we could choose the song, and watch her brain answer? We come back to her at the end. Photo: Peter van der Sluijs, Wikimedia Commons, CC BY-SA 4.0.'))

S.append(oldk('Same notes, same sound', 0))

S.append(sec(0, 'Music to brain is three steps, and this talk walks all three',
    mapfig(None, notes3=True) + keybox('AI can now set the music to a ' + kw('dose') + ', and the brain can ' + kw('grade') + ' it.', 4, '.1em'),
    '', 'The map of the talk, it comes back at each part. Music on the left, the brain on the right. Model goes over the top, predict the brain from the music. Read comes back underneath, decode the music from the brain. Write is the dial on the music, dashed because it is the open step. Click by click, the three findings. One: sound moves the brain, but in the trials the music was never set. Two: a small graph of which note follows which tracks the listening brain. Three: generators give us the dial, and the brain can be the judge. Click: the one line to remember.'))

# Part 1. Why now
S.append(pick('Part 2. Hearing loss: a quiet epidemic', 1).replace('Part 2. Hearing loss', 'Part 1. Hearing loss', 1))
S.append(stack(pick('Sound acts on the brain', 1), oldk('Music releases dopamine twice', 1), oldk("A steady beat can make a person with Parkinson", 1)))
S.append(stack(pick('Music already acts on the brain, as medicine', 1), oldk('In dementia, music lifts mood slightly', 1)))

_tg, _th, _tw = table(['Trial', 'People', 'Music or sound given', 'Compared with', 'Primary outcome', 'Result'],
    [[['HOPE'], '673', ['40 Hz light and sound,', '1 hour a day, 12 months'], ['sham device'], ['cognition plus', 'daily living'], ['missed', 'CTAD 2026, verify']],
     [['MIDDEL'], '1,021', ['group music therapy or', 'choir, 6 countries'], ['usual care'], ['depression', 'at 6 months'], ['no change', 'β 0.8 [−1.0 to 2.6]']],
     [['ICU trial'], '158', ['slow music, 60 to 80 bpm,', 'twice a day'], ['silent track,', 'same headphones'], ['days without', 'delirium or coma'], ['2.5 vs 3 days', 'p = 0.66']],
     [['LongSTEP'], '206', ['parent singing,', 'preterm infants'], ['standard care'], ['language', 'at 24 months'], ['no effect']]],
    [130, 90, 250, 190, 190, 200], top=34, rh=72, size=18)
S.append(sec(1, 'The biggest, best controlled trials of music and sound came back null',
    line('Expected: music helps. Measured, in the four largest recent trials:', 21, MUT, 0).replace('text-align:left', 'text-align:center')
    + f'<div class="fragment" data-fragment-index="1">{svgfig(_tw, _th, _tg, 1120)}</div>'
    + keybox('The larger the trial and the better the control, the closer the effect to ' + kw('zero') + '.', 2, '.4em'),
    ref(a('Cognito HOPE, NCT05637801', 'https://clinicaltrials.gov/study/NCT05637801'), a('MIDDEL, Lancet Healthy Longevity 2025', 'https://doi.org/10.1016/j.lanhl.2025.100783'),
        a('JAMA Intern Med 2025', 'https://doi.org/10.1001/jamainternmed.2025.5263'), a('LongSTEP, JAMA Netw Open 2024', 'https://doi.org/10.1001/jamanetworkopen.2024.10721')),
    'Ask the room first: hands up if you expect music to help in these trials. Click: the four largest recent trials. HOPE, 40 Hz light and sound for Alzheimer disease, 673 enrolled, one hour a day for a year against a sham device, missed its primary endpoint at CTAD in November 2026 (VERIFY against the CTAD slides, numbers so far from news reports, a mild subgroup looked better but is unadjusted). MIDDEL, 1,021 care home residents in six countries, music therapy 0.8 and choir 0.4 on the depression scale, both intervals include zero, the country predicted more than the intervention. ICU, 158 ventilated older adults, slow music against a silent track through the same headphones, 2.5 against 3 days without delirium or coma. LongSTEP, 206 preterm infants, parent singing, no language effect at 24 months. Click: not that music does nothing, but that music given as a fixed playlist is not a controlled dose.'))

_loop = (f'<rect x="10" y="40" width="170" height="70" rx="6" fill="{TINT}"/>' + T(95, 72, 'a body signal', 20, INK, 'middle') + T(95, 96, 'steps, sensors', 16, MUT, 'middle')
    + f'<path d="M180,75 L270,75" stroke="{SLATE}" stroke-width="3" marker-end="url(#ah)"/>'
    + f'<circle cx="320" cy="75" r="40" fill="#fff" stroke="{ACC}" stroke-width="3"/><line x1="320" y1="75" x2="343" y2="51" stroke="{ACC}" stroke-width="3"/>' + T(320, 140, 'one dial', 18, INK, 'middle')
    + f'<path d="M362,75 L452,75" stroke="{SLATE}" stroke-width="3" marker-end="url(#ah)"/>'
    + f'<rect x="456" y="40" width="170" height="70" rx="6" fill="{TINT}"/>' + T(541, 72, 'the music', 20, INK, 'middle') + T(541, 96, 'or the sound', 16, MUT, 'middle')
    + f'<path d="M541,110 C541,170 95,170 95,115" fill="none" stroke="{SLATE}" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#ah)"/>' + T(318, 178, 'the body answers, the dial moves again', 16, MUT, 'middle'))
_wg, _wh, _ww = table(['Condition, device', 'People', 'The dial', 'Result', 'Status'],
    [[['Stroke walking'], '87', ['music tempo follows', 'the steps, 5 weeks'], ['walking speed', '+0.14 vs +0.06 m/s'], ['FDA cleared,', 'Medicare code 2024']],
     [["Parkinson's"], '41', ['tempo from', 'shoe sensors'], ['more daily steps', 'than brisk walking'], ['RCT, 2025']],
     [['Tinnitus'], '112', ['sound paired with', 'tongue stimulation'], ['58.6% respond', 'single arm'], ['FDA De Novo 2023']]],
    [170, 90, 220, 220, 200], top=30, rh=66, size=18)
S.append(sec(1, 'What works sets the music from a body signal, in a closed loop',
    svgfig(640, 190, _loop, 520) + svgfig(_ww, _wh, _wg, 1060)
    + keybox('The devices that work control ' + kw('one parameter') + ' and read the body back.', 1, '.6em'),
    ref(a('Hutchinson et al., Nat Commun 2024', 'https://www.nature.com/articles/s41467-024-44791-5'), a('CMS HCPCS E3200', 'https://www.cms.gov/files/document/2024-hcpcs-application-summary-biannual-2-2024-non-drug-and-non-biological-items-and-services-pdf.pdf'),
        a('Porciuncula et al., npj Parkinson\'s Dis 2025', 'https://www.nature.com/articles/s41531-025-00952-x'), a('Conlon et al., Nat Commun 2024', 'https://www.nature.com/articles/s41467-024-50473-z')),
    'The contrast. What makes it through trials, FDA and payment is a loop with one dial. InTandem for chronic stroke walking: sensors on the shoes, the music tempo follows the steps, a randomized trial of 87 against an active control, walking speed up 0.14 against 0.06 meters per second (that pair is from the company release, VERIFY against the paper), FDA cleared, Medicare code E3200 in 2024. Parkinson disease: tempo from shoe sensors, 41 patients, more daily steps than brisk walking. Lenire for tinnitus, 112 patients, single arm, 58.6 percent responders among moderate or worse cases, De Novo 2023. Click: one parameter, set from a body signal. That is a biosignal problem, this room\'s problem.'))

# Part 2. Read
S.append(landmark(2, 'read', 'Part 2. Read: can we hear the music in the brain?',
    'In every trial the music was fixed. Before we set it, can we even ' + kw('see') + ' it in the brain?',
    'Landmark. We are at Read, the bottom arrow: from brain activity back to the music. Start with the most famous example, then the state of the art and the one control everyone should show.'))
S.append(sec(2, 'Pink Floyd, played back from electrodes on the brains of 29 patients',
    two(img('bellier_spec_orig.png', 560, 'Spectrogram of the song as heard') + '<div style="height:8px"></div>' + img('bellier_spec_recon.png', 560, 'Spectrogram decoded from the brain'),
        btn('heard', 'bellier_original.mp3', 'pf_heard') + '<br>' + btn('decoded from the brain', 'bellier_nonlinear.mp3', 'pf_dec')
        + line('Rhythm and melody contour survive. The decoder learned this one song.', 20, MUT, 18)),
    ref(a('Bellier et al., PLoS Biology 2023', 'https://doi.org/10.1371/journal.pbio.3002176')),
    'Play the heard clip, then the decoded one. Twenty nine epilepsy patients with electrodes on the brain heard Another Brick in the Wall, and a decoder turned their brain activity back into sound. Honest line: it was trained on this one song. So we can read music back out of the brain. Today is about the other direction: can music be set so that it plays the brain? Spectrograms from Bellier et al. 2023, CC BY.'))
S.append(colk('The brain keeps enough of the music to rebuild it', 2))
S.append(oldk('From brain scans, an AI composer', 2))
S.append(oldk('Your auditory cortex has a population', 2))
_g1, _h1 = hbars([('EEG plus generator', 0.60, True, '0.60'), ('same generator, no EEG', 0.38, False, '0.38'), ('EEG, simple regression', 0.26, False, '0.26')], 0.8, w=300, lab_w=250, bh=34, gap=14, top=50, size=18)
_g2, _h2 = hbars([('fMRI conditioned', 85.4, True, '85.4%'), ('shuffled within category', 73.6, False, '73.6%'), ('shuffled freely', 53.4, False, '53.4%')], 100, w=280, lab_w=250, bh=34, gap=14, top=50, chance=50, size=18)
S.append(sec(2, 'Music decoded from the brain sounds right partly because the generator is good',
    '<div style="display:flex;justify-content:center;gap:20px">'
    + svgfig(620, _h1, T(10, 26, 'EEG to music, CLAP similarity', 20, INK, 'start', 600) + _g1, 600)
    + f'<div class="fragment" data-fragment-index="1">{svgfig(620, _h2 + 10, T(10, 26, "7T fMRI to music, pairwise identification", 20, INK, "start", 600) + _g2, 600)}</div></div>'
    + keybox('Always show the ' + kw('shuffled control') + ': a good generator sounds right without the brain.', 2, '.6em'),
    ref(a('Postolache et al., ICASSP 2025', 'https://arxiv.org/abs/2405.09062'), a('MAAS, NeurIPS 2026', 'https://arxiv.org/abs/2611.12603')),
    'Read, state of the art in two plots. Left, EEG to music on the Stanford NMED data with a ControlNet on a music diffusion model: CLAP 0.60 with EEG, but the same generator with no EEG already gets 0.38, and it does not generalize to unseen songs. Click: right, MAAS at NeurIPS 2026 conditions Stable Audio on 7 tesla fMRI from six auditory regions: 85.4 percent pairwise identification, 73.6 when brain and sound are shuffled within category, 53.4 when shuffled freely, chance 50. Click: the lesson for anyone in this room who decodes.'))
S.append(pick('The brain is read as a graph, too', 2))

# Part 3. Model
S.append(landmark(3, 'model', 'Part 3. Model: what does the listening brain expect?',
    'Read works. To ' + kw('set') + ' music for a brain, we first need to predict the brain from the music.',
    'Landmark. We are at Model, the top arrow. The thread of this part: the brain predicts the next note, the prediction is a small graph of notes, music generators learn that graph, and we can watch it live.'))
S.append(sec(3, 'Listeners do not hear which note it is. They hear how far it is from home.',
    '<iframe class="fe-frame ffh" data-src="figs/far-from-home-en.html" width="1240" height="505" style="border:0;display:block;width:1240px !important;height:505px !important;max-width:none !important;max-height:none !important;flex:0 0 auto;position:relative;left:50%;transform:translateX(calc(-50% - 33px))" title="How far from home"></iframe>'
    + ''.join(f'<span class="fragment ffstep" data-fragment-index="{k}"></span>' for k in range(1, 8))
    ,
    ref(a('Bigand and Poulin-Charronnat, Cognition 2006', 'https://doi.org/10.1016/j.cognition.2005.11.007'), 'After the Pocket Music lesson, how far from home (LAVA MUSIC)'),
    'Live demo in eight steps. The slide opens on step 1, the two songs side by side, play each with its own button as often as you like. Then each click of the clicker plays the next scene and stops (seven fragments drive the demo, the eighth click goes to the next slide). Steps: 1 what sounds wrong, 2 this is right, 3 the note you wait for, 4 three endings, 5 how far from home, 6 notes that stand and lean, 7 find home yourself, 8 your turn. It asks the room what sounds wrong, finds home, changes the ending of Twinkle, Twinkle three ways, shows that do, mi and sol stand while la, fa and re lean back, and ends with Ode to Joy where the room sings the last note. Voice is read by the browser, check the English voice on the presentation laptop, or untick Voice and narrate it yourself. Bigand and Poulin-Charronnat 2006: this sense of finished and unfinished is learned by listening. Meyer 1956: emotion in music lives in expectations delayed or broken. The next slides show the brain measures it, and the live EEG demo is the same pull in data. English version of Zhiqian\'s far from home page (knowledge base, life/music), after the Pocket Music video by LAVA MUSIC.'))
eran = OLDS and [t for t in OLDS if title(t).startswith('Change one chord')][0]
eran_svg = padvb(re.search(r'<svg class="fig".*?</svg>', eran, re.S).group(0))
S.append(sec(3, 'Change one chord, and the brain flags it within 200 ms, trained or not',
    two(eran_svg.replace('<svg class="fig"', '<svg class="fig" style="width:600px;max-width:100%"', 1),
        btn('a regular ending', 'cadence_regular.mp3', 'cad0') + '<br>' + btn('the same, odd last chord', 'cadence_odd.mp3', 'cad1')
        + line('Five chords. In the odd version the last one is a Neapolitan sixth: legal in theory, unexpected at the end.', 20, INK, 16)
        + line('About 150 to 200 ms later, a negative wave over the right front of the head: the ERAN.', 20, MUT, 10)
        + line('It shows up in listeners with no musical training.', 20, MUT, 10), lw=600)
    + keybox('The brain held a ' + kw('prediction') + ' for the next chord, and the odd one broke it.', None, '.6em'),
    ref(a('Koelsch et al., J Cogn Neurosci 2000', 'https://doi.org/10.1162/089892900562183')),
    'Play both. Everyone hears the odd one. Koelsch and colleagues 2000: an unexpected chord at the end of a cadence evokes the early right anterior negativity, about 150 to 200 milliseconds after the chord, in nonmusicians too. The drawing is a schematic of the paper\'s finding, not data. Cadences synthesized for the talk in the style of Koelsch 2000. Bridge: expectation is not only for chords, it is for time too.'))
march = [t for t in OLDS if title(t).startswith('Try it: imagine a march')][0]
march_svg = padvb(re.search(r'<svg class="fig".*?</svg>', march, re.S).group(0))
S.append(sec(3, 'Imagine a march, and the brain adds a beat the sound does not have',
    two(march_svg.replace('<svg class="fig"', '<svg class="fig" style="width:600px;max-width:100%"', 1),
        line('The sound: a steady pulse, 2.4 beats per second. The EEG locks on: a peak at 2.4 Hz.', 20, INK, 0)
        + line('Imagine a march, one two, one two: a new peak at 1.2 Hz.', 20, INK, 12)
        + line('Imagine a waltz, one two three: new peaks at 0.8 and 1.6 Hz.', 20, INK, 12)
        + line('The sound never changed. Try it now, in your head.', 20, MUT, 16), lw=600)
    + keybox('Listening is ' + kw('predicting') + '. To measure it note by note, we need a model of it.', None, '.6em'),
    ref(a('Nozaradan et al., J Neurosci 2011', 'https://doi.org/10.1523/JNEUROSCI.0411-11.2011')),
    'Audience moment. Ask the room to imagine a steady beat as a march, one two, one two. Nozaradan and colleagues 2011, frequency tagging: listening to a 2.4 Hz pulse, the EEG spectrum has a peak at 2.4 Hz. Imagining a march adds a peak at 1.2 Hz, a waltz adds 0.8 and 1.6 Hz. The meter exists only in the brain. Schematic of the paper\'s finding. Bridge: the brain predicts. To measure prediction note by note we need a model of it, and the simplest model is a graph.'))
S.append(pick('A tiny graph is enough to represent a piece of music', 3).replace('A tiny graph is enough to represent a piece of music', 'The simplest model of expectation is a graph: which note follows which', 1))
S.append(pick('Fold 88 keys into 12 scale degrees', 3))
S.append(pick("Occam's razor: the simplest graph already names the tradition", 3))
S.append(colk('Richer nodes beat longer memory', 3))
S.append(colk('The longest memory sounds most like the style', 3))
S.append(stack(pick('A note transition graph predicts the listening brain', 3), oldk('Your brain predicts every next note', 3)))
old = OLDS
kern = [t for t in old if title(t).startswith('Past about eight notes')][0]
kern_svg = padvb(re.search(r'<svg class="fig".*?</svg>', kern, re.S).group(0)).replace('style="width:1000px"', 'style="width:900px;display:block;margin:6px auto 0"')
S.append(sec(3, 'Past about eight notes, a better music model fits the brain worse', kern_svg,
    ref('Redrawn after ' + a('Kern et al., eLife 2022', 'https://doi.org/10.7554/eLife.80935')),
    'Kern and colleagues, eLife 2022: give a music model more and more context, it predicts the next note better and better, but its surprise fits the brain best at short context, under about ten notes, and worse after. The brain tracks short range expectations. Our own data agree: about four notes is enough.'))
S.append(colk('MusicGen is a next token predictor for sound', 3))
S.append(pick('A music generator is a language model, with a pitch graph inside', 3))
S.append(pick('Do music generation models encode music theory?', 3))
S.append(colk('Inside a music generator, music theory has a shape', 3))
S.append(oldk("A music AI's layers line up", 3))
S.append(colk('Predict the next word well, and you predict the brain', 3))
S.append(oldk('Averaged over hundreds of notes', 3))
S.append(demo_slide())
_d = dots(29, 29, 40, 80, cols=10) + T(40, 40, '107 pop songs, 29 listeners', 19, INK, 'start', 600)
_d += dots(21, 19, 380, 80, cols=7) + T(380, 40, 'Bach chorales, 21 musicians', 19, INK, 'start', 600)
_bg, _bh = hbars([('trained model', 0.090, True, '0.090'), ('same model, random weights', 0.004, False, 'about 0')], 0.12, w=190, lab_w=0, bh=30, gap=40, top=80, size=17)
_bg = _bg.replace(f'x="-12"', 'x="0"')
_bars = ''.join([T(640, 40, 'Trained vs untrained, pop', 19, INK, 'start', 600),
                 f'<rect x="640" y="80" width="{0.090 / 0.12 * 300:.0f}" height="30" fill="{ACC}"/>', T(640 + 0.090 / 0.12 * 300 + 10, 101, '0.090 trained', 17, INK),
                 f'<rect x="640" y="150" width="4" height="30" fill="#ACA39A"/>', T(654, 171, 'about 0, random weights', 17, MUT)])
S.append(sec(3, 'A brain readout learned on Bach predicts pop listeners with no refitting',
    svgfig(1000, 200, _d + T(40, 190, 'filled: correlation above 0, readout frozen from 20 Bach listeners', 16, MUT) + f'<g class="fragment" data-fragment-index="1">{_bars}</g>', 1000)
    + keybox('The brain tracks what the model ' + kw('learned') + ', not its architecture.', 2, '.6em'),
    ref('Chen et al., music model and EEG, in progress. Data: Di Liberto 2020, OpenNeuro ds005876, Marion 2021'),
    'Our own work, in progress, preregistered. We read one direction from the middle layer of a symbolic music model on 20 people listening to Bach piano, freeze it, and apply it to other people and other music. Every dot is a listener, filled means the frozen readout predicts that person\'s EEG. 29 of 29 listeners of 107 pop songs, 19 of 21 musicians hearing Bach chorales. Click: the same network with random weights, 0.090 against about 0. Say plainly: per note the correlations are small, the strength is how consistent they are across people. Novelty check: frozen cross dataset transfer has no precedent we found.', st='In progress'))

# Part 4. Write
_rows = [('Vision, 2019', 'model of V4', 'synthesized images', 'monkey V4 sites', True),
         ('Language, 2024', 'GPT based encoder', 'chosen sentences', 'new people, fMRI', True),
         ('Music', 'music model + EEG', 'generated music', 'not done yet', False)]
_w = ''
for i, (dom, enc, stim, ver, ok) in enumerate(_rows):
    y = 60 + i * 95; fr = ' class="fragment" data-fragment-index="1"' if not ok else ''
    _w += f'<g{fr}>' + T(20, y + 40, dom, 21, INK, 'start', 600)
    for j, (txt, x) in enumerate(((enc, 230), (stim, 520), (ver, 810))):
        col = TINT if (ok or j < 2) else '#fff'
        _w += f'<rect x="{x}" y="{y}" width="240" height="64" rx="5" fill="{col}" stroke="{ACC if (not ok and j == 2) else "none"}" stroke-width="2.5" {"stroke-dasharray=\"7 6\"" if (not ok and j == 2) else ""}/>' + T(x + 120, y + 40, txt, 19, ACC if (not ok and j == 2) else INK, 'middle')
        if j < 2: _w += f'<path d="M{x + 242},{y + 32} L{x + 286},{y + 32}" stroke="{SLATE}" stroke-width="2.5" marker-end="url(#ah)"/>'
    _w += '</g>'
_w += T(350, 30, 'model of the brain', 17, MUT, 'middle') + T(640, 30, 'write a stimulus', 17, MUT, 'middle') + T(930, 30, 'verify in brains', 17, MUT, 'middle')
S.append(sec(4, 'Part 4. Write: vision and language already write stimuli for a brain. Music has not.',
    svgfig(1080, 340, _w, 1040) + keybox('The missing step for music: ' + kw('write, then verify') + ' in new listeners.', 2, '.3em'),
    ref(a('Bashivan et al., Science 2019', 'https://doi.org/10.1126/science.aav9436'), a('Tuckute et al., Nat Hum Behav 2024', 'https://doi.org/10.1038/s41562-023-01783-7')),
    'Part Write, the dial on the map. In vision, Bashivan, Kar and DiCarlo 2019 used a model of area V4 to synthesize images that drove neural sites beyond natural images. In language, Tuckute and colleagues 2024 used a GPT based encoding model to pick sentences that drive or suppress the language network, confirmed in new participants. Click: in music, the last box is empty, we found no study through November 2026. (VERIFY both papers against the PDFs before the talk.)'))
S.append(sec(4, 'Turn one dial: the same notes go from shuffled to almost a tune, then Beethoven',
    two(f'<iframe class="fe-frame" data-src="figs/fe-chain.html?autoplay=1" width="600" height="340" style="border:0;display:block" title="Für Elise Markov chain"></iframe>',
        btn('order 0, shuffled', 'fe_shuffled.mp3', 'fd0') + '<br>' + btn('order 1, walk the graph', 'fe_order1.mp3', 'fd1') + '<br>' + btn('Beethoven', 'fe_real.mp3', 'fd2')
        + line('Same notes and rhythm. Only the order moves.', 20, MUT, 16), lw=600),
    ref('Chen et al., Markov graph analysis, in preparation'),
    'Back to the running example from Part Model. One dial, the order of the note graph. Order 0 shuffles the same notes, order 1 walks the tiny graph, and then Beethoven. Same notes and rhythm. A stimulus set with one parameter, the thing the trials lacked.', st='In progress'))
dial = [t for t in old if title(t).startswith('Turn one dial inside a neural music generator')][0]
dial_svg = padvb(re.search(r'<svg class="fig".*?</svg>', dial, re.S).group(0)).replace('#7D55C7', SLATE).replace('style="width:1150px"', 'style="width:1000px;display:block;margin:6px auto 0"')
S.append(sec(4, 'Turn one dial inside MusicGen: same seed, only the tempo words change',
    '<div style="text-align:center">' + btn('slow', 'mg_tempo_slow.mp3', 'mg0') + btn('medium', 'mg_tempo_medium.mp3', 'mg1') + btn('fast', 'mg_tempo_fast.mp3', 'mg2') + '</div>' + dial_svg,
    ref(a('Copet et al., MusicGen, NeurIPS 2023', 'https://arxiv.org/abs/2306.05284')),
    'Same dial in a neural generator. Same seed, only the tempo words in the prompt change. We asked for 60, 100 and 160 beats per minute and measured 59, 100 and 158. Generated for this talk. A dial a body signal could set.'))
S.append(oldk('A neural generator plays the same three melodies', 4))
_g3, _h3 = hbars([('group EEG + model readout', 96, True, '96%'), ('one listener, median', 65, False, 'about 65%'), ('37 known note features', 51, False, '51%')], 100, w=420, lab_w=330, bh=36, gap=16, top=40, chance=50)
_g4, _h4 = hbars([('FCz alone', 96, True, '96%'), ('headband positions', 52, False, '50 to 54%')], 100, w=230, lab_w=200, bh=36, gap=16, top=40, chance=50)
S.append(sec(4, 'The brain can tell real Bach from a model\'s continuation. Note features cannot.',
    '<div style="display:flex;justify-content:center;gap:10px">' + svgfig(820, _h3, T(330, 24, 'pick the real Bach, 80 notes, 93 new passages', 18, MUT) + _g3, 760)
    + f'<div class="fragment" data-fragment-index="1">{svgfig(520, _h4, T(200, 24, "which electrodes", 18, MUT) + _g4, 420)}</div></div>'
    + keybox('The brain is a ' + kw('judge') + ' a generator can be graded by.', 2, '.6em'),
    ref('Chen et al., music model and EEG, in progress. Data: Di Liberto et al., eLife 2020'),
    'The core result, in progress and preregistered. Take a Bach opening, let a music model write continuations, keep the one whose leaps best match the real piece. From the group EEG and the model readout, 80 notes later, we pick the real Bach 96 percent of the time on 93 new passages. One listener alone gets about 65, 19 of 20 above chance. The 37 standard note features do 51, chance. Click: one electrode at FCz is enough, the forehead and behind the ear positions of a consumer headband are at chance. Click: the brain can grade a generator.', st='In progress'))
_g5, _h5 = hbars([('along the brain direction', 4.3, True, '+4.3 semitones'), ('replication, new seed', 4.5, True, '+4.5'), ('largest of 30 random directions', 3.7, False, '3.7')], 5.5, w=420, lab_w=330, bh=36, gap=16, top=40)
S.append(sec(4, 'Push a music model along the brain\'s direction, and its melodies leap further',
    svgfig(1000, _h5, T(330, 24, 'change in mean melodic interval while composing', 18, MUT) + _g5, 900)
    + line('Honest limit: the push changes leap size only, and another model does not rate the result as more brain like.', 20, MUT, 10).replace('text-align:left', 'text-align:center')
    + keybox('A first ' + kw('dial') + ' found by the brain, not yet a dose.', 1, '.5em'),
    ref('Chen et al., music model and EEG, in progress'),
    'A first step from reading to writing. Steer the symbolic model while it composes, along the direction that matched the brain. Mean leap grows by 4.3 semitones, 4.5 in a replication, more than any of 30 random directions, the largest gave 3.7. Say the limit on screen. A dial found by the brain, not yet a dose.', st='In progress'))
S.append(oldk('Prediction: the more natural the order', 4))
S.append(sec(4, 'Close the loop: the brain\'s response chooses the next phrase',
    two(img('eeg_experiment.jpg', 360, 'A listener in an EEG cap'),
        btn('the same piece moving through three settings', 'mg_adapt_mockup.mp3', 'loop')
        + line('Read the response, set the dial, play the next phrase.', 22, INK, 18)
        + line('Baseline EEG already predicts who responds to sleep sound stimulation and to 40 Hz.', 20, MUT, 14), lw=360)
    + keybox('From a playlist to a ' + kw('controller') + '.', 1, '.9em'),
    ref('Sound: a mock up. ' + a('Responder preprint, medRxiv 2025', 'https://www.medrxiv.org/content/10.1101/2025.11.12.25340010v1.full.pdf'), a('Chan et al. 2025', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12552893/')),
    'Vision. The sound is a mock up of the same piece moving through three settings. Read the response, set the dial, play the next phrase. InTandem already does it with steps instead of EEG, and in sleep stimulation and 40 Hz the people who respond can be told apart by their EEG. Click: from a playlist to a controller. Photo: Flexagoon, Wikimedia Commons, CC0.', st='Vision'))
S.append(oldk('One day a music therapy could read like a prescription', 4))
S.append(colk('Our plan: a graph from inside MusicGen', 4))
S.append(sec(4, 'Three experiments you could run next month with these stimuli',
    row(card('EEG lab', '3 orders', 'of the same notes. Fit your own TRF. ' + btn('play', 'fe_order1.mp3', 'x1'), w=300),
        card('ECG or wearables lab', '3 tempi', 'same seed. Heart rate and skin conductance. ' + btn('play', 'mg_tempo_fast.mp3', 'x2'), w=300),
        card('Clinical team', 'log the dial', 'record the settings of whatever music you already play', w=300), top=20)
    + mapfig('write').replace('max-width:100%', 'max-width:100%;max-height:230px', 1)
    + keybox('Stimuli, settings and code are ' + kw('open') + '. Take them.', None, '.2em'),
    '', 'The ask, made concrete, and the map once more with Write lit. An EEG lab can run the three orders tomorrow. A wearables lab can run the three tempi. A clinical team can start by logging what was played, so trials stop being playlists.'))

S.append(f'''<section data-ch="5">
  <h2>Next time she sings, we choose the song, and her brain shows us what she responds to</h2>{status('Vision')}
  {two(img('older_adults_choir.jpg', 440, 'Older adults singing together'),
       line('We can read it. We can model it. Generators give us the dial, and the brain can grade it.', 22, INK, 0)
       + line('Looking for an EEG or physiology lab with older or hearing impaired listeners.', 21, MUT, 14)
       + f'<div style="display:flex;gap:18px;align-items:center;margin-top:16px"><img src="figs/qr_deck.svg" alt="QR code to this deck" style="width:150px;height:150px"><p style="font-family:et-book,Georgia,serif;font-size:20px;color:{MUT};margin:0">this deck<br>or zhiqian.ai, then Talks</p></div>', lw=440)}
  {keybox('AI can now set the music to a ' + kw('dose') + ', and the brain can ' + kw('grade') + ' it.', None, '.6em')}
  <aside class="notes">Close the loop on the opening. She can still sing. Next time, we choose the song, and her brain tells us what she responds to. Three contributions, one line each: sound moves the brain but the music was never set, a small graph of notes tracks the brain, and the brain can grade a generator. The ask: a lab with older or hearing impaired listeners. Stay on this slide for questions so people can scan.</aside>
</section>''')


body = '\n\n'.join(S)
body = body.replace('<section data-ch="3">\n  <h2>Listeners do not hear which note it is.', '<section data-ch="3" data-background-color="#F4F0EA">\n  <h2>Listeners do not hear which note it is.', 1)
body = body.replace('class="status progress"', 'class="status prog"').replace('#7D55C7', SLATE)
body = body.replace('<text x="220" y="50" font-size="16.5" font-weight="600" fill="#1F1E1B" text-anchor="middle" >A tiny classifier', '<text x="220" y="44" font-size="16.5" font-weight="600" fill="#1F1E1B" text-anchor="middle" >A tiny classifier').replace('<text x="220" y="68" font-size="16.5" font-weight="600" fill="#1F1E1B" text-anchor="middle" >reads music theory', '<text x="220" y="66" font-size="16.5" font-weight="600" fill="#1F1E1B" text-anchor="middle" >reads music theory')
head = head.replace('</head>', '<style>.reveal .status.prog{background:#F76902}\n' + '\n'.join(KSCSS) + '</style>\n</head>', 1)
FFJS = '''<script>
(function(){function post(k){var s=Reveal.getCurrentSlide(),f=s&&s.querySelector('iframe.ffh');if(f&&f.contentWindow)f.contentWindow.postMessage({ffstep:k},'*');}
function pos(e){return Array.prototype.indexOf.call(Reveal.getCurrentSlide().querySelectorAll('.ffstep'),e.fragment)+1;}
Reveal.on('fragmentshown',function(e){if(e.fragment.classList.contains('ffstep'))post(pos(e)+1);});
Reveal.on('fragmenthidden',function(e){if(e.fragment.classList.contains('ffstep'))post(pos(e));});})();
</script>
'''
tail = tail.replace('</body>', FFJS + '</body>', 1)
html = head + '\n\n' + body + '\n\n</div></div>\n' + tail
_txt = re.sub(r'&[#a-z0-9]+;', '', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body, flags=re.S)))
bad = [c for c in '—–;' if c in _txt]
open(os.path.join(DECK, 'index.html'), 'w').write(html)
print(len(S), 'main slides', '| style check:', 'dash or semicolon found ' + str(bad) if bad else 'ok')
