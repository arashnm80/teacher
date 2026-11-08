# RTL / LTR rules (Persian + English)

This project is **bilingual**: Persian UI/copy with English/Python fragments (`for`, `input()`, `Hello, NAME`, URLs, digit runs). Mixed direction must never “look broken”.

## Defaults

| Surface | Direction |
|---------|-----------|
| Page shell (`index.html`, chrome, prose) | **RTL** (`lang="fa"` + `dir="rtl"`) |
| Python editor, samples, diffs, stack traces, URLs | **LTR** (`dir="ltr"` + `unicode-bidi: isolate`) |
| Inline code / Latin keywords inside Persian sentences | **LTR island** |

Never put student code or judge output in an unmarked RTL run — parentheses, commas, and `http://` reorder badly.

## Required patterns

### 1. HTML / CSS

- Root: `<html lang="fa" dir="rtl">` and `html { direction: rtl; }`.
- LTR blocks: editor, `pre.sample`, `.diff-block`, fenced code, boot progress fill.
- LTR islands: `<code class="ltr" dir="ltr">…</code>` or `<span class="ltr" dir="ltr">…</span>`.
- Inline Latin chips must stay on the **same baseline** as Persian (`display: inline`, shared `line-height`, small `top` nudge for mono vs Tahoma) — never float high with `inline-block` alone.
- Prefer logical CSS (`padding-inline-start`, `margin-inline`) over raw `left`/`right` when adding layout.

### 2. JavaScript strings

Use helpers in `app/js/bidi.js`:

- `ltrHtml(text)` — known LTR token when building **HTML** (no trailing `.` after a number).
- `indexLabelHtml(n)` — RTL-safe `1.` / `12.` for lists and titles (digit + dot as separate nodes).
- `ltrIsolate(text)` — known LTR token in **plain text** / `textContent` (Unicode U+2066…U+2069).
- `bidiMixHtml(text)` — escape + auto-wrap Latin/digit runs (titles, topics).

Examples:

```js
// Good — numbered item in RTL
el.innerHTML = `${indexLabelHtml(3)} ${bidiMixHtml(title)}`;
msg = `فقط بنویسید: ${ltrIsolate("input()")}`;

// Bad — "3." as one LTR island looks like ".3" on an RTL line
el.innerHTML = `${ltrHtml("3.")} ${title}`;
el.textContent = `3. ${title}`;
msg = "فقط بنویسید: input()";
```

### 3. Content in `data/*.json`

- Surround Python/English tokens with markdown backticks: `` `for` ``, `` `input()` ``, `` `Hello, NAME` ``.
- Keep full code samples in fenced ``` blocks (rendered as LTR `pre`).
- Do not rely on bare `for`/`while` sitting unmarked in a Persian paragraph.

### 4. Tkinter launcher (`app/launcher.py`)

Windows Tk **does not** implement browser-quality bidi. Rules:

- Wrap every Persian string with `rtl()` from `app/tk_bidi.py` (RLE…PDF).
- Wrap every Latin/URL/path string with `ltr()`.
- **Never** put `شروع.bat` / `index.html` / `http://…` inside the same Label as Persian — use a separate LTR line.
- Never use a Latin-only font (e.g. Consolas) for Persian text; Tahoma for FA, Consolas only for pure LTR.
- `messagebox.*(…, parent=self.root)` so Tk does not spawn a ghost root window on close.
- Single-instance lock (port 8764) + `start "" /B …` in `شروع.bat` (empty START title) so closing one window does not leave a second launcher.

## Checklist before shipping UI copy

- [ ] Open a problem whose statement mixes Persian + `` `code` `` — code reads left-to-right.
- [ ] Fail a test with a space/punctuation mismatch — expected/actual glyphs stay ordered.
- [ ] Constraint warning mentioning `for` / `while` looks correct.
- [ ] Progress dialog numbers (`3 از 30`) do not reverse.
- [ ] Editor caret and Python indentation remain LTR.

## Agent / contributor rule

Any new Persian string that embeds English, Python, paths, URLs, or digit runs **must** use an LTR island (`ltrHtml` / `ltrIsolate` / `dir="ltr"` / backticks in JSON). Do not ship mixed runs “hoping the browser gets it right”.
