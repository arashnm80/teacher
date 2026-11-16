// Cache-bust query on every import: Cloudflare was caching /playground/*.js for
// 24h, so a fixed bootlog.js SyntaxError kept failing after the source was fixed.
import { bidiMixHtml, codeHtml, indexLabelHtml, isolateLatin, ltrHtml, ltrIsolate, mdLite, renderMarkdown } from "./bidi.js?v=18";
import { ONLINE, OFFLINE, initAccountUi, ensureStudent, fetchProblems, fetchProgress, fetchGuide, fetchSchedule, noteTyping, scheduleDraft, flushDraft, sendAttempt, getSession, onSessionChange, requireSignIn } from "./account.js?v=3";
import { backfill, guideFor, noteSyncTyping, onSyncChange, queueResult, queueLength, serverState, solvedStatus, startAutoSync,
  statusText, statusTip, summarize, syncNow, typingFor } from "./sync.js?v=1";
import { initUpdateNotice } from "./update.js?v=1";
import { define, t as tr } from "./i18n.js?v=1";
import { fa, level, longText, remainingMs, setServerTime, shortText } from "./countdown.js?v=1";
import { aiFailureChanged, aiProblemChanged, failureFromOutcome, initAi } from "./ai.js?v=3";
import {
  charDiff,
  explainFirstDifference,
  lineDiff,
  normalizeNewlines,
  visibleChar,
} from "./diff.js?v=11";
import { CODEMIRROR_SCRIPTS, createPythonEditor, ensureCodeMirror } from "./editor.js?v=12";
import {
  LEGACY,
  PRIMARY,
  isWasmCompatError,
  loadScript,
  needsLegacyEngine,
  setScriptLoadObserver,
} from "./compat.js?v=11";
import {
  bootNote,
  buildTeacherBootLog,
  recordScriptLoad,
  startPageErrorCapture,
} from "./bootlog.js?v=11";
import {
  installEngineFetch,
  loadEngineManifest,
  preloadAsmScript,
  prefetchEngine,
} from "./enginefetch.js?v=13";
import { runProblem } from "./runner.js?v=11";

startPageErrorCapture();
setScriptLoadObserver(recordScriptLoad);
bootNote("module app.js evaluating");
// Signal the classic index.html watchdog that the ES module graph parsed.
window.__pgModuleLoaded = true;

/** Online and offline both: hidden tests show no expected output, tutorials come from the account. */
const MANAGED = ONLINE || OFFLINE;

define({
  "bar.signin": { fa: "ورود / ثبت‌نام", en: "Sign in / sign up" },
  "bar.guide": { fa: "آموزش این مسئله بعد از ورود (یک بار، با اینترنت) روی این دستگاه ذخیره می‌شود و بعد از آن بدون اینترنت هم کار می‌کند.", en: "The tutorial for this problem is saved on this device after you sign in once (with internet), and then works without internet." },
  "progress.sync": { fa: "روی این دستگاه حل شده: {solved} · به معلم ارسال شده: {synced} · منتظر ارسال: {pending}", en: "Solved on this device: {solved} · sent to the teacher: {synced} · waiting to send: {pending}" },
  "progress.last": { fa: "آخرین همگام‌سازی: {time}", en: "Last sync: {time}" },
  "progress.never": { fa: "هنوز همگام‌سازی نشده است.", en: "Not synced yet." },
  "progress.rule": { fa: "یک نتیجه وقتی برای نمره حساب می‌شود که قبل از مهلت به معلم برسد؛ پس نتیجه‌ی حل‌شده را قبل از مهلت ارسال کن.", en: "A result counts for the score when it reaches the teacher before the deadline, so send solved problems before it." },
  "progress.syncnow": { fa: "ارسال و همگام‌سازی حالا", en: "Send and sync now" },
  "deadline.unsent": { fa: "حل شده، اما هنوز به معلم نرسیده است؛ قبل از مهلت ارسال کن.", en: "Solved, but it has not reached the teacher yet; send it before the deadline." },
});

const STORAGE_KEY = "teacher-playground-progress-v1";
const HINT_KEY = "teacher-playground-hints-v1";
const CODE_KEY = "teacher-playground-code-v1";
/** Old names from before the teacher-helper → teacher-playground rename. */
const LEGACY_KEYS = {
  [STORAGE_KEY]: "teacher-helper-progress-v1",
  [HINT_KEY]: "teacher-helper-hints-v1",
  [CODE_KEY]: "teacher-helper-code-v1",
};

const state = {
  pyodide: null,
  engineManifest: null,
  problems: [],
  concepts: {},
  currentId: null,
  hintLevel: {},
  progress: ONLINE ? {} : loadJson(STORAGE_KEY, {}),
  codes: ONLINE ? {} : loadJson(CODE_KEY, {}),
  editor: null,
};

const el = {
  boot: document.getElementById("boot"),
  bootMsg: document.getElementById("boot-msg"),
  bootBar: document.getElementById("boot-bar"),
  topicFilter: document.getElementById("topic-filter"),
  problemList: document.getElementById("problem-list"),
  problemTopic: document.getElementById("problem-topic"),
  problemTitle: document.getElementById("problem-title"),
  problemMode: document.getElementById("problem-mode"),
  statement: document.getElementById("statement"),
  lessonLink: document.getElementById("lesson-link"),
  constraintNote: document.getElementById("constraint-note"),
  editorTextarea: document.getElementById("editor"),
  btnRun: document.getElementById("btn-run"),
  btnReset: document.getElementById("btn-reset"),
  btnHint: document.getElementById("btn-hint"),
  hintList: document.getElementById("hint-list"),
  concept: document.getElementById("concept"),
  results: document.getElementById("results"),
  progressDialog: document.getElementById("progress-dialog"),
  progressSummary: document.getElementById("progress-summary"),
  progressList: document.getElementById("progress-list"),
  btnProgress: document.getElementById("btn-progress"),
  btnClearProgress: document.getElementById("btn-clear-progress"),
  bootRetry: document.getElementById("boot-retry"),
  bootOffline: document.getElementById("boot-offline"),
  bootDetails: document.getElementById("boot-details"),
  bootTech: document.getElementById("boot-tech"),
};

if (el.bootRetry) {
  el.bootRetry.addEventListener("click", () => window.location.reload());
}

init().catch(async (err) => {
  window.__pgFailed = true;
  console.error(err);
  const detail = String(err?.message || err || "").trim();
  el.bootMsg.textContent = detail
    ? `بارگذاری ناموفق: ${detail}`
    : "بارگذاری موتور پایتون ناموفق بود. با start.bat از همین پوشه سرو کنید و صفحه را تازه کنید.";
  if (el.bootTech) {
    el.bootTech.textContent = "در حال جمع‌آوری جزئیات فنی…";
    try {
      const probes = [
        ...CODEMIRROR_SCRIPTS,
        "vendor/pyodide/pyodide.js",
        "vendor/pyodide/chunks/manifest.json",
        "data/problems.json?v=28",
        "js/app.js?v=14",
        "js/enginefetch.js?v=13",
        "js/editor.js?v=12",
        "js/bootlog.js?v=11",
      ];
      el.bootTech.textContent = await buildTeacherBootLog(err, { extraProbes: probes });
    } catch (logErr) {
      el.bootTech.textContent = `${String(err?.name || "Error")}: ${detail}\n${String(
        err?.stack || ""
      )}\n\n(boot log failed: ${String(logErr?.message || logErr)})`;
    }
  }
  if (el.bootDetails) {
    el.bootDetails.hidden = false;
    try {
      el.bootDetails.open = true;
    } catch {
      /* ignore */
    }
  }
  if (el.bootRetry) el.bootRetry.hidden = false;
  if (el.bootOffline) el.bootOffline.hidden = false;
});

async function init() {
  bootNote("init start");
  initAccountUi();
  if (ONLINE) {
    setBoot(8, "ورود به حساب…");
    await ensureStudent();
  }
  setBoot(12, "خواندن مسئله‌ها…");
  const [problems, concepts] = await Promise.all([
    ONLINE ? fetchProblems() : fetchJson("data/problems.json?v=29"),
    fetchJson("data/concepts.json?v=28"),
  ]);
  // Stable `id` keeps progress across inserts; `number` is display order only.
  state.problems = [...problems].sort(
    (a, b) => (Number(a.number) || 0) - (Number(b.number) || 0) || String(a.id).localeCompare(String(b.id))
  );
  state.concepts = Object.fromEntries(concepts.map((c) => [c.id, c]));
  state.hintLevel = ONLINE ? {} : loadJson(HINT_KEY, {});
  if (ONLINE) adoptServerProgress(await fetchProgress());
  if (ONLINE) {
    state.schedule = await fetchSchedule();
    if (state.schedule?.serverTime) setServerTime(state.schedule.serverTime);
  }
  if (OFFLINE) {
    // From the last sync: the class's deadlines and the tutorials kept on this device.
    await ensureStudent();
    const known = serverState();
    state.schedule = known.packs?.length ? { classCode: known.classCode, packs: known.packs } : null;
    applyCachedGuides();
  }
  syncProgressWithCatalog();
  bootNote(`loaded problems=${state.problems.length} concepts=${concepts.length}`);

  fillTopics();
  renderList();
  bindUi();
  initAi({
    getProblem: currentProblem,
    getCode: editorCode,
    getFailure: () => state.lastFailure,
    render: renderMarkdown,
  });

  setBoot(35, "بررسی فایل‌های آفلاین…");
  state.engineManifest = await loadEngineManifest(bootNote);
  bootNote(`engine manifest ${state.engineManifest ? "found" : "absent"}`);
  const hasLegacy = await assertOfflineAssets(Boolean(state.engineManifest));
  bootNote(`assertOfflineAssets hasLegacy=${hasLegacy}`);

  setBoot(45, "آماده‌سازی ویرایشگر کد…");
  // Do not rely only on <script> tags in index.html — some school proxies /
  // Cloudflare optimizers skip classic scripts while HEAD still returns 200.
  await ensureCodeMirror();
  state.editor = createPythonEditor(el.editorTextarea, {
    onChange(code, change) {
      if (!state.currentId) return;
      state.codes[state.currentId] = code;
      saveJson(CODE_KEY, state.codes);
      if (ONLINE && change?.origin !== "setValue") {
        noteTyping(state.currentId, change);
        scheduleDraft({ problemId: state.currentId, code, revision: problemRevision(currentProblem()),
                        hintLevel: state.hintLevel[state.currentId] || 0 });
      } else if (OFFLINE) {
        noteSyncTyping(state.currentId, change);
      }
    },
  });
  state.editor.setReadOnly(true);
  bootNote("editor ready");

  const forceEngine = new URLSearchParams(location.search).get("engine");
  bootNote(`bootPyodide forceEngine=${forceEngine || "auto"}`);
  state.pyodide = await bootPyodide(hasLegacy, forceEngine);

  setBoot(90, "آزمون کوتاه موتور پایتون…");
  await smokeTestPyodide(state.pyodide);
  bootNote("smokeTest ok");

  setBoot(100, "آماده است");
  await sleep(250);
  el.boot.hidden = true;
  el.btnRun.disabled = false;
  state.editor.refresh();

  const first = state.problems[0];
  if (first) selectProblem(first.id);
  if (OFFLINE) startOfflineSync();
  bootNote("init done");
  window.__pgReady = true;
}

/** Boot the Python engine: modern Pyodide, with a legacy fallback for old lab browsers. */
async function bootPyodide(hasLegacy, forceEngine = null) {
  if (forceEngine === "legacy" && hasLegacy) {
    setBoot(55, "مرورگر این رایانه قدیمی است؛ در حال بارگذاری موتور سازگار…");
    return bootOneEngine(LEGACY);
  }
  const ua = typeof navigator !== "undefined" ? navigator.userAgent || "" : "";
  if (hasLegacy && needsLegacyEngine(ua)) {
    setBoot(55, "مرورگر این رایانه قدیمی است؛ در حال بارگذاری موتور سازگار…");
    return bootOneEngine(LEGACY);
  }

  setBoot(55, "بارگذاری Pyodide (آفلاین)…");
  let uninstallEngineFetch = null;
  if (state.engineManifest) {
    const files = await prefetchEngine(state.engineManifest, {
      note: bootNote,
      onProgress(done, total) {
        const mb = (n) => (n / 1048576).toFixed(1);
        setBoot(
          55 + Math.round((25 * done) / Math.max(total, 1)),
          `دانلود موتور پایتون: ${mb(done)} از ${mb(total)} مگابایت (اگر قطع شود، از همان‌جا ادامه می‌یابد)…`
        );
      },
    });
    await preloadAsmScript(files, PRIMARY.indexURL);
    uninstallEngineFetch = installEngineFetch(files);
  }
  // Compiling ~10MB of WebAssembly can take 20–90s on weak lab PCs with no
  // callback — keep the message honest so it does not look permanently stuck.
  const tick = startBootTicker(
    state.engineManifest ? 80 : 55,
    88,
    "در حال آماده‌سازی موتور پایتون (اولین بار روی این رایانه ممکن است تا یک دقیقه طول بکشد)…"
  );
  try {
    await loadScript(PRIMARY.js);
    return await withTimeout(
      callLoader(PRIMARY.indexURL),
      120000,
      "بارگذاری Pyodide بیش از ۲ دقیقه طول کشید. مرورگر را تازه کنید؛ اگر باز هم ماند، Chrome/Edge را به‌روز کنید یا از کپی روی دیسک محلی (نه USB کند) اجرا کنید."
    );
  } catch (err) {
    if (forceEngine !== "modern" && hasLegacy && isWasmCompatError(err)) {
      tick.stop();
      setBoot(60, "این مرورگر نسخه جدید موتور را پشتیبانی نمی‌کند؛ در حال بارگذاری موتور سازگار…");
      return bootOneEngine(LEGACY);
    }
    throw err;
  } finally {
    tick.stop();
    uninstallEngineFetch?.();
  }
}

/** Resolve the loader regardless of how a Pyodide release exposes it. */
function callLoader(indexURL) {
  const ns = globalThis.loadPyodide;
  const fn = typeof ns === "function" ? ns : ns?.loadPyodide;
  if (typeof fn !== "function") {
    throw new Error("موتور پایتون بارگذاری نشد. پوشه موتور را کامل کپی کنید.");
  }
  return fn({ indexURL });
}

async function bootOneEngine(engine) {
  const tick = startBootTicker(
    60,
    88,
    engine === LEGACY
      ? "در حال آماده‌سازی موتور سازگار (ممکن است تا یک دقیقه طول بکشد)…"
      : "در حال آماده‌سازی موتور پایتون (ممکن است تا یک دقیقه طول بکشد)…"
  );
  try {
    await loadScript(engine.js);
    return await withTimeout(
      callLoader(engine.indexURL),
      120000,
      "بارگذاری موتور پایتون بیش از ۲ دقیقه طول کشید. مرورگر را تازه کنید؛ اگر باز هم ماند، از کپی روی دیسک محلی (نه USB کند) اجرا کنید."
    );
  } finally {
    tick.stop();
  }
}

/**
 * Fail fast with a Persian message if the USB/copy is missing vendor files.
 * Returns true when the legacy engine for old browsers is also present.
 */
async function assertOfflineAssets(engineFromParts = false) {
  // With the parts manifest, the big engine files are verified by checksum
  // during download; probing them here would hit the same flaky link twice.
  const engine = engineFromParts
    ? ["vendor/pyodide/pyodide.js"]
    : [
        "vendor/pyodide/pyodide.js",
        "vendor/pyodide/pyodide.asm.js",
        "vendor/pyodide/pyodide.asm.wasm",
        "vendor/pyodide/python_stdlib.zip",
      ];
  const required = [
    ...engine,
    "vendor/codemirror/codemirror.min.js",
    "vendor/codemirror/mode/python/python.min.js",
    "vendor/codemirror/addon/edit/closebrackets.min.js",
    "vendor/codemirror/addon/edit/matchbrackets.min.js",
  ];
  for (const path of required) {
    if (!(await assetOk(path))) {
      throw new Error(
        `فایل آفلاین پیدا نشد: ${ltrIsolate(path)}. پوشه موتور را کامل کپی کنید.`
      );
    }
  }
  const legacy = [
    "vendor/pyodide-legacy/pyodide.js",
    "vendor/pyodide-legacy/pyodide.asm.js",
    "vendor/pyodide-legacy/pyodide.asm.wasm",
    "vendor/pyodide-legacy/python_stdlib.zip",
    "vendor/pyodide-legacy/repodata.json",
  ];
  for (const path of legacy) {
    if (!(await assetOk(path))) return false;
  }
  return true;
}

async function assetOk(path) {
  const res = await fetch(path, { method: "HEAD" }).catch(() => null);
  if (res && res.ok) return true;
  // Some static servers dislike HEAD — fall back to GET.
  const getRes = await fetch(path).catch(() => null);
  const ok = Boolean(getRes && getRes.ok);
  if (!ok) bootNote(`asset missing: ${path}`, { head: res?.status, get: getRes?.status });
  return ok;
}

/** Confirms stdlib modules used by module-1 (e.g. math) work without network. */
async function smokeTestPyodide(pyodide) {
  const out = await pyodide.runPythonAsync(
    "import math\nfloat(math.sqrt(16)) + float(math.pi > 3)"
  );
  if (Number(out) !== 5) {
    throw new Error("موتور پایتون آفلاین به‌درستی math را بارگذاری نکرد.");
  }
}

function bindUi() {
  document.getElementById("backup-export")?.addEventListener("click", exportProgress);
  document.getElementById("backup-file")?.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    try {
      await importProgress(file);
    } catch (err) {
      showBackupStatus(String(err?.message || err));
    }
  });
  el.topicFilter.addEventListener("change", renderList);
  el.btnRun.addEventListener("click", onRun);
  el.btnReset.addEventListener("click", onReset);
  el.btnHint.addEventListener("click", onHint);
  el.btnProgress.addEventListener("click", showProgress);
  el.btnClearProgress.addEventListener("click", clearProgress);
  // Only the problem's own tabs (the sign-in dialog has tabs of its own, with no panels here).
  document.querySelectorAll(".tab[data-tab]").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab[data-tab]").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    });
  });
  window.addEventListener("resize", () => state.editor?.refresh());
}

function editorCode() {
  return state.editor ? state.editor.getValue() : "";
}

function setEditorCode(code) {
  if (!state.editor) return;
  state.editor.setValue(code ?? "");
}

function problemRevision(problem) {
  const n = Number(problem?.revision);
  return Number.isFinite(n) && n > 0 ? n : 1;
}

/**
 * Progress is keyed by stable problem.id (never renumber ids when inserting).
 * Display order uses problem.number and may change freely.
 * If a problem's revision bumps (a major edit: its tests, mode or constraints changed),
 * its solved mark and hints start again. The saved code stays.
 */
/** Online: the server's progress of this student (solved marks, hints and the last code). */
function adoptServerProgress(serverProgress) {
  for (const [id, entry] of Object.entries(serverProgress)) {
    state.progress[id] = entry.solved
      ? { solved: true, at: entry.at, revision: entry.revision }
      : { revision: entry.revision };
    if (entry.hintLevel) state.hintLevel[id] = entry.hintLevel;
    if (entry.lastCode) state.codes[id] = entry.lastCode;
  }
}

function syncProgressWithCatalog() {
  let progressChanged = false;
  let hintsChanged = false;
  let codesChanged = false;
  const known = new Set(state.problems.map((p) => p.id));

  for (const p of state.problems) {
    const rev = problemRevision(p);
    const prev = state.progress[p.id];
    if (!prev) continue;
    if (prev.revision == null) {
      // First time we store revisions: keep old solves for unchanged rev=1 items.
      prev.revision = rev;
      progressChanged = true;
      continue;
    }
    if (prev.revision !== rev) {
      // A major edit: the solved mark and the hints start again. The saved code stays.
      const from = prev.revision;
      delete state.progress[p.id];
      progressChanged = true;
      if (state.hintLevel[p.id]) {
        delete state.hintLevel[p.id];
        hintsChanged = true;
      }
      bootNote(`new revision of ${p.id}`, { from, to: rev });
    }
  }

  // Entries for problems missing from this version are kept: the id may come back.

  if (progressChanged) saveJson(STORAGE_KEY, state.progress);
  if (hintsChanged) saveJson(HINT_KEY, state.hintLevel);
  if (codesChanged) saveJson(CODE_KEY, state.codes);
}

function fillTopics() {
  const topics = [...new Set(state.problems.map((p) => p.topic))];
  for (const topic of topics) {
    const opt = document.createElement("option");
    opt.value = topic;
    opt.textContent = topic;
    el.topicFilter.appendChild(opt);
  }
}

function renderList() {
  const filter = el.topicFilter.value;
  el.problemList.innerHTML = "";
  state.problems
    .filter((p) => !filter || p.topic === filter)
    .forEach((p, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "problem-link";
      if (p.id === state.currentId) btn.classList.add("active");
      if (state.progress[p.id]?.solved) btn.classList.add("done");
      const sync = OFFLINE ? solvedStatus(p.id, state.progress[p.id], problemRevision(p)) : null;
      const mark = sync
        ? ` <span class="sync-mark ${sync}" title="${statusTip(sync)}">${sync === "synced" ? "✓" : sync === "outdated" ? "⚠" : "●"}</span>`
        : "";
      btn.innerHTML = `
        <span class="num ltr" dir="ltr">${String(p.number).padStart(2, "0")}</span>
        <span>
          <div class="title">${bidiMixHtml(p.title)}${mark}</div>
          <div class="meta">${bidiMixHtml(p.topic)} · ${difficultyLabel(p.difficulty)} <span class="remain" data-pid="${p.id}"></span></div>
        </span>
      `;
      btn.addEventListener("click", () => selectProblem(p.id));
      el.problemList.appendChild(btn);
    });
  updateRemaining();
}

function selectProblem(id) {
  const problem = state.problems.find((p) => p.id === id);
  if (!problem) return;
  flushDraft();
  state.currentId = id;

  el.problemTopic.innerHTML = bidiMixHtml(problem.topic);
  el.problemTitle.innerHTML = `${indexLabelHtml(problem.number)} ${bidiMixHtml(problem.title)}`;
  el.problemMode.textContent =
    problem.mode === "function" ? "آزمون تابع" : "ورودی / خروجی";
  el.statement.innerHTML = renderStatement(problem);
  renderLessonLink(problem);
  aiProblemChanged();
  el.constraintNote.hidden = !hasConstraints(problem);
  el.constraintNote.innerHTML = constraintHtml(problem);

  const saved = state.codes[id];
  setEditorCode(saved != null ? saved : problem.starter || defaultStarter(problem));
  state.editor?.setReadOnly(false);
  requestAnimationFrame(() => state.editor?.refresh());
  el.btnHint.disabled = false;
  el.results.className = "results empty";
  el.results.textContent = "هنوز آزمونی اجرا نشده است.";

  renderHints(problem);
  renderConcept(problem);
  renderList();
  if (ONLINE) ensureGuide(problem); // the آموزش of a question opens from the start
  renderDeadline(problem);
}

/** Book pages: relative on the site; the offline copy links to the public book. */
const LESSON_BASE = location.pathname.includes("/playground/")
  ? "../book/"
  : "https://teacher.arashnm80.ir/book/";

function renderLessonLink(problem) {
  const lesson = state.concepts[problem.conceptId]?.lesson;
  if (!lesson) {
    el.lessonLink.hidden = true;
    el.lessonLink.innerHTML = "";
    return;
  }
  el.lessonLink.hidden = false;
  el.lessonLink.innerHTML =
    `درس مرتبط در کتاب: <a href="${LESSON_BASE}${lesson.page}.html">${isolateLatin(lesson.fa)}</a>`;
}

function defaultStarter(problem) {
  if (problem.mode === "function") {
    return `def ${problem.functionName || "solve"}():\n    pass\n`;
  }
  return "";
}

function hasConstraints(problem) {
  const c = problem.constraints || {};
  return (c.require && c.require.length) || (c.forbid && c.forbid.length);
}

function constraintHtml(problem) {
  const c = problem.constraints || {};
  const parts = [];
  if (c.require?.length) {
    parts.push(
      "باید استفاده شود: " + c.require.map((t) => ltrHtml(constraintLabel(t))).join("، ")
    );
  }
  if (c.forbid?.length) {
    parts.push(
      "نباید استفاده شود: " + c.forbid.map((t) => ltrHtml(constraintLabel(t))).join("، ")
    );
  }
  return parts.join(" · ");
}

function constraintLabel(token) {
  return (
    {
      for: "for",
      while: "while",
      if: "if",
      def: "def",
      import: "import",
      max: "max(...)",
      min: "min(...)",
      sum: "sum(...)",
      sorted: "sorted(...)",
      len: "len(...)",
      str: "str(...)",
    }[token] || token
  );
}

function renderStatement(problem) {
  let html = mdLite(problem.statement || "");
  if (problem.samples?.length) {
    for (const sample of problem.samples) {
      if (sample.stdin != null) {
        html += `<p class="sample-label">نمونه ورودی</p><pre class="sample ltr" dir="ltr">${codeHtml(sample.stdin, { comments: false })}</pre>`;
      }
      if (sample.stdout != null) {
        html += `<p class="sample-label">نمونه خروجی</p><pre class="sample ltr" dir="ltr">${codeHtml(sample.stdout, { comments: false })}</pre>`;
      }
      if (sample.call) {
        html += `<p class="sample-label">نمونه فراخوانی</p><pre class="sample ltr" dir="ltr">${codeHtml(
          `${problem.functionName}(${(sample.call.args || [])
            .map((x) => JSON.stringify(x))
            .join(", ")})  →  ${JSON.stringify(sample.call.expected)}`
        )}</pre>`;
      }
    }
  }
  return html;
}

function renderHints(problem) {
  const level = state.hintLevel[problem.id] || 0;
  el.hintList.innerHTML = "";
  const hints = problem.hints || [];
  for (let i = 0; i < level; i++) {
    const item = document.createElement("div");
    item.className = "hint-item";
    item.innerHTML = `<h3>راهنما ${ltrHtml(String(i + 1))}</h3><div>${mdLite(hints[i] || "")}</div>`;
    el.hintList.appendChild(item);
  }
  el.btnHint.disabled = level >= hints.length;
  el.btnHint.textContent =
    level >= hints.length
      ? "همه راهنماها باز شده‌اند"
      : `نمایش راهنمای ${ltrIsolate(String(level + 1))}`;
  if (!hints.length) {
    el.btnHint.disabled = true;
    el.btnHint.textContent = "راهنمایی برای این مسئله نیست";
  }
}

function renderConcept(problem) {
  // Prefer per-problem guide so siblings that share a topic (e.g. p01/p02)
  // do not show the same آموزش text.
  // Online, the guide is fetched when the question opens; until it arrives the lesson text shows.
  const lockedGuide = MANAGED && problem.guide === undefined;
  const title = (!lockedGuide && problem.guideTitle) || state.concepts[problem.conceptId]?.title;
  const body = (!lockedGuide && problem.guide) || state.concepts[problem.conceptId]?.body;
  if (!title || !body) {
    el.concept.className = "prose muted";
    el.concept.textContent = "آموزش مرتبطی تعریف نشده است.";
    return;
  }
  el.concept.className = "prose";
  const key = !lockedGuide && problem.guide
    ? `<p class="diff-legend-intro">وقتی آزمونی رد می‌شود، در بخش «نتایج» این رنگ‌ها را می‌بینید:</p>${colourLegendHtml()}`
    : "";
  const note = OFFLINE && lockedGuide ? `<p class="muted">${tr("bar.guide")}</p>` : "";
  el.concept.innerHTML = `<h3 style="margin-top:0">${bidiMixHtml(title)}</h3>${note}${key}${mdLite(
    body
  )}`;
}

/** Offline: puts the tutorials kept on this device into the problems. */
function applyCachedGuides() {
  for (const problem of state.problems) {
    const guide = guideFor(problem.id);
    if (guide) Object.assign(problem, guide);
  }
}

/** Offline: adds what the server knows (for example work done on another computer) to this device. */
function mergeServerProgress() {
  const known = serverState();
  const changedCode = new Set();
  let progressChanged = false;
  let codesChanged = false;
  for (const problem of state.problems) {
    const entry = known.progress?.[problem.id];
    if (!entry || entry.revision !== problemRevision(problem)) continue;
    if (entry.solved && !state.progress[problem.id]?.solved) {
      state.progress[problem.id] = { solved: true, at: entry.at, revision: entry.revision };
      progressChanged = true;
    }
    // The code of another computer comes along unless this device has code of its own (the starter does not count).
    const mine = state.codes[problem.id];
    if (entry.lastCode && (mine == null || mine === (problem.starter || defaultStarter(problem)))) {
      if (mine !== entry.lastCode) {
        state.codes[problem.id] = entry.lastCode;
        codesChanged = true;
        changedCode.add(problem.id);
      }
    }
    if (entry.hintLevel > (state.hintLevel[problem.id] || 0)) state.hintLevel[problem.id] = entry.hintLevel;
  }
  if (progressChanged) saveJson(STORAGE_KEY, state.progress);
  if (codesChanged) saveJson(CODE_KEY, state.codes);
  saveJson(HINT_KEY, state.hintLevel);
  return changedCode;
}

/** Offline: the chip in the bar says whether everything has reached the teacher. */
function paintSyncBar() {
  const chip = document.getElementById("sync-chip");
  if (!chip || !OFFLINE) return;
  const view = summarize(state.problems, state.progress, problemRevision);
  chip.className = `sync-chip ${view.state}`;
  chip.textContent = view.text;
  chip.title = view.lastSyncAt ? tr("progress.last", { time: new Date(view.lastSyncAt).toLocaleString() }) : tr("progress.never");
}

function startOfflineSync() {
  const refresh = () => {
    const newCode = mergeServerProgress();
    if (state.currentId && newCode.has(state.currentId)) setEditorCode(state.codes[state.currentId]);
    applyCachedGuides();
    const known = serverState();
    state.schedule = known.packs?.length ? { classCode: known.classCode, packs: known.packs } : null;
    renderList();
    paintSyncBar();
    const problem = currentProblem();
    if (problem) {
      renderConcept(problem);
      renderDeadline(problem);
    }
  };
  onSyncChange(refresh);
  onSessionChange((who) => {
    if (who) {
      backfill(state.problems, state.progress, state.codes);
      syncNow();
    } else {
      refresh();
    }
  });
  document.getElementById("sync-chip")?.addEventListener("click", () => (getSession() ? syncNow() : requireSignIn()));
  document.getElementById("btn-sync-now")?.addEventListener("click", () => (getSession() ? syncNow() : requireSignIn()));
  if (getSession()) backfill(state.problems, state.progress, state.codes);
  startAutoSync();
  initUpdateNotice();
  refresh();
}

function onHint() {
  const problem = currentProblem();
  if (!problem) return;
  const level = state.hintLevel[problem.id] || 0;
  if (level >= (problem.hints || []).length) return;
  state.hintLevel[problem.id] = level + 1;
  saveJson(HINT_KEY, state.hintLevel);
  scheduleDraft({ problemId: problem.id, code: editorCode(), revision: problemRevision(problem),
                  hintLevel: level + 1 });
  renderHints(problem);
  document.querySelector('.tab[data-tab="hints"]').click();
}

function onReset() {
  const problem = currentProblem();
  if (!problem) return;
  if (!confirm("کد فعلی پاک شود و به کد اولیه برگردد؟")) return;
  const starter = problem.starter || defaultStarter(problem);
  setEditorCode(starter);
  state.codes[problem.id] = starter;
  saveJson(CODE_KEY, state.codes);
  scheduleDraft({ problemId: problem.id, code: starter, revision: problemRevision(problem),
                  hintLevel: state.hintLevel[problem.id] || 0 });
}

async function onRun() {
  const problem = currentProblem();
  if (!problem || !state.pyodide) return;
  el.btnRun.disabled = true;
  el.btnRun.textContent = "در حال تست…";
  document.querySelector('.tab[data-tab="results"]').click();
  el.results.className = "results";
  el.results.textContent = "آزمون‌ها در حال اجرا هستند…";

  try {
    const outcome = await runProblem(state.pyodide, problem, editorCode());
    renderResults(problem, outcome);
    state.lastFailure = failureFromOutcome(problem, outcome, MANAGED ? visibleTests(problem) : Infinity);
    aiFailureChanged();
    if (ONLINE) {
      await recordRun(problem, outcome);
    } else {
      recordOfflineRun(problem, outcome);
    }
  } catch (err) {
    el.results.innerHTML = `<div class="test-card bad"><strong>خطای اجرا</strong><p>${isolateLatin(
      String(err?.message || err)
    )}</p></div>`;
  } finally {
    el.btnRun.disabled = false;
    el.btnRun.textContent = "بررسی و تست";
  }
}

/** Offline: the run is kept on this device and queued to be sent to the teacher (see sync.js). */
function recordOfflineRun(problem, outcome) {
  const total = problem.tests.length;
  const passed = outcome.blocked ? 0 : outcome.results.filter((r) => r.ok).length;
  const solvedNow = !outcome.blocked && total > 0 && passed === total;
  if (solvedNow && !state.progress[problem.id]?.solved) {
    state.progress[problem.id] = { solved: true, at: new Date().toISOString(), revision: problemRevision(problem) };
    saveJson(STORAGE_KEY, state.progress);
  }
  const count = typingFor(problem.id);
  queueResult({
    problemId: problem.id, revision: problemRevision(problem), code: editorCode(), passed, total,
    blocked: Boolean(outcome.blocked), typed: count.typed, inserted: count.inserted,
  });
  renderList();
  renderDeadline(problem);
  paintSyncBar();
}

/** Online: the pack (a day's group of questions) that holds this question for the student's class. */
function packOf(problemId) {
  return (state.schedule?.packs || []).find((pack) => pack.questions.some((q) => q.id === problemId)) || null;
}

/** Online: the deadline of this question, with the time left, or a note that it is practice only. */
function hasSchedule() {
  return Boolean(state.schedule?.packs?.length);
}

function renderDeadline(problem) {
  const note = document.getElementById("problem-deadline");
  if (!note) return;
  if (!ONLINE && !hasSchedule()) {
    note.hidden = true;
    return;
  }
  const pack = packOf(problem.id);
  note.hidden = false;
  note.classList.remove("ok", "soon", "urgent", "late");
  if (!pack) {
    note.textContent = "این مسئله برای کلاس شما نمره ندارد؛ برای تمرین است.";
  } else if (remainingMs(pack.until) <= 0) {
    note.classList.add("late");
    note.textContent = `مهلت نمره‌ی این مسئله گذشته است (${pack.untilText}). اکنون فقط برای تمرین است.`;
  } else if (state.progress[problem.id]?.solved) {
    const status = OFFLINE ? solvedStatus(problem.id, state.progress[problem.id], problemRevision(problem)) : "synced";
    if (status === "synced") note.textContent = `حل شده است. مهلت نمره‌ی این مسئله (${pack.title}): ${pack.untilText}`;
    else {
      note.classList.add("soon");
      note.textContent = `${tr("deadline.unsent")} (${pack.untilText})`;
    }
  } else {
    note.innerHTML = `مهلت نمره‌ی این مسئله (${bidiMixHtml(pack.title)}): ${bidiMixHtml(pack.untilText)} · زمان باقی‌مانده: <strong class="countdown" id="problem-countdown" dir="ltr"></strong>`;
    tickDeadline();
  }
}

/** Once a second: the countdown of the open question. When its deadline passes, the note changes. */
function tickDeadline() {
  const problem = currentProblem();
  const pack = problem && (ONLINE || hasSchedule()) ? packOf(problem.id) : null;
  const out = document.getElementById("problem-countdown");
  if (!pack || !out) return;
  const ms = remainingMs(pack.until);
  if (ms <= 0) return renderDeadline(problem);
  out.textContent = longText(ms);
  const note = document.getElementById("problem-deadline");
  note.classList.remove("ok", "soon", "urgent", "late");
  note.classList.add(level(ms));
}

/** The remaining time next to each question in the list (solved questions show none). */
function updateRemaining() {
  if (!ONLINE && !hasSchedule()) return;
  for (const chip of el.problemList.querySelectorAll(".remain")) {
    const pack = state.progress[chip.dataset.pid]?.solved ? null : packOf(chip.dataset.pid);
    chip.classList.remove("ok", "soon", "urgent", "late");
    if (!pack) {
      chip.textContent = "";
      continue;
    }
    const ms = remainingMs(pack.until);
    chip.textContent = `⏳ ${shortText(ms)}`;
    chip.classList.add(level(ms));
    chip.title = `${pack.title}: ${pack.untilText}`;
  }
}

setInterval(() => {
  tickDeadline();
  if (Math.floor(Date.now() / 1000) % 20 === 0) updateRemaining();
}, 1000);

/** Online: the packs of the class, each with its markdown and the state of its questions. */
function renderPacks() {
  const box = document.getElementById("pack-list");
  if (!box) return;
  box.replaceChildren();
  for (const pack of state.schedule?.packs || []) {
    const section = document.createElement("section");
    section.className = "pack";
    section.innerHTML = `<h3>${bidiMixHtml(pack.title)} · ${bidiMixHtml(pack.untilText)}</h3>${renderMarkdown(pack.markdown || "")}`;
    const list = document.createElement("ul");
    list.className = "pack-questions";
    for (const q of pack.questions) {
      const item = document.createElement("li");
      const done = state.progress[q.id]?.solved;
      item.textContent = `${q.number}. ${q.title} — ${done ? "قبول شد" : "هنوز قبول نشده"}`;
      list.append(item);
    }
    section.append(list);
    box.append(section);
  }
  if (!box.children.length) box.textContent = "برای کلاس شما هنوز سری‌ای تعریف نشده است.";
}

/** Online, the tests after the samples are hidden: the student sees only their result. */
function visibleTests(problem) {
  return problem.samples?.length || 1;
}

/** Online: the server decides whether the question is solved; the guide opens after a pass. */
async function recordRun(problem, outcome) {
  const passed = outcome.blocked ? 0 : outcome.results.filter((r) => r.ok).length;
  const result = await sendAttempt({
    problemId: problem.id,
    code: editorCode(),
    revision: problemRevision(problem),
    total: problem.tests.length,
    passed,
    blocked: outcome.blocked,
  });
  if (!result) return;
  if (result.stale) {
    el.results.className = "results";
    el.results.innerHTML = `<div class="test-card warn"><p>این مسئله به‌روز شده است. صفحه دوباره بارگذاری می‌شود.</p></div>`;
    setTimeout(() => window.location.reload(), 2000);
    return;
  }
  if (result.solved) {
    state.progress[problem.id] = { solved: true, at: new Date().toISOString(), revision: problemRevision(problem) };
    renderList();
    await ensureGuide(problem);
  }
  if (result.solvedNow && !result.scored) {
    el.results.insertAdjacentHTML("afterbegin",
      `<p class="deadline-note">قبول شدی، اما مهلت نمره‌ی این مسئله گذشته است. این مسئله فقط برای تمرین است.</p>`);
  }
}

/** Online: the solution material of a question arrives once the question has been passed. */
async function ensureGuide(problem) {
  if (!ONLINE || problem.guide !== undefined) return;
  const guide = await fetchGuide(problem.id);
  if (!guide) return;
  Object.assign(problem, guide);
  if (state.currentId === problem.id) renderConcept(problem);
}

function renderResults(problem, outcome) {
  if (outcome.blocked) {
    el.results.innerHTML = outcome.constraintIssues
      .map(
        (issue) => `
      <div class="test-card warn">
        <div class="test-head">
          <strong>محدودیت مسئله</strong>
          <span class="badge warn">رد شده</span>
        </div>
        <p>${isolateLatin(issue.message)}</p>
      </div>`
      )
      .join("");
    return;
  }

  const passed = outcome.results.filter((r) => r.ok).length;
  const total = outcome.results.length;
  let html = `<p class="muted" style="margin-top:0">${ltrHtml(String(passed))} از ${ltrHtml(
    String(total)
  )} آزمون قبول شد.</p>`;

  for (const result of outcome.results) {
    html += renderTestCard(problem, result);
  }
  el.results.innerHTML = html;
}

function renderTestCard(problem, result) {
  if (result.kind === "runtime" || result.kind === "runner") {
    return `
      <div class="test-card bad">
        <div class="test-head">
          <strong>آزمون ${ltrHtml(String(result.index))}</strong>
          <span class="badge bad">خطا</span>
        </div>
        <pre class="diff-block" dir="ltr">${codeHtml(result.message || "", { comments: false })}</pre>
      </div>`;
  }

  if (result.ok) {
    return `
      <div class="test-card ok">
        <div class="test-head">
          <strong>آزمون ${ltrHtml(String(result.index))}</strong>
          <span class="badge ok">قبول</span>
        </div>
      </div>`;
  }

  if (MANAGED && result.index > visibleTests(problem)) {
    // Online, the hidden tests show no expected output, so a student cannot copy it.
    return `
      <div class="test-card bad">
        <div class="test-head">
          <strong>آزمون ${ltrHtml(String(result.index))}</strong>
          <span class="badge bad">رد</span>
        </div>
        <p class="diff-meta">این آزمون پنهان است؛ ورودی و خروجی آن در حالت آنلاین نشان داده نمی‌شود. خروجی برنامه‌ات را با نمونه‌ی بالای صفحه مقایسه کن.</p>
      </div>`;
  }

  let body = "";
  if (result.kind === "function") {
    body += `<p class="diff-meta">خروجی تابع با مقدار مورد انتظار فرق دارد.</p>`;
    body += `<div class="diff-block"><span class="del">${codeHtml(
      "باید باشد: " + result.expected, { comments: false }
    )}</span>\n<span class="add">${codeHtml("خروجی شما: " + result.actual, { comments: false })}</span></div>`;
    body += colourLegendHtml();
  } else {
    body += renderStdioDiff(result.expected, result.actual);
  }

  return `
    <div class="test-card bad">
      <div class="test-head">
        <strong>آزمون ${ltrHtml(String(result.index))}</strong>
        <span class="badge bad">رد</span>
      </div>
      ${body}
    </div>`;
}

function renderStdioDiff(expected, actual) {
  const rows = lineDiff(expected, actual);
  const first = explainFirstDifference(expected, actual);
  let html = "";
  const promptTip = inputPromptTip(expected, actual);
  if (promptTip) {
    html += `<p class="diff-meta">${isolateLatin(promptTip)}</p>`;
  }
  if (first) {
    html += `<p class="diff-meta">اولین تفاوت در موقعیت ${ltrHtml(String(first.index + 1))}: انتظار «${ltrHtml(
      showChar(first.expected)
    )}»، خروجی شما «${ltrHtml(showChar(first.actual))}». فاصله‌ها با ${ltrHtml("·")} نشان داده می‌شوند.</p>`;
  }

  html += `<div class="diff-block">`;
  for (const row of rows) {
    if (row.type === "same") {
      html += `<div class="same">${codeHtml(row.expected ?? "", { comments: false })}</div>`;
      continue;
    }
    const e = row.expected ?? "";
    const a = row.actual ?? "";
    const parts = charDiff(e, a);
    html += `<div>`;
    html += parts
      .map((p) => {
        const text = [...p.text].map(visibleChar).join("");
        return `<span class="${p.type}">${codeHtml(text, { comments: false })}</span>`;
      })
      .join("");
    html += `</div>`;
  }
  html += `</div>`;

  html += colourLegendHtml();
  html += `<details style="margin-top:0.5rem"><summary>متن کامل مورد انتظار / خروجی شما</summary>
    <p class="sample-label">مورد انتظار</p><pre class="sample" dir="ltr">${codeHtml(normalizeNewlines(expected), { comments: false })}</pre>
    <p class="sample-label">خروجی شما</p><pre class="sample" dir="ltr">${codeHtml(normalizeNewlines(actual), { comments: false })}</pre>
  </details>`;
  return html;
}

/** The colour key: shown under every failed test and at the top of each guide. */
function colourLegendHtml() {
  return `<p class="diff-legend"><span class="chip-del">قرمز</span> = باید باشد ولی نیست · <span class="chip-add">سبز</span> = اضافه‌ی خروجی شما</p>`;
}

function showChar(ch) {
  if (ch === "⟨پایان⟩") return ch;
  if (ch === " ") return "فاصله";
  if (ch === "\n") return "خط جدید";
  if (ch === "\t") return "تب";
  return String(ch);
}

/** Detect common input("prompt") pollution that prepends text to stdout. */
function inputPromptTip(expected, actual) {
  const e = normalizeNewlines(expected);
  const a = normalizeNewlines(actual);
  if (!e || !a || a === e) return "";
  if (a.endsWith(e) && a.length > e.length) {
    return `احتمالاً داخل ${ltrIsolate("input()")} پیام گذاشته‌اید؛ همان پیام هم چاپ می‌شود و آزمون را خراب می‌کند. فقط بنویسید: ${ltrIsolate("input()")}`;
  }
  return "";
}

function showProgress() {
  if (ONLINE || hasSchedule()) renderPacks();
  const solved = state.problems.filter((p) => state.progress[p.id]?.solved).length;
  el.progressSummary.innerHTML = `${ltrHtml(String(solved))} از ${ltrHtml(
    String(state.problems.length)
  )} مسئله حل شده${OFFLINE ? "." : " (فقط روی همین مرورگر ذخیره می‌شود)."}`;
  paintSyncSummary();
  el.progressList.innerHTML = state.problems
    .map((p) => {
      const ok = state.progress[p.id]?.solved;
      const sync = OFFLINE ? solvedStatus(p.id, state.progress[p.id], problemRevision(p)) : null;
      const label = ok ? `حل‌شده${sync ? ` · ${statusText(sync)}` : ""}` : "—";
      return `<li><span class="progress-item-text">${indexLabelHtml(p.number)} ${bidiMixHtml(
        p.title
      )}</span><strong class="progress-item-state ${sync || ""}" style="color:${
        ok ? "var(--ok)" : "var(--muted)"
      }">${label}</strong></li>`;
    })
    .join("");
  el.progressDialog.showModal();
}

/** Offline: the lines at the top of the progress window about what reached the teacher. */
function paintSyncSummary() {
  const box = document.getElementById("sync-summary");
  if (!box) return;
  box.hidden = !OFFLINE;
  if (!OFFLINE) return;
  const view = summarize(state.problems, state.progress, problemRevision);
  document.getElementById("sync-summary-text").textContent = `${tr("progress.sync", view)}`;
  document.getElementById("sync-summary-last").textContent = view.lastSyncAt
    ? tr("progress.last", { time: new Date(view.lastSyncAt).toLocaleString() })
    : tr("progress.never");
  const bar = document.getElementById("sync-summary-state");
  bar.textContent = view.text;
  bar.className = `sync-chip ${view.state}`;
}

function clearProgress() {
  if (!confirm("پیشرفت و کدهای ذخیره‌شده این مرورگر پاک شوند؟")) return;
  state.progress = {};
  state.hintLevel = {};
  state.codes = {};
  saveJson(STORAGE_KEY, state.progress);
  saveJson(HINT_KEY, state.hintLevel);
  saveJson(CODE_KEY, state.codes);
  renderList();
  if (state.currentId) selectProblem(state.currentId);
  showProgress();
}

function currentProblem() {
  return state.problems.find((p) => p.id === state.currentId);
}

function difficultyLabel(n) {
  return ["", "خیلی آسان", "آسان", "متوسط", "سخت", "چالشی"][n] || "—";
}

function setBoot(pct, msg) {
  el.bootBar.style.width = `${pct}%`;
  el.bootMsg.textContent = msg;
}

/** Animate boot percent while a long await (Pyodide compile) has no real progress. */
function startBootTicker(fromPct, toPct, msg) {
  setBoot(fromPct, msg);
  let pct = fromPct;
  const id = setInterval(() => {
    pct = Math.min(toPct, pct + 1);
    setBoot(pct, msg);
    if (pct >= toPct) clearInterval(id);
  }, 1500);
  return {
    stop() {
      clearInterval(id);
    },
  };
}

function withTimeout(promise, ms, message) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(message)), ms);
    promise.then(
      (value) => {
        clearTimeout(timer);
        resolve(value);
      },
      (err) => {
        clearTimeout(timer);
        reject(err);
      }
    );
  });
}

async function fetchJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`نتوانستم ${ltrIsolate(path)} را بخوانم`);
  return res.json();
}

function loadJson(key, fallback) {
  try {
    let raw = localStorage.getItem(key);
    if (raw == null && LEGACY_KEYS[key]) {
      raw = localStorage.getItem(LEGACY_KEYS[key]);
      if (raw != null) localStorage.setItem(key, raw);
    }
    return JSON.parse(raw || "null") ?? fallback;
  } catch {
    return fallback;
  }
}

function saveJson(key, value) {
  if (ONLINE) return; // online, the server keeps the progress and the code
  localStorage.setItem(key, JSON.stringify(value));
}

function exportProgress() {
  const data = {
    format: "teacher-playground-backup",
    version: 1,
    exportedAt: new Date().toISOString(),
    progress: state.progress,
    hints: state.hintLevel,
    codes: state.codes,
  };
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "playground-progress-backup.json";
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  showBackupStatus("پشتیبان ذخیره شد.");
}

/** Merge a backup into this browser. Nothing local is lost: solved stays solved,
 *  hints keep the higher level, and a local code draft is never overwritten. */
async function importProgress(file) {
  const data = JSON.parse(await file.text());
  if (!data || data.format !== "teacher-playground-backup") throw new Error("این فایل پشتیبان پیشرفت نیست.");
  for (const [id, entry] of Object.entries(data.progress || {})) {
    const mine = state.progress[id];
    if (!mine) state.progress[id] = entry;
    else if (entry.solved && !mine.solved) state.progress[id] = { ...mine, solved: true, at: entry.at };
  }
  for (const [id, level] of Object.entries(data.hints || {})) {
    state.hintLevel[id] = Math.max(Number(state.hintLevel[id]) || 0, Number(level) || 0);
  }
  for (const [id, code] of Object.entries(data.codes || {})) {
    if (state.codes[id] == null) state.codes[id] = code;
  }
  saveJson(STORAGE_KEY, state.progress);
  saveJson(HINT_KEY, state.hintLevel);
  saveJson(CODE_KEY, state.codes);
  renderList();
  showBackupStatus("پیشرفت از پشتیبان بازیابی شد.");
}

function showBackupStatus(message) {
  const box = document.getElementById("backup-status");
  if (!box) return;
  box.textContent = message;
  box.hidden = false;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
