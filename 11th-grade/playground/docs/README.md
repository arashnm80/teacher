> This app now lives inside the `teacher` repo at `11th-grade/playground/`.
> Online: https://teacher.arashnm80.ir/playground/

# teacher-playground — تمرین پایتون (پودمان ۱)

Offline, browser-based Python practice for grade-11 lab PCs. Students get Quera-style tests **plus** learning tools Quera does not show: multi-level hints, concept tutorials, and line/character diffs when a test fails.

Primary language of the UI and problem statements: **Persian (RTL)**.

---

## Students (Windows lab PC)

1. Open the `teacher-playground` folder.
2. Double-click **`شروع.bat`** (the only file in that folder).
3. Click **شروع تمرین** in the small window.
4. Leave that window open while practicing.

Do **not** open anything inside `app/` or `tools/`.

---

## Folder layout

```
teacher-playground/
  شروع.bat          ← only file students should open
  app/              web app + Tkinter launcher + vendored Pyodide
  tools/            teacher/CLI helpers
  docs/             this README and technical notes
```

---

## Goal

Classroom reality: students submit to Quera but cannot see *why* a test failed (missing space, wrong case, `input("prompt")` pollution, used `while` instead of `for`, …).

This app is copied onto lab machines (USB / local share), runs **without internet**, and is used for **self-practice only** (progress stays in that browser’s `localStorage`).

| Topic | Choice |
|-------|--------|
| Runtime | **Pyodide in the browser** (no server-side judge) |
| Problem types | **Both** stdin/stdout and callable-function tests |
| Style constraints | Per-problem `require` / `forbid` (keywords as words; builtins only as calls — `sum = 0` OK, `sum(...)` blocked when forbidden) |
| Content | **30** problems for book module 1 |
| Networking | **No class server** |
| Hints | **Multi-level** + concept panel |

### What the lab PC needs (and what it does **not**)

| Needed | Not needed |
|--------|------------|
| This folder **including** `app/vendor/pyodide/` | `pip install …` |
| Chrome or Edge | Internet after the folder is copied |
| **Python 3** with Tkinter (normal python.org install) | Anaconda, VS Code, Jupyter |

Student code runs **inside the browser** via vendored Pyodide. Host Python only shows the launcher and serves static files.

Teacher checks before class:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File tools\check-bundle.ps1
```

CLI server (no GUI):

```bat
tools\start-cli.bat
```

### Important Windows notes

- Do **not** open `app\index.html` via double-click (`file://`).
- Prefer **Chrome** or **Edge** (Chromium; not IE mode or legacy Edge).
- `app/vendor/pyodide/` (modern) + `app/vendor/pyodide-legacy/` (for browsers older than Chrome/Edge 96) are already in the repo (~30 MB total).
- First open on a slow lab PC can sit on «بارگذاری Pyodide» for up to about a minute while the browser compiles WebAssembly — that is normal; copy the folder to the local disk if USB makes it worse.

### Linux / macOS

```bash
bash tools/start.sh
```

If Pyodide is missing (needs internet, once):

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File tools\fetch-pyodide.ps1
```

```bash
bash tools/fetch-pyodide.sh
```

---

## What students see

1. Problem list filtered by topic.
2. Statement + samples.
3. Editor (offline CodeMirror): Python colors, line numbers, auto-indent, auto-close `()[]{}''""`, Tab indent, Ctrl+/ comment, Alt+Shift+↓ duplicate line, Alt+↑/↓ move line — drafts saved in `localStorage`.
4. Run tests — pass/fail per case.
5. On failure: first differing character, spaces as `·`, line/char highlighting.
6. Hints (up to three levels) + concept tutorial.
7. Progress on this browser only.

Teaching tip: never put a message inside `input()`; it prints and breaks stdout tests.

---

## Problem JSON shape

Edit `app/data/problems.json`. See `docs/ARCHITECTURE.md` for judging details.

## RTL / bilingual text

Persian UI + English/Python fragments must stay readable. Follow **`docs/RTL-BIDI.md`** (LTR islands for code, URLs, digits). Cursor rule: `.cursor/rules/rtl-bidi.mdc`.

---

## License / ownership

Course material helper for Arash’s grade-11 Python module. Push target: [arashnm80/teacher-playground](https://github.com/arashnm80/teacher-playground).
