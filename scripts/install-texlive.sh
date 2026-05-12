#!/usr/bin/env bash
# Portable TeXLive installer for LuaLaTeX document production
# Installs to /home/z/.texlive/2026 (outside the repo)
set -euo pipefail

TEXLIVE_DIR="/home/z/.texlive"
INSTALL_DIR="${TEXLIVE_DIR}/2026"
BIN_DIR="${INSTALL_DIR}/bin/x86_64-linux"

# Check if already installed
if [ -x "${BIN_DIR}/lualatex" ]; then
    echo "LuaLaTeX already installed."
    export PATH="${BIN_DIR}:${PATH}"
    lualatex --version | head -1
    exit 0
fi

echo "=== Installing portable TeXLive to ${TEXLIVE_DIR} ==="
mkdir -p "${TEXLIVE_DIR}"
TMPDIR=$(mktemp -d)
trap "rm -rf ${TMPDIR}" EXIT

# Download install-tl
echo "[1/4] Downloading TeXLive installer..."
cd "${TMPDIR}"
curl -L -o install-tl.tar.gz \
    "https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz" 2>&1 | tail -3
tar xzf install-tl.tar.gz
cd "$(ls -d install-tl-*/)"

# Create profile for minimal install
echo "[2/4] Configuring minimal install..."
cat > texlive.profile << 'PROFILE'
selected_scheme scheme-basic
TEXDIR /home/z/.texlive/2026
TEXMFLOCAL /home/z/.texlive/texmf-local
TEXMFSYSCONFIG /home/z/.texlive/2026/texmf-config
TEXMFSYSVAR /home/z/.texlive/2026/texmf-var
TEXMFHOME ~/texmf
TEXMFCONFIG ~/.texlive2026/texmf-config
TEXMFVAR ~/.texlive2026/texmf-var
binary_x86_64-linux 1
instopt_adjustpath 0
instopt_adjustrepo 1
instopt_letter 0
instopt_portable 0
instopt_write18_restricted 1
PROFILE

# Run installer
echo "[3/4] Installing TeXLive (scheme-basic)..."
./install-tl --profile=texlive.profile --no-interaction 2>&1 | tail -5

export PATH="${BIN_DIR}:${PATH}"

# Install additional packages (skip errors for already-installed ones)
echo "[4/4] Installing additional packages..."
PACKAGES=(
    pgf fontspec geometry titlesec tocloft booktabs enumitem xcolor
    hyperref microtype koma-script calc etoolbox listings caption
    luatexbase luaotfload metalogo mdframed tcolorbox
    parskip setspace fancyhdr lastpage bookmark
    amsmath amssymb mathtools unicode-math fontawesome5
    sourcecodepro
)

for pkg in "${PACKAGES[@]}"; do
    echo -n "  ${pkg}... "
    tlmgr install "${pkg}" 2>&1 | tail -1 || true
done

# Update font maps
echo "Updating font maps..."
luaotfload-tool --update --force 2>&1 | tail -1 || true

echo ""
echo "=== Installation complete ==="
lualatex --version | head -1
echo "Add to shell: export PATH=\"${BIN_DIR}:\${PATH}\""
