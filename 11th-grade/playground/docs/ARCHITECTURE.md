# Architecture

## Why a static + Pyodide app?

Lab PCs are Windows, often without reliable LAN under load, and without internet during class. A folder that serves itself locally is the most portable shape:

- Student opens a local URL.
- Python code runs **inside the browser** via Pyodide (CPython compiled to WebAssembly).
- No shared judge server, no Docker, no admin rights beyond “run Python once to serve files”.

Trade-off: behavior is very close to CPython, but not a bit-identical Quera sandbox (time limits and filesystem rules differ). Good enough for module-1 pedagogy.

## Student-facing layout

```
teacher-playground/
  شروع.bat     ← only file at repo root (students open this)
  app/         ← static site + launcher.py + vendor/pyodide
  tools/       ← CLI / fetch / bundle check
  docs/        ← teacher documentation
```

The HTTP document root is **`app/`**, not the repo root.

## Code editor

The student editor is **CodeMirror 5** vendored under `app/vendor/codemirror/` (MIT), wrapped by `app/js/editor.js`:

- Python syntax highlighting
- Line numbers, active line, match brackets
- Auto-close brackets/quotes, smart indent on Enter
- Tab / Shift-Tab indent, Ctrl+/ comment toggle
- Alt+Shift+↑/↓ duplicate lines (fallback Ctrl+Shift+D), Alt+↑/↓ move lines, Ctrl+Shift+K delete line

Still fully offline — no CDN.

## Data flow

```
app/data/problems.json ──► app/js/app.js ──► editor + UI
                                │
                                ▼
                         app/js/runner.js ──► constraint check
                                │
                                ▼
                         Pyodide (app/vendor/pyodide)
                                │
                                ▼
                         app/js/diff.js ──► results panel
```

Progress keys in `localStorage`:

- `teacher-playground-progress-v1` — solved flags
- `teacher-playground-hints-v1` — how many hint levels revealed
- `teacher-playground-code-v1` — draft code per problem id

## Judging modes

### `stdio`

1. Redirect `stdin` to the test string.
2. `exec` student code.
3. Capture `stdout`.
4. Compare with expected using exact newline-normalized equality.

### `function`

1. `exec` student code.
2. Call `functionName(*args, **kwargs)`.
3. JSON-normalize the return value (tuples → lists, etc.) and deep-compare.

### Constraints

Before running tests, `runner.js` strips strings/comments roughly and checks style rules. Violations **block** judging even if output would be correct — intentional for “solve with for not while” / “no `max(...)`” exercises.

Matching rules (important for fairness):

| Token kind | Examples | How we match | OK | Blocked |
|------------|----------|--------------|----|---------|
| Keyword | `for`, `while`, `def`, `import` | whole word | — | forbidden keyword present / required missing |
| Builtin call | `max`, `min`, `sum`, `sorted`, … | **call form only** `(?<![\w.])max\s*\(` | variable `max = a` or name `best` | `max(a, b)` |

So a student who solves with `if` and names a variable `max` / `sum` is **not** punished. Calling `max(...)` / `sum(...)` is.

Exercises that use callable forbids (same rule everywhere):

| Problem | Forbid (calls) | Why variable names must stay allowed |
|---------|----------------|--------------------------------------|
| p07 | `max`, `sorted` | `max = a` is a normal student pattern |
| p10, p14 | `sum` | `sum = 0` then `sum += x` is common |
| p15 | `str` | statement bans converting via `str(...)` |

Keyword forbids (`for` / `while` / …) are already safe: those are not legal variable names in Python.

This is still not a security sandbox: tricks like `getattr(__builtins__, "max")` or `f"{n}"` instead of `str(n)` can bypass the source scan. Good enough for lab self-practice; do not treat it as anti-cheat for graded contests.

## Failure UX

`diff.js` reports:

- First differing character index (spaces labeled as فاصله / shown as `·`)
- Per-line char diff (red = missing expected, green = unexpected actual)
- Expandable full expected / actual blocks

## Host Python vs browser Python

Lab PCs often have a bare Python install (no pip packages). That is fine:

- **Host Python** (or PowerShell) only serves static files. Uses stdlib `http.server` — **zero pip dependencies**.
- **Student Python** runs in-browser via vendored Pyodide (`app/vendor/pyodide/`), including stdlib modules such as `math`.

So “missing packages on the lab image” does not affect judging. Copy the whole repo folder; do not rely on site-packages.

## Offline assets

`app/vendor/pyodide/` must contain at least:

- `pyodide.js`
- `pyodide.asm.js`
- `pyodide.asm.wasm`
- `python_stdlib.zip`
- `package.json`
- `pyodide-lock.json` (if present for that release)

Served from `indexURL: "vendor/pyodide/"` relative to `app/`.

### Why boot often looks “stuck” on lab PCs

The UI message «بارگذاری Pyodide» waits on `loadPyodide()`, which downloads ~10 MB of local assets and **compiles WebAssembly in the browser**. On weak school machines that compile step commonly takes **20–90 seconds** with no real progress events — so the bar used to freeze at ~55% and look hung even when work was happening. The boot ticker now advances slowly during that wait and times out after 2 minutes with a Persian hint.

Other real failure modes:

| Cause | Symptom |
|-------|---------|
| Wrong `.wasm` MIME (old Python `http.server`) | Load never finishes or fails quietly |
| Opening `index.html` via `file://` | Fetch of wasm/stdlib blocked |
| Incomplete USB copy (missing `pyodide.asm.wasm`) | Fail at «بررسی فایل‌های آفلاین» |
| Internet Explorer / non-Chromium Edge | No supported WebAssembly at all |
| Running from a slow USB stick | Same compile, much longer I/O |

`launcher.py` forces `Content-Type: application/wasm` for `.wasm` so lab Pythons that lack that MIME mapping do not break the load.

### Two engines: modern + legacy fallback

Current Pyodide (0.26.4, `app/vendor/pyodide/`) needs WebAssembly reference types (`externref`), i.e. **Chrome/Edge 96+** (released Nov 2021). Older lab browsers fail with:

```
CompileError: WebAssembly.instantiateStreaming(): invalid value type 'externref' …
wasm instantiation failed!
```

So the app also vendors Pyodide **0.23.4** (`app/vendor/pyodide-legacy/`) — the last line before `externref` (Chrome 71+, Firefox 70+, Safari 14+). Boot flow (`app/js/compat.js` + `app.js`):

1. `needsLegacyEngine(userAgent)` — Chrome/Edge < 96 or Firefox < 79 go **straight** to legacy (no wasted 10 MB download).
2. Otherwise load modern; if it throws an `isWasmCompatError()` failure (externref / CompileError / instantiateStreaming), automatically fall back to legacy.
3. Missing files and timeouts are **not** compat errors — they surface as Persian errors with a «تلاش دوباره» button and expandable technical details.

Both engines run the same `runner.js` harness and stdlib subset (`math` smoke test), so exercises behave identically. `tools/fetch-pyodide.*` downloads both; `tools/check-bundle.ps1` requires both; `شروع.bat` / `launcher.py` / `serve.ps1` verify both.

Teachers can verify the fallback on any modern PC by opening the app with `?engine=legacy` in the URL (forces the legacy engine); `?engine=modern` disables the fallback.

## Windows local server

Lab PCs double-click `شروع.bat`, which launches `app/launcher.py` (Tkinter, stdlib only):

1. Verify the vendored Pyodide files exist.
2. On **شروع تمرین**, bind a free loopback port (8765–8785) with `ThreadingHTTPServer` serving `app/`.
3. Optionally open the default browser (checkbox, on by default after an explicit click).
4. **توقف** / window close shuts the server down.

CLI fallback for teachers: `tools/start-cli.bat` → `tools/serve.ps1` (Python or PowerShell HttpListener).

Students must use `http://127.0.0.1:…`, never `file://`.
