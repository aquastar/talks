"""Running example: Fur Elise opening. Per note surprise under a first order chain
counted on the excerpt itself, and audio for the real excerpt vs chain samples.
Run: python3 -I src/fur_elise.py (writes ../shared/audio/fe_*.mp3 and src/fe_surprise.json)"""
import json, math, random, subprocess, wave, struct, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, '..', '..', 'shared', 'audio')
mel = ["E5","D#5","E5","D#5","E5","B4","D5","C5","A4","C4","E4","A4","B4","E4","G#4","B4","C5","E4",
       "E5","D#5","E5","D#5","E5","B4","D5","C5","A4","C4","E4","A4","B4","E4","C5","B4","A4"]
# durations in eighths-ish units (16th = 1): theme rhythm
dur = [1,1,1,1,1,1,1,1,3,1,1,1,3,1,1,1,3,1,
       1,1,1,1,1,1,1,1,3,1,1,1,3,1,1,1,4]
trans = defaultdict(Counter)
for a, b in zip(mel, mel[1:]): trans[a][b] += 1
def p(a, b): return trans[a][b] / sum(trans[a].values())
surprise = [None] + [round(-math.log2(p(a, b)), 3) for a, b in zip(mel, mel[1:])]
json.dump({"melody": mel, "surprise": surprise}, open(os.path.join(HERE, 'fe_surprise.json'), 'w'))
SEMI = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
def freq(n): return 440 * 2 ** ((SEMI[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)
SR = 44100; T16 = 0.16
def render(notes, durs, path):
    buf = []
    for n, d in zip(notes, durs):
        f = freq(n); L = int(SR * T16 * d)
        for i in range(L):
            t = i / SR
            env = math.exp(-3.2 * t) * min(1, i / 200)
            s = sum(a * math.sin(2 * math.pi * f * k * t) for k, a in ((1, .6), (2, .25), (3, .1), (4, .05)))
            buf.append(s * env * .5)
    buf += [0.0] * int(SR * .4)
    wav = path + '.wav'
    with wave.open(wav, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x)) * 30000)) for x in buf))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-b:a', '128k', path + '.mp3'], check=True)
    os.remove(wav)
render(mel, dur, os.path.join(AUD, 'fe_real'))
rng = random.Random(29)
walk = ["E5"]
while len(walk) < len(mel):
    c = trans[walk[-1]]; walk.append(rng.choices(list(c), weights=list(c.values()))[0])
render(walk, dur, os.path.join(AUD, 'fe_order1'))
shuf = mel[:]; rng.shuffle(shuf)
render(shuf, dur, os.path.join(AUD, 'fe_shuffled'))
d = json.load(open(os.path.join(HERE, 'fe_surprise.json'))); d['order1'] = walk; d['shuffled'] = shuf
json.dump(d, open(os.path.join(HERE, 'fe_surprise.json'), 'w'))
print(' '.join(walk))
