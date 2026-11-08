import { bidiMixHtml, indexLabelHtml, ltrHtml, ltrIsolate } from "./bidi.js";
import {
  charDiff,
  explainFirstDifference,
  lineDiff,
  normalizeNewlines,
  visibleChar,
} from "./diff.js";
import { createPythonEditor } from "./editor.js";
import {
  LEGACY,
  PRIMARY,
  isWasmCompatError,
  loadScript,
  needsLegacyEngine,
} from "./compat.js";
import { runProblem } from "./runner.js";

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
  problems: [],
  concepts: {},
  currentId: null,
  hintLevel: {},
  progress: loadJson(STORAGE_KEY, {}),
  codes: loadJson(CODE_KEY, {}),
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
  bootDetails: document.getElementById("boot-details"),
  bootTech: document.getElementById("boot-tech"),
};

if (el.bootRetry) {
  el.bootRetry.addEventListener("click", () => window.location.reload());
}

init().catch((err) => {
  console.error(err);
  const detail = String(err?.message || err || "").trim();
  el.bootMsg.textContent = detail
    ? `بارگذاری ناموفق: ${detail}`
    : "بارگذاری موتور پایتون ناموفق بود. با start.bat از همین پوشه سرو کنید و صفحه را تازه کنید.";
  if (el.bootTech) {
    el.bootTech.textContent = `${String(
      err?.name || "Error"
    )}: ${detail}\n${String(err?.stack || "").split("\n").slice(0, 6).join("\n")}`;
  }
  if (el.bootDetails) el.bootDetails.hidden = false;
  if (el.bootRetry) el.bootRetry.hidden = false;
});

async function init() {
  setBoot(12, "خواندن مسئله‌ها…");
  const [problems, concepts] = await Promise.all([
    fetchJson("data/problems.json"),
    fetchJson("data/concepts.json"),
  ]);
  state.problems = problems;
  state.concepts = Object.fromEntries(concepts.map((c) => [c.id, c]));
  state.hintLevel = loadJson(HINT_KEY, {});

  fillTopics();
  renderList();
  bindUi();

  setBoot(35, "بررسی فایل‌های آفلاین…");
  const hasLegacy = await assertOfflineAssets();

  setBoot(45, "آماده‌سازی ویرایشگر کد…");
  state.editor = createPythonEditor(el.editorTextarea, {
    onChange(code) {
      if (!state.currentId) return;
      state.codes[state.currentId] = code;
      saveJson(CODE_KEY, state.codes);
    },
  });
  state.editor.setReadOnly(true);

  const forceEngine = new URLSearchParams(location.search).get("engine");
  state.pyodide = await bootPyodide(hasLegacy, forceEngine);

  setBoot(90, "آزمون کوتاه موتور پایتون…");
  await smokeTestPyodide(state.pyodide);

  setBoot(100, "آماده است");
  await sleep(250);
  el.boot.hidden = true;
  el.btnRun.disabled = false;
  state.editor.refresh();

  const first = state.problems[0];
  if (first) selectProblem(first.id);
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
  // Compiling ~10MB of WebAssembly can take 20–90s on weak lab PCs with no
  // callback — keep the message honest so it does not look permanently stuck.
  const tick = startBootTicker(
    55,
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
async function assertOfflineAssets() {
  const required = [
    "vendor/pyodide/pyodide.js",
    "vendor/pyodide/pyodide.asm.js",
    "vendor/pyodide/pyodide.asm.wasm",
    "vendor/pyodide/python_stdlib.zip",
    "vendor/codemirror/codemirror.min.js",
    "vendor/codemirror/mode/python/python.min.js",
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
  return Boolean(getRes && getRes.ok);
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
  el.topicFilter.addEventListener("change", renderList);
  el.btnRun.addEventListener("click", onRun);
  el.btnReset.addEventListener("click", onReset);
  el.btnHint.addEventListener("click", onHint);
  el.btnProgress.addEventListener("click", showProgress);
  el.btnClearProgress.addEventListener("click", clearProgress);
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
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
      btn.innerHTML = `
        <span class="num ltr" dir="ltr">${String(p.number).padStart(2, "0")}</span>
        <span>
          <div class="title">${bidiMixHtml(p.title)}</div>
          <div class="meta">${bidiMixHtml(p.topic)} · ${difficultyLabel(p.difficulty)}</div>
        </span>
      `;
      btn.addEventListener("click", () => selectProblem(p.id));
      el.problemList.appendChild(btn);
    });
}

function selectProblem(id) {
  const problem = state.problems.find((p) => p.id === id);
  if (!problem) return;
  state.currentId = id;

  el.problemTopic.innerHTML = bidiMixHtml(problem.topic);
  el.problemTitle.innerHTML = `${indexLabelHtml(problem.number)} ${bidiMixHtml(problem.title)}`;
  el.problemMode.textContent =
    problem.mode === "function" ? "آزمون تابع" : "ورودی / خروجی";
  el.statement.innerHTML = renderStatement(problem);
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
        html += `<p class="sample-label">نمونه ورودی</p><pre class="sample ltr" dir="ltr">${escapeHtml(
          sample.stdin
        )}</pre>`;
      }
      if (sample.stdout != null) {
        html += `<p class="sample-label">نمونه خروجی</p><pre class="sample ltr" dir="ltr">${escapeHtml(
          sample.stdout
        )}</pre>`;
      }
      if (sample.call) {
        html += `<p class="sample-label">نمونه فراخوانی</p><pre class="sample ltr" dir="ltr">${escapeHtml(
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
  const concept = state.concepts[problem.conceptId];
  if (!concept) {
    el.concept.className = "prose muted";
    el.concept.textContent = "آموزش مرتبطی تعریف نشده است.";
    return;
  }
  el.concept.className = "prose";
  el.concept.innerHTML = `<h3 style="margin-top:0">${bidiMixHtml(concept.title)}</h3>${mdLite(
    concept.body
  )}`;
}

function onHint() {
  const problem = currentProblem();
  if (!problem) return;
  const level = state.hintLevel[problem.id] || 0;
  if (level >= (problem.hints || []).length) return;
  state.hintLevel[problem.id] = level + 1;
  saveJson(HINT_KEY, state.hintLevel);
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
}

async function onRun() {
  const problem = currentProblem();
  if (!problem || !state.pyodide) return;
  el.btnRun.disabled = true;
  el.btnRun.textContent = "در حال اجرا…";
  document.querySelector('.tab[data-tab="results"]').click();
  el.results.className = "results";
  el.results.textContent = "آزمون‌ها در حال اجرا هستند…";

  try {
    const outcome = await runProblem(state.pyodide, problem, editorCode());
    renderResults(problem, outcome);
    if (!outcome.blocked && outcome.results.every((r) => r.ok)) {
      state.progress[problem.id] = {
        solved: true,
        at: new Date().toISOString(),
      };
      saveJson(STORAGE_KEY, state.progress);
      renderList();
    }
  } catch (err) {
    el.results.innerHTML = `<div class="test-card bad"><strong>خطای اجرا</strong><p>${escapeHtml(
      String(err?.message || err)
    )}</p></div>`;
  } finally {
    el.btnRun.disabled = false;
    el.btnRun.textContent = "اجرا و آزمون";
  }
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
        <p>${escapeHtml(issue.message)}</p>
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
        <pre class="diff-block" dir="ltr">${escapeHtml(result.message || "")}</pre>
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

  let body = "";
  if (result.kind === "function") {
    body += `<p class="diff-meta">خروجی تابع با مقدار مورد انتظار فرق دارد.</p>`;
    body += `<div class="diff-block"><span class="del">${escapeHtml(
      "expected: " + result.expected
    )}</span>\n<span class="add">${escapeHtml("actual:   " + result.actual)}</span></div>`;
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
    html += `<p class="diff-meta">${escapeHtml(promptTip)}</p>`;
  }
  if (first) {
    html += `<p class="diff-meta">اولین تفاوت در موقعیت ${ltrHtml(String(first.index + 1))}: انتظار «${ltrHtml(
      showChar(first.expected)
    )}»، خروجی شما «${ltrHtml(showChar(first.actual))}». فاصله‌ها با ${ltrHtml("·")} نشان داده می‌شوند.</p>`;
  }

  html += `<div class="diff-block">`;
  for (const row of rows) {
    if (row.type === "same") {
      html += `<div class="same">${escapeHtml(row.expected ?? "")}</div>`;
      continue;
    }
    const e = row.expected ?? "";
    const a = row.actual ?? "";
    const parts = charDiff(e, a);
    html += `<div>`;
    html += parts
      .map((p) => {
        const text = [...p.text].map(visibleChar).join("");
        return `<span class="${p.type}">${escapeHtml(text)}</span>`;
      })
      .join("");
    html += `</div>`;
  }
  html += `</div>`;

  html += `<p class="diff-meta">قرمز = باید باشد ولی نیست · سبز = اضافه‌ی خروجی شما</p>`;
  html += `<details style="margin-top:0.5rem"><summary>متن کامل مورد انتظار / خروجی شما</summary>
    <p class="sample-label">مورد انتظار</p><pre class="sample" dir="ltr">${escapeHtml(
      normalizeNewlines(expected)
    )}</pre>
    <p class="sample-label">خروجی شما</p><pre class="sample" dir="ltr">${escapeHtml(
      normalizeNewlines(actual)
    )}</pre>
  </details>`;
  return html;
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
  const solved = state.problems.filter((p) => state.progress[p.id]?.solved).length;
  el.progressSummary.innerHTML = `${ltrHtml(String(solved))} از ${ltrHtml(
    String(state.problems.length)
  )} مسئله حل شده (فقط روی همین مرورگر ذخیره می‌شود).`;
  el.progressList.innerHTML = state.problems
    .map((p) => {
      const ok = state.progress[p.id]?.solved;
      return `<li><span class="progress-item-text">${indexLabelHtml(p.number)} ${bidiMixHtml(
        p.title
      )}</span><strong class="progress-item-state" style="color:${
        ok ? "var(--ok)" : "var(--muted)"
      }">${ok ? "حل‌شده" : "—"}</strong></li>`;
    })
    .join("");
  el.progressDialog.showModal();
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
  return ["", "آسان", "متوسط", "چالشی"][n] || "—";
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
  localStorage.setItem(key, JSON.stringify(value));
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

/** Tiny markdown subset: paragraphs, `code`, ``` fences, **bold**, lists. */
function mdLite(src) {
  const parts = String(src || "").replace(/\r\n/g, "\n").split(/```/);
  let html = "";
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 1) {
      const body = parts[i].replace(/^\w*\n/, "");
      html += `<pre class="ltr" dir="ltr"><code>${escapeHtml(body.replace(/\n$/, ""))}</code></pre>`;
      continue;
    }
    const blocks = parts[i].split(/\n{2,}/);
    for (const block of blocks) {
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

function inlineMd(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, '<code class="ltr" dir="ltr">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
