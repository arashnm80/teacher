/**
 * Bidirectional helpers for Persian UI mixed with English/Python snippets.
 *
 * Important: never wrap "1." as a single LTR island. In an RTL line the period
 * becomes the outer (rightmost) glyph and reads as ".1". Split number + dot.
 */

/** Wrap plain text so Latin/code/digits stay LTR inside an RTL sentence (textContent-safe). */
export function ltrIsolate(text) {
  return `\u2066${String(text ?? "")}\u2069`;
}

/** HTML snippet for an LTR island (code, URL, Latin keyword, bare digits — no trailing dot). */
export function ltrHtml(text) {
  return `<span class="ltr" dir="ltr">${escapeHtml(String(text ?? ""))}</span>`;
}

/**
 * Numbered label for RTL lists/titles: visual "1. عنوان" (digit on the outside, then dot).
 * Do NOT use ltrHtml(`${n}.`) — that renders as ".1" in RTL.
 */
export function indexLabelHtml(n) {
  return (
    `<span class="idx-num" dir="ltr">${escapeHtml(String(n))}</span>` +
    `<span class="idx-dot">.</span>`
  );
}

/**
 * Escape Persian/English mixed copy and wrap Latin/python-ish runs as LTR islands.
 * Use for titles, topics, and other strings that are not full markdown.
 * Digits are wrapped alone (no trailing "." glued into the island).
 */
export function bidiMixHtml(text) {
  const esc = escapeHtml(String(text ?? ""));
  return esc.replace(
    /[A-Za-z][A-Za-z0-9_./()<>+\-]*(?:\(\))?|[0-9]+(?:\.[0-9]+)*/g,
    (m) => `<span class="ltr" dir="ltr">${m}</span>`
  );
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}
