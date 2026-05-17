# TTS Engine Comparison: German on CPU (4 vCPU, 8 GB RAM, no GPU)

**Updated:** 2026-05-17
**Hardware:** 4 vCPU, 8 GB RAM, 10 GB disk, no GPU
**Test text:** German passages (~10-30 seconds of speech)

---

## Tested Engines (with results)

### 1. Piper TTS + Thorsten — BEST PICK

| Metric | Value |
|--------|-------|
| **Model size** | 109 MB (high quality), 74 MB (emotional medium) |
| **Install time** | ~2 min |
| **RAM usage** | ~200 MB |
| **Realtime factor** | 2.9x (32s audio in 11s) |
| **German quality** | ⭐⭐⭐⭐ — Clear, natural male voice |
| **Speaker variety** | 8 emotional voices (amused, angry, disgusted, drunk, neutral, sleepy, surprised, whisper) |
| **License** | GPL-3.0 (engine) + CC0 (voice data) — ✅ Commercial OK |
| **Disk footprint** | ~200 MB total |
| **Female voice** | No |

**Verdict:** Best balance of speed, size, reliability, and licensing. The 74 MB emotional medium model gives 8 distinct voices in a tiny package. Install script: `scripts/install-piper.sh`.

---

### 2. Kokoro-82M German (Martin)

| Metric | Value |
|--------|-------|
| **Model size** | 311 MB (ONNX), 511 KB (voice pack) |
| **Install time** | ~3 min |
| **RAM usage** | ~400 MB |
| **Realtime factor** | 2.9x (33.9s audio in 11.7s) |
| **German quality** | ⭐⭐⭐⭐ — Smoother timbre, slightly less crisp |
| **Speaker variety** | 1 voice (Martin, male) |
| **License** | Permissive — ✅ Commercial OK |
| **Disk footprint** | ~350 MB total |
| **Female voice** | No |

**Verdict:** Smoother timbre than Piper, same speed. Worth keeping alongside Piper for voice diversity. Only 1 voice limits variety.

---

### 3. OmniVoice (k2-fsa) — BEST MULTI-SPEAKER + FEMALE VOICE

| Metric | Value |
|--------|-------|
| **Model size** | 2.45 GB (main) + 0.81 GB (audio tokenizer) = 3.27 GB |
| **Install time** | ~5 min (PyTorch CPU + deps) |
| **RAM usage** | ~2-3 GB during inference |
| **Realtime factor** | ~1.0x (num_step=16) |
| **German quality** | ⭐⭐⭐⭐ — Natural, clear, good prosody |
| **Speaker variety** | Unlimited via voice design tags + voice cloning + auto voice |
| **Languages** | 646 languages (German: 21,927h training data) |
| **License** | Apache-2.0 — ✅ Commercial OK |
| **Disk footprint** | ~5 GB total (1.7 GB venv + 3.3 GB model) |
| **Female voice** | Yes |

**Voice design mode** (no reference audio needed): describe voice attributes with predefined tags.
Valid tags: `female`, `male`, `child`, `teenager`, `young adult`, `middle-aged`, `elderly`, `low pitch`, `moderate pitch`, `high pitch`, `very low pitch`, `very high pitch`, `whisper`, `american/british/australian/canadian/indian/chinese/japanese/korean/portuguese/russian accent`

Example: `"female, young adult, moderate pitch"` or `"male, middle-aged, low pitch"` or `"female, teenager, high pitch, whisper"`

**Non-verbal symbols:** `[laughter]`, `[sigh]`, `[laughter]`, `[cough]` etc. in text.

**CLI:** `python -m omnivoice.cli.infer --model k2-fsa/OmniVoice --text "..." --language de --instruct "female, young adult, moderate pitch" --num_step 16 --output out.wav`

**Install trick:** Use `--index-url https://download.pytorch.org/whl/cpu` to get CPU-only PyTorch (~200 MB) instead of the CUDA version (~900 MB). Saves ~700 MB disk.

**Verdict:** Best multi-speaker engine. Voice design mode is unique — generate any voice from a text description, no reference audio. First open-source engine on our hardware with convincing female German voices. Apache 2.0 license. Slower than Piper (1x vs 2.9x) but the voice variety makes it worth it for content creation.

---

### 4. Coqui XTTS v2 — BEST VOICE CLONING

| Metric | Value |
|--------|-------|
| **Model size** | 1.8 GB |
| **Install time** | ~8 min (heavy deps) |
| **RAM usage** | ~3-4 GB during inference |
| **Realtime factor** | 0.33-0.81x (male faster, female slower) |
| **German quality** | ⭐⭐⭐⭐ — Natural, good prosody |
| **Speaker variety** | 65 built-in speakers + zero-shot voice cloning from 6s reference audio |
| **License** | CPML — ❌ Non-commercial only |
| **Disk footprint** | ~3.5 GB total (1.7 GB venv + 1.8 GB model) |
| **Female voice** | Yes (via cloning or built-in speakers) |

**Install gotchas:** Pin `huggingface-hub<0.35` + `transformers<5`. Install `torchcodec`. Pre-create `tos_agreed.txt`. Install script: `scripts/install-xtts.sh`.

**Verdict:** Best voice cloning on our hardware — clone any voice from 6 seconds of audio. 65 built-in speakers including female voices. But non-commercial license and slow CPU inference (0.3-0.8x realtime). Project is abandoned (Coqui shut down Jan 2024).

---

### 5. Bark (Suno) — MOST EXPRESSIVE

| Metric | Value |
|--------|-------|
| **Model size** | 4.4 GB (small models) + 89 MB codec |
| **Install time** | ~10 min |
| **RAM usage** | ~5 GB during inference |
| **Realtime factor** | 0.12x (11.9s audio in 95.8s — very slow) |
| **German quality** | ⭐⭐⭐ — Decent but inconsistent |
| **Speaker variety** | 100+ speaker presets |
| **License** | MIT — ✅ Commercial OK |
| **Disk footprint** | ~5.9 GB total (1.3 GB venv + 4.4 GB models + 89 MB codec) |
| **Female voice** | Yes |

**PyTorch 2.6+ fix:** Monkey-patch `torch.load` to use `weights_only=False`. Bark uses old pickle format that breaks with newer PyTorch defaults.

**Install trick:** Install `bark --no-deps` then add deps individually to avoid a 5.1 GB venv.

**Verdict:** MIT license and extreme expressiveness are the draws. But 0.12x realtime is impractically slow, 13s generation limit is restrictive, and hallucinations (unprompted sounds/music) are a real problem. Fun to experiment with, not usable for production on CPU.

---

## Head-to-Head Comparison

| Feature | Piper | Kokoro | OmniVoice | XTTS v2 | Bark |
|---------|-------|--------|-----------|---------|------|
| **Disk footprint** | 200 MB | 350 MB | 5 GB | 3.5 GB | 5.9 GB |
| **RAM usage** | 200 MB | 400 MB | 2-3 GB | 3-4 GB | 5 GB |
| **Realtime speed** | 2.9x | 2.9x | 1.0x | 0.3-0.8x | 0.12x |
| **German quality** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speaker variety** | 8 emotions | 1 voice | Unlimited | 65 + cloning | 100+ |
| **Female voice** | No | No | Yes | Yes | Yes |
| **Voice cloning** | No | No | Yes | Yes | No |
| **Voice design** | No | No | Yes | No | No |
| **Commercial license** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Install complexity** | Trivial | Easy | Medium | Hard | Medium |

---

## Final Recommendation

**Primary: Piper TTS + Thorsten** — fastest, smallest, most reliable. 8 emotional voices in 74 MB. Install: `scripts/install-piper.sh`.

**Secondary: OmniVoice** — best voice variety. Voice design mode generates male/female/child/elderly voices from text tags. Apache 2.0. Install: PyTorch CPU + `pip install --no-deps omnivoice` + deps.

**For voice cloning: Coqui XTTS v2** — clone any voice from 6s audio. Non-commercial only.

**Not recommended for production on this hardware:** Bark (0.12x realtime is too slow).

---

## Skipped Engines

| Engine | Why Skipped |
|--------|------------|
| **CosyVoice 300M** | Python 3.10 required (ttsfrd no cp312 wheel), 16+ GB RAM, 8-10 GB disk |
| **Fish Speech** | S2 Pro needs 24 GB VRAM |
| **F5-TTS** | Requires reference audio, CC-BY-NC non-commercial |
| **StyleTTS2** | English only |
| **MeloTTS** | No German support |
| **MMS TTS** | Robotic quality + non-commercial |
| **ZeroVOX** | pip install fails (readline build error, missing deps) |
| **Thorsten-Voice** | Voice dataset, covered under Piper |

---

## Test Infrastructure

All tests used German passages. Audio generated as WAV, converted to MP3 (ffmpeg), sent to Discord. Performance measured as realtime factor (audio duration / generation time). Higher is better.

- Piper: 32.0s audio in 11.0s = 2.9x
- Kokoro: 33.9s audio in 11.7s = 2.9x
- OmniVoice: ~6s audio in ~6s = 1.0x (num_step=16)
- XTTS v2: male 0.81x, female 0.33-0.40x
- Bark: 11.9s audio in 95.8s = 0.12x
