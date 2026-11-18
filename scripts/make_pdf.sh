#!/bin/sh
# Print site/handbook.html to handbook.pdf with headless Chromium. Run after build.py.
set -e
cd "$(dirname "$0")/.."
chromium --headless --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
  --virtual-time-budget=10000 --print-to-pdf=handbook.pdf "file://$PWD/site/handbook.html"
echo "wrote handbook.pdf"
