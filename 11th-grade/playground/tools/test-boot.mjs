/**
 * Smoke-test boot-compat decisions (mirrors app/js/compat.js — keep in sync).
 * Self-contained because node treats app .js files as CommonJS.
 * Usage: node tools/test-boot.mjs
 */

function isWasmCompatError(err) {
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

function browserKind(ua = "") {
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

function needsLegacyEngine(ua = "") {
  const { name, major } = browserKind(ua);
  if (major == null || Number.isNaN(major)) return false;
  if (name === "chrome" || name === "edge") return major < 96;
  if (name === "firefox") return major < 79;
  if (name === "safari") return major < 15;
  return false;
}

function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    process.exitCode = 1;
  } else {
    console.log("OK:", msg);
  }
}

// The exact failure from the failing lab PCs.
assert(
  isWasmCompatError(
    new Error(
      "CompileError: WebAssembly.instantiateStreaming(): invalid value type 'externref', enable with --experimental-wasm-reftypes @+179"
    )
  ),
  "externref CompileError is classified as compat error"
);
assert(isWasmCompatError(new Error("wasm instantiation failed!")), "wasm instantiation failed is compat");
assert(
  !isWasmCompatError(new Error("فایل آفلاین پیدا نشد: vendor/pyodide/pyodide.js")),
  "missing file is NOT a compat error"
);
assert(
  !isWasmCompatError(new Error("بارگذاری Pyodide بیش از ۲ دقیقه طول کشید")),
  "timeout is NOT a compat error (stays a real error)"
);

// Old lab browsers go straight to legacy.
assert(
  needsLegacyEngine(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  ),
  "Chrome 91 needs legacy"
);
assert(
  needsLegacyEngine(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
  ),
  "Edge 95 needs legacy"
);
assert(
  needsLegacyEngine("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"),
  "Firefox 78 needs legacy"
);

// Modern browsers try the modern engine first.
assert(
  !needsLegacyEngine(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  ),
  "Chrome 120 tries modern first"
);
assert(
  !needsLegacyEngine(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
  ),
  "Chrome 96 tries modern first"
);
assert(!needsLegacyEngine(""), "empty UA tries modern first");
assert(browserKind("").name === "unknown", "empty UA is unknown");

if (process.exitCode) {
  console.error("\nBoot tests FAILED");
} else {
  console.log("\nBoot tests PASSED");
}
