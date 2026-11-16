"""Recompute the per note check shown in eeg-demo (scatter panel), same rule as its JS:
3 public domain songs, notes after the first 1 s, response = mean over the 11 highlighted
channels of the song averaged EEG from 0.1 to 0.35 s after the note, Pearson r with the note's
MusicGen surprise (z within song, n[3]) and with the untrained random model's surprise (n[4]),
two sided permutation count over 2000 shuffles. Writes eeg_pernote.json."""
import json, re, os, random, math
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, '..', '..', 'eeg-demo', 'index.html')).read()
D = json.loads(re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>', t, re.S).group(1))
HI = [c in D['highlight'] for c in D['ch']]
pts = []
for s in D['songs']:
    tr = [sum(r[i] for r, h in zip(s['eeg'], HI) if h) / sum(HI) for i in range(len(s['eeg'][0]))]
    for n in s['notes']:
        if n[0] < 1.0: continue
        a = round((n[0] + 0.1 - s['eeg_t0']) * D['fs']); b = round((n[0] + 0.35 - s['eeg_t0']) * D['fs'])
        if a < 0 or b >= len(tr): continue
        pts.append((n[3], n[4], sum(tr[a:b + 1]) / (b - a + 1)))
def pr(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy)
NULL = []
def perm(x, y, r, n=2000, seed=12345):
    rng = random.Random(seed); yy = list(y); k = 0
    for _ in range(n):
        rng.shuffle(yy); v = pr(x, yy); k += abs(v) >= abs(r)
        if not NULL or len(NULL) < n: NULL.append(round(v, 4))
    return k
x, xt, y = [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts]
r1, r2 = pr(x, y), pr(xt, y)
out = {'n_notes': len(pts), 'songs': [s['title'] for s in D['songs']], 'r_musicgen': round(r1, 3), 'perm_musicgen_of_2000': perm(x, y, r1),
       'r_random_model': round(r2, 3), 'perm_random_of_2000': perm(xt, y, r2)}
out['null_r'] = NULL[:2000]
json.dump(out, open(os.path.join(HERE, 'eeg_pernote.json'), 'w'), indent=1); print(out)
