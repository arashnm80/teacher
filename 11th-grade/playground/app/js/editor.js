/**
 * Offline CodeMirror 5 Python editor (line numbers, highlight, indent, autoclose).
 * Uses global `CodeMirror` from vendor/codemirror/*.js (classic scripts, not ESM).
 *
 * VS Code-like shortcuts:
 * - Alt+Shift+↓/↑ — duplicate line(s)  (also Ctrl+Shift+D / Ctrl+Shift+Alt+↑)
 * - Alt+↓/↑ — move line(s)
 * - Ctrl+Shift+K — delete line(s)
 * - Tab / Shift+Tab, Ctrl+/, Enter indent
 *
 * Note: On some Windows layouts Alt+Shift alone switches keyboard language, so we
 * also handle the combo via a capturing keydown listener (not only extraKeys).
 */

import { define, t } from "./i18n.js?v=5";

define({
  "edit.load": { fa: "ویرایشگر کد بارگذاری نشد (CodeMirror). فایل‌های vendor/codemirror را کامل کپی کنید یا صفحه را تازه کنید.", en: "The code editor (CodeMirror) did not load. Copy the whole vendor/codemirror folder, or reload the page." },
  "edit.tab": { fa: "تورفتگی (Tab)", en: "Indent (Tab)" },
  "edit.left": { fa: "یک نویسه به چپ", en: "One character left" },
  "edit.right": { fa: "یک نویسه به راست", en: "One character right" },
  "edit.undo": { fa: "واگرد", en: "Undo" },
  "edit.keys": { fa: "نویسه‌های کدنویسی", en: "Coding keys" },
  "edit.ready": { fa: "ویرایشگر کد آماده نیست (CodeMirror). صفحه را تازه کنید؛ اگر آفلاین هستید پوشه vendor/codemirror را کامل کپی کنید.", en: "The code editor (CodeMirror) is not ready. Reload the page; if you are offline, copy the whole vendor/codemirror folder." },
});

import { loadScript } from "./compat.js?v=12";
import { bootNote } from "./bootlog.js?v=12";

export const CODEMIRROR_SCRIPTS = [
  "vendor/codemirror/codemirror.min.js",
  "vendor/codemirror/mode/python/python.min.js",
  "vendor/codemirror/addon/edit/closebrackets.min.js",
  "vendor/codemirror/addon/edit/matchbrackets.min.js",
  "vendor/codemirror/addon/edit/trailingspace.min.js",
  "vendor/codemirror/addon/selection/active-line.min.js",
  "vendor/codemirror/addon/comment/comment.min.js",
];

let codemirrorReady = null;

/** Load vendor scripts if the HTML tags did not define window.CodeMirror. */
export async function ensureCodeMirror() {
  if (typeof globalThis.CodeMirror === "function") {
    bootNote("CodeMirror already present from HTML script tags");
    return globalThis.CodeMirror;
  }
  bootNote("CodeMirror missing after HTML tags; loading vendor scripts dynamically");
  if (!codemirrorReady) {
    codemirrorReady = (async () => {
      for (const src of CODEMIRROR_SCRIPTS) {
        bootNote(`loading ${src}`);
        await loadScript(src);
      }
      if (typeof globalThis.CodeMirror !== "function") {
        throw new Error(
          t("edit.load")
        );
      }
      bootNote("CodeMirror ready after dynamic load");
      return globalThis.CodeMirror;
    })().catch((err) => {
      codemirrorReady = null;
      throw err;
    });
  }
  return codemirrorReady;
}

function selectedLineRange(cm) {
  const from = cm.getCursor("from");
  const to = cm.getCursor("to");
  let start = from.line;
  let end = to.line;
  if (to.line > from.line && to.ch === 0) {
    end = to.line - 1;
  }
  return { start, end, anchorCh: from.ch, headCh: to.ch };
}

function linesText(cm, start, end) {
  const parts = [];
  for (let i = start; i <= end; i++) {
    parts.push(cm.getLine(i) ?? "");
  }
  return parts.join("\n");
}

function duplicateLines(cm, direction) {
  if (cm.getOption("readOnly")) return;
  const { start, end, anchorCh, headCh } = selectedLineRange(cm);
  const text = linesText(cm, start, end);
  const lineCount = end - start + 1;

  cm.operation(() => {
    if (direction === "down") {
      // Insert a copy immediately below the block.
      const endLen = (cm.getLine(end) || "").length;
      cm.replaceRange("\n" + text, { line: end, ch: endLen }, null, "+input");
      cm.setSelection(
        { line: start + lineCount, ch: anchorCh },
        { line: end + lineCount, ch: headCh }
      );
    } else {
      cm.replaceRange(text + "\n", { line: start, ch: 0 }, null, "+input");
      cm.setSelection(
        { line: start, ch: anchorCh },
        { line: end, ch: headCh }
      );
    }
  });
}

function moveLines(cm, direction) {
  if (cm.getOption("readOnly")) return;
  const { start, end, anchorCh, headCh } = selectedLineRange(cm);
  if (direction === "up" && start === 0) return;
  if (direction === "down" && end >= cm.lastLine()) return;

  cm.operation(() => {
    const block = linesText(cm, start, end);
    if (direction === "down") {
      const below = cm.getLine(end + 1) ?? "";
      // Replace start..end+1 with below + block
      const from = { line: start, ch: 0 };
      const to =
        end + 1 < cm.lastLine()
          ? { line: end + 2, ch: 0 }
          : { line: end + 1, ch: below.length };
      let next = below + "\n" + block;
      if (end + 1 < cm.lastLine()) next += "\n";
      cm.replaceRange(next, from, to, "+input");
      cm.setSelection(
        { line: start + 1, ch: anchorCh },
        { line: end + 1, ch: headCh }
      );
    } else {
      const above = cm.getLine(start - 1) ?? "";
      const from = { line: start - 1, ch: 0 };
      const to =
        end < cm.lastLine()
          ? { line: end + 1, ch: 0 }
          : { line: end, ch: (cm.getLine(end) || "").length };
      let next = block + "\n" + above;
      if (end < cm.lastLine()) next += "\n";
      else if (!next.endsWith("\n") && end === cm.lastLine() && start - 1 >= 0) {
        // keep as-is
      }
      cm.replaceRange(next, from, to, "+input");
      cm.setSelection(
        { line: start - 1, ch: anchorCh },
        { line: end - 1, ch: headCh }
      );
    }
  });
}

function deleteLines(cm) {
  if (cm.getOption("readOnly")) return;
  const { start, end } = selectedLineRange(cm);
  cm.operation(() => {
    if (end < cm.lastLine()) {
      cm.replaceRange("", { line: start, ch: 0 }, { line: end + 1, ch: 0 }, "+input");
    } else if (start > 0) {
      const prevLen = (cm.getLine(start - 1) || "").length;
      cm.replaceRange(
        "",
        { line: start - 1, ch: prevLen },
        { line: end, ch: (cm.getLine(end) || "").length },
        "+input"
      );
    } else {
      cm.setValue("");
    }
    cm.setCursor({ line: Math.min(start, cm.lastLine()), ch: 0 });
  });
}

function isArrowDown(e) {
  return e.key === "ArrowDown" || e.key === "Down" || e.keyCode === 40;
}

function isArrowUp(e) {
  return e.key === "ArrowUp" || e.key === "Up" || e.keyCode === 38;
}

/** Closing characters that Tab can step over (the ones closebrackets inserts). */
const TAB_OUT_CLOSERS = ")]}'\"";

/**
 * Tab-out: when the cursor sits right before a closing bracket or quote, Tab moves
 * the cursor past it instead of inserting spaces. A quote is stepped over only when
 * an odd number of the same quote comes before the cursor on this line, so an
 * opening quote is never skipped. At the start of a line Tab still indents.
 * Returns true when the cursor moved.
 */
function tabOut(cm) {
  const cur = cm.getCursor();
  const line = cm.getLine(cur.line) || "";
  const next = line.charAt(cur.ch);
  if (!next || !TAB_OUT_CLOSERS.includes(next)) return false;
  const before = line.slice(0, cur.ch);
  if (!before.trim()) return false;
  if (next === "'" || next === '"') {
    const quotes = before.split(next).length - 1;
    if (quotes % 2 === 0) return false;
  }
  cm.setCursor({ line: cur.line, ch: cur.ch + 1 });
  return true;
}

/** Capture Alt/Shift combos before Windows layout-switch / CM default maps eat them. */
function attachLineShortcutCapture(cm) {
  const onKeyDown = (e) => {
    if (cm.getOption("readOnly")) return;
    const down = isArrowDown(e);
    const up = isArrowUp(e);
    if (!down && !up) return;

    const onlyAltShift = e.altKey && e.shiftKey && !e.ctrlKey && !e.metaKey;
    const onlyAlt = e.altKey && !e.shiftKey && !e.ctrlKey && !e.metaKey;

    if (onlyAltShift) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof e.stopImmediatePropagation === "function") e.stopImmediatePropagation();
      duplicateLines(cm, down ? "down" : "up");
      return;
    }
    if (onlyAlt) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof e.stopImmediatePropagation === "function") e.stopImmediatePropagation();
      moveLines(cm, down ? "down" : "up");
    }
  };

  // Capture on both the hidden textarea and the visible wrapper.
  const input = cm.getInputField();
  const wrap = cm.getWrapperElement();
  input.addEventListener("keydown", onKeyDown, true);
  wrap.addEventListener("keydown", onKeyDown, true);
}

export function createPythonEditor(textarea, { onChange } = {}) {
  if (typeof globalThis.CodeMirror !== "function") {
    throw new Error(
      t("edit.ready")
    );
  }

  const cm = globalThis.CodeMirror.fromTextArea(textarea, {
    mode: { name: "python", version: 3, singleLineStringErrors: false },
    theme: "material-darker",
    lineNumbers: true,
    lineWrapping: true,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    smartIndent: true,
    electricChars: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    styleActiveLine: true,
    showTrailingSpace: true,
    autofocus: false,
    direction: "ltr",
    rtlMoveVisually: true,
    viewportMargin: Infinity,
    extraKeys: {
      Tab(cm) {
        if (cm.somethingSelected()) {
          cm.indentSelection("add");
        } else if (!tabOut(cm)) {
          cm.replaceSelection("    ", "end", "+input");
        }
      },
      "Shift-Tab"(cm) {
        cm.indentSelection("subtract");
      },
      Enter(cm) {
        cm.execCommand("newlineAndIndent");
      },
      "Ctrl-/"() {
        cm.execCommand("toggleComment");
      },
      "Cmd-/"() {
        cm.execCommand("toggleComment");
      },
      // Keep CM map entries too (name order Alt- then Shift- matches CM keyName()).
      "Alt-Shift-Down"(cm) {
        duplicateLines(cm, "down");
      },
      "Alt-Shift-Up"(cm) {
        duplicateLines(cm, "up");
      },
      "Shift-Alt-Down"(cm) {
        duplicateLines(cm, "down");
      },
      "Shift-Alt-Up"(cm) {
        duplicateLines(cm, "up");
      },
      "Alt-Down"(cm) {
        moveLines(cm, "down");
      },
      "Alt-Up"(cm) {
        moveLines(cm, "up");
      },
      // Reliable fallback when Windows steals Alt+Shift for language switch.
      "Ctrl-Shift-D"(cm) {
        duplicateLines(cm, "down");
      },
      "Cmd-Shift-D"(cm) {
        duplicateLines(cm, "down");
      },
      "Ctrl-Shift-Alt-Up"(cm) {
        duplicateLines(cm, "up");
      },
      "Ctrl-Shift-K"(cm) {
        deleteLines(cm);
      },
      "Cmd-Shift-K"(cm) {
        deleteLines(cm);
      },
    },
  });

  cm.setOption("autoCloseBrackets", {
    pairs: "()[]{}''\"\"",
    closeBefore: ")]}'\":;,>",
    triples: "",
    explode: "[]{}",
  });

  attachLineShortcutCapture(cm);
  // Phone keyboards fix, capitalise and suggest words: none of that belongs in code.
  const field = cm.getInputField();
  for (const [name, value] of [["autocapitalize", "off"], ["autocorrect", "off"], ["autocomplete", "off"], ["spellcheck", "false"]]) {
    field.setAttribute(name, value);
  }

  if (typeof onChange === "function") {
    cm.on("change", (instance, change) => onChange(cm.getValue(), change));
  }

  requestAnimationFrame(() => cm.refresh());

  return {
    getValue: () => cm.getValue(),
    setValue(value) {
      const next = value ?? "";
      const cur = cm.getValue();
      if (cur === next) return;
      const scroll = cm.getScrollInfo();
      cm.setValue(next);
      cm.scrollTo(scroll.left, scroll.top);
    },
    setReadOnly(ro) {
      cm.setOption("readOnly", ro ? "nocursor" : false);
    },
    focus() {
      cm.focus();
    },
    refresh() {
      cm.refresh();
    },
    raw: cm,
  };
}

/**
 * A row of the characters that are slow to find on a phone keyboard (brackets, colon, quotes, Tab, ...).
 * It is shown only on touch screens (see .keybar in style.css). Pressing a key does not take the
 * focus from the editor, so the keyboard stays open. What a key types counts as typing.
 */
const KEYS = [
  { label: "Tab", tab: true },
  { label: ":", text: ":" },
  { label: "( )", pair: "()" },
  { label: "[ ]", pair: "[]" },
  { label: "{ }", pair: "{}" },
  { label: "\" \"", pair: '""' },
  { label: "' '", pair: "''" },
  { label: "=", text: "=" },
  { label: "#", text: "#" },
  { label: "_", text: "_" },
  { label: ",", text: "," },
  { label: ".", text: "." },
  { label: "+", text: "+" },
  { label: "-", text: "-" },
  { label: "*", text: "*" },
  { label: "/", text: "/" },
  { label: "%", text: "%" },
  { label: "<", text: "<" },
  { label: ">", text: ">" },
  { label: "!", text: "!" },
  { label: "\\", text: "\\" },
  ..."0123456789".split("").map((d) => ({ label: d, text: d })),
];

export function createKeyBar(editor, container) {
  const cm = editor.raw;
  container.replaceChildren();
  container.setAttribute("role", "toolbar");
  container.setAttribute("aria-label", t("edit.keys"));
  const add = (label, title, action, extra = "") => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `key ${extra}`.trim();
    button.textContent = label;
    button.title = title;
    button.setAttribute("aria-label", title);
    // Keep the editor focused (and the keyboard open) when a key is pressed.
    button.addEventListener("pointerdown", (event) => event.preventDefault());
    button.addEventListener("mousedown", (event) => event.preventDefault());
    button.addEventListener("click", () => {
      if (cm.getOption("readOnly")) return;
      action();
      cm.focus();
    });
    container.append(button);
  };
  add("↶", t("edit.undo"), () => cm.undo(), "icon");
  add("←", t("edit.left"), () => cm.execCommand("goCharLeft"), "icon");
  add("→", t("edit.right"), () => cm.execCommand("goCharRight"), "icon");
  for (const key of KEYS) {
    if (key.tab) {
      add("Tab", t("edit.tab"), () => {
        if (cm.somethingSelected()) cm.indentSelection("add");
        else cm.replaceSelection("    ", "end", "+input");
      }, "wide");
    } else if (key.pair) {
      add(key.label, key.pair, () => {
        const picked = cm.getSelection();
        cm.replaceSelection(key.pair[0] + picked + key.pair[1], "end", "+input");
        if (!picked) cm.execCommand("goCharLeft");
      });
    } else {
      add(key.label, key.text, () => cm.replaceSelection(key.text, "end", "+input"));
    }
  }
  return container;
}
