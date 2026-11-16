# Run with a venv that has torch, torchaudio, transformers, scipy, librosa (CPU is fine, about 5 min per clip).
# MusicGen-melody on CPU: same prompt and seed, conditioned on three versions of the Fur Elise notes
import torch, scipy.io.wavfile as w, subprocess, numpy as np, sys
from transformers import AutoProcessor, MusicgenMelodyForConditionalGeneration
A = '/home/user/music-to-brain/shared/audio'; out = sys.argv[1]
proc = AutoProcessor.from_pretrained("facebook/musicgen-melody")
model = MusicgenMelodyForConditionalGeneration.from_pretrained("facebook/musicgen-melody")
sr = model.config.audio_encoder.sampling_rate
def load(name):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f'{A}/{name}.mp3', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    return x[:sr * 8]
for tag in ['fe_shuffled', 'fe_order1', 'fe_real']:
    torch.manual_seed(11)
    inp = proc(audio=load(tag), sampling_rate=sr, text=["gentle solo piano, classical, warm room"], padding=True, return_tensors="pt")
    a = model.generate(**inp, do_sample=True, guidance_scale=3.0, max_new_tokens=400)
    w.write(f'{out}/mgmel_{tag}.wav', sr, a[0, 0].numpy()); print(tag, flush=True)
