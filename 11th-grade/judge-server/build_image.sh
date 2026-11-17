#!/bin/bash
# Builds the sandbox image "teacher-judge:current" from this server's own Python, with no download.
# The image holds only Python, its standard library, and runner.py / child.py: no shell, no tools,
# no other programs, and nothing of the website, the database or the questions.
set -euo pipefail
cd "$(dirname "$0")"
PY=$(readlink -f /usr/bin/python3)
VER=$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
ROOT=$(mktemp -d)
trap 'rm -rf "$ROOT"' EXIT

copy_with_libs() {              # copy a file and the shared libraries it needs, at the same paths
  local f=$1
  cp --parents -L "$f" "$ROOT"
  ldd "$f" 2>/dev/null | awk '/=> \//{print $3} /^\t\//{print $1}' | while read -r lib; do
    [ -e "$ROOT$lib" ] || cp --parents -L "$lib" "$ROOT"
  done
}

mkdir -p "$ROOT"/{work,tmp,opt/judge,proc,dev,sys,etc,usr/bin}
copy_with_libs "$PY"
cp -L "$PY" "$ROOT/usr/bin/python3"
STDLIB=/usr/lib/python$VER
mkdir -p "$ROOT$STDLIB"
rsync -a --exclude 'test/' --exclude 'tests/' --exclude 'idlelib/' --exclude 'tkinter/' \
  --exclude 'turtledemo/' --exclude 'ensurepip/' --exclude 'lib2to3/' --exclude '__pycache__/' \
  --exclude 'site-packages/' --exclude 'dist-packages/' "$STDLIB/" "$ROOT$STDLIB/"
for so in "$ROOT$STDLIB"/lib-dynload/*.so; do      # the libraries the extension modules need
  copy_with_libs "${so#"$ROOT"}"
done
# compiled once here: the image is read-only, so Python could not save them later
"$PY" -m compileall -q -j0 -d "$STDLIB" "$ROOT$STDLIB" >/dev/null 2>&1 || true
cp child.py runner.py "$ROOT/opt/judge/"
"$PY" -m py_compile "$ROOT/opt/judge/child.py" "$ROOT/opt/judge/runner.py"
chmod 0755 "$ROOT/opt/judge" && chmod 0444 "$ROOT/opt/judge/"*.py
echo "root:x:0:0:root:/work:/nonexistent" > "$ROOT/etc/passwd"
echo "nobody:x:65534:65534:nobody:/work:/nonexistent" >> "$ROOT/etc/passwd"
echo "root:x:0:" > "$ROOT/etc/group"; echo "nogroup:x:65534:" >> "$ROOT/etc/group"
"$PY" -c 'import sys; print(sys.version)' >&2
tar -C "$ROOT" -c . | docker import \
  --change 'ENV PATH=/usr/bin' \
  --change 'WORKDIR /work' \
  --change 'CMD ["/usr/bin/python3","-I","-S","-X","utf8","/opt/judge/runner.py"]' \
  - teacher-judge:current >/dev/null
echo "image teacher-judge:current built ($(docker image inspect teacher-judge:current --format '{{.Size}}') bytes)"
