#!/usr/bin/env bash
# یک‌بار با اینترنت اجرا شود تا موتور پایتون آفلاین شود.
# موتور جدید (0.26.4) + موتور سازگار برای مرورگرهای قدیمی (0.23.4).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="$ROOT/app"
VER="${PYODIDE_VERSION:-0.26.4}"
LEGACY_VER="${PYODIDE_LEGACY_VERSION:-0.23.4}"

fetch_engine() {
  local ver="$1" dest_name="$2"; shift 2
  local tmp="$APP/vendor/_tmp_pyodide" dest="$APP/vendor/$dest_name"
  local url="https://github.com/pyodide/pyodide/releases/download/${ver}/pyodide-${ver}.tar.bz2"
  mkdir -p "$APP/vendor"
  rm -rf "$tmp" "$dest"
  mkdir -p "$tmp"
  echo "Downloading Pyodide ${ver}…"
  curl -fL "$url" -o "$tmp/pyodide.tar.bz2"
  tar -xjf "$tmp/pyodide.tar.bz2" -C "$tmp"
  local src="$tmp/pyodide"
  mkdir -p "$dest"
  for f in "$@"; do
    cp "$src/$f" "$dest/"
  done
  # Sourcemap files are not vendored — drop the comment to avoid 404 noise.
  sed -i '/^\/\/# sourceMappingURL=.*$/d' "$dest/pyodide.js"
  rm -rf "$tmp"
  echo "OK → $dest"
  ls -lh "$dest" | head
}

fetch_engine "$VER" "pyodide" \
  pyodide.js pyodide.asm.js pyodide.asm.wasm python_stdlib.zip package.json pyodide-lock.json

# 0.23.x is the last line before WebAssembly externref (works on Chrome 71+).
fetch_engine "$LEGACY_VER" "pyodide-legacy" \
  pyodide.js pyodide.asm.js pyodide.asm.wasm python_stdlib.zip package.json repodata.json
