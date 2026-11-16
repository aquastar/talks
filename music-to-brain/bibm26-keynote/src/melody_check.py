"""Acceptance test for the MusicGen melody dial: chroma correlation of each generated clip with its own
conditioning melody and with the other two. Writes melody_check.json (numbers shown on the melody slide).
Run in a venv with librosa: python -I melody_check.py GENERATED_DIR"""
import json, os, subprocess, sys
import numpy as np, librosa
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, '..', '..', 'shared', 'audio')
gen = sys.argv[1] if len(sys.argv) > 1 else A
def mp3(n, sr=22050):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(A, n + '.mp3'), '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
tags = ['fe_shuffled', 'fe_order1', 'fe_real']; out = {}
for t in tags:
    y = mp3('mgmel_' + t); cy = librosa.feature.chroma_cqt(y=y, sr=22050)
    row = {}
    for o in tags:
        x = mp3(o)[:len(y)]; cx = librosa.feature.chroma_cqt(y=x, sr=22050); n = min(cy.shape[1], cx.shape[1])
        row[o] = round(float(np.corrcoef(cy[:, :n].flatten(), cx[:, :n].flatten())[0, 1]), 3)
    out[t] = row
json.dump(out, open(os.path.join(HERE, 'melody_check.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
