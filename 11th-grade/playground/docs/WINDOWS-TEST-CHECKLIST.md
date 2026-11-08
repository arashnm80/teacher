# Windows test checklist

Use this after cloning on a lab Windows machine.

## Setup

- [ ] Folder copied including `app/vendor/pyodide/`
- [ ] Root contains **only** `شروع.bat` as a visible file (plus `app/`, `tools/`, `docs/` folders)
- [ ] `tools\check-bundle.ps1` prints PASSED
- [ ] Double-click `شروع.bat` → small Persian launcher window appears
- [ ] Click **شروع تمرین** → browser opens the practice app; boot reaches «آماده است»
- [ ] **توقف** stops the server; closing the window asks before quit
- [ ] Problem list shows 01–30
- [ ] Optional stress: occupy 8765, start again → next free port works
- [ ] Optional CLI: `tools\start-cli.bat` still serves `app/`

## RTL / bilingual display

- [ ] Problem 01 statement: `` `Hello, NAME` `` stays LTR inside Persian prose
- [ ] Inline tip under editor: `input()` reads correctly
- [ ] Constraint on problem 09: `for` / `while` do not reverse
- [ ] Failed diff meta (position + expected/actual chars) stays ordered
- [ ] Title/progress numbers show as `1. عنوان` (not `.1 عنوان`); summary `1 از 30` correct

## Editor (CodeMirror)

- [ ] Line numbers visible; Python keywords colored
- [ ] Typing `(` inserts `)`; same for `[]{}` and quotes
- [ ] Enter after `:` indents the next line
- [ ] Tab indents; Shift+Tab dedents
- [ ] Alt+Shift+Down duplicates the current line; Alt+Down moves it
- [ ] Editor stays LTR inside the RTL page

## Core flows

- [ ] Open problem 01, paste a **correct** solution → all tests green; problem marked solved
- [ ] Break the space in `Hello, NAME` → failure message mentions فاصله / shows `·`
- [ ] Put `input("name?")` → failure (extra prompt text in output)
- [ ] Problem 09 (for-only): solve with `while` → constraint warning, tests not run
- [ ] Problem 13 (while-only): solve with `for` → constraint warning
- [ ] Problem 07: `max(a,b,c)` or `sorted([...])[-1]` → constraint warning; `if` + variable `max` → tests run
- [ ] Problem 10: `sum([...])` → constraint warning; `sum = 0` / `sum += x` in a `for` → tests run
- [ ] Problem 14: same `sum(...)` vs variable `sum` check under `while`
- [ ] Problem 15: `len(str(n))` → constraint warning; digit-count with `//= 10` → tests run
- [ ] Problem 19 or 25 (function mode) → callable tests pass
- [ ] Reveal hints 1→2→3; concept tab shows related tutorial
- [ ] Reload page → draft code and progress still there
- [ ] “پیشرفت من” shows solved count; clear progress works

## Browser matrix (at least one lab PC each)

- [ ] Microsoft Edge (Chromium)
- [ ] Google Chrome
- [ ] Old lab browser (Chrome/Edge < 96): boot shows «موتور سازگار» and still reaches «آماده است» via `pyodide-legacy` (on a modern PC, simulate with `?engine=legacy` in the URL)

## Performance / lab

- [ ] Works with network cable unplugged
- [ ] Two browsers on same PC don’t share progress (expected: separate profiles / storage)
- [ ] Acceptable first-load time for Pyodide on typical lab hardware
- [ ] DevTools console shows no 404 for `favicon.ico` or `pyodide.js.map`
- [ ] Boot failure (if forced, e.g. renamed vendor file) shows «بارگذاری ناموفق» + «تلاش دوباره» button, not a frozen bar

## Known issues to watch

- Antivirus locking `.wasm` (rare) — allow the folder
- Internet Explorer / Edge Legacy (non-Chromium) — unsupported, even by the legacy engine
- Chrome/Edge < 96 runs the legacy engine (0.23.4): same exercises, slightly slower boot
- `python` vs `py` launcher naming on locked-down images
- Stale server still bound to 8765 — launcher should move to the next free port
- Students opening files inside `app/` by mistake — remind them: only `شروع.bat`
