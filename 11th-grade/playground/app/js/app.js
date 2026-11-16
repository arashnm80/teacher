// Cache-bust query on every import: Cloudflare was caching /playground/*.js for
// 24h, so a fixed bootlog.js SyntaxError kept failing after the source was fixed.
import { bidiMixHtml, codeHtml, indexLabelHtml, isolateLatin, ltrHtml, ltrIsolate, mdLite, renderMarkdown } from "./bidi.js?v=19";
import { ONLINE, OFFLINE, initAccountUi, ensureStudent, fetchProblems, fetchProgress, fetchGuide, fetchSchedule, noteTyping, scheduleDraft, flushDraft, sendAttempt, getSession, onSessionChange, requireSignIn } from "./account.js?v=4";
import { backfill, guideFor, noteSyncTyping, onSyncChange, queueResult, queueLength, serverState, solvedStatus, startAutoSync,
  statusText, statusTip, summarize, syncNow, typingFor } from "./sync.js?v=2";
import { initUpdateNotice } from "./update.js?v=2";
import { define, initLang, isEnglish, onLangChange, t as tr } from "./i18n.js?v=5";
import { fa, level, longText, remainingMs, setServerTime, shortText } from "./countdown.js?v=2";
import { aiFailureChanged, aiProblemChanged, failureFromOutcome, initAi } from "./ai.js?v=4";
import {
  END_MARK,
  charDiff,
  explainFirstDifference,
  lineDiff,
  normalizeNewlines,
  visibleChar,
} from "./diff.js?v=12";
import { CODEMIRROR_SCRIPTS, createPythonEditor, ensureCodeMirror } from "./editor.js?v=13";
import {
  LEGACY,
  PRIMARY,
  isWasmCompatError,
  loadScript,
  needsLegacyEngine,
  setScriptLoadObserver,
} from "./compat.js?v=12";
import {
  bootNote,
  buildTeacherBootLog,
  recordScriptLoad,
  startPageErrorCapture,
} from "./bootlog.js?v=12";
import {
  installEngineFetch,
  loadEngineManifest,
  preloadAsmScript,
  prefetchEngine,
} from "./enginefetch.js?v=14";
import { runProblem } from "./runner.js?v=12";

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

define({
  "boot.failed": { fa: "بارگذاری ناموفق: {detail}", en: "Loading failed: {detail}" },
  "boot.failed.generic": { fa: "بارگذاری موتور پایتون ناموفق بود. با start.bat از همین پوشه سرو کنید و صفحه را تازه کنید.", en: "The Python engine could not be loaded. Serve this folder with start.bat and refresh the page." },
  "boot.collect": { fa: "در حال جمع‌آوری جزئیات فنی…", en: "Collecting technical details…" },
  "boot.login": { fa: "ورود به حساب…", en: "Signing in…" },
  "boot.read": { fa: "خواندن مسئله‌ها…", en: "Reading the problems…" },
  "boot.check": { fa: "بررسی فایل‌های آفلاین…", en: "Checking the offline files…" },
  "boot.editor": { fa: "آماده‌سازی ویرایشگر کد…", en: "Preparing the code editor…" },
  "boot.smoke": { fa: "آزمون کوتاه موتور پایتون…", en: "Short test of the Python engine…" },
  "boot.ready": { fa: "آماده است", en: "Ready" },
  "boot.legacy": { fa: "مرورگر این رایانه قدیمی است؛ در حال بارگذاری موتور سازگار…", en: "This computer's browser is old; loading the compatible engine…" },
  "boot.pyodide": { fa: "بارگذاری Pyodide (آفلاین)…", en: "Loading Pyodide (offline)…" },
  "boot.download": { fa: "دانلود موتور پایتون: {done} از {total} مگابایت (اگر قطع شود، از همان‌جا ادامه می‌یابد)…", en: "Downloading the Python engine: {done} of {total} MB (if it is cut, it continues from there)…" },
  "boot.preparing.first": { fa: "در حال آماده‌سازی موتور پایتون (اولین بار روی این رایانه ممکن است تا یک دقیقه طول بکشد)…", en: "Preparing the Python engine (the first time on this computer it can take up to a minute)…" },
  "boot.timeout.modern": { fa: "بارگذاری Pyodide بیش از ۲ دقیقه طول کشید. مرورگر را تازه کنید؛ اگر باز هم ماند، Chrome/Edge را به‌روز کنید یا از کپی روی دیسک محلی (نه USB کند) اجرا کنید.", en: "Loading Pyodide took more than 2 minutes. Refresh the browser; if it stays stuck, update Chrome/Edge or run the copy from a local disk (not a slow USB stick)." },
  "boot.unsupported": { fa: "این مرورگر نسخه جدید موتور را پشتیبانی نمی‌کند؛ در حال بارگذاری موتور سازگار…", en: "This browser does not support the new engine; loading the compatible engine…" },
  "boot.noengine": { fa: "موتور پایتون بارگذاری نشد. پوشه موتور را کامل کپی کنید.", en: "The Python engine did not load. Copy the whole engine folder." },
  "boot.preparing.legacy": { fa: "در حال آماده‌سازی موتور سازگار (ممکن است تا یک دقیقه طول بکشد)…", en: "Preparing the compatible engine (it can take up to a minute)…" },
  "boot.preparing.modern": { fa: "در حال آماده‌سازی موتور پایتون (ممکن است تا یک دقیقه طول بکشد)…", en: "Preparing the Python engine (it can take up to a minute)…" },
  "boot.timeout.plain": { fa: "بارگذاری موتور پایتون بیش از ۲ دقیقه طول کشید. مرورگر را تازه کنید؛ اگر باز هم ماند، از کپی روی دیسک محلی (نه USB کند) اجرا کنید.", en: "Loading the Python engine took more than 2 minutes. Refresh the browser; if it stays stuck, run the copy from a local disk (not a slow USB stick)." },
  "boot.missing": { fa: "فایل آفلاین پیدا نشد: {path}. پوشه موتور را کامل کپی کنید.", en: "An offline file was not found: {path}. Copy the whole engine folder." },
  "boot.math": { fa: "موتور پایتون آفلاین به‌درستی math را بارگذاری نکرد.", en: "The offline Python engine did not load math correctly." },
  "boot.cantread": { fa: "نتوانستم {path} را بخوانم", en: "Could not read {path}" },
  "mode.function": { fa: "آزمون تابع", en: "Function test" },
  "mode.io": { fa: "ورودی / خروجی", en: "Input / output" },
  "results.empty": { fa: "هنوز آزمونی اجرا نشده است.", en: "No test has been run yet." },
  "lesson.related": { fa: "درس مرتبط در کتاب:", en: "Related lesson in the book:" },
  "constraint.require": { fa: "باید استفاده شود:", en: "Must be used:" },
  "constraint.forbid": { fa: "نباید استفاده شود:", en: "Must not be used:" },
  "constraint.comma": { fa: "، ", en: ", " },
  "sample.in": { fa: "نمونه ورودی", en: "Sample input" },
  "sample.out": { fa: "نمونه خروجی", en: "Sample output" },
  "sample.call": { fa: "نمونه فراخوانی", en: "Sample call" },
  "hint.title": { fa: "راهنما {n}", en: "Hint {n}" },
  "hint.all": { fa: "همه راهنماها باز شده‌اند", en: "All hints are open" },
  "hint.show": { fa: "نمایش راهنمای {n}", en: "Show hint {n}" },
  "hint.none": { fa: "راهنمایی برای این مسئله نیست", en: "This problem has no hints" },
  "concept.none": { fa: "آموزش مرتبطی تعریف نشده است.", en: "No related tutorial is defined." },
  "concept.legend": { fa: "وقتی آزمونی رد می‌شود، در بخش «نتایج» این رنگ‌ها را می‌بینید:", en: "When a test fails, you see these colours in the “Results” tab:" },
  "confirm.reset": { fa: "کد فعلی پاک شود و به کد اولیه برگردد؟", en: "Erase the current code and go back to the starting code?" },
  "run.testing": { fa: "در حال تست…", en: "Testing…" },
  "run.running": { fa: "آزمون‌ها در حال اجرا هستند…", en: "The tests are running…" },
  "run.error": { fa: "خطای اجرا", en: "Run error" },
  "run.button": { fa: "بررسی و تست", en: "Check and test" },
  "deadline.none": { fa: "این مسئله برای کلاس شما نمره ندارد؛ برای تمرین است.", en: "This problem has no score for your class; it is for practice." },
  "deadline.late": { fa: "مهلت نمره‌ی این مسئله گذشته است ({until}). اکنون فقط برای تمرین است.", en: "The deadline for this problem's score has passed ({until}). It is now for practice only." },
  "deadline.solved": { fa: "حل شده است. مهلت نمره‌ی این مسئله ({title}): {until}", en: "Solved. Deadline for this problem's score ({title}): {until}" },
  "deadline.open": { fa: "مهلت نمره‌ی این مسئله ({title}): {until} · زمان باقی‌مانده:", en: "Deadline for this problem's score ({title}): {until} · time left:" },
  "pack.passed": { fa: "قبول شد", en: "passed" },
  "pack.notyet": { fa: "هنوز قبول نشده", en: "not passed yet" },
  "pack.empty": { fa: "برای کلاس شما هنوز سری‌ای تعریف نشده است.", en: "No series has been defined for your class yet." },
  "stale": { fa: "این مسئله به‌روز شده است. صفحه دوباره بارگذاری می‌شود.", en: "This problem has been updated. The page will reload." },
  "passed.late": { fa: "قبول شدی، اما مهلت نمره‌ی این مسئله گذشته است. این مسئله فقط برای تمرین است.", en: "You passed, but the deadline for this problem's score has passed. It is for practice only." },
  "card.constraint": { fa: "محدودیت مسئله", en: "Problem rule" },
  "badge.blocked": { fa: "رد شده", en: "Rejected" },
  "results.count": { fa: "{passed} از {total} آزمون قبول شد.", en: "{passed} of {total} tests passed." },
  "card.test": { fa: "آزمون {n}", en: "Test {n}" },
  "badge.error": { fa: "خطا", en: "Error" },
  "badge.ok": { fa: "قبول", en: "Passed" },
  "badge.bad": { fa: "رد", en: "Failed" },
  "card.hidden": { fa: "این آزمون پنهان است؛ ورودی و خروجی آن در حالت آنلاین نشان داده نمی‌شود. خروجی برنامه‌ات را با نمونه‌ی بالای صفحه مقایسه کن.", en: "This test is hidden; its input and output are not shown. Compare your program's output with the sample above." },
  "fn.differs": { fa: "خروجی تابع با مقدار مورد انتظار فرق دارد.", en: "The function's result differs from the expected value." },
  "fn.expected": { fa: "باید باشد: ", en: "Expected: " },
  "fn.actual": { fa: "خروجی شما: ", en: "Your result: " },
  "diff.first": { fa: "اولین تفاوت در موقعیت {pos}: انتظار «{want}»، خروجی شما «{got}». فاصله‌ها با {dot} نشان داده می‌شوند.", en: "First difference at position {pos}: expected “{want}”, your output “{got}”. Spaces are shown as {dot}." },
  "diff.full": { fa: "متن کامل مورد انتظار / خروجی شما", en: "Full expected text / your output" },
  "diff.expected": { fa: "مورد انتظار", en: "Expected" },
  "diff.yours": { fa: "خروجی شما", en: "Your output" },
  "legend.red": { fa: "قرمز", en: "red" },
  "legend.green": { fa: "سبز", en: "green" },
  "legend.text": { fa: "{red} = باید باشد ولی نیست · {green} = اضافه‌ی خروجی شما", en: "{red} = should be there but is missing · {green} = extra in your output" },
  "char.end": { fa: "⟨پایان⟩", en: "⟨end⟩" },
  "char.space": { fa: "فاصله", en: "space" },
  "char.newline": { fa: "خط جدید", en: "new line" },
  "char.tab": { fa: "تب", en: "tab" },
  "prompt.tip": { fa: "احتمالاً داخل {call} پیام گذاشته‌اید؛ همان پیام هم چاپ می‌شود و آزمون را خراب می‌کند. فقط بنویسید: {call}", en: "You probably put a message inside {call}; that message is printed too and breaks the test. Write only: {call}" },
  "progress.summary": { fa: "{solved} از {total} مسئله حل شده.", en: "{solved} of {total} problems solved." },
  "progress.summary.local": { fa: "{solved} از {total} مسئله حل شده (فقط روی همین مرورگر ذخیره می‌شود).", en: "{solved} of {total} problems solved (saved only in this browser)." },
  "progress.solved": { fa: "حل‌شده", en: "Solved" },
  "confirm.clear": { fa: "پیشرفت و کدهای ذخیره‌شده این مرورگر پاک شوند؟", en: "Erase the progress and saved code of this browser?" },
  "diff.level1": { fa: "خیلی آسان", en: "Very easy" },
  "diff.level2": { fa: "آسان", en: "Easy" },
  "diff.level3": { fa: "متوسط", en: "Medium" },
  "diff.level4": { fa: "سخت", en: "Hard" },
  "diff.level5": { fa: "چالشی", en: "Challenging" },
  "backup.saved": { fa: "پشتیبان ذخیره شد.", en: "Backup saved." },
  "backup.invalid": { fa: "این فایل پشتیبان پیشرفت نیست.", en: "This is not a progress backup file." },
  "backup.restored": { fa: "پیشرفت از پشتیبان بازیابی شد.", en: "Progress restored from the backup." },
});

/** A field of a problem or tutorial in the chosen language: the English text sits in `en`, Persian is the fallback. */
function loc(obj, field) {
  if (isEnglish()) {
    const value = obj?.en?.[field];
    if (value != null && value !== "") return value;
  }
  return obj?.[field];
}

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
    ? tr("boot.failed", { detail })
    : tr("boot.failed.generic");
  if (el.bootTech) {
    el.bootTech.textContent = tr("boot.collect");
    try {
      const probes = [
        ...CODEMIRROR_SCRIPTS,
        "vendor/pyodide/pyodide.js",
        "vendor/pyodide/chunks/manifest.json",
        "data/problems.json?v=28",
        "js/app.js?v=15",
        "js/enginefetch.js?v=14",
        "js/editor.js?v=13",
        "js/bootlog.js?v=12",
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
  initLang();
  initAccountUi();
  if (ONLINE) {
    setBoot(8, tr("boot.login"));
    await ensureStudent();
  }
  setBoot(12, tr("boot.read"));
  const [problems, concepts] = await Promise.all([
    ONLINE ? fetchProblems() : fetchJson("data/problems.json?v=30"),
    fetchJson("data/concepts.json?v=29"),
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

  setBoot(35, tr("boot.check"));
  state.engineManifest = await loadEngineManifest(bootNote);
  bootNote(`engine manifest ${state.engineManifest ? "found" : "absent"}`);
  const hasLegacy = await assertOfflineAssets(Boolean(state.engineManifest));
  bootNote(`assertOfflineAssets hasLegacy=${hasLegacy}`);

  setBoot(45, tr("boot.editor"));
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

  setBoot(90, tr("boot.smoke"));
  await smokeTestPyodide(state.pyodide);
  bootNote("smokeTest ok");

  setBoot(100, tr("boot.ready"));
  await sleep(250);
  el.boot.hidden = true;
  el.btnRun.disabled = false;
  state.editor.refresh();

  const first = state.problems[0];
  if (first) selectProblem(first.id);
  // From here the results panel holds real results: the static two-language text must not overwrite them.
  el.results.removeAttribute("data-fa");
  el.results.removeAttribute("data-en");
  // Switching the language draws the parts built by scripts again (the results panel stays as it was).
  onLangChange(() => {
    fillTopics();
    renderList();
    if (state.currentId) {
      const keep = el.results.innerHTML;
      const keepClass = el.results.className;
      selectProblem(state.currentId);
      el.results.innerHTML = keep;
      el.results.className = keepClass;
    }
    if (OFFLINE) paintSyncBar();
  });
  if (OFFLINE) startOfflineSync();
  bootNote("init done");
  window.__pgReady = true;
}

/** Boot the Python engine: modern Pyodide, with a legacy fallback for old lab browsers. */
async function bootPyodide(hasLegacy, forceEngine = null) {
  if (forceEngine === "legacy" && hasLegacy) {
    setBoot(55, tr("boot.legacy"));
    return bootOneEngine(LEGACY);
  }
  const ua = typeof navigator !== "undefined" ? navigator.userAgent || "" : "";
  if (hasLegacy && needsLegacyEngine(ua)) {
    setBoot(55, tr("boot.legacy"));
    return bootOneEngine(LEGACY);
  }

  setBoot(55, tr("boot.pyodide"));
  let uninstallEngineFetch = null;
  if (state.engineManifest) {
    const files = await prefetchEngine(state.engineManifest, {
      note: bootNote,
      onProgress(done, total) {
        const mb = (n) => (n / 1048576).toFixed(1);
        setBoot(
          55 + Math.round((25 * done) / Math.max(total, 1)),
          tr("boot.download", { done: mb(done), total: mb(total) })
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
    tr("boot.preparing.first")
  );
  try {
    await loadScript(PRIMARY.js);
    return await withTimeout(
      callLoader(PRIMARY.indexURL),
      120000,
      tr("boot.timeout.modern")
    );
  } catch (err) {
    if (forceEngine !== "modern" && hasLegacy && isWasmCompatError(err)) {
      tick.stop();
      setBoot(60, tr("boot.unsupported"));
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
    throw new Error(tr("boot.noengine"));
  }
  return fn({ indexURL });
}

async function bootOneEngine(engine) {
  const tick = startBootTicker(
    60,
    88,
    engine === LEGACY
      ? tr("boot.preparing.legacy")
      : tr("boot.preparing.modern")
  );
  try {
    await loadScript(engine.js);
    return await withTimeout(
      callLoader(engine.indexURL),
      120000,
      tr("boot.timeout.plain")
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
        tr("boot.missing", { path: ltrIsolate(path) })
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
    throw new Error(tr("boot.math"));
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

/** The topic filter. The value stays the Persian topic (it identifies the group); the label follows the language. */
function fillTopics() {
  const keep = el.topicFilter.value;
  const all = el.topicFilter.options[0];
  el.topicFilter.replaceChildren(...(all ? [all] : []));
  const firstOfTopic = new Map();
  for (const p of state.problems) if (!firstOfTopic.has(p.topic)) firstOfTopic.set(p.topic, p);
  for (const [topic, p] of firstOfTopic) {
    const opt = document.createElement("option");
    opt.value = topic;
    opt.textContent = loc(p, "topic");
    el.topicFilter.appendChild(opt);
  }
  el.topicFilter.value = keep;
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
          <div class="title">${bidiMixHtml(loc(p, "title"))}${mark}</div>
          <div class="meta">${bidiMixHtml(loc(p, "topic"))} · ${difficultyLabel(p.difficulty)} <span class="remain" data-pid="${p.id}"></span></div>
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

  el.problemTopic.innerHTML = bidiMixHtml(loc(problem, "topic"));
  el.problemTitle.innerHTML = `${indexLabelHtml(problem.number)} ${bidiMixHtml(loc(problem, "title"))}`;
  el.problemMode.textContent = problem.mode === "function" ? tr("mode.function") : tr("mode.io");
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
  el.results.textContent = tr("results.empty");

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
    `${tr("lesson.related")} <a href="${LESSON_BASE}${lesson.page}.html">${isolateLatin(isEnglish() && lesson.en ? lesson.en : lesson.fa)}</a>`;
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
      tr("constraint.require") + " " + c.require.map((t) => ltrHtml(constraintLabel(t))).join(tr("constraint.comma"))
    );
  }
  if (c.forbid?.length) {
    parts.push(
      tr("constraint.forbid") + " " + c.forbid.map((t) => ltrHtml(constraintLabel(t))).join(tr("constraint.comma"))
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
  let html = mdLite(loc(problem, "statement") || "");
  if (problem.samples?.length) {
    for (const sample of problem.samples) {
      if (sample.stdin != null) {
        html += `<p class="sample-label">${tr("sample.in")}</p><pre class="sample ltr" dir="ltr">${codeHtml(sample.stdin, { comments: false })}</pre>`;
      }
      if (sample.stdout != null) {
        html += `<p class="sample-label">${tr("sample.out")}</p><pre class="sample ltr" dir="ltr">${codeHtml(sample.stdout, { comments: false })}</pre>`;
      }
      if (sample.call) {
        html += `<p class="sample-label">${tr("sample.call")}</p><pre class="sample ltr" dir="ltr">${codeHtml(
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
  const hints = loc(problem, "hints") || [];
  for (let i = 0; i < level; i++) {
    const item = document.createElement("div");
    item.className = "hint-item";
    item.innerHTML = `<h3>${tr("hint.title", { n: ltrHtml(String(i + 1)) })}</h3><div>${mdLite(hints[i] || "")}</div>`;
    el.hintList.appendChild(item);
  }
  el.btnHint.disabled = level >= hints.length;
  el.btnHint.textContent =
    level >= hints.length
      ? tr("hint.all")
      : tr("hint.show", { n: ltrIsolate(String(level + 1)) });
  if (!hints.length) {
    el.btnHint.disabled = true;
    el.btnHint.textContent = tr("hint.none");
  }
}

function renderConcept(problem) {
  // Prefer per-problem guide so siblings that share a topic (e.g. p01/p02)
  // do not show the same آموزش text.
  // Online, the guide is fetched when the question opens; until it arrives the lesson text shows.
  const lockedGuide = MANAGED && problem.guide === undefined;
  const concept = state.concepts[problem.conceptId];
  // The tutorial's English text is kept back with it, in `guideEn`.
  const own = (field) => (isEnglish() && problem.guideEn?.[field]) || problem[field];
  const title = (!lockedGuide && own("guideTitle")) || loc(concept, "title");
  const body = (!lockedGuide && own("guide")) || loc(concept, "body");
  if (!title || !body) {
    el.concept.className = "prose muted";
    el.concept.textContent = tr("concept.none");
    return;
  }
  el.concept.className = "prose";
  const key = !lockedGuide && problem.guide
    ? `<p class="diff-legend-intro">${tr("concept.legend")}</p>${colourLegendHtml()}`
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
  if (!confirm(tr("confirm.reset"))) return;
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
  el.btnRun.textContent = tr("run.testing");
  document.querySelector('.tab[data-tab="results"]').click();
  el.results.className = "results";
  el.results.textContent = tr("run.running");

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
    el.results.innerHTML = `<div class="test-card bad"><strong>${tr("run.error")}</strong><p>${isolateLatin(
      String(err?.message || err)
    )}</p></div>`;
  } finally {
    el.btnRun.disabled = false;
    el.btnRun.textContent = tr("run.button");
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

/** A text of a pack (title, untilText, markdown) in the chosen language; the server sends the English one in `en`. */
const packText = (pack, field) => (isEnglish() && pack.en?.[field]) || pack[field];

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
    note.textContent = tr("deadline.none");
  } else if (remainingMs(pack.until) <= 0) {
    note.classList.add("late");
    note.textContent = tr("deadline.late", { until: packText(pack, "untilText") });
  } else if (state.progress[problem.id]?.solved) {
    const status = OFFLINE ? solvedStatus(problem.id, state.progress[problem.id], problemRevision(problem)) : "synced";
    if (status === "synced") note.textContent = tr("deadline.solved", { title: packText(pack, "title"), until: packText(pack, "untilText") });
    else {
      note.classList.add("soon");
      note.textContent = `${tr("deadline.unsent")} (${packText(pack, "untilText")})`;
    }
  } else {
    note.innerHTML = `${tr("deadline.open", { title: bidiMixHtml(packText(pack, "title")), until: bidiMixHtml(packText(pack, "untilText")) })} <strong class="countdown" id="problem-countdown" dir="ltr"></strong>`;
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
    chip.title = `${packText(pack, "title")}: ${packText(pack, "untilText")}`;
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
    section.innerHTML = `<h3>${bidiMixHtml(packText(pack, "title"))} · ${bidiMixHtml(packText(pack, "untilText"))}</h3>${renderMarkdown(packText(pack, "markdown") || "")}`;
    const list = document.createElement("ul");
    list.className = "pack-questions";
    for (const q of pack.questions) {
      const item = document.createElement("li");
      const done = state.progress[q.id]?.solved;
      item.textContent = `${q.number}. ${loc(state.problems.find((p) => p.id === q.id), "title") || q.title} — ${done ? tr("pack.passed") : tr("pack.notyet")}`;
      list.append(item);
    }
    section.append(list);
    box.append(section);
  }
  if (!box.children.length) box.textContent = tr("pack.empty");
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
    el.results.innerHTML = `<div class="test-card warn"><p>${tr("stale")}</p></div>`;
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
      `<p class="deadline-note">${tr("passed.late")}</p>`);
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
          <strong>${tr("card.constraint")}</strong>
          <span class="badge warn">${tr("badge.blocked")}</span>
        </div>
        <p>${isolateLatin(issue.message)}</p>
      </div>`
      )
      .join("");
    return;
  }

  const passed = outcome.results.filter((r) => r.ok).length;
  const total = outcome.results.length;
  let html = `<p class="muted" style="margin-top:0">${tr("results.count", { passed: ltrHtml(String(passed)), total: ltrHtml(String(total)) })}</p>`;

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
          <strong>${tr("card.test", { n: ltrHtml(String(result.index)) })}</strong>
          <span class="badge bad">${tr("badge.error")}</span>
        </div>
        <pre class="diff-block" dir="ltr">${codeHtml(result.message || "", { comments: false })}</pre>
      </div>`;
  }

  if (result.ok) {
    return `
      <div class="test-card ok">
        <div class="test-head">
          <strong>${tr("card.test", { n: ltrHtml(String(result.index)) })}</strong>
          <span class="badge ok">${tr("badge.ok")}</span>
        </div>
      </div>`;
  }

  if (MANAGED && result.index > visibleTests(problem)) {
    // Online, the hidden tests show no expected output, so a student cannot copy it.
    return `
      <div class="test-card bad">
        <div class="test-head">
          <strong>${tr("card.test", { n: ltrHtml(String(result.index)) })}</strong>
          <span class="badge bad">${tr("badge.bad")}</span>
        </div>
        <p class="diff-meta">${tr("card.hidden")}</p>
      </div>`;
  }

  let body = "";
  if (result.kind === "function") {
    body += `<p class="diff-meta">${tr("fn.differs")}</p>`;
    body += `<div class="diff-block"><span class="del">${codeHtml(
      tr("fn.expected") + result.expected, { comments: false }
    )}</span>\n<span class="add">${codeHtml(tr("fn.actual") + result.actual, { comments: false })}</span></div>`;
    body += colourLegendHtml();
  } else {
    body += renderStdioDiff(result.expected, result.actual);
  }

  return `
    <div class="test-card bad">
      <div class="test-head">
        <strong>${tr("card.test", { n: ltrHtml(String(result.index)) })}</strong>
        <span class="badge bad">${tr("badge.bad")}</span>
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
    html += `<p class="diff-meta">${tr("diff.first", {
      pos: ltrHtml(String(first.index + 1)),
      want: ltrHtml(showChar(first.expected)),
      got: ltrHtml(showChar(first.actual)),
      dot: ltrHtml("·"),
    })}</p>`;
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
  html += `<details style="margin-top:0.5rem"><summary>${tr("diff.full")}</summary>
    <p class="sample-label">${tr("diff.expected")}</p><pre class="sample" dir="ltr">${codeHtml(normalizeNewlines(expected), { comments: false })}</pre>
    <p class="sample-label">${tr("diff.yours")}</p><pre class="sample" dir="ltr">${codeHtml(normalizeNewlines(actual), { comments: false })}</pre>
  </details>`;
  return html;
}

/** The colour key: shown under every failed test and at the top of each guide. */
function colourLegendHtml() {
  return `<p class="diff-legend">${tr("legend.text", {
    red: `<span class="chip-del">${tr("legend.red")}</span>`,
    green: `<span class="chip-add">${tr("legend.green")}</span>`,
  })}</p>`;
}

function showChar(ch) {
  if (ch === END_MARK) return tr("char.end");
  if (ch === " ") return tr("char.space");
  if (ch === "\n") return tr("char.newline");
  if (ch === "\t") return tr("char.tab");
  return String(ch);
}

/** Detect common input("prompt") pollution that prepends text to stdout. */
function inputPromptTip(expected, actual) {
  const e = normalizeNewlines(expected);
  const a = normalizeNewlines(actual);
  if (!e || !a || a === e) return "";
  if (a.endsWith(e) && a.length > e.length) {
    return tr("prompt.tip", { call: ltrIsolate("input()") });
  }
  return "";
}

function showProgress() {
  if (ONLINE || hasSchedule()) renderPacks();
  const solved = state.problems.filter((p) => state.progress[p.id]?.solved).length;
  el.progressSummary.innerHTML = tr(MANAGED ? "progress.summary" : "progress.summary.local", {
    solved: ltrHtml(String(solved)),
    total: ltrHtml(String(state.problems.length)),
  });
  paintSyncSummary();
  el.progressList.innerHTML = state.problems
    .map((p) => {
      const ok = state.progress[p.id]?.solved;
      const sync = OFFLINE ? solvedStatus(p.id, state.progress[p.id], problemRevision(p)) : null;
      const label = ok ? `${tr("progress.solved")}${sync ? ` · ${statusText(sync)}` : ""}` : "—";
      return `<li><span class="progress-item-text">${indexLabelHtml(p.number)} ${bidiMixHtml(
        loc(p, "title")
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
  if (!confirm(tr("confirm.clear"))) return;
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
  return n >= 1 && n <= 5 ? tr(`diff.level${n}`) : "—";
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
  if (!res.ok) throw new Error(tr("boot.cantread", { path: ltrIsolate(path) }));
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
  showBackupStatus(tr("backup.saved"));
}

/** Merge a backup into this browser. Nothing local is lost: solved stays solved,
 *  hints keep the higher level, and a local code draft is never overwritten. */
async function importProgress(file) {
  const data = JSON.parse(await file.text());
  if (!data || data.format !== "teacher-playground-backup") throw new Error(tr("backup.invalid"));
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
  showBackupStatus(tr("backup.restored"));
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
