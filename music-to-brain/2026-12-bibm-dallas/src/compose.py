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
    return t[:h_end] + '\n  <div class="ksw">' + t[h_end:cut] + '</div>\n  ' + t[cut:]
def colk(start, ch, add=''):
    x = pick(start, ch, add)
    return re.sub(r'(<span class="status [^"]*">)Backup, ', r'\1', x)

# ---------- the slides ----------
S = []
S.append(f'''<section class="title full" data-ch="0" data-background-color="#FBFAF7">
  <div style="margin:120px 80px 0;text-align:left">
    <p style="font:600 15px Fira Sans,sans-serif;letter-spacing:.12em;color:{MUT};text-transform:uppercase;margin:0">Keynote · AI4BioSig Workshop · IEEE BIBM 2026 · Dallas</p>
    <h1 style="font-family:et-book,Georgia,serif;font-weight:400;font-size:86px;line-height:1.05;color:{INK};margin:26px 0 0;text-transform:none">The Music That<br>Plays the <span style="color:#F76902">Brain</span></h1>
    <div style="width:120px;height:3px;background:#F76902;margin:34px 0 26px"></div>
    <p style="font-family:et-book,Georgia,serif;font-size:26px;color:{INK};margin:0">Zhiqian Chen</p>
    <p style="font-family:et-book,Georgia,serif;font-size:20px;color:{MUT};margin:4px 0 0">Department of Computer Science, Rochester Institute of Technology</p>
  </div>
  <aside class="notes">Open with sound, not with me. Go straight to the next slide.</aside>
</section>''')

S.append(sec(0, 'Pink Floyd, played back from electrodes on the brains of 29 patients',
    two(img('bellier_spec_orig.png', 560, 'Spectrogram of the song as heard') + '<div style="height:8px"></div>' + img('bellier_spec_recon.png', 560, 'Spectrogram decoded from the brain'),
        btn('heard', 'bellier_original.mp3', 'pf_heard') + '<br>' + btn('decoded from the brain', 'bellier_nonlinear.mp3', 'pf_dec')
        + line('Rhythm and melody contour survive. The decoder learned this one song.', 20, MUT, 18)),
    ref(a('Bellier et al., PLoS Biology 2023', 'https://doi.org/10.1371/journal.pbio.3002176')),
    'Play the heard clip, then the decoded one. Twenty nine epilepsy patients with electrodes on the brain heard Another Brick in the Wall, and a decoder turned their brain activity back into sound. Honest line: it was trained on this one song. So we can read music back out of the brain. Today is about the other direction: can music be set so that it plays the brain? Spectrograms from Bellier et al. 2023, CC BY.'))

S.append(sec(0, 'Many people with advanced dementia can still sing the hymns of their youth',
    two(img('older_adults_choir.jpg', 520, 'Older adults singing together'),
        line('Music reaches a brain that has lost almost everything else.', 26, INK, 0)
        + line('What if we could choose the song for one of them, and watch her brain answer?', 26, MUT, 26)),
    ref(a('Jacobsen et al., Brain 2015', 'https://doi.org/10.1093/brain/awv135')),
    'Musical memory is among the last to go in Alzheimer disease, Jacobsen 2015 shows the regions that hold it are among the least affected. Pose the question and leave it open: what if we could choose the song, and watch her brain answer? We come back to her at the end. Photo: Peter van der Sluijs, Wikimedia Commons, CC BY-SA 4.0.'))

S.append(oldk('Same notes, same sound', 0))
S.append(sec(0, 'Three findings in the next 40 minutes',
    row(card('1 · Why now', 'Sound moves<br>the brain', 'but music used as a fixed stimulus rarely moves the clinic', w=300),
        card('2 · Model', 'A small graph', 'of note transitions names a style and tracks the listening brain', frag=1, w=300),
        card('3 · Write', 'A dial, and<br>a judge', 'generators can be turned, and the brain can tell real music from a generated one', frag=2, w=300), top=40)
    + keybox('AI can now set the music to a ' + kw('dose') + ', and the brain can ' + kw('grade') + ' it.', 3, '1.2em'),
    '', 'Three findings, one per part. First, sound reliably moves brain signals, but the big trials of music as medicine are mostly null, because the music was never set. Second, a small graph of which note follows which already names a style and tracks the brain. Third, generators now give us a dial, and the brain can act as the judge. Click: the one line to remember. The map on top, Read, Model, Write, follows us through the talk.'))

S.append(pick('Part 2. Hearing loss: a quiet epidemic', 1).replace('Part 2. Hearing loss', 'Hearing loss', 1))
S.append(oldk('Music releases dopamine twice', 1))
S.append(oldk("A steady beat can make a person with Parkinson", 1))
S.append(pick('Sound acts on the brain', 1))
S.append(pick('Music already acts on the brain, as medicine', 1))

S.append(oldk('In dementia, music lifts mood slightly', 1))
S.append(sec(1, 'The biggest, best controlled trials of music and sound came back null',
    line('Expected: music helps. Measured, in the four largest recent trials:', 21, MUT, 4).replace('text-align:left', 'text-align:center')
    + row(card('40 Hz light and sound · Alzheimer', '673 people', '12 months at home. Missed its primary endpoint (CTAD, Nov 2026)', frag=1, w=230),
          card('Group music therapy · dementia', '1,021 residents', '6 countries. No change in depression at 6 months', frag=1, w=230),
          card('Slow music · ICU', '158 patients', 'No better than a silent track on delirium, pain, anxiety', frag=1, w=230),
          card('Parent singing · preterm', '206 infants', 'No effect on language at 24 months', frag=1, w=230))
    + keybox('The larger the trial and the better the control, the closer the effect to ' + kw('zero') + '.', 2, '.9em'),
    ref(a('Cognito HOPE, NCT05637801', 'https://clinicaltrials.gov/study/NCT05637801'), a('MIDDEL, Lancet Healthy Longevity 2025', 'https://doi.org/10.1016/j.lanhl.2025.100783'),
        a('JAMA Intern Med 2025', 'https://doi.org/10.1001/jamainternmed.2025.5263'), a('LongSTEP, JAMA Netw Open 2024', 'https://doi.org/10.1001/jamanetworkopen.2024.10721')),
    'Ask the room first: hands up if you expect music to help in these trials. Click: the four largest recent trials. HOPE, 40 Hz light and sound for Alzheimer disease, 673 people, missed its primary endpoint, presented at CTAD in November 2026, a mild subgroup looked better but that is unadjusted, say only that the primary endpoint was missed until the paper is out (VERIFY numbers against the CTAD slides before the talk). MIDDEL, 1,021 care home residents in six countries, music therapy and choir did not change depression at six months, the country predicted more than the intervention. ICU, 158 ventilated older adults, slow music no better than a silent track through the same headphones. LongSTEP, preterm infants, parent singing, no language effect at 24 months. Click: the pattern. Not that music does nothing, but that music given as a fixed playlist is not a controlled dose.'))

S.append(sec(1, 'What works sets the music from a body signal, in a closed loop',
    two(img('gait_rehab.jpg', 300, 'Gait training with a therapist'),
        line('<b>Stroke walking.</b> The beat follows the patient\'s steps. RCT of 87, FDA cleared, a Medicare code since 2024.', 21, INK, 0)
        + line('<b>Parkinson\'s.</b> Music tempo adapted from shoe sensors raised daily steps, RCT of 41.', 21, INK, 14)
        + line('<b>Tinnitus.</b> Sound paired with tongue stimulation, FDA De Novo 2023.', 21, INK, 14), lw=300)
    + keybox('The devices that work control ' + kw('one parameter') + ' and read the body back.', 1, '.9em'),
    ref(a('Hutchinson et al., Nat Commun 2024', 'https://www.nature.com/articles/s41467-024-44791-5'), a('CMS HCPCS E3200', 'https://www.cms.gov/files/document/2024-hcpcs-application-summary-biannual-2-2024-non-drug-and-non-biological-items-and-services-pdf.pdf'),
        a('Porciuncula et al., npj Parkinson\'s Dis 2025', 'https://www.nature.com/articles/s41531-025-00952-x'), a('Conlon et al., Nat Commun 2024', 'https://www.nature.com/articles/s41467-024-50473-z')),
    'The contrast. What does make it through trials, FDA and payment is specific. InTandem for chronic stroke walking: the beat adapts to the steps, a randomized trial of 87 in Nature Communications 2024, FDA cleared, and Medicare created code E3200 in 2024. Parkinson disease: tempo adapted in real time from shoe sensors, 41 patients, more daily steps. Lenire for tinnitus, De Novo 2023, a single arm trial. Click: one parameter, set from a body signal. That is a biosignal problem, this room\'s problem. Photo: U.S. Navy, public domain.'))

S.append(oldk('Four ways the field studies music and the brain', 1))
S.append(sec(1, 'In every trial the music was fixed. The missing piece is a dial.',
    row(card('Read', 'brain to music', 'decode what was heard', w=260),
        card('Model', 'music to brain', 'predict the response to each note', w=260),
        card('Write', 'set the music', 'choose music for a brain response, then check it', frag=1, w=260), top=50)
    + keybox('Read and Model have evidence. ' + kw('Write') + ' is the step nobody has closed for music.', 2, '1.2em'),
    '', 'Landmark. Three steps, and the bar on top of every slide shows where we are. Read: decode music from the brain. Model: predict the brain from the music. Click: Write, choose music to get a brain response and check that it happened. Click: the first two have evidence, the third has not been closed for music. Vision and language have done it, we will see that in Part Write.', cls='breath'))

S.append(sec(2, 'The brain can be read back into music, and the generator sets the ceiling',
    row(card('EEG to music · Sony CSL', 'CLAP 0.60', 'with EEG, against 0.38 for the same generator without it. Fails on unseen songs', w=330),
        card('7T fMRI to music · MAAS', '85.4%', 'pairwise identification. 53.4% when brain and sound are shuffled, chance 50%', frag=1, w=330), top=34)
    + keybox('Always show the ' + kw('shuffled control') + ': a good generator sounds right without the brain.', 2, '1em'),
    ref(a('Postolache et al., ICASSP 2025', 'https://arxiv.org/abs/2405.09062'), a('MAAS, NeurIPS 2026', 'https://arxiv.org/abs/2611.12603')),
    'Read, the state of the art in two lines. EEG to music on the Stanford NMED data: a ControlNet on a music diffusion model, CLAP score 0.60, but the same model with no EEG already gets 0.38, and it does not generalize to songs it did not train on. Click: MAAS, NeurIPS 2026, conditions Stable Audio directly on 7 tesla fMRI, 85.4 percent pairwise identification, and only 53.4 when brain and sound are shuffled. Click: the lesson for anyone in this room who decodes: a strong generator sounds right without the brain, so the shuffled control is the result.'))

S.append(oldk('From brain scans, an AI composer', 2))
S.append(colk('The brain keeps enough of the music to rebuild it', 2))
S.append(pick('Knowledge is not only text', 3, 'In this talk: the point of this slide is Meyer, emotion lives in expectation. That is what Part Model measures.'))
S.append(pick('A music generator is a language model, with a pitch graph inside', 3))
S.append(pick('Do music generation models encode music theory?', 3))
S.append(colk('MusicGen is a next token predictor for sound', 3))
S.append(colk('Inside a music generator, music theory has a shape', 3))
S.append(colk('A new idea is a new edge', 3))
S.append(pick('A tiny graph is enough to represent a piece of music', 3))
S.append(pick('Fold 88 keys into 12 scale degrees', 3))
S.append(pick("Occam's razor: the simplest graph already names the tradition", 3))
S.append(colk('Richer nodes beat longer memory', 3))
S.append(colk('The longest memory sounds most like the style', 3))
S.append(oldk('Your auditory cortex has a population', 3))
S.append(oldk('Your brain predicts every next note', 3))
S.append(pick('A note transition graph predicts the listening brain', 3))

old = top_sections(open(os.path.join(DECK, '..', '2026-12-01-bibm-dallas', 'index.html')).read())
kern = [t for t in old if title(t).startswith('Past about eight notes')][0]
kern_svg = re.search(r'<svg class="fig".*?</svg>', kern, re.S).group(0).replace('style="width:1000px"', 'style="width:900px;display:block;margin:6px auto 0"')
S.append(sec(3, 'Past about eight notes, a better music model fits the brain worse', kern_svg,
    ref('Redrawn after ' + a('Kern et al., eLife 2022', 'https://doi.org/10.7554/eLife.80935')),
    'Kern and colleagues, eLife 2022: give a music model more and more context, it predicts the next note better and better, but its surprise fits the brain best at short context, under about ten notes, and worse after. The brain tracks short range expectations. Our own data agree: about four notes is enough. Keep this in mind for the demo.'))

S.append(oldk('Try it: imagine a march', 3))
S.append(oldk('Change one chord, and the brain answers', 3))
S.append(oldk("A music AI's layers line up", 3))
S.append(colk('Predict the next word well, and you predict the brain', 3))
S.append(oldk('Averaged over hundreds of notes', 3))
S.append(demo_slide())

S.append(sec(3, 'A brain readout learned on Bach predicts pop listeners with no refitting',
    row(card('107 pop songs', '29 of 29', 'listeners positive, readout learned only on 20 Bach listeners', w=280),
        card('Bach chorales', '19 of 21', 'listeners positive, same readout, nothing refit', w=280),
        card('Same model, untrained', 'about 0', 'the random twin does not transfer', frag=1, w=280), top=34)
    + keybox('The brain tracks what the model ' + kw('learned') + ', not its architecture.', 2, '1em'),
    ref('Chen et al., music model and EEG, in progress. Data: Di Liberto 2020, OpenNeuro ds005876, Marion 2021'),
    'Our own work, in progress, preregistered. We take a symbolic music model, read one direction from its middle layer on 20 people listening to Bach piano, freeze it, and apply it to other people and other music with no refitting. 29 of 29 listeners of 107 pop songs, 19 of 21 musicians hearing Bach chorales. Click: the same network with random weights does not transfer. Say plainly: per note the correlations are small, the strength is in how consistent they are across listeners. Novelty check: frozen cross dataset transfer has no precedent we found, Noguchi 2026 lists it as untested.', st='In progress'))

S.append(pick('The brain is read as a graph, too', 3))

S.append(sec(4, 'Vision and language already write stimuli for a brain response. Music has not.',
    row(card('Vision · 2019', 'Images', 'synthesized from a model of V4 drive single sites beyond any natural image', w=300),
        card('Language · 2024', 'Sentences', 'chosen by a GPT based encoder drive or suppress the language network in new people', w=300),
        card('Music', 'none yet', 'no study has optimized music on an encoder and verified it in new listeners', frag=1, w=300), top=34)
    + keybox('The missing step: ' + kw('write, then verify') + ' in new listeners.', 2, '1em'),
    ref(a('Bashivan et al., Science 2019', 'https://doi.org/10.1126/science.aav9436'), a('Tuckute et al., Nat Hum Behav 2024', 'https://doi.org/10.1038/s41562-023-01783-7')),
    'Part Write. In vision, Bashivan, Kar and DiCarlo 2019 used a model of area V4 to synthesize images that drove neural sites beyond natural images. In language, Tuckute and colleagues 2024 used a GPT based encoding model to pick sentences that drive or suppress the language network, confirmed in new participants with fMRI. Click: in music we found none, in peer review or preprints through November 2026. One in silico preprint runs songs through Meta TRIBE v2 with no human data. That is the gap. (VERIFY both papers against the PDFs before the talk.)'))

S.append(sec(4, 'The brain can tell real Bach from a model\'s continuation. Note features cannot.',
    row(card('Group EEG, 80 notes', '96%', 'real Bach picked over a matched continuation from the same opening, 93 new passages', w=300),
        card('37 known note features', '51%', 'the same test without a music model, chance 50%', w=300),
        card('One electrode', 'FCz', 'is enough. A forehead headband position is at chance', frag=1, w=300), top=34)
    + keybox('The brain is a ' + kw('judge') + ' a generator can be graded by.', 2, '1em'),
    ref('Chen et al., music model and EEG, in progress. Data: Di Liberto et al., eLife 2020'),
    'The core result of the talk, in progress and preregistered. Take a Bach opening, let a music model write continuations, keep the one whose leaps best match the real piece. From the group EEG and the model\'s readout, 80 notes later, we pick the real Bach 96 percent of the time on 93 new passages. The 37 standard note features do 51, chance. A single listener gets about 65 percent, 19 of 20 above chance. Click: one electrode at FCz is enough, the forehead and behind the ear positions of a consumer headband are at chance. Click: so the brain can grade a generator. That is the Write step\'s missing half.', st='In progress'))

S.append(sec(4, 'Push a music model along the brain\'s direction, and its melodies leap further',
    row(card('Along the brain direction', '+4.3', 'semitones mean interval, replicated with a new seed (+4.5)', w=300),
        card('Thirty random directions', 'at most 3.7', 'same push, same model', w=300), top=40)
    + line('Honest limit: the push changes leap size only, and another model does not rate the result as more brain like.', 20, MUT, 26).replace('text-align:left', 'text-align:center')
    + keybox('A first ' + kw('dial') + ' found by the brain, not yet a dose.', 1, '.8em'),
    ref('Chen et al., music model and EEG, in progress'),
    'A first step from reading to writing. Steer the symbolic model while it composes, along the direction that matched the brain. Mean leap grows by 4.3 semitones, 4.5 in a replication, more than any of 30 random directions. Say the limit on screen: it moves leap size only, and when another model reads the new music it is not more brain like. So this is a dial found by the brain, not yet a dose.', st='In progress'))

S.append(sec(4, 'Turn one dial: the same notes go from shuffled to almost a tune, then Beethoven',
    two(f'<iframe class="fe-frame" data-src="figs/fe-chain.html?autoplay=1" width="600" height="340" style="border:0;display:block" title="Für Elise Markov chain"></iframe>',
        btn('order 0, shuffled', 'fe_shuffled.mp3', 'fd0') + '<br>' + btn('order 1, walk the graph', 'fe_order1.mp3', 'fd1') + '<br>' + btn('Beethoven', 'fe_real.mp3', 'fd2')
        + line('Same notes and rhythm. Only the order moves.', 20, MUT, 16), lw=600),
    ref('Chen et al., Markov graph analysis, in preparation'),
    'Back to the running example. One dial, the order of the note graph. Order 0 shuffles the same notes, order 1 walks the tiny graph from the start of Part Model, and then Beethoven. Same notes and rhythm. This is a stimulus set with one parameter, the thing the trials lacked.', st='In progress'))

dial = [t for t in old if title(t).startswith('Turn one dial inside a neural music generator')][0]
dial_svg = re.search(r'<svg class="fig".*?</svg>', dial, re.S).group(0).replace('#7D55C7', SLATE).replace('style="width:1150px"', 'style="width:1000px;display:block;margin:6px auto 0"')
S.append(sec(4, 'Turn one dial inside MusicGen: same seed, only the tempo words change',
    '<div style="text-align:center">' + btn('slow', 'mg_tempo_slow.mp3', 'mg0') + btn('medium', 'mg_tempo_medium.mp3', 'mg1') + btn('fast', 'mg_tempo_fast.mp3', 'mg2') + '</div>' + dial_svg,
    ref(a('Copet et al., MusicGen, NeurIPS 2023', 'https://arxiv.org/abs/2306.05284')),
    'Same dial in a neural generator. Same seed, only the tempo words in the prompt change. We asked for 60, 100 and 160 beats per minute and measured 59, 100 and 158. Generated for this talk. A dial a body signal could set.'))

S.append(oldk('A neural generator plays the same three melodies', 4))
S.append(oldk('Prediction: the more natural the order', 4))
S.append(sec(4, 'Close the loop: the brain\'s response chooses the next phrase',
    two(img('eeg_experiment.jpg', 360, 'A listener in an EEG cap'),
        btn('the same piece moving through three settings', 'mg_adapt_mockup.mp3', 'loop')
        + line('Read the response, set the dial, play the next phrase.', 22, INK, 18)
        + line('Baseline EEG already predicts who responds to sleep sound stimulation and to 40 Hz.', 20, MUT, 14), lw=360)
    + keybox('From a playlist to a ' + kw('controller') + '.', 1, '.9em'),
    ref('Sound: a mock up. ' + a('Responder preprint, medRxiv 2025', 'https://www.medrxiv.org/content/10.1101/2025.11.12.25340010v1.full.pdf'), a('Chan et al. 2025', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12552893/')),
    'Vision. The sound is a mock up of the same piece moving through three settings. Read the response, set the dial, play the next phrase. Two reasons this is not science fiction: InTandem already does it with steps instead of EEG, and in sleep stimulation and 40 Hz the people who respond can be told apart by their EEG. Click: from a playlist to a controller. Photo: Flexagoon, Wikimedia Commons, CC0.', st='Vision'))

S.append(oldk('One day a music therapy could read like a prescription', 4))
S.append(colk('Our plan: a graph from inside MusicGen', 4))
S.append(sec(4, 'Three experiments you could run next month with these stimuli',
    row(card('EEG lab', '3 orders', 'of the same notes. Fit your own TRF. ' + btn('play', 'fe_order1.mp3', 'x1'), w=300),
        card('ECG or wearables lab', '3 tempi', 'same seed. Heart rate and skin conductance. ' + btn('play', 'mg_tempo_fast.mp3', 'x2'), w=300),
        card('Clinical team', 'log the dial', 'record the settings of whatever music you already play', w=300), top=34)
    + keybox('Stimuli, settings and code are ' + kw('open') + '. Take them.', None, '1em'),
    '', 'The ask, made concrete. An EEG lab can run the three orders tomorrow. A wearables lab can run the three tempi. A clinical team can start by logging what was played, so trials stop being playlists. All stimuli are on the stimuli page linked from the last slide.'))

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
body = body.replace('class="status progress"', 'class="status prog"').replace('#7D55C7', SLATE)
head = head.replace('</head>', '<style>.reveal .status.prog{background:#F76902}\n' + '\n'.join(KSCSS) + '</style>\n</head>', 1)
html = head + '\n\n' + body + '\n\n</div></div>\n' + tail
_txt = re.sub(r'&[#a-z0-9]+;', '', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body, flags=re.S)))
bad = [c for c in '—–;' if c in _txt]
open(os.path.join(DECK, 'index.html'), 'w').write(html)
print(len(S), 'main slides', '| style check:', 'dash or semicolon found ' + str(bad) if bad else 'ok')
