#!/usr/bin/env bash
# One-time (per session) setup for the daily video generator. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p .cache
pip install -q --break-system-packages pillow numpy scipy soundfile kokoro-onnx 2>&1 | grep -v -i "warning" || true
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s .cache/kokoro-v1.0.onnx ] || curl -sSL -o .cache/kokoro-v1.0.onnx $REL/kokoro-v1.0.onnx
[ -s .cache/voices-v1.0.bin ]  || curl -sSL -o .cache/voices-v1.0.bin  $REL/voices-v1.0.bin
if [ ! -d .cache/node_modules/@fontsource/plus-jakarta-sans ]; then
  (cd .cache && echo '{"name":"gd-fonts","private":true}' > package.json && npm i --no-audit --no-fund @fontsource/plus-jakarta-sans >/dev/null)
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
python3 -c "import kokoro_onnx, PIL, scipy, soundfile; print('generator ready')"
