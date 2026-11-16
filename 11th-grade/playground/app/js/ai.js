/**
 * AI agent for the playground. It sits in the left column and is always visible.
 *
 * A student picks one of three fixed actions. The browser sends the action, the
 * problem, the student's code and, for "review", the failed test. The server
 * builds the prompt (the browser never writes a prompt). The key stays in this
 * browser (localStorage) and goes only to the site's relay, /api/ai/ask.
 */

const KEYS_STORE = "teacher-ai-keys-v1";
const PROVIDER_STORE = "teacher-ai-provider-v1";
const RELAY_HOST = "teacher.arashnm80.ir";
/** Longest wait before a request counts as failed. The server stops at about 80 s. */
export const ASK_TIMEOUT_MS = window.__teacherAiTimeoutMs || 95000;
const SLOW_AFTER_S = 25;

export const PROVIDERS = {
  openrouter: {
    label: "OpenRouter",
    placeholder: "sk-or-…",
    keyRe: /^sk-or-[A-Za-z0-9_\-]{8,250}$/,
    keyUrl: "https://openrouter.ai/keys",
  },
  groq: {
    label: "Groq",
    placeholder: "gsk_…",
    keyRe: /^gsk_[A-Za-z0-9_\-]{8,250}$/,
    keyUrl: "https://console.groq.com/keys",
  },
};

export function aiEndpoint() {
  return location.hostname === RELAY_HOST ? "/api/ai/ask" : `https://${RELAY_HOST}/api/ai/ask`;
}

function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw == null ? fallback : JSON.parse(raw) ?? fallback;
  } catch {
    return fallback;
  }
}

function writeJson(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

export function storedKeys() {
  return readJson(KEYS_STORE, {});
}

export function storedProvider() {
  const name = readJson(PROVIDER_STORE, "openrouter");
  return PROVIDERS[name] ? name : "openrouter";
}

export function saveProvider(name) {
  return writeJson(PROVIDER_STORE, name);
}

export function saveKey(provider, key) {
  return writeJson(KEYS_STORE, { ...storedKeys(), [provider]: key });
}

export function removeKey(provider) {
  const keys = { ...storedKeys() };
  delete keys[provider];
  return writeJson(KEYS_STORE, keys);
}

/**
 * The failed test (or the blocked constraint) of a run, or null when the run passed.
 * visibleCount: the tests the student sees. Online, a failing test after them stays hidden:
 * its input and expected output must not reach the assistant either.
 */
export function failureFromOutcome(problem, outcome, visibleCount = Infinity) {
  if (!problem || !outcome) return null;
  if (outcome.blocked) {
    return {
      problemId: problem.id,
      kind: "constraint",
      index: 0,
      stdin: "",
      expected: "",
      actual: "",
      message: (outcome.constraintIssues || []).map((issue) => issue.message).join(" | "),
    };
  }
  const bad = (outcome.results || []).find((result) => !result.ok);
  if (!bad) return null;
  if (bad.index > visibleCount) {
    return {
      problemId: problem.id,
      kind: "hidden",
      index: bad.index,
      stdin: "",
      expected: "",
      actual: "",
      message: "این آزمون پنهان است و ورودی و خروجی آن به دانش‌آموز نشان داده نمی‌شود. فقط بگو کدام بخش برنامه را با صورت مسئله دوباره بررسی کند؛ ورودی یا خروجی این آزمون را حدس نزن.",
    };
  }
  const test = bad.test || {};
  const isFunction = (problem.mode || "stdio") === "function";
  return {
    problemId: problem.id,
    kind: bad.kind,
    index: bad.index,
    stdin: isFunction ? JSON.stringify(test.call?.args ?? []) : String(test.stdin ?? ""),
    expected: String(bad.expected ?? ""),
    actual: String(bad.actual ?? ""),
    message: String(bad.message ?? ""),
  };
}

function problemPayload(problem) {
  return {
    title: problem.title || "",
    topic: problem.topic || "",
    statement: problem.statement || "",
    mode: problem.mode || "stdio",
    functionName: problem.functionName || "",
    samples: problem.samples || [],
  };
}

function aiError(kind, message) {
  const error = new Error(message);
  error.kind = kind;
  return error;
}

/**
 * One request to the relay. Resolves with {answer, model, provider} or rejects
 * with an Error whose .kind is "timeout", "aborted", "network" or "server".
 */
export async function askAi({ provider, key, payload, onTick, onController }) {
  const controller = new AbortController();
  onController?.(controller);
  let timedOut = false;
  const started = Date.now();
  const timeout = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, ASK_TIMEOUT_MS);
  const ticker = setInterval(() => onTick?.(Math.floor((Date.now() - started) / 1000)), 1000);
  onTick?.(0);
  try {
    const response = await fetch(aiEndpoint(), {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-AI-Key": key },
      body: JSON.stringify({ provider, ...payload }),
      signal: controller.signal,
      cache: "no-store",
    });
    let data = null;
    try {
      data = await response.json();
    } catch {
      data = null;
    }
    if (!response.ok) {
      throw aiError("server", data?.error || `خطای سرور (${response.status}). دوباره امتحان کنید.`);
    }
    if (!data || typeof data.answer !== "string") {
      throw aiError("server", "پاسخ سرویس خوانده نشد. دوباره امتحان کنید.");
    }
    return data;
  } catch (err) {
    if (err.kind) throw err;
    if (timedOut) {
      throw aiError(
        "timeout",
        `پاسخ نرسید: بیش از ${Math.round(ASK_TIMEOUT_MS / 1000)} ثانیه طول کشید. دوباره امتحان کنید، یا سرویس دیگری را انتخاب کنید.`
      );
    }
    if (err.name === "AbortError") throw aiError("aborted", "درخواست لغو شد.");
    throw aiError("network", "اتصال به سرور برقرار نشد. اینترنت را بررسی کنید و دوباره امتحان کنید.");
  } finally {
    clearTimeout(timeout);
    clearInterval(ticker);
  }
}

// ---- panel ----------------------------------------------------------------

const el = {};
let ctx = null;
let busy = null; // {problemId, action, provider, controller, startedAt}
let lastRequest = null; // {action} for the retry button
let lastAnswer = null; // {label, text, provider, model} of the answer on screen

function $(id) {
  return document.getElementById(id);
}

export function initAi(context) {
  ctx = context;
  Object.assign(el, {
    provider: $("ai-provider"),
    key: $("ai-key"),
    keyLabel: $("ai-key-label"),
    keySave: $("ai-key-save"),
    keyRemove: $("ai-key-remove"),
    keyStatus: $("ai-key-status"),
    keyLink: $("ai-key-link"),
    hint: $("ai-hint"),
    actions: [...document.querySelectorAll(".ai-action")],
    status: $("ai-status"),
    statusLine: $("ai-status-line"),
    bar: $("ai-bar"),
    cancel: $("ai-cancel"),
    error: $("ai-error"),
    errorText: $("ai-error-text"),
    retry: $("ai-retry"),
    info: $("ai-info"),
    answer: $("ai-answer"),
    result: $("ai-result"),
    meta: $("ai-meta"),
    expand: $("ai-expand"),
    dialog: $("ai-dialog"),
    dialogBody: $("ai-dialog-body"),
    dialogMeta: $("ai-dialog-meta"),
    dialogClose: $("ai-dialog-close"),
  });
  el.provider.value = storedProvider();
  el.provider.addEventListener("change", () => {
    saveProvider(el.provider.value);
    el.key.value = "";
    hideMessages();
    refresh();
  });
  el.keySave.addEventListener("click", saveTypedKey);
  el.key.addEventListener("keydown", (event) => {
    if (event.key === "Enter") saveTypedKey();
  });
  el.keyRemove.addEventListener("click", () => {
    if (!confirm("کلید این سرویس از این مرورگر پاک شود؟")) return;
    removeKey(el.provider.value);
    refresh();
  });
  el.actions.forEach((button) => button.addEventListener("click", () => runAction(button.dataset.action)));
  el.cancel.addEventListener("click", () => busy?.controller?.abort());
  el.expand.addEventListener("click", openBigAnswer);
  el.dialogClose.addEventListener("click", () => el.dialog.close());
  el.dialog.addEventListener("click", (event) => {
    if (event.target === el.dialog) el.dialog.close();
  });
  el.retry.addEventListener("click", () => {
    if (lastRequest) runAction(lastRequest.action);
  });
  refresh();
}

export function aiProblemChanged() {
  lastAnswer = null;
  if (busy && busy.problemId !== ctx?.getProblem()?.id) {
    // The answer is still coming for the old problem; it will not be shown here.
  }
  hideMessages();
  el.result.hidden = true;
  el.answer.innerHTML = "";
  refresh();
}

export function aiFailureChanged() {
  refresh();
}

function selectedProvider() {
  return el.provider.value;
}

function refresh() {
  if (!el.provider) return;
  const provider = selectedProvider();
  const meta = PROVIDERS[provider];
  el.key.placeholder = meta.placeholder;
  el.keyLabel.textContent = `کلید ${meta.label}`;
  el.keyLink.href = meta.keyUrl;
  el.keyLink.textContent = `گرفتن کلید ${meta.label}`;
  const hasKey = Boolean(storedKeys()[provider]);
  el.keyStatus.textContent = hasKey
    ? `کلید ${meta.label} در همین مرورگر ذخیره است.`
    : `کلید ${meta.label} هنوز وارد نشده است. بدون کلید، دستیار کار نمی‌کند.`;
  el.keyRemove.hidden = !hasKey;
  const problem = ctx?.getProblem();
  const failure = ctx?.getFailure?.();
  const wrong = Boolean(problem && failure && failure.problemId === problem.id);
  el.hint.textContent = !problem
    ? "یک مسئله را از فهرست سمت راست انتخاب کن."
    : !hasKey
    ? `برای استفاده از دستیار، کلید ${meta.label} را وارد و ذخیره کن.`
    : wrong
    ? "پاسخ تو این بار رد شد. «بررسی پاسخ من» را بزن تا دستیار بگوید کدام قسمت اشتباه است."
    : "یکی از کارهای زیر را انتخاب کن.";
  const ready = Boolean(problem && hasKey && !busy);
  el.actions.forEach((button) => {
    button.disabled = !ready;
    button.classList.toggle("is-suggested", wrong && button.dataset.action === "review_answer");
  });
}

function saveTypedKey() {
  const provider = selectedProvider();
  const meta = PROVIDERS[provider];
  // Keys copied from right-to-left text often carry invisible direction marks or spaces: remove them.
  const typed = el.key.value.replace(/[\s\u00a0\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]/g, "");
  if (!meta.keyRe.test(typed)) {
    const other = Object.entries(PROVIDERS).find(([name, m]) => name !== provider && m.keyRe.test(typed));
    showError(other
      ? `این کلید مال ${other[1].label} است. سرویس را روی «${other[1].label}» بگذار.`
      : `کلید ${meta.label} معتبر به نظر نمی‌رسد. کلید را کامل و بدون فاصله وارد کن.`);
    return;
  }
  if (!saveKey(provider, typed)) {
    showError("این مرورگر اجازه ذخیره‌سازی نمی‌دهد. تنظیمات مرورگر را بررسی کن.");
    return;
  }
  el.key.value = "";
  hideMessages();
  refresh();
}

function hideMessages() {
  el.error.hidden = true;
  el.info.hidden = true;
  el.retry.hidden = true;
}

function showError(message, { retry = false } = {}) {
  el.errorText.textContent = message;
  el.error.hidden = false;
  el.retry.hidden = !retry;
}

function showInfo(message) {
  el.info.textContent = message;
  el.info.hidden = false;
}

function phaseText(label, seconds) {
  const limit = Math.round(ASK_TIMEOUT_MS / 1000);
  if (seconds >= SLOW_AFTER_S) {
    return `هنوز پاسخی نرسیده؛ مدل‌های رایگان گاهی کندند. ${seconds} از ${limit} ثانیه گذشته است.`;
  }
  if (seconds >= 6) return `${label} دارد پاسخ می‌سازد… ${seconds} از ${limit} ثانیه.`;
  return `درخواست به ${label} فرستاده شد… ${seconds} از ${limit} ثانیه.`;
}

function showStatus(label, seconds) {
  el.status.hidden = false;
  el.statusLine.textContent = phaseText(label, seconds);
  el.bar.style.width = `${Math.min(100, (seconds / (ASK_TIMEOUT_MS / 1000)) * 100)}%`;
  el.cancel.hidden = false;
}

function hideStatus() {
  el.status.hidden = true;
  el.cancel.hidden = true;
  el.bar.style.width = "0%";
}

function showAnswer(entry) {
  const meta = PROVIDERS[entry.provider];
  lastAnswer = { ...entry, label: `پاسخ ${meta.label} · مدل ${entry.model}` };
  el.meta.textContent = lastAnswer.label;
  el.answer.innerHTML = ctx.render(entry.text);
  el.answer.scrollTop = 0;
  el.result.hidden = false;
}

/** The same answer in a larger card, for a small side panel. */
function openBigAnswer() {
  if (!lastAnswer) return;
  el.dialogMeta.textContent = lastAnswer.label;
  el.dialogBody.innerHTML = ctx.render(lastAnswer.text);
  el.dialogBody.scrollTop = 0;
  el.dialog.showModal();
  el.dialogClose.focus();
}

async function runAction(action) {
  const problem = ctx?.getProblem();
  const provider = selectedProvider();
  const key = storedKeys()[provider];
  if (!problem || !key || busy) return;
  const failure = ctx.getFailure?.();
  const attachFailure = action === "review_answer" && failure && failure.problemId === problem.id ? failure : null;
  lastRequest = { action };
  busy = { problemId: problem.id, action, provider, controller: null };
  hideMessages();
  el.result.hidden = true;
  refresh();
  showStatus(PROVIDERS[provider].label, 0);
  try {
    const data = await askAi({
      provider,
      key,
      payload: {
        action,
        problem: problemPayload(problem),
        code: ctx.getCode(),
        failure: attachFailure,
      },
      onTick: (seconds) => showStatus(PROVIDERS[provider].label, seconds),
      onController: (controller) => {
        if (busy) busy.controller = controller;
      },
    });
    if (ctx.getProblem()?.id === problem.id) {
      showAnswer({ provider, model: data.model, text: data.answer });
    }
  } catch (err) {
    if (err.kind === "aborted") {
      showInfo("درخواست لغو شد. هر وقت خواستی دوباره بپرس.");
    } else {
      showError(err.message, { retry: true });
    }
  } finally {
    busy = null;
    hideStatus();
    refresh();
  }
}
