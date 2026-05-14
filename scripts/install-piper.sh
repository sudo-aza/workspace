#!/bin/bash
# Install Piper TTS with Thorsten German voice models
# Usage: bash install-piper.sh [INSTALL_DIR]
# Default install dir: /home/z/tts-env

set -euo pipefail

INSTALL_DIR="${1:-/home/z/tts-env}"
MODEL_DIR="$INSTALL_DIR/models"
VENV_DIR="$INSTALL_DIR/venv"

echo "=== Piper TTS + Thorsten German Voice Installer ==="
echo "Install dir: $INSTALL_DIR"
echo ""

# Create directories
mkdir -p "$MODEL_DIR"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "[1/4] Virtual environment already exists, skipping..."
fi

# Activate and install piper-tts
echo "[2/4] Installing piper-tts..."
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet piper-tts

# Download models
echo "[3/4] Downloading Thorsten German voice models..."

# High quality neutral
if [ ! -f "$MODEL_DIR/de_DE-thorsten-high.onnx" ]; then
    echo "  - Downloading de_DE-thorsten-high (109 MB)..."
    wget -q --show-progress -O "$MODEL_DIR/de_DE-thorsten-high.onnx" \
        "https://huggingface.co/Thorsten-Voice/Piper/resolve/main/de_DE-thorsten-high.onnx"
    wget -q -O "$MODEL_DIR/de_DE-thorsten-high.onnx.json" \
        "https://huggingface.co/Thorsten-Voice/Piper/resolve/main/de_DE-thorsten-high.onnx.json"
else
    echo "  - de_DE-thorsten-high already exists, skipping..."
fi

# Emotional medium quality (8 speakers: amused, angry, disgusted, drunk, neutral, sleepy, surprised, whisper)
if [ ! -f "$MODEL_DIR/de_DE-thorsten_emotional-medium.onnx" ]; then
    echo "  - Downloading de_DE-thorsten_emotional-medium (74 MB)..."
    wget -q --show-progress -O "$MODEL_DIR/de_DE-thorsten_emotional-medium.onnx" \
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx"
    wget -q -O "$MODEL_DIR/de_DE-thorsten_emotional-medium.onnx.json" \
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx.json"
else
    echo "  - de_DE-thorsten_emotional-medium already exists, skipping..."
fi

echo "[4/4] Done!"
echo ""
echo "Usage:"
echo "  source $VENV_DIR/bin/activate"
echo "  piper -m $MODEL_DIR/de_DE-thorsten-high.onnx -f output.wav -i text.txt"
echo ""
echo "Emotional model (8 speakers, use -s ID):"
echo "  0=amused 1=angry 2=disgusted 3=drunk 4=neutral 5=sleepy 6=surprised 7=whisper"
echo "  piper -m $MODEL_DIR/de_DE-thorsten_emotional-medium.onnx -f output.wav -i text.txt -s 0"
