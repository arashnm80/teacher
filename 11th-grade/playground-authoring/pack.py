#!/usr/bin/env python3
"""Check, version, zip and publish the playground.

    python3 pack.py          # build + check, bump version, rebuild zip,
                             # then build_site.py and deploy.sh
    python3 pack.py --no-deploy

Nothing is published if build.py (the checks) fails.
"""
from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # 11th-grade/
PLAY = ROOT / "playground"
ZIP = ROOT / "extras" / "teacher-playground-offline.zip"
SKIP = {"__pycache__", ".DS_Store"}


def run(cmd: list[str], cwd: Path) -> None:
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def bump_version() -> int:
    vfile = HERE / "VERSION"
    v = int(vfile.read_text().strip()) + 1
    vfile.write_text(f"{v}\n")
    return v


def replace_in(path: Path, pattern: str, repl: str) -> int:
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(pattern, repl, text)
    if n:
        path.write_text(new, encoding="utf-8")
    return n


def build_zip() -> int:
    ZIP.parent.mkdir(parents=True, exist_ok=True)
    tmp = ZIP.with_suffix(".zip.tmp")
    count = 0
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(PLAY.rglob("*")):
            if not path.is_file() or any(part in SKIP for part in path.parts) or path.suffix == ".pyc":
                continue
            z.write(path, "teacher-playground/" + path.relative_to(PLAY).as_posix())
            count += 1
    tmp.replace(ZIP)
    return count


def main() -> int:
    no_deploy = "--no-deploy" in sys.argv
    run([sys.executable, "build.py"], HERE)          # fails here if any check fails
    v = bump_version()
    app_js = PLAY / "app" / "js" / "app.js"
    n1 = replace_in(app_js, r"data/(problems|concepts)\.json\?v=\d+", rf"data/\1.json?v={v}")
    n2 = replace_in(PLAY / "app" / "index.html", r"teacher-playground-offline\.zip\?v=\d+", f"teacher-playground-offline.zip?v={v}")
    n3 = replace_in(ROOT / "build_site.py", r"teacher-playground-offline\.zip\?v=\d+", f"teacher-playground-offline.zip?v={v}")
    # app.js changes on every publish (data refs), so its URL in index.html must change too.
    n4 = replace_in(PLAY / "app" / "index.html", r'var APP_JS = "js/app\.js\?v=\d+";', f'var APP_JS = "js/app.js?v={v}";')
    print(f"version {v}: data refs {n1}, index refs {n2}, build_site refs {n3}, app.js key {n4}")
    # The separate playground zip was replaced by the whole-site zip (build_site.py).
    if not no_deploy:
        run([sys.executable, "build_site.py"], ROOT)
        run(["bash", "deploy.sh"], ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
