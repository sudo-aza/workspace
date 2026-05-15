# TTS Engine Comparison: German on CPU (4 vCPU, 8 GB RAM, no GPU)

**Date:** 2026-05-15
**Hardware:** 4 vCPU, 8 GB RAM, 10 GB disk, no GPU
**Test text:** German story passage (~30 seconds of speech)
**All tests used the same German passage for fair comparison.**

---

## Tested Engines (with results)

### 1. Piper TTS + Thorsten — ⭐ BEST PICK

| Metric | Value |
|--------|-------|
| **Model size** | 109 MB (high quality), 74 MB (emotional medium) |
| **Install time** | ~2 min (pip + model download) |
| **RAM usage** | ~200 MB |
| **Realtime factor** | 2.9x (32s audio in 11s) |
| **German quality** | ⭐⭐⭐⭐ — Clear, natural male voice |
| **Speaker variety** | 8 emotional voices (amused, angry, disgusted, drunk, neutral, sleepy, surprised, whisper) |
| **License** | GPL-3.0 (engine) + CC0 (voice data) — ✅ Commercial OK |
| **Disk footprint** | ~200 MB total (engine + both models) |
| **Install complexity** | Trivial — `pip install piper-tts` + download ONNX |

**Strengths:**
- Fastest install, smallest footprint, most reliable
- 8 distinct emotional speakers add real variety (whisper and angry are particularly convincing)
- The emotional medium model is only 74 MB with 8 speakers — incredible value
- Best-documented German TTS in the open-source ecosystem
- Designed for embedded/CPU use — exactly our use case

**Weaknesses:**
- Male voice only (no female option without separate voice dataset)
- espeak-ng phonemization occasionally mispronounces complex German compound words
- Slightly mechanical timbre compared to larger models (but still very listenable)
- No voice cloning capability

**Verdict:** **Recommended as the primary TTS engine.** Best balance of quality, speed, size, and licensing. The 8 emotional voices provide genuine variety for content creation.

---

### 2. Kokoro-82M German (Martin) — ⭐ VIABLE ALTERNATIVE

| Metric | Value |
|--------|-------|
| **Model size** | 311 MB (ONNX), 511 KB (voice pack) |
| **Install time** | ~3 min (pip + model download) |
| **RAM usage** | ~400 MB |
| **Realtime factor** | 2.9x (33.9s audio in 11.7s) |
| **German quality** | ⭐⭐⭐⭐ — Smoother timbre, slightly less crisp |
| **Speaker variety** | 1 voice (Martin, male) |
| **License** | Permissive open-weight — ✅ Commercial OK |
| **Disk footprint** | ~350 MB total |
| **Install complexity** | Easy — `pip install kokoro-onnx` + community model |

**Strengths:**
- Smoother, more pleasant timbre than Piper (less "synthetic" edge)
- StyleTTS2 architecture — more advanced than Piper's approach
- Same realtime speed as Piper despite 3x larger model
- Very clean, intelligible German pronunciation

**Weaknesses:**
- 3x larger model for same speed — worse size-to-performance ratio
- Only 1 voice vs Piper's 8 emotional variants
- Community-maintained German model (not officially supported)
- No emotional control, no voice cloning
- Single male voice (Martin)

**Verdict:** Good alternative if you prefer a smoother timbre over emotional variety. Worth keeping installed alongside Piper for voice diversity, but Piper wins on features and size.

---

## Skipped Engines (with reasons)

### Hardware Blockers (insufficient RAM or disk)

| Engine | Why Skipped | Would Need |
|--------|------------|------------|
| **Coqui XTTS v2** | 2 GB model + PyTorch deps exceed 9 GB disk. CPU inference timed out. | 16 GB RAM, GPU, 15+ GB disk |
| **Bark** | 2.3 GB model + PyTorch fills disk. `weights_only` compatibility issue. | 16 GB RAM, GPU, 15+ GB disk |
| **CosyVoice 300M** | Requires Python 3.10, 16+ GB RAM, 8-10 GB disk for full install. `ttsfrd` has no cp312 wheel. | Python 3.10, 16 GB RAM, GPU |
| **Fish Speech** | S2 Pro needs 24 GB VRAM. Way beyond hardware. | 24 GB VRAM GPU |

### Dependency/Install Failures

| Engine | Why Skipped |
|--------|------------|
| **ZeroVOX** | `pip install zerovox` fails: readline build error + missing deps (h5py, nemo_text_processing, nltk, lightning). Early alpha quality. |
| **F5-TTS** | Requires reference audio for voice cloning (needs Piper installed first to generate). Heavy PyTorch deps fill disk. CC-BY-NC non-commercial. |

### Language or Quality Eliminations

| Engine | Why Skipped |
|--------|------------|
| **StyleTTS2** | English only. Author unresponsive to multilingual requests. |
| **MeloTTS** | No German support. Issue #145 open, no model released. |
| **MMS TTS** | Robotic quality + CC-BY-NC 4.0 non-commercial license. |
| **Thorsten-Voice** | Not a separate engine — voice dataset already covered under Piper. |

### License Blockers (non-commercial only)

| Engine | License | Notes |
|--------|---------|-------|
| **F5-TTS** | CC-BY-NC (model weights) | Best quality among non-commercial options |
| **Coqui XTTS v2** | CPML (non-commercial) | Also abandoned project |
| **Fish Speech** | CC-BY-NC-SA 4.0 | Highest quality but too heavy |
| **MMS TTS** | CC-BY-NC 4.0 | Also robotic quality |

---

## Head-to-Head: Piper vs Kokoro

| Feature | Piper + Thorsten | Kokoro Martin | Winner |
|---------|-----------------|---------------|--------|
| **Model size** | 109 MB (high) / 74 MB (emotional) | 311 MB | Piper (3x smaller) |
| **Disk footprint** | ~200 MB | ~350 MB | Piper |
| **RAM usage** | ~200 MB | ~400 MB | Piper |
| **Realtime speed** | 2.9x | 2.9x | Tie |
| **German quality** | ⭐⭐⭐⭐ Crisp, natural | ⭐⭐⭐⭐ Smoother | Tie (different character) |
| **Speaker variety** | 8 emotional voices | 1 voice | Piper (8x more) |
| **Voice cloning** | No | No | Neither |
| **Female voice** | No | No | Neither |
| **Install complexity** | Trivial | Easy | Piper (slightly easier) |
| **License** | GPL-3.0 + CC0 | Permissive | Both OK |
| **Community support** | Strong (OHF-Voice, Rhasspy) | Moderate (huggingFresse) | Piper |
| **Maintenance** | Active | Community (1 maintainer) | Piper |

---

## Final Recommendation

**Primary engine: Piper TTS + Thorsten (emotional medium model)**

The 74 MB emotional medium model gives you 8 distinct voices in a tiny package. Install via:
```bash
python3 -m venv /home/z/venv
source /home/z/venv/bin/activate
pip install piper-tts
# Download models from HuggingFace (see scripts/install-piper.sh)
```

**Secondary engine: Kokoro-82M German Martin**

Keep installed for projects where you want a smoother, warmer timbre. Install via:
```bash
pip install kokoro-onnx soundfile
# Download kokoro-martin.onnx + voices-martin.npz from huggingFresse
```

**For future upgrades (when hardware allows):**
1. **CosyVoice** — Best long-term pick (Apache 2.0, voice cloning, LLM architecture). Needs 16 GB RAM + GPU.
2. **F5-TTS** — Best quality (if non-commercial is acceptable). Needs reference audio.
3. **Coqui XTTS v2** — Mature voice cloning, but abandoned project + non-commercial.

**Open gap: No female German voice exists** in any open-source engine that fits 8 GB RAM CPU. Options to get female voice:
- Use Coqui XTTS v2 voice cloning with female reference audio (needs GPU machine)
- Use a commercial API (ElevenLabs, Azure) for female voices
- Wait for community female Thorsten model for Piper

---

## Test Infrastructure

All tests used the same German passage (from a German story) to ensure fair comparison. Audio was generated as WAV, converted to MP3 (ffmpeg), and sent to Discord for evaluation. Performance measured as realtime factor: audio duration / generation time. Higher is better.

- Piper test: 32.0s audio in 11.0s = 2.9x realtime
- Kokoro test: 33.9s audio in 11.7s = 2.9x realtime
