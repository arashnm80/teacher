/**
 * Bidirectional helpers for Persian UI mixed with English/Python snippets.
 *
 * Important: never wrap "1." as a single LTR island. In an RTL line the period
 * becomes the outer (rightmost) glyph and reads as ".1". Split number + dot.
 */

import { define, t } from "./i18n.js?v=5";

define({
  "md.done": { fa: "انجام شده", en: "Done" },
  "md.todo": { fa: "انجام نشده", en: "Not done" },
  "md.image": { fa: "تصویر", en: "Image" },
});

/** Wrap plain text so Latin/code/digits stay LTR inside an RTL sentence (textContent-safe). */
export function ltrIsolate(text) {
  return `⁦${String(text ?? "")}⁩`;
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

// ---------------------------------------------------------------------------
// Markdown-lite for the playground (statement, hints, guide, solutions).
//
// Persian text is the base direction. Every Latin run (English word, name,
// quoted string, operator) becomes an LTR island, so it keeps its order and
// its punctuation. Code blocks are LTR; the Persian parts inside them (Python
// comments, Persian strings) become RTL islands, so they read correctly too.
// ---------------------------------------------------------------------------

/** Latin runs with their quotes and inner punctuation (same rule as the lesson site). */
const LATIN_RUN =
  /["“]?_*[A-Za-z][A-Za-z0-9_.\-+#\/:\\'"“”’()\[\]{}=;,!?@$%*\s]*[A-Za-z0-9_#+)\]}"”’!?%]|["“]?[A-Za-z]/g;
/** Persian words, joined by spaces or punctuation (Persian text inside code). */
const PERSIAN_RUN =
  /[؀-ۿ‌‍]+(?:[\s،؛؟.:!«»()\-]+[؀-ۿ‌‍]+)*/g;
const HAS_PERSIAN = /[؀-ۿ]/;

/** Escape text and wrap every Latin run in an LTR island. */
export function isolateLatin(text) {
  const src = String(text ?? "");
  let out = "";
  let last = 0;
  for (const m of src.matchAll(LATIN_RUN)) {
    const run = m[0];
    const keep = latinIslandLength(run);
    out += escapeHtml(src.slice(last, m.index));
    out += `<span class="ltr" dir="ltr">${escapeHtml(run.slice(0, keep))}</span>`;
    // A closing bracket without its opening bracket in the run belongs to the Persian
    // sentence: it stays outside the island, so it is not mirrored by the LTR run.
    out += escapeHtml(run.slice(keep));
    last = m.index + run.length;
  }
  return out + escapeHtml(src.slice(last));
}

const CLOSING_TO_OPENING = { ")": "(", "]": "[", "}": "{" };

/** Length of the Latin island: unmatched closing brackets at its end are left out. */
function latinIslandLength(run) {
  let end = run.length;
  while (end > 0 && CLOSING_TO_OPENING[run[end - 1]]) {
    const closing = run[end - 1];
    const body = run.slice(0, end);
    const opens = body.split(CLOSING_TO_OPENING[closing]).length - 1;
    const closes = body.split(closing).length - 1;
    if (closes <= opens) break;
    end -= 1;
  }
  return end;
}

/** One paragraph or list item (statements, hints, concept text): the same rules as mdInline. */
export function inlineMd(text) {
  return mdInline(text);
}

/**
 * Text for a <pre> (LTR). Persian runs become RTL islands. With comments on,
 * a Python comment (the «#» outside quotes) keeps its «#» on the code side and
 * its Persian text in an RTL island, so the sentence reads in Persian order.
 */
export function codeHtml(text, { comments = true } = {}) {
  return String(text ?? "")
    .split("\n")
    .map((line) => codeLine(line, comments))
    .join("\n");
}

/** Tiny markdown subset: paragraphs, `code`, ``` fences, **bold**, lists. */
export function mdLite(src) {
  const parts = String(src || "").replace(/\r\n/g, "\n").split(/```/);
  let html = "";
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 1) {
      const body = parts[i].replace(/^\w*\n/, "").replace(/\n$/, "");
      html += `<pre class="ltr" dir="ltr"><code>${codeHtml(body)}</code></pre>`;
      continue;
    }
    for (const block of parts[i].split(/\n{2,}/)) {
      const trimmed = block.trim();
      if (!trimmed) continue;
      if (/^[-*] /.test(trimmed)) {
        const items = trimmed
          .split(/\n/)
          .map((line) => line.replace(/^[-*] /, "").trim())
          .filter(Boolean)
          .map((line) => `<li>${inlineMd(line)}</li>`)
          .join("");
        html += `<ul>${items}</ul>`;
      } else {
        html += `<p>${inlineMd(trimmed).replaceAll("\n", "<br>")}</p>`;
      }
    }
  }
  return html;
}

function codeLine(line, comments) {
  const cut = comments ? commentStart(line) : -1;
  if (cut < 0) return codeSpans(line);
  const code = codeSpans(line.slice(0, cut));
  const body = line.slice(cut + 1); // everything after the «#»
  if (!HAS_PERSIAN.test(body)) return code + escapeHtml("#" + body);
  // The «#» stays on the code side, on the left. The rest of the comment (Persian,
  // English or both) is one RTL island to its right: Persian runs right-to-left,
  // and English runs stay LTR islands in their own order.
  const lead = body.match(/^\s*/)[0];
  const tail = body.match(/\s*$/)[0];
  const core = body.trim();
  return (
    code +
    "#" +
    escapeHtml(lead) +
    `<span class="cm-fa" dir="rtl">${isolateLatin(core)}</span>` +
    escapeHtml(tail)
  );
}

function codeSpans(code) {
  let out = "";
  let last = 0;
  for (const m of code.matchAll(PERSIAN_RUN)) {
    out += escapeHtml(code.slice(last, m.index));
    out += `<span class="cm-fa" dir="rtl">${escapeHtml(m[0])}</span>`;
    last = m.index + m[0].length;
  }
  return out + escapeHtml(code.slice(last));
}

/** Index of a Python comment's «#» (outside quotes), or -1. */
function commentStart(line) {
  let quote = "";
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (quote) {
      if (ch === "\\") i++;
      else if (ch === quote) quote = "";
    } else if (ch === '"' || ch === "'") {
      quote = ch;
    } else if (ch === "#") {
      return i;
    }
  }
  return -1;
}


// ---------------------------------------------------------------------------
// Markdown for AI answers: headings, nested lists, tables, quotes, rules, code
// blocks, bold, italic and safe links. Every text is escaped, and only these
// tags are written. Latin runs stay LTR islands inside Persian text.
// ---------------------------------------------------------------------------

const MD_FENCE = /^\s*(`{3,}|~{3,})/;
const MD_HEADING = /^\s{0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$/;
const MD_RULE = /^\s{0,3}([-*_])(?:\s*\1){2,}\s*$/;
const MD_QUOTE = /^\s{0,3}>/;
const MD_LIST = /^(\s*)([-*+•◦▪●]|[\d۰-۹٠-٩]{1,3}[.)])\s+(.*)$/;
const MD_TABLE_SEP = /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/;
/** A heading underlined on the next line: === (large) or --- (smaller), like # and ##. */
const MD_SETEXT = /^\s{0,3}(=+|-+)\s*$/;
/** A formula on lines of its own, between $$ and $$ or between \[ and \]. */
const MD_DISPLAY = /^\s*(\$\$|\\\[)\s*$/;
/**
 * Set aside first, read left to right: `code`, \(LaTeX\), \[LaTeX\], $$LaTeX$$, $LaTeX$
 * and a backslash before punctuation. The first one that starts at a place wins.
 */
const MD_TOKEN =
  /`([^`\n]+)`|\\\(([^\n]+?)\\\)|\\\[([^\n]+?)\\\]|\$\$([^$\n]+?)\$\$|\$([^\s$](?:[^$\n]*?[^\s$])?)\$(?!\p{N})|\\([!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~])/gu;
/** Links, images, <autolinks> and bare addresses. Only http and https addresses become links. */
const MD_LINK =
  /(!?)\[([^\]\n]+)\]\(([^)\s]+)\)|<(https?:\/\/[^\s<>]+)>|(https?:\/\/[^\s<>"'`\u0000]*[^\s<>"'`.,;:!?)»”،؛؟\u0000])/giu;
const MD_ENTITY = /&(#[0-9]{1,7}|#[xX][0-9a-fA-F]{1,6}|[a-zA-Z]{2,8});/g;
const MD_BR = /<br\s*\/?>/gi;
/** Inline tags that are allowed, only as a complete pair (<b>…</b>); any other tag is shown as text. */
const MD_PAIRED_TAG = /<(b|strong|i|em|u|s|del|sub|sup|mark|kbd)>([\s\S]*?)<\/\1>/gi;
/** Emphasis, read on the text left after code, links and escapes were set aside. */
const MD_EMPHASIS =
  /\*\*\*([^*\n]+?)\*\*\*|\*\*((?:(?!\*\*)[^\n])+?)\*\*|\*([^*\s](?:[^*\n]*?[^*\s])?)\*|~~([^~\n]+?)~~|__([^\s_](?:[^_\n]*?[^\s_])?)__(?![\p{L}\p{N}])|_([^\s_](?:[^_\n]*?[^\s_])?)_(?![\p{L}\p{N}_])/gu;

/** Markdown from an AI answer, as safe HTML for the playground. */
export function renderMarkdown(source) {
  const lines = String(source ?? "").replaceAll("\u0000", "").replace(/\r\n?/g, "\n").replace(/\t/g, "    ").split("\n");
  return mdBlocks(lines);
}

function mdBlocks(lines) {
  let html = "";
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (MD_FENCE.test(line)) {
      const open = line.match(MD_FENCE)[1];
      const fenceIndent = line.match(/^\s*/)[0].length;
      const lang = line.trim().slice(open.length).trim().split(/\s+/)[0].toLowerCase();
      const start = i + 1;
      let end = start;
      while (end < lines.length && !isFenceClose(lines[end], open)) end += 1;
      const closed = end < lines.length;
      let body = lines.slice(start, end);
      if (!closed) {
        // The answer forgot the closing fence: the code ends before a note written in italics.
        const note = body.findIndex((l) => /^\s*\*[^*\n]+\*\s*$/.test(l));
        if (note >= 0) {
          body = body.slice(0, note);
          end = start + note;
        }
      }
      i = closed ? end + 1 : end;
      const code = body.map((l) => l.slice(Math.min(fenceIndent, l.match(/^\s*/)[0].length)));
      const comments = !["text", "txt", "plain"].includes(lang);
      // An answer cut off right after its opening fence has no code to show: no empty box.
      if (closed || code.some((l) => l.trim())) {
        html += `<pre class="ltr" dir="ltr"><code>${codeHtml(code.join("\n"), { comments })}</code></pre>`;
      }
      continue;
    }
    if (!line.trim()) {
      i += 1;
      continue;
    }
    const heading = line.match(MD_HEADING);
    if (heading) {
      const level = Math.min(heading[1].length + 1, 4);
      html += `<h${level}>${mdInline(heading[2])}</h${level}>`;
      i += 1;
      continue;
    }
    if (MD_RULE.test(line)) {
      html += "<hr>";
      i += 1;
      continue;
    }
    if (MD_QUOTE.test(line)) {
      const quote = [];
      while (i < lines.length && MD_QUOTE.test(lines[i])) quote.push(lines[i++].replace(/^\s{0,3}>\s?/, ""));
      html += `<blockquote>${mdBlocks(quote)}</blockquote>`;
      continue;
    }
    if (isTableStart(lines, i)) {
      const head = splitRow(line);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].trim() && lines[i].includes("|")) rows.push(splitRow(lines[i++]));
      html += mdTable(head, rows);
      continue;
    }
    if (MD_LIST.test(line)) {
      const base = line.match(MD_LIST)[1].length;
      // A bullet list and a numbered list are two lists, even when they follow each other.
      const kind = isOrderedMarker(line.match(MD_LIST)[2]);
      const items = [];
      while (i < lines.length) {
        const m = lines[i].match(MD_LIST);
        if (m && m[1].length <= base + 1 && isOrderedMarker(m[2]) === kind) {
          items.push({ ordered: /[\d۰-۹٠-٩]/.test(m[2]), start: mdNumber(m[2]), text: m[3], body: [] });
          i += 1;
          continue;
        }
        if (!lines[i].trim()) {
          let next = i + 1;
          while (next < lines.length && !lines[next].trim()) next += 1;
          const nextIsItem =
            next < lines.length &&
            MD_LIST.test(lines[next]) &&
            lines[next].match(MD_LIST)[1].length <= base + 1 &&
            isOrderedMarker(lines[next].match(MD_LIST)[2]) === kind;
          if (nextIsItem) {
            i = next;
            continue;
          }
          if (items.length && next < lines.length && /^\s{2,}\S/.test(lines[next])) {
            for (; i < next; i += 1) items[items.length - 1].body.push(lines[i]);
            continue;
          }
          break;
        }
        if (items.length && /^\s{2,}\S/.test(lines[i])) {
          items[items.length - 1].body.push(lines[i]);
          i += 1;
          continue;
        }
        break;
      }
      html += mdList(items);
      continue;
    }
    const display = line.match(MD_DISPLAY);
    if (display) {
      const closer = display[1] === "$$" ? /^\s*\$\$\s*$/ : /^\s*\\\]\s*$/;
      let end = i + 1;
      while (end < lines.length && !closer.test(lines[end])) end += 1;
      if (end < lines.length) {
        html += `<div class="math-block">${mathHtml(lines.slice(i + 1, end).join(" "))}</div>`;
        i = end + 1;
        continue;
      }
    }
    const para = [lines[i++]];
    while (i < lines.length && lines[i].trim() && !startsBlock(lines, i) && !MD_SETEXT.test(lines[i])) {
      para.push(lines[i++]);
    }
    if (i < lines.length && MD_SETEXT.test(lines[i])) {
      const level = lines[i].trim()[0] === "=" ? 2 : 3;
      html += `<h${level}>${mdInline(para.join(" "))}</h${level}>`;
      i += 1;
      continue;
    }
    // A backslash at the end of a line is a line break marker: the break shows, the backslash does not.
    const text = para.map((l, k) => (k < para.length - 1 ? l.replace(/\\$/, "") : l)).join("\n");
    html += `<p>${mdInline(text).replace(/\n/g, "<br>")}</p>`;
  }
  return html;
}

function isTableStart(lines, i) {
  return (
    lines[i].includes("|") &&
    i + 1 < lines.length &&
    lines[i + 1].includes("-") &&
    MD_TABLE_SEP.test(lines[i + 1])
  );
}

function startsBlock(lines, i) {
  const line = lines[i];
  return (
    MD_FENCE.test(line) ||
    MD_HEADING.test(line) ||
    MD_RULE.test(line) ||
    MD_QUOTE.test(line) ||
    MD_LIST.test(line) ||
    MD_DISPLAY.test(line) ||
    isTableStart(lines, i)
  );
}

/** A closing fence: the same character as the opening one, at least as long, and nothing else. */
function isFenceClose(line, open) {
  const m = line.match(/^\s*(`{3,}|~{3,})\s*$/);
  return Boolean(m) && m[1][0] === open[0] && m[1].length >= open.length;
}

function isOrderedMarker(marker) {
  return /[\d۰-۹٠-٩]/.test(marker);
}

function mdNumber(marker) {
  const digits = [...marker]
    .map((ch) => {
      const code = ch.charCodeAt(0);
      if (code >= 0x06f0 && code <= 0x06f9) return String(code - 0x06f0);
      if (code >= 0x0660 && code <= 0x0669) return String(code - 0x0660);
      return /\d/.test(ch) ? ch : "";
    })
    .join("");
  return parseInt(digits, 10) || 1;
}

function splitRow(line) {
  let s = line.trim();
  if (s.startsWith("|")) s = s.slice(1);
  if (s.endsWith("|") && !s.endsWith("\\|")) s = s.slice(0, -1);
  // Only a pipe that is not escaped separates cells; an escaped pipe (\|) is part of the cell.
  const cells = [];
  let cell = "";
  for (let k = 0; k < s.length; k++) {
    if (s[k] === "\\" && s[k + 1] === "|") {
      cell += "|";
      k += 1;
    } else if (s[k] === "|") {
      cells.push(cell.trim());
      cell = "";
    } else {
      cell += s[k];
    }
  }
  cells.push(cell.trim());
  return cells;
}

function mdTable(head, rows) {
  const th = head.map((cell) => `<th>${mdInline(cell)}</th>`).join("");
  const body = rows
    .map((row) => `<tr>${head.map((_, k) => `<td>${mdInline(row[k] ?? "")}</td>`).join("")}</tr>`)
    .join("");
  return `<div class="table-wrap"><table><thead><tr>${th}</tr></thead><tbody>${body}</tbody></table></div>`;
}

function mdList(items) {
  const first = items[0];
  const tag = first.ordered ? "ol" : "ul";
  const start = first.ordered && first.start !== 1 ? ` start="${first.start}"` : "";
  const body = items
    .map((item) => {
      const blocks = item.body.some((l) => l.trim()) ? mdBlocks(dedentBlock(item.body)) : "";
      const task = item.text.match(/^\[([ xX])\]\s*(.*)$/);
      if (!task) return `<li>${mdInline(item.text)}${blocks}</li>`;
      const done = task[1] !== " ";
      const box = `<span class="task-box" title="${done ? t("md.done") : t("md.todo")}">${done ? "☑" : "☐"}</span>`;
      return `<li class="task">${box}${mdInline(task[2])}${blocks}</li>`;
    })
    .join("");
  return `<${tag}${start}>${body}</${tag}>`;
}

/** Removes the indentation a nested block shares, so it reads as markdown of its own. */
function dedentBlock(lines) {
  const indent = (l) => l.match(/^[ \t]*/)[0].length;
  const cut = Math.min(...lines.filter((l) => l.trim()).map(indent));
  return lines.map((l) => l.slice(Math.min(cut, indent(l))));
}

/**
 * One line of an answer, in passes. First, code, LaTeX and escapes are set aside as placeholders,
 * so no marker is read inside them. Then links and addresses, entities, line breaks and inline
 * tags. Last, emphasis on the text that is left, so **a `if`** and [**bold link**](url) both work.
 */
function mdInline(text) {
  const pieces = [];
  const keep = (html) => {
    pieces.push(html);
    return `\u0000${pieces.length - 1}\u0000`;
  };
  let src = String(text ?? "").replaceAll("\u0000", "");
  src = src.replace(MD_TOKEN, (whole, code, paren, bracket, display, inline, escaped) => {
    if (code !== undefined) return keep(`<code class="ltr" dir="ltr">${escapeHtml(code)}</code>`);
    if (escaped !== undefined) return keep(escapeHtml(escaped));
    return keep(mathHtml(paren ?? bracket ?? display ?? inline));
  });
  src = src.replace(MD_LINK, (whole, bang, label, url, autolink, bare) => {
    if (url !== undefined) {
      if (url.includes("\u0000")) return whole;
      // Images are not loaded from other sites: they show as a link with their description.
      if (!/^https?:\/\//i.test(url)) return bang ? imageLabel(label) : label;
      return keep(linkOpen(url)) + (bang ? imageLabel(label) : label) + keep("</a>");
    }
    const href = autolink ?? bare;
    if (href.includes("\u0000")) return whole;
    return keep(`${linkOpen(href)}<span class="ltr" dir="ltr">${escapeHtml(href)}</span></a>`);
  });
  src = src.replace(MD_BR, () => keep("<br>"));
  src = src.replace(MD_ENTITY, (whole, name) => {
    const ch = decodeEntity(name);
    return ch === null ? whole : keep(escapeHtml(ch));
  });
  src = src.replace(MD_PAIRED_TAG, (whole, tag, inner) => {
    const name = tag.toLowerCase();
    return keep(`<${name}>`) + inner + keep(`</${name}>`);
  });
  return mdEmphasis(src).replace(/\u0000(\d+)\u0000/g, (_, n) => pieces[Number(n)]);
}

function mdEmphasis(text) {
  let out = "";
  let last = 0;
  for (const m of text.matchAll(MD_EMPHASIS)) {
    const [whole, boldItalic, bold, italic, strike, dunder, single] = m;
    const before = m.index > 0 ? text[m.index - 1] : "";
    // Not emphasis, so the text stays as it is: an underscore inside a word (my_name), and a
    // Python name between double underscores (__init__). The match stays part of the text.
    if ((dunder !== undefined || single !== undefined) && /[\p{L}\p{N}_]/u.test(before)) continue;
    if (dunder !== undefined && /^[A-Za-z0-9]+$/.test(dunder)) continue;
    out += isolateLatin(text.slice(last, m.index));
    if (boldItalic !== undefined) {
      out += `<strong><em>${mdEmphasis(boldItalic)}</em></strong>`;
    } else if (bold !== undefined) {
      out += `<strong>${mdEmphasis(bold)}</strong>`;
    } else if (italic !== undefined) {
      out += `<em>${mdEmphasis(italic)}</em>`;
    } else if (strike !== undefined) {
      out += `<del>${mdEmphasis(strike)}</del>`;
    } else if (dunder !== undefined) {
      out += `<strong>${mdEmphasis(dunder)}</strong>`;
    } else {
      out += `<em>${mdEmphasis(single)}</em>`;
    }
    last = m.index + whole.length;
  }
  return out + isolateLatin(text.slice(last));
}

/** The opening tag of a link: the address opens in a new tab. */
function linkOpen(href) {
  return `<a href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">`;
}

function imageLabel(label) {
  return label.trim() ? `${t("md.image")}: ${label}` : t("md.image");
}

const NAMED_ENTITIES = new Map([
  ["amp", "&"], ["lt", "<"], ["gt", ">"], ["quot", '"'], ["apos", "'"], ["nbsp", " "],
  ["ndash", "–"], ["mdash", "—"], ["hellip", "…"], ["laquo", "«"], ["raquo", "»"],
  ["zwnj", "‌"], ["zwj", "‍"],
]);

/** The character of an HTML entity (&amp; &#1575; &#x627;), or null when it is not one. */
function decodeEntity(name) {
  if (name[0] !== "#") return NAMED_ENTITIES.get(name) ?? null;
  const hex = name[1] === "x" || name[1] === "X";
  const code = parseInt(name.slice(hex ? 2 : 1), hex ? 16 : 10);
  return code > 0 && code <= 0x10ffff && (code < 0xd800 || code > 0xdfff) ? String.fromCodePoint(code) : null;
}

/** A LaTeX formula as readable text (symbols, fractions, small sub- and superscripts), set LTR. */
function mathHtml(tex) {
  return `<span class="ltr" dir="ltr">${escapeHtml(mathText(tex))}</span>`;
}

function mathText(tex) {
  return String(tex)
    .replace(/\\(?:left|right|big|Big|bigg|Bigg)(?![A-Za-z])/g, "")
    .replace(/\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, (_, top, bottom) => `${wrapTerm(top)}/${wrapTerm(bottom)}`)
    .replace(/\\sqrt\s*\{([^{}]*)\}/g, (_, inner) => `√${wrapTerm(inner)}`)
    .replace(/\\(?:text|textbf|textit|mathrm|mathbf|mathit|operatorname|mathcal)\s*\{([^{}]*)\}/g, "$1")
    .replace(/\^\s*\{([^{}]*)\}|\^(\S)/g, (_, group, one) => script(group ?? one, SUPERSCRIPT, "^"))
    .replace(/_\s*\{([^{}]*)\}|_(\S)/g, (_, group, one) => script(group ?? one, SUBSCRIPT, "_"))
    .replace(/\\\\/g, " ")
    .replace(/\\[,;:! ]/g, " ")
    .replace(/\\([a-zA-Z]+)/g, (_, name) => TEX_SYMBOLS.get(name) ?? name)
    .replace(/\\([{}$%&#_])/g, "$1")
    .replace(/[{}]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

/** A single word or number stays as it is; anything longer is put in brackets. */
function wrapTerm(term) {
  return /^[\w.]+$/.test(term) ? term : `(${term})`;
}

/** Text as small script characters; when one character has no such form, it keeps ^ or _. */
function script(text, table, marker) {
  const chars = [...text].map((ch) => table[ch]);
  return chars.every(Boolean) ? chars.join("") : marker + (text.length > 1 ? `(${text})` : text);
}

const SUPERSCRIPT = {
  0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹",
  "+": "⁺", "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾", n: "ⁿ", i: "ⁱ",
};
const SUBSCRIPT = {
  0: "₀", 1: "₁", 2: "₂", 3: "₃", 4: "₄", 5: "₅", 6: "₆", 7: "₇", 8: "₈", 9: "₉",
  "+": "₊", "-": "₋", "=": "₌", "(": "₍", ")": "₎", a: "ₐ", e: "ₑ", o: "ₒ", x: "ₓ", h: "ₕ",
  k: "ₖ", l: "ₗ", m: "ₘ", n: "ₙ", p: "ₚ", s: "ₛ", t: "ₜ",
};
const TEX_SYMBOLS = new Map(
  Object.entries({
    ge: "≥", geq: "≥", le: "≤", leq: "≤", ne: "≠", neq: "≠", approx: "≈", equiv: "≡", sim: "∼",
    times: "×", div: "÷", cdot: "·", pm: "±", mp: "∓", infty: "∞", degree: "°", circ: "°",
    pi: "π", theta: "θ", alpha: "α", beta: "β", gamma: "γ", delta: "δ", lambda: "λ", mu: "μ",
    sigma: "σ", omega: "ω", Delta: "Δ", Omega: "Ω",
    to: "→", rightarrow: "→", leftarrow: "←", Rightarrow: "⇒", Leftarrow: "⇐", leftrightarrow: "↔",
    in: "∈", notin: "∉", subset: "⊂", subseteq: "⊆", cup: "∪", cap: "∩", emptyset: "∅",
    sum: "∑", prod: "∏", int: "∫", sqrt: "√", ldots: "…", dots: "…", cdots: "⋯",
    forall: "∀", exists: "∃", neg: "¬", land: "∧", lor: "∨", therefore: "∴",
  }),
);
