"""Extract real CHB-MIT clips (patient chb01) for the running example. Input EDF files from PhysioNet chbmit 1.0.0.
Usage: python3 -I edf_clips.py EDF_DIR  -> writes clips.json next to this file."""
import json, os, sys
import numpy as np
def read_edf(p):
    f = open(p, 'rb'); h = f.read(256)
    ns = int(h[252:256]); nrec = int(h[236:244]); dur = float(h[244:252])
    hs = f.read(ns * 256)
    def fld(off, w): return [hs[off*ns + i*w: off*ns + (i+1)*w].decode().strip() for i in range(ns)]
    lab = [hs[i*16:(i+1)*16].decode().strip() for i in range(ns)]
    o = 16 + 80 + 8
    pmin = np.array(list(map(float, [hs[o*ns+i*8:o*ns+i*8+8].decode() for i in range(ns)]))); o += 8
    pmax = np.array(list(map(float, [hs[o*ns+i*8:o*ns+i*8+8].decode() for i in range(ns)]))); o += 8
    dmin = np.array(list(map(float, [hs[o*ns+i*8:o*ns+i*8+8].decode() for i in range(ns)]))); o += 8
    dmax = np.array(list(map(float, [hs[o*ns+i*8:o*ns+i*8+8].decode() for i in range(ns)]))); o += 8 + 80
    nsamp = list(map(int, [hs[o*ns+i*8:o*ns+i*8+8].decode() for i in range(ns)]))
    raw = np.frombuffer(f.read(), dtype='<i2')[: nrec * sum(nsamp)].reshape(nrec, sum(nsamp))
    sig = raw.reshape(nrec, ns, nsamp[0]).transpose(1, 0, 2).reshape(ns, -1).astype(float)
    g = (pmax - pmin) / (dmax - dmin)
    return lab, (sig - dmin[:, None]) * g[:, None] + pmin[:, None], nsamp[0] / dur
D = sys.argv[1]
CH = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP2-F8', 'F8-T8', 'T8-P8-0', 'P8-O2']
out = {}
for name, fn, t0, secs in [('seizure', 'chb01_03', 2986, 30), ('preictal', 'chb01_03', 2396, 10), ('interictal', 'chb01_01', 1800, 10)]:
    lab, x, fs = read_edf(os.path.join(D, fn + '.edf'))
    rows = []
    for c in CH:
        i = lab.index(c) if c in lab else lab.index(c.replace('-0', ''))
        seg = x[i, int(t0*fs): int((t0+secs)*fs)]
        step = 2 if secs <= 10 else 4
        rows.append([round(v, 1) for v in seg[::step]])
    out[name] = {'file': fn, 'start_s': t0, 'secs': secs, 'fs': fs, 'step': 2 if secs <= 10 else 4, 'channels': [c.replace('-0', '') for c in CH], 'uV': rows}
    print(name, fn, t0, fs, np.percentile(np.abs(np.array(rows)), 99))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clips.json'), 'w'))
