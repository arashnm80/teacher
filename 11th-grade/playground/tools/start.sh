#!/usr/bin/env bash
# سرو محلی آفلاین برای تمرین پایتون
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
APP="$REPO/app"
cd "$APP"

if [[ ! -f vendor/pyodide/pyodide.js ]]; then
  echo "موتور Pyodide هنوز نصب نشده. یک‌بار با اینترنت اجرا کنید:"
  echo "  bash tools/fetch-pyodide.sh"
  exit 1
fi

if [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && command -v python3 >/dev/null; then
  if python3 -c "import tkinter" 2>/dev/null; then
    exec python3 launcher.py
  fi
fi

PORT="${1:-8765}"
echo "سرو روی http://127.0.0.1:${PORT}"
echo "در مرورگر همین آدرس را باز کنید. Ctrl+C برای توقف."
python3 -m http.server "$PORT" --bind 127.0.0.1
