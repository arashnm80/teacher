/**
 * Boot-compat helpers for Pyodide loading.
 *
 * Dependency-free on purpose: `tools/test-boot.mjs` imports this file in
 * plain node, so nothing here may touch the DOM at import time.
 */

export const PRIMARY = {
  js: "vendor/pyodide/pyodide.js",
  indexURL: "vendor/pyodide/",
  version: "0.26.4",
  // Needs WebAssembly reference types (externref): Chrome/Edge 96+.
  minChrome: 96,
  minFirefox: 79,
};

export const LEGACY = {
  js: "vendor/pyodide-legacy/pyodide.js",
  indexURL: "vendor/pyodide-legacy/",
  version: "0.23.4",
  // Last release line before externref: Chrome 71+, Firefox 70+, Safari 14+.
};

/** Load a classic (non-module) script and resolve when it executes. */
export function loadScript(src) {
  return new Promise((resolve, reject) => {
    if (typeof document === "undefined") {
      reject(new Error("loadScript needs a browser document"));
      return;
    }
    const tag = document.createElement("script");
    tag.src = src;
    tag.async = false;
    tag.onload = () => resolve();
    tag.onerror = () =>
      reject(new Error(`اسکریپت بارگذاری نشد: ${src}`));
    document.head.appendChild(tag);
  });
}

/**
 * True when a loadPyodide failure looks like “browser too old for this
 * WebAssembly build” rather than a missing file or a timeout.
 */
export function isWasmCompatError(err) {
  const text = String(err?.message ?? err ?? "");
  return (
    /externref/i.test(text) ||
    /reftype/i.test(text) ||
    /reference type/i.test(text) ||
    /CompileError/i.test(text) ||
    /instantiateStreaming/i.test(text) ||
    (/WebAssembly/i.test(text) && /invalid/i.test(text)) ||
    (/wasm/i.test(text) && /instantiation failed/i.test(text))
  );
}

/** Parse `{ name, major }` out of a user-agent string. `major` may be null. */
export function browserKind(ua = "") {
  const text = String(ua || "");
  let m = text.match(/Edg\/(\d+)/) || text.match(/Edge\/(\d+)/);
  if (m) return { name: "edge", major: Number(m[1]) };
  m = text.match(/OPR\/(\d+)/) || text.match(/Opera\/(\d+)/);
  if (m) return { name: "opera", major: Number(m[1]) };
  m = text.match(/Firefox\/(\d+)/);
  if (m) return { name: "firefox", major: Number(m[1]) };
  m = text.match(/Chrome\/(\d+)/) || text.match(/Chromium\/(\d+)/);
  if (m) return { name: "chrome", major: Number(m[1]) };
  m = text.match(/Version\/(\d+).*Safari/);
  if (m) return { name: "safari", major: Number(m[1]) };
  m = text.match(/Safari\/(\d+)/);
  if (m) return { name: "safari", major: null };
  return { name: "unknown", major: null };
}

/**
 * Fast path: skip downloading the modern ~10MB build when the browser is
 * known to be too old for it and go straight to the legacy engine.
 * Unknown browsers return false (try modern first, fall back on error).
 */
export function needsLegacyEngine(ua = "") {
  const { name, major } = browserKind(ua);
  if (major == null || Number.isNaN(major)) return false;
  if (name === "chrome" || name === "edge") return major < 96;
  if (name === "firefox") return major < 79;
  if (name === "safari") return major < 15;
  return false;
}
