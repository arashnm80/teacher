/**
 * Teacher-facing boot diagnostics. Keep English/LTR so screenshots paste cleanly.
 * Safe on missing DOM; nothing throws from collectors.
 */

import { browserKind } from "./compat.js?v=12";

const startedAt = Date.now();
const notes = [];
const scriptLoads = [];
const pageErrors = [];
const assetProbes = [];

export function bootNote(message, extra = null) {
  notes.push({
    t: Date.now() - startedAt,
    message: String(message || ""),
    extra: extra == null ? undefined : extra,
  });
}

export function recordScriptLoad(entry) {
  scriptLoads.push({
    t: Date.now() - startedAt,
    ...entry,
  });
}

export function startPageErrorCapture() {
  if (typeof window === "undefined") return;
  window.addEventListener("error", (ev) => {
    pageErrors.push({
      t: Date.now() - startedAt,
      kind: "error",
      message: String(ev?.message || ev?.error?.message || "error"),
      source: String(ev?.filename || ""),
      line: ev?.lineno || 0,
      col: ev?.colno || 0,
      stack: String(ev?.error?.stack || "")
        .split("\n")
        .slice(0, 8)
        .join("\n"),
    });
  });
  window.addEventListener("unhandledrejection", (ev) => {
    const reason = ev?.reason;
    pageErrors.push({
      t: Date.now() - startedAt,
      kind: "unhandledrejection",
      message: String(reason?.message || reason || "rejection"),
      stack: String(reason?.stack || "")
        .split("\n")
        .slice(0, 8)
        .join("\n"),
    });
  });
}

/** HEAD then GET; sniff whether a .js URL actually returned JavaScript. */
export async function probeAsset(path) {
  const row = { path, t: Date.now() - startedAt };
  try {
    let res = await fetch(path, { method: "HEAD", cache: "no-store" }).catch(() => null);
    if (!res || !res.ok) {
      res = await fetch(path, { cache: "no-store" }).catch((err) => {
        row.fetchError = String(err?.message || err);
        return null;
      });
    }
    if (!res) {
      row.ok = false;
      assetProbes.push(row);
      return row;
    }
    row.ok = res.ok;
    row.status = res.status;
    row.method = res.type || undefined;
    row.contentType = res.headers.get("content-type") || "";
    row.contentLength = res.headers.get("content-length") || "";
    row.cfCache = res.headers.get("cf-cache-status") || "";
    row.server = res.headers.get("server") || "";
    // Read a small prefix to detect HTML fallback / empty body.
    try {
      const buf = await res.clone().arrayBuffer();
      row.bytes = buf.byteLength;
      const text = new TextDecoder("utf-8", { fatal: false })
        .decode(buf.slice(0, 120))
        .replace(/\s+/g, " ")
        .trim();
      row.head = text.slice(0, 100);
      const lower = text.toLowerCase();
      row.looksLikeHtml = /<!doctype html|<html|<head|<body/.test(lower);
      row.looksLikeJs =
        /codemirror|function|=>|module\.exports|\(function|!function/.test(lower) ||
        (path.endsWith(".js") && !row.looksLikeHtml && buf.byteLength > 20);
    } catch (err) {
      row.readError = String(err?.message || err);
    }
  } catch (err) {
    row.ok = false;
    row.fetchError = String(err?.message || err);
  }
  assetProbes.push(row);
  return row;
}

export async function probeMany(paths) {
  const out = [];
  for (const path of paths) {
    out.push(await probeAsset(path));
  }
  return out;
}

function envBlock() {
  const ua = typeof navigator !== "undefined" ? navigator.userAgent || "" : "";
  const kind = browserKind(ua);
  const loc = typeof location !== "undefined" ? location : {};
  const doc = typeof document !== "undefined" ? document : null;
  const nav = typeof navigator !== "undefined" ? navigator : {};
  return [
    `time: ${new Date().toISOString()}`,
    `elapsedMs: ${Date.now() - startedAt}`,
    `href: ${loc.href || ""}`,
    `baseURI: ${doc?.baseURI || ""}`,
    `protocol: ${loc.protocol || ""}`,
    `origin: ${loc.origin || ""}`,
    `pathname: ${loc.pathname || ""}`,
    `search: ${loc.search || ""}`,
    `hash: ${loc.hash || ""}`,
    `secureContext: ${typeof window !== "undefined" ? String(window.isSecureContext) : "?"}`,
    `online: ${typeof nav.onLine === "boolean" ? String(nav.onLine) : "?"}`,
    `language: ${nav.language || ""}`,
    `languages: ${Array.isArray(nav.languages) ? nav.languages.join(",") : ""}`,
    `platform: ${nav.platform || ""}`,
    `vendor: ${nav.vendor || ""}`,
    `userAgent: ${ua}`,
    `browserKind: ${kind.name} major=${kind.major ?? "null"}`,
    `cookieEnabled: ${typeof nav.cookieEnabled === "boolean" ? String(nav.cookieEnabled) : "?"}`,
    `hardwareConcurrency: ${nav.hardwareConcurrency ?? "?"}`,
    `deviceMemory: ${nav.deviceMemory ?? "?"}`,
    `viewport: ${typeof window !== "undefined" ? `${window.innerWidth}x${window.innerHeight}` : "?"}`,
    `screen: ${typeof screen !== "undefined" ? `${screen.width}x${screen.height}` : "?"}`,
  ].join("\n");
}

function globalsBlock() {
  const g = typeof globalThis !== "undefined" ? globalThis : {};
  const scripts =
    typeof document !== "undefined"
      ? Array.from(document.scripts || [])
          .map((s) => s.src || "(inline)")
          .filter((src) => /codemirror|pyodide|app\.js|editor\.js/i.test(src) || src === "(inline)")
      : [];
  return [
    `typeof CodeMirror: ${typeof g.CodeMirror}`,
    `typeof loadPyodide: ${typeof g.loadPyodide}`,
    `typeof WebAssembly: ${typeof g.WebAssembly}`,
    `document.scripts (filtered):`,
    ...(scripts.length ? scripts.map((s) => `  - ${s}`) : ["  (none)"]),
  ].join("\n");
}

function formatList(title, rows, formatter) {
  if (!rows.length) return `${title}: (none)`;
  return `${title}:\n${rows.map(formatter).join("\n")}`;
}

export async function buildTeacherBootLog(err, { extraProbes = [] } = {}) {
  if (extraProbes.length) {
    await probeMany(extraProbes);
  }

  const detail = String(err?.message || err || "").trim();
  const stack = String(err?.stack || "")
    .split("\n")
    .slice(0, 16)
    .join("\n");

  const parts = [
    "=== teacher playground boot log ===",
    envBlock(),
    "",
    globalsBlock(),
    "",
    `error.name: ${String(err?.name || "Error")}`,
    `error.message: ${detail}`,
    `error.stack:\n${stack || "(no stack)"}`,
    "",
    formatList("boot notes", notes, (n) => `  +${n.t}ms ${n.message}${n.extra != null ? ` | ${JSON.stringify(n.extra)}` : ""}`),
    "",
    formatList(
      "script loads",
      scriptLoads,
      (s) =>
        `  +${s.t}ms ${s.ok ? "OK" : "FAIL"} ${s.src}${s.error ? ` | ${s.error}` : ""}${
          s.afterGlobal != null ? ` | CodeMirror=${s.afterGlobal}` : ""
        }`
    ),
    "",
    formatList(
      "asset probes",
      assetProbes,
      (a) =>
        `  ${a.ok ? "OK" : "FAIL"} ${a.path} status=${a.status ?? "?"}` +
        ` type=${a.contentType || "?"}` +
        ` bytes=${(a.bytes ?? a.contentLength) || "?"}` +
        ` html=${a.looksLikeHtml ?? "?"}` +
        ` js=${a.looksLikeJs ?? "?"}` +
        `${a.cfCache ? ` cf=${a.cfCache}` : ""}` +
        `${a.server ? ` server=${a.server}` : ""}` +
        `${a.fetchError ? ` err=${a.fetchError}` : ""}` +
        `${a.head ? ` head=${JSON.stringify(a.head)}` : ""}`
    ),
    "",
    formatList(
      "page errors during boot",
      pageErrors.slice(-12),
      (e) =>
        `  +${e.t}ms [${e.kind}] ${e.message}` +
        `${e.source ? ` @ ${e.source}:${e.line}:${e.col}` : ""}` +
        `${e.stack ? `\n${e.stack}` : ""}`
    ),
  ];

  return parts.join("\n");
}
