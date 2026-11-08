/**
 * Offline CodeMirror 5 Python editor (line numbers, highlight, indent, autoclose).
 * Expects global `CodeMirror` from vendor/codemirror/*.js (classic scripts, not ESM).
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
  if (typeof CodeMirror !== "function") {
    throw new Error("CodeMirror offline bundle missing (vendor/codemirror).");
  }

  const cm = CodeMirror.fromTextArea(textarea, {
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
        } else {
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

  if (typeof onChange === "function") {
    cm.on("change", () => onChange(cm.getValue()));
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
