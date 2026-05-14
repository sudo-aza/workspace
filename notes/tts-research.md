# TTS Engine Research: Best German Multi-Speaker TTS for CPU (4 vCPU, 8GB RAM, no GPU)

**Date:** 2026-05-14
**Hardware constraints:** 4 vCPU, 8 GB RAM, no GPU
**Requirements:** German language, multi-speaker or voice variety, natural prosody, open source

---

## Summary Ranking

| Rank | Engine | German | Hardware Fit | Quality (DE) | License | Commercial? | Verdict |
|------|--------|--------|-------------|-------------|---------|-------------|---------|
| 1 | **Piper TTS + Thorsten** | ✅ Native | ✅ Perfect | ⭐⭐⭐⭐ | GPL-3.0 + CC0 | ✅ | **Best overall** |
| 2 | **Kokoro-82M (German-Martin)** | ⚠️ Community | ✅ Perfect | ⭐⭐⭐ | Permissive | ✅ | Worth testing |
| 3 | **ZeroVOX** | ✅ First-class | ✅ Perfect | ⭐⭐⭐ | Open source | ✅ | Alpha quality |
| 4 | **Bark (Suno)** | ✅ Yes | ⚠️ Marginal | ⭐⭐⭐ | MIT | ✅ | Hallucinations, 13s limit |
| 5 | **CosyVoice (300M)** | ✅ Yes | ⚠️ Tight | ⭐⭐⭐⭐ | Apache 2.0 | ✅ | Complex install |
| 6 | **F5-TTS (German fine-tune)** | ✅ Excellent | ✅ Feasible | ⭐⭐⭐⭐ | MIT code / CC-BY-NC weights | ❌ | Non-commercial weights |
| 7 | **Coqui XTTS v2** | ✅ First-class | ⚠️ Marginal | ⭐⭐⭐⭐ | CPML (non-comm.) | ❌ | Abandoned project |
| 8 | **Fish Speech** | ✅ Yes | ❌ No (24GB VRAM) | ⭐⭐⭐⭐⭐ | CC-BY-NC-SA | ❌ | Too heavy |
| -- | **MMS TTS (Meta)** | ✅ Yes | ✅ Feasible | ⭐⭐ | CC-BY-NC 4.0 | ❌ | Robotic + non-commercial |
| -- | **StyleTTS2** | ❌ English only | ✅ Feasible | N/A | Unclear | ⚠️ | Eliminated |
| -- | **MeloTTS** | ❌ No German | ✅ Feasible | N/A | MIT | ✅ | Eliminated |
| -- | **Thorsten-Voice** | ✅ (same as Piper) | ✅ (same) | ⭐⭐⭐⭐ | CC0 | ✅ | Not a separate engine |

---

## Detailed Engine Analysis

### 1. Piper TTS + Thorsten Voice (RECOMMENDED)

**Best balance of quality, ease of installation, performance, and licensing.**

- **Architecture:** ONNX-based neural TTS, designed for embedded/Raspberry Pi use
- **German support:** Full native support via Thorsten Müller's voice models (de_DE)
- **Voices:** 1 male speaker (Thorsten), 8 emotional variants (neutral, disgusted, furious, amused, sad, sleepy, angry, surprised), 1 dialect variant (Südhessisch), 3 quality tiers (low/medium/high)
- **Model size:** 63 MB (medium) to 114 MB (high) — runs trivially on 4 vCPU / 8 GB
- **Prosody:** Natural intonation for neutral reading, emotional variants add expressiveness but can sound slightly forced. Widely regarded as best open-source German voice in community
- **License:** GPL-3.0 (engine) + CC0 (voice data) — commercial use allowed
- **Install:** `pip install piper-tts`, download ONNX models from HuggingFace
- **Limitations:** Single speaker (male only), espeak-ng phonemization can mispronounce some German words, no female voice
- **Sources:** [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl), [Piper Samples](https://rhasspy.github.io/piper-samples/), [thorsten-voice.de](https://www.thorsten-voice.de)

### 2. Kokoro-82M-ONNX-German-Martin (WORTH TESTING)

**Lightweight StyleTTS2-architecture model with community German adaptation.**

- **Architecture:** StyleTTS2-based, 82M parameters, ONNX runtime
- **German support:** Community model by huggingFresse, not officially maintained
- **Voices:** 1 male voice ("Martin") for German; 10+ voices for English
- **Model size:** ~80 MB (quantized) to ~300 MB (unquantized)
- **Prosody:** Very good for English; German quality unverified but reports suggest clear, intelligible output. May lack prosodic richness for complex German
- **License:** Permissive open-weight for base model; verify German community model terms
- **Install:** `pip install kokoro-onnx`, download from huggingFresse/Kokoro-82M-ONNX-German-Martin
- **Limitations:** Community-maintained German model (uncertain long-term support), single voice, no female option, undocumented training methodology
- **Sources:** [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), [thewh1teagle/kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx)

### 3. ZeroVOX (PROTOYPE-QUALITY)

**Ultra-lightweight FastSpeech2 with native German, but early alpha.**

- **Architecture:** Non-autoregressive FastSpeech2 with zero-shot speaker cloning
- **German support:** First-class — one of only 2 supported languages (EN + DE)
- **Voices:** Zero-shot cloning from reference audio
- **Model size:** ~1-2 GB RAM footprint, designed for real-time embedded use
- **Prosody:** Moderate — functional but below SOTA models. Predictable output, lacks expressiveness
- **License:** Open source, free, fully offline
- **Install:** `pip install zerovox` — simplest install of all candidates
- **Limitations:** Labeled "early alpha, not for production", only 2 languages, quality below alternatives, small community, limited track record
- **Sources:** [gooofy/zerovox](https://github.com/gooofy/zerovox), [goooofy/tts_en_de_zerovox_alpha1](https://huggingface.co/goooofy/tts_en_de_zerovox_alpha1)

### 4. Bark by Suno (EXPRESSIVE BUT UNPREDICTABLE)

**Highly expressive generative model with MIT license, but hallucinations and 13s limit.**

- **Architecture:** Transformer-based text-to-audio model (generates speech, sounds, music)
- **German support:** Yes, one of 13+ supported languages with auto-detection
- **Voices:** 100+ speaker presets, can generate novel voices
- **Model size:** ~6 GB VRAM (small models) to ~12 GB (full); CPU-only works but very slow
- **Prosody:** Highly expressive — can produce laughter, gasps, music snippets. German quality is decent but inconsistent
- **License:** MIT — fully open source, commercial use allowed
- **Install:** `pip install suno-bark`
- **Limitations:** 13-second generation limit per clip, hallucinations (unprompted sounds/words/music), slow CPU inference, German quality inconsistent, development has slowed
- **Sources:** [suno-ai/bark](https://github.com/suno-ai/bark), [suno/bark on HuggingFace](https://huggingface.co/suno/bark)

### 5. CosyVoice by Alibaba (BEST FEATURES, TIGHT FIT)

**LLM-based multilingual TTS with best license (Apache 2.0), complex installation.**

- **Architecture:** LLM-based multilingual voice model (Fun-CosyVoice 3.0)
- **German support:** Officially supported (one of 9 languages); community German fine-tuning effort exists
- **Voices:** Zero-shot voice cloning, accent-preserving conversion, multi-timbral generation
- **Model size:** 300M model (~4-6 GB VRAM), 0.5B model (~6-8 GB VRAM); 16 GB RAM recommended
- **Prosody:** Very good to excellent — nuanced prosody, natural rhythm, emotion control, cross-lingual voice cloning
- **License:** Apache 2.0 — open source, commercial use explicitly permitted
- **Install:** `pip install cosyvoice` (limited) or clone from source (complex build, Python 3.10, Docker available)
- **Limitations:** Complex installation, 300M model is tight on 8 GB RAM, German quality behind English/Chinese, documentation gaps, large model downloads
- **Sources:** [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice), [cosyvoice.org](https://cosyvoice.org), [horstmann.tech German demo](https://horstmann.tech/cosyvoice2-demo)

### 6. F5-TTS (BEST QUALITY-TO-WEIGHT, NON-COMMERCIAL)

**Diffusion-transformer TTS with excellent German fine-tunes, but non-commercial license.**

- **Architecture:** Diffusion-transformer with flow matching, 335M parameters
- **German support:** Excellent — multiple community German fine-tunes (tabularisai, hvoss-techfak, aihpi)
- **Voices:** Zero-shot voice cloning from reference audio
- **Model size:** ~2-3 GB VRAM, 8 GB RAM — very lightweight for a diffusion model
- **Prosody:** Very good — among the best open-source TTS for quality. German fine-tunes improve pronunciation and prosody
- **License:** MIT (code), CC-BY-NC (model weights — non-commercial due to Emilia training data). OpenF5-TTS-Base has permissive weights but may differ in quality
- **Install:** `pip install f5-tts`
- **Limitations:** Non-commercial model weights, diffusion-based can be slow on CPU, no explicit emotion control
- **Sources:** [SWivid/F5-TTS](https://github.com/SWivid/F5-TTS), [hvoss-techfak/F5-TTS-German](https://huggingface.co/hvoss-techfak/F5-TTS-German)

### 7. Coqui XTTS v2 (GOOD BUT ABANDONED)

**Mature multilingual TTS with voice cloning, but company shut down and non-commercial license.**

- **Architecture:** Multilingual TTS with zero-shot voice cloning from 6s reference audio
- **German support:** First-class — Coqui was a German company, German is well-supported
- **Voices:** Unlimited via zero-shot cloning, cross-language cloning supported
- **Model size:** ~4 GB VRAM, 8 GB RAM minimum
- **Prosody:** Good to very good — natural output, emotion/style transfer from reference
- **License:** CPML (non-commercial only). Coqui shut down Jan 2024, commercial licenses no longer available
- **Install:** `pip install TTS`
- **Limitations:** Non-commercial only, abandoned project (community-maintained), slow CPU inference, long texts need manual chunking, no explicit emotion parameters
- **Sources:** [coqui-ai/TTS](https://github.com/coqui-ai/TTS), [coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2)

### 8. Fish Speech (HIGHEST QUALITY, TOO HEAVY)

**SOTA quality LLM-based TTS, but requires 24 GB VRAM — doesn't fit our hardware.**

- **Architecture:** LLM-based, trained on 10M+ hours across 80+ languages
- **German support:** Yes (S1.5 and S2 Pro), though lower training tier than EN/ZH/JP
- **Voices:** Zero-shot cloning, native multi-speaker, multi-turn generation
- **Model size:** S1.5 ~12 GB VRAM, S2 Pro ~17-24 GB VRAM, 16+ GB RAM
- **Prosody:** Excellent — natural language emotion tags ("speak happily", "whisper"), <150ms latency, superior style adherence
- **License:** Apache 2.0 (code), CC-BY-NC-SA-4.0 (weights — non-commercial without paid license)
- **Install:** Clone repo, pip install -e ., download large model weights
- **Limitations:** Far exceeds hardware constraints (24 GB VRAM), non-commercial weights, complex install, Linux/WSL only
- **Sources:** [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech), [speech.fish.audio](https://speech.fish.audio)

---

## Eliminated Engines

### MMS TTS (Meta)
- **Why eliminated:** CC-BY-NC 4.0 (non-commercial), noticeably robotic quality for German, no prosody control, single speaker. Better alternatives exist for German (a well-resourced language).

### StyleTTS2
- **Why eliminated:** English only. No German support, author unresponsive to multilingual requests. Near-human English quality but irrelevant for our use case.

### MeloTTS
- **Why eliminated:** No German support. Open issue #145 requesting German, maintainers haven't implemented it. Training a new language requires significant effort (custom G2P, BERT model, tone annotations).

### Thorsten-Voice
- **Why not separate:** This is a voice dataset/project, not a standalone TTS engine. The models are already covered under Piper TTS + Thorsten above. Using Piper to run Thorsten models is the recommended path.

---

## Key Findings

1. **No female German voice** exists in any open-source engine that fits our hardware. All viable options are male-only. Female voice requires either Coqui XTTS v2 voice cloning (with a female reference sample) or a commercial API (ElevenLabs, Azure).

2. **License matters:** Most high-quality models (F5-TTS, Coqui XTTS, Fish Speech, MMS) have non-commercial licenses. Only Piper, Kokoro, Bark, CosyVoice, and ZeroVOX permit commercial use.

3. **Piper + Thorsten is the safe default:** Best documented, easiest install, smallest footprint, most mature German support, permissive license. Not the most cutting-edge quality, but reliable and well-tested.

4. **CosyVoice is the most promising for the future:** Apache 2.0 license, active development, LLM architecture, voice cloning — but installation complexity and tight hardware fit are concerns.

5. **For multi-speaker variety** (the user's original requirement): Coqui XTTS v2 and F5-TTS offer zero-shot voice cloning, but both have non-commercial licenses. ZeroVOX and CosyVoice are the commercially-viable multi-speaker options, but with caveats (alpha quality / complex install).

---

## Recommended Testing Order

Based on quality-feasibility analysis, the following engines should be tried in order:

1. **Piper TTS + Thorsten High** — baseline, fastest to set up, highest confidence
2. **Kokoro-82M German-Martin** — quick comparison, very light, interesting architecture
3. **ZeroVOX** — test the native DE support, evaluate alpha quality
4. **F5-TTS German** — test quality despite non-commercial license (for research/comparison)
5. **Coqui XTTS v2** — test voice cloning capability (clone a female voice from reference audio)
6. **Bark** — test expressiveness despite limitations
7. **CosyVoice 300M** — test if it fits in memory, evaluate quality advantage

Skip: Fish Speech (too heavy), MMS TTS (robotic + non-commercial), MeloTTS (no German), StyleTTS2 (no German)
