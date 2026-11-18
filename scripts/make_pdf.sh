#!/bin/sh
# Print each course handbook to PDF with headless Chromium. Run after build.py.
set -e
cd "$(dirname "$0")/.."
pdf() {
  chromium --headless --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
    --virtual-time-budget=10000 --print-to-pdf="$2" "file://$PWD/$1" 2>/dev/null
  echo "wrote $2"
}
pdf site/handbook.html handbook.pdf
[ -f site/linux/handbook.html ] && pdf site/linux/handbook.html linux-handbook.pdf
exit 0
