/** Line and character diffs for expected vs actual output. */

export function normalizeNewlines(text) {
  return String(text ?? "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

export function lineDiff(expected, actual) {
  const a = normalizeNewlines(expected).split("\n");
  const b = normalizeNewlines(actual).split("\n");
  // Drop single trailing empty line for friendlier comparison display,
  // but keep content differences intact in the raw strings.
  while (a.length > 1 && a[a.length - 1] === "") a.pop();
  while (b.length > 1 && b[b.length - 1] === "") b.pop();

  const max = Math.max(a.length, b.length);
  const rows = [];
  for (let i = 0; i < max; i++) {
    const left = i < a.length ? a[i] : null;
    const right = i < b.length ? b[i] : null;
    if (left === right) {
      rows.push({ type: "same", expected: left, actual: right, index: i + 1 });
    } else {
      rows.push({ type: "diff", expected: left, actual: right, index: i + 1 });
    }
  }
  return rows;
}

/** Myers-inspired short char diff for a single line pair. */
export function charDiff(expected, actual) {
  const a = [...normalizeNewlines(expected ?? "")];
  const b = [...normalizeNewlines(actual ?? "")];
  const n = a.length;
  const m = b.length;
  const dp = Array.from({ length: n + 1 }, () => Array(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[i][j] =
        a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    }
  }
  const parts = [];
  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) {
      parts.push({ type: "same", text: a[i] });
      i += 1;
      j += 1;
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      parts.push({ type: "del", text: a[i] });
      i += 1;
    } else {
      parts.push({ type: "add", text: b[j] });
      j += 1;
    }
  }
  while (i < n) {
    parts.push({ type: "del", text: a[i++] });
  }
  while (j < m) {
    parts.push({ type: "add", text: b[j++] });
  }
  return mergeParts(parts);
}

function mergeParts(parts) {
  const out = [];
  for (const part of parts) {
    const last = out[out.length - 1];
    if (last && last.type === part.type) last.text += part.text;
    else out.push({ ...part });
  }
  return out;
}

export function visibleChar(ch) {
  if (ch === " ") return "·";
  if (ch === "\t") return "→";
  if (ch === "\n") return "↵\n";
  return ch;
}

export function explainFirstDifference(expected, actual) {
  const e = normalizeNewlines(expected);
  const a = normalizeNewlines(actual);
  const len = Math.min(e.length, a.length);
  for (let i = 0; i < len; i++) {
    if (e[i] !== a[i]) {
      return {
        index: i,
        expected: e[i],
        actual: a[i],
        contextExpected: e.slice(Math.max(0, i - 8), i + 8),
        contextActual: a.slice(Math.max(0, i - 8), i + 8),
      };
    }
  }
  if (e.length !== a.length) {
    return {
      index: len,
      expected: e.length > a.length ? e[len] ?? "⟨پایان⟩" : "⟨پایان⟩",
      actual: a.length > e.length ? a[len] ?? "⟨پایان⟩" : "⟨پایان⟩",
      contextExpected: e.slice(Math.max(0, len - 8), len + 8),
      contextActual: a.slice(Math.max(0, len - 8), len + 8),
    };
  }
  return null;
}
