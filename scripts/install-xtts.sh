#!/bin/bash
# Install Coqui XTTS v2 for German TTS
# Requires: Python 3.10+, 8GB RAM, ~5 GB free disk
# License: CPML (non-commercial)

set -e

VENV_DIR="${1:-/home/z/venv}"
MODEL_DIR="$HOME/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2"

echo "=== Coqui XTTS v2 Install Script ==="

# Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Creating Python venv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "[1/4] Venv already exists at $VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "[2/4] Installing coqui-tts + PyTorch CPU..."
pip install --no-cache-dir coqui-tts 'huggingface-hub>=0.30,<0.35' 'transformers>=4.57,<5' torchcodec 2>/dev/null
pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu 2>/dev/null

echo "[3/4] Pre-agreeing to Coqui CPML license..."
mkdir -p "$MODEL_DIR"
echo "I have read, understood and agreed to the Terms and Conditions." > "$MODEL_DIR/tos_agreed.txt"

echo "[4/4] Model will auto-download on first use (~1.8 GB)"
echo ""
echo "=== Install complete ==="
echo "Usage:"
echo "  source $VENV_DIR/bin/activate"
echo "  python3 -c \""
echo "  from TTS.api import TTS"
echo "  tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
echo "  tts.tts_to_file(text='Hallo Welt', speaker='Ana Florence', language='de', file_path='output.wav')"
echo "  \""
echo ""
echo "Available speakers: 65 (male + female)"
echo "Key speakers: Dionisio Schuyler (male), Ana Florence (female), Claribel Dervla (female)"
echo "Voice cloning: tts.tts_to_file(text='...', speaker_wav='reference.wav', language='de', file_path='out.wav')"
