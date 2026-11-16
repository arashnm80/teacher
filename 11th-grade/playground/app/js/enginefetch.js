/**
 * Resumable download of the Pyodide engine for flaky home connections.
 *
 * build_site.py gzips each engine file and splits it into small immutable
 * parts (vendor/pyodide/chunks/manifest.json). Parts are fetched with retries
 * and stored in Cache Storage one by one, so a dropped connection or a reload
 * resumes instead of restarting a 10 MB download. Concurrency that worked
 * last time is remembered in localStorage and adjusted after every run.
 */

const CACHE_NAME = "pg-engine-parts-v1";
const POLICY_KEY = "pg-engine-dl-policy-v1";
const MANIFEST = "vendor/pyodide/chunks/manifest.json";
const MAX_ATTEMPTS = 12;
const PART_TIMEOUT_MS = 30000;
const MIN_CONCURRENCY = 1;
const MAX_CONCURRENCY = 6;

/** Returns null when the chunked path cannot be used (file://, old browser, no manifest). */
export async function loadEngineManifest(note = () => {}) {
  if (!/^https?:$/.test(location.protocol)) return null;
  const missing = ["caches", "DecompressionStream", "crypto"].filter((k) => !(k in globalThis));
  if (missing.length || !globalThis.crypto?.subtle) {
    note(`engine parts: unsupported (${missing.join(",") || "crypto.subtle"})`);
    return null;
  }
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const res = await fetchWithTimeout(MANIFEST, { cache: "no-cache" }, 15000);
      if (res.status === 404) return null;
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      note(`engine manifest attempt ${attempt} failed: ${err?.message || err}`);
      await sleep(backoff(attempt));
    }
  }
  return null;
}

/**
 * Download (or read from cache) every part, then gunzip each file.
 * Returns Map(absolute URL -> { bytes: Uint8Array, type }).
 */
export async function prefetchEngine(manifest, { onProgress = () => {}, note = () => {} } = {}) {
  const base = new URL(MANIFEST, location.href);
  const cache = await caches.open(CACHE_NAME);
  const parts = manifest.files.flatMap((file) =>
    file.parts.map((part) => ({ ...part, url: new URL(part.name, base).href }))
  );
  await pruneCache(cache, new Set(parts.map((p) => p.url)));

  const totalBytes = parts.reduce((sum, p) => sum + p.size, 0);
  const data = new Map();
  let doneBytes = 0;
  const report = () => onProgress(doneBytes, totalBytes);

  for (const part of parts) {
    const hit = await cache.match(part.url);
    if (!hit) continue;
    const buf = await hit.arrayBuffer();
    if (buf.byteLength === part.size && (await sha256Hex(buf)) === part.sha256) {
      data.set(part.url, buf);
      doneBytes += part.size;
    } else {
      await cache.delete(part.url);
    }
  }
  const cachedCount = data.size;
  report();

  const queue = parts.filter((p) => !data.has(p.url));
  const policy = loadPolicy();
  let limit = policy.concurrency;
  let failures = 0;
  note(`engine parts: ${cachedCount}/${parts.length} cached, fetching ${queue.length} (concurrency ${limit})`);

  async function fetchPart(part) {
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      try {
        const res = await fetchWithTimeout(part.url, { cache: "default" }, PART_TIMEOUT_MS);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const buf = await res.arrayBuffer();
        if (buf.byteLength !== part.size) throw new Error(`size ${buf.byteLength} != ${part.size}`);
        if ((await sha256Hex(buf)) !== part.sha256) throw new Error("checksum mismatch");
        await cache.put(part.url, new Response(buf)).catch(() => {});
        return buf;
      } catch (err) {
        failures++;
        limit = Math.max(MIN_CONCURRENCY, limit - 1);
        note(`engine part ${part.name} attempt ${attempt} failed: ${err?.message || err}`);
        if (attempt === MAX_ATTEMPTS) throw err;
        await sleep(backoff(attempt));
      }
    }
    throw new Error("unreachable");
  }

  let next = 0;
  let active = 0;
  let fatal = null;
  await new Promise((resolve) => {
    const pump = () => {
      if (fatal || (next >= queue.length && active === 0)) return resolve();
      while (!fatal && active < limit && next < queue.length) {
        const part = queue[next++];
        active++;
        fetchPart(part).then(
          (buf) => {
            data.set(part.url, buf);
            doneBytes += part.size;
            report();
          },
          (err) => {
            fatal = err;
          }
        ).finally(() => {
          active--;
          pump();
        });
      }
    };
    pump();
  });

  savePolicy(policy, limit, failures);
  if (fatal) {
    throw new Error(
      `دانلود موتور پایتون چند بار قطع شد (${String(fatal?.message || fatal)}). ` +
        "صفحه را تازه کنید؛ بخش‌های دانلودشده ذخیره شده‌اند و دانلود از همان‌جا ادامه می‌یابد."
    );
  }

  const files = new Map();
  for (const file of manifest.files) {
    const gz = new Blob(file.parts.map((p) => data.get(new URL(p.name, base).href)));
    const raw = new Uint8Array(
      await new Response(gz.stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer()
    );
    if (raw.byteLength !== file.size) {
      await caches.delete(CACHE_NAME);
      throw new Error(`فایل موتور خراب بود (${file.name}). صفحه را تازه کنید.`);
    }
    files.set(new URL(file.name, new URL("../", base)).href, { bytes: raw, type: file.type });
  }
  note(`engine parts ready: ${files.size} files, ${failures} retries`);
  return files;
}

/** Serve prefetched engine files to Pyodide's internal fetch() calls. Returns an uninstall fn. */
export function installEngineFetch(files) {
  const original = globalThis.fetch;
  globalThis.fetch = function engineFetch(input, init) {
    // Pyodide passes URL objects for binaries and strings for the lock file.
    const raw = input instanceof Request ? input.url : input != null ? String(input) : "";
    if (raw) {
      const hit = files.get(new URL(raw, location.href).href);
      if (hit) {
        return Promise.resolve(
          new Response(hit.bytes, { status: 200, headers: { "Content-Type": hit.type } })
        );
      }
    }
    return original.call(this, input, init);
  };
  return () => {
    globalThis.fetch = original;
    files.clear();
  };
}

/** Run pyodide.asm.js from memory so loadPyodide() skips its own network load. */
export async function preloadAsmScript(files, indexURL) {
  if (typeof globalThis._createPyodideModule === "function") return;
  const hit = files.get(new URL("pyodide.asm.js", new URL(indexURL, location.href)).href);
  if (!hit) return;
  const url = URL.createObjectURL(new Blob([hit.bytes], { type: "text/javascript" }));
  try {
    await import(/* webpackIgnore */ url);
  } finally {
    URL.revokeObjectURL(url);
  }
}

async function pruneCache(cache, keep) {
  for (const req of await cache.keys()) {
    if (!keep.has(req.url)) await cache.delete(req);
  }
}

function loadPolicy() {
  try {
    const p = JSON.parse(localStorage.getItem(POLICY_KEY) || "null");
    if (p && Number.isFinite(p.concurrency)) {
      return { ...p, concurrency: clamp(p.concurrency) };
    }
  } catch {
    /* ignore */
  }
  return { concurrency: 3, runs: 0, cleanRuns: 0 };
}

function savePolicy(policy, limit, failures) {
  const clean = failures === 0;
  const concurrency = clean ? clamp(limit + 1) : clamp(limit);
  try {
    localStorage.setItem(
      POLICY_KEY,
      JSON.stringify({
        concurrency,
        runs: (policy.runs || 0) + 1,
        cleanRuns: (policy.cleanRuns || 0) + (clean ? 1 : 0),
        lastFailures: failures,
      })
    );
  } catch {
    /* ignore */
  }
}

function clamp(n) {
  return Math.min(MAX_CONCURRENCY, Math.max(MIN_CONCURRENCY, Math.round(n)));
}

function backoff(attempt) {
  return Math.min(15000, 800 * 2 ** (attempt - 1)) + Math.random() * 500;
}

async function fetchWithTimeout(url, init, ms) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), ms);
  try {
    const res = await fetch(url, { ...init, signal: ctrl.signal });
    // Keep the abort timer alive while the body streams in.
    const buf = await res.arrayBuffer();
    return new Response(buf, { status: res.status, headers: res.headers });
  } finally {
    clearTimeout(timer);
  }
}

async function sha256Hex(buf) {
  const digest = await crypto.subtle.digest("SHA-256", buf);
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
