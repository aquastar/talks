# Run with a venv that has torch, torchaudio, transformers, scipy, librosa (CPU is fine, about 5 min per clip).
# MusicGen-small on CPU: same prompt and seed, only the tempo word changes.
import torch, scipy.io.wavfile as w, sys
from transformers import AutoProcessor, MusicgenForConditionalGeneration
out = sys.argv[1]
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
sr = model.config.audio_encoder.sampling_rate
for tag, tempo in [("slow", "very slow, 60 bpm"), ("medium", "moderate, 100 bpm"), ("fast", "very fast, 160 bpm")]:
    torch.manual_seed(7)
    prompt = f"solo piano melody, calm and simple, {tempo}"
    x = proc(text=[prompt], padding=True, return_tensors="pt")
    a = model.generate(**x, do_sample=True, guidance_scale=3.0, max_new_tokens=400)
    w.write(f"{out}/mg_tempo_{tag}.wav", sr, a[0, 0].numpy())
    print(tag, prompt, flush=True)
