#!/bin/bash
# Install Suno Bark TTS (small models)
# Requires: Python 3.10+, 8GB RAM, ~6 GB free disk
# License: MIT (fully open source, commercial OK)
# NOTE: Very slow on CPU (~0.12x realtime). 13s clip limit.

set -e

VENV_DIR="${1:-/home/z/venv}"

echo "=== Bark TTS Install Script ==="

# Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Creating Python venv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "[1/4] Venv already exists at $VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "[2/4] Installing suno-bark (no deps) + PyTorch CPU..."
pip install --no-cache-dir suno-bark --no-deps 2>/dev/null
pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu 2>/dev/null

echo "[3/4] Installing bark dependencies..."
pip install --no-cache-dir scipy tokenizers tqdm transformers encodec soundfile funcy 2>/dev/null

echo "[4/4] Models will auto-download on first use (~4.4 GB)"
echo ""
echo "=== Install complete ==="
echo "IMPORTANT: Bark needs a torch.load monkey-patch for PyTorch 2.6+:"
echo ""
echo '  SUNO_USE_SMALL_MODELS=1 python3 -c "'
echo "  import os, torch"
echo "  os.environ['SUNO_USE_SMALL_MODELS'] = '1'"
echo "  _load = torch.load"
echo "  torch.load = lambda *a, **k: _load(*a, **{**k, 'weights_only': k.get('weights_only', False)})"
echo "  from bark import SAMPLE_RATE, generate_audio"
echo "  audio = generate_audio('Hallo Welt')"
echo "  import soundfile as sf"
echo "  sf.write('output.wav', audio, SAMPLE_RATE)"
echo '  "'
echo ""
echo "Speed: ~0.12x realtime (very slow). 13s clip limit."
echo "Language: Auto-detected from text."
echo "License: MIT"
