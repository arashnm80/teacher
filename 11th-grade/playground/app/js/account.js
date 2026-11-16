/**
 * The online playground: sign-in, progress kept on the server, and solution material released
 * only after a pass. The answers are still checked in this browser, where Python runs; the
 * server keeps what the browser reports and checks what it can.
 *
 * In the offline copy (meta pg-mode="offline") nothing here runs and progress stays in the
 * browser, as it always did.
 */

export const ONLINE = document.querySelector('meta[name="pg-mode"]')?.content === "online";

const API = "/api/student";
const DRAFT_DELAY_MS = 2500;
const MESSAGES = {
  network: "اتصال به سرور برقرار نشد. اینترنت را بررسی کن و دوباره امتحان کن.",
  mismatch: "رمزها یکی نیستند. هر دو را یکسان بنویس.",
  generic: "این کار انجام نشد. دوباره امتحان کن.",
};

let student = null;
let pendingSignIn = null;
let formMode = "login";
let draftTimer = null;
let draftPending = null;
const typing = {}; // problem id -> { typed, inserted }, for this visit

function $(id) {
  return document.getElementById(id);
}

async function request(path, { method = "GET", body } = {}) {
  let res;
  try {
    res = await fetch(API + path, {
      method,
      credentials: "same-origin",
      cache: "no-store",
      headers: body !== undefined ? { "Content-Type": "application/json" } : {},
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    return { status: 0, data: { message: MESSAGES.network } };
  }
  let data = {};
  try {
    data = await res.json();
  } catch {
    data = {};
  }
  return { status: res.status, data };
}

/** Repeats a request after a sign-in when the session has ended. */
export async function authed(path, options) {
  let result = await request(path, options);
  if (result.status === 401) {
    // The server ended this session (signed out elsewhere, reset, or expired): ask again.
    student = null;
    const bar = $("student-bar");
    if (bar) bar.hidden = true;
    await requireSignIn();
    result = await request(path, options);
  }
  return result;
}

export function currentStudent() {
  return student;
}

// ---- the sign-in dialog -------------------------------------------------------------------

const FIELDS = {
  phone: { label: "شماره موبایل", modes: ["login", "register", "reset"] },
  nationalCode: { label: "کد ملی", modes: ["register", "reset"] },
  fullName: { label: "نام و نام خانوادگی (فارسی)", modes: ["register"] },
  classCode: { label: "کلاس", modes: ["register"] },
  password: { label: "رمز", modes: ["login", "register", "reset"] },
  password2: { label: "تکرار رمز", modes: ["register", "reset"] },
};
const MODE_TEXT = {
  login: { title: "ورود به زمین بازی", submit: "ورود" },
  register: { title: "ثبت‌نام", submit: "ثبت‌نام و شروع" },
  reset: { title: "انتخاب رمز تازه", submit: "ذخیره رمز تازه" },
};

function showError(text) {
  const box = $("auth-error");
  box.textContent = text || "";
  box.hidden = !text;
}

function setMode(mode, note = "") {
  formMode = mode;
  const dialog = $("auth-dialog");
  dialog.dataset.mode = mode;
  $("auth-title").textContent = MODE_TEXT[mode].title;
  $("auth-submit").textContent = MODE_TEXT[mode].submit;
  $("auth-tab-login").classList.toggle("active", mode === "login");
  $("auth-tab-register").classList.toggle("active", mode === "register");
  $("auth-tabs").hidden = mode === "reset";
  for (const [name, spec] of Object.entries(FIELDS)) {
    const field = document.querySelector(`[data-field="${name}"]`);
    if (field) field.hidden = !spec.modes.includes(mode);
  }
  $("auth-password").autocomplete = mode === "register" ? "new-password" : "current-password";
  $("auth-note").textContent = note;
  $("auth-note").hidden = !note;
  showError("");
}

function value(id) {
  return String($(id).value || "").trim();
}

function finishSignIn(data) {
  student = data.student;
  $("auth-password").value = "";
  $("auth-password2").value = "";
  $("auth-dialog").close();
  const resolve = resolveSignIn;
  pendingSignIn = null;
  resolveSignIn = null;
  if (resolve) resolve(student);
  paintStudentBar();
}

let resolveSignIn = null;

/** Opens the sign-in dialog (once) and resolves with the student when they are signed in. */
export function requireSignIn() {
  if (!ONLINE) return Promise.resolve(null);
  if (student) return Promise.resolve(student);
  if (!pendingSignIn) {
    pendingSignIn = new Promise((resolve) => {
      resolveSignIn = resolve;
    });
    setMode("login");
    $("auth-dialog").showModal();
  }
  return pendingSignIn;
}

async function submitAuth(event) {
  event.preventDefault();
  showError("");
  const submit = $("auth-submit");
  submit.disabled = true;
  try {
    if (formMode === "login") {
      const res = await request("/login", {
        method: "POST",
        body: { phone: value("auth-phone"), password: $("auth-password").value },
      });
      if (res.status === 200) return finishSignIn(res.data);
      if (res.status === 403 && res.data.error === "reset_required") {
        setMode("reset", res.data.message);
        return;
      }
      return showError(res.data.message || MESSAGES.generic);
    }
    if (formMode === "register") {
      if ($("auth-password").value !== $("auth-password2").value) return showError(MESSAGES.mismatch);
      const res = await request("/register", {
        method: "POST",
        body: {
          phone: value("auth-phone"),
          nationalCode: value("auth-national"),
          fullName: value("auth-name"),
          classCode: value("auth-class"),
          password: $("auth-password").value,
        },
      });
      if (res.status === 201) return finishSignIn(res.data);
      return showError(res.data.message || MESSAGES.generic);
    }
    if ($("auth-password").value !== $("auth-password2").value) return showError(MESSAGES.mismatch);
    const res = await request("/complete-reset", {
      method: "POST",
      body: {
        phone: value("auth-phone"),
        nationalCode: value("auth-national"),
        newPassword: $("auth-password").value,
      },
    });
    if (res.status === 200) return finishSignIn(res.data);
    return showError(res.data.message || MESSAGES.generic);
  } finally {
    submit.disabled = false;
  }
}

function paintStudentBar() {
  const bar = $("student-bar");
  if (!bar || !student) return;
  $("student-name").textContent = student.fullName;
  $("student-class").textContent = student.classCode || "—";
  bar.hidden = false;
}

export async function logout() {
  flushDraft();
  await request("/logout", { method: "POST", body: {} });
  location.reload();
}

/** Wires the dialog and the sign-in bar. Call once at start-up. */
export function initAccountUi() {
  if (!ONLINE) return;
  const dialog = $("auth-dialog");
  $("auth-form").addEventListener("submit", submitAuth);
  $("auth-tab-login").addEventListener("click", () => setMode("login"));
  $("auth-tab-register").addEventListener("click", () => setMode("register"));
  dialog.addEventListener("cancel", (event) => event.preventDefault()); // the sign-in cannot be skipped
  $("student-logout").addEventListener("click", logout);
  // Offline-only controls: the server keeps the progress, so these do not apply.
  document.querySelector(".backup")?.setAttribute("hidden", "");
  $("btn-clear-progress")?.setAttribute("hidden", "");
}

/** Resolves the signed-in student for the first time. Opens the dialog when there is none. */
export async function ensureStudent() {
  if (!ONLINE) return null;
  const res = await request("/me");
  if (res.status === 200) {
    student = res.data.student;
    paintStudentBar();
    return student;
  }
  return requireSignIn();
}

// ---- problems, progress and guides ---------------------------------------------------------

export async function fetchProblems() {
  const res = await authed("/problems");
  if (res.status !== 200) throw new Error(res.data.message || MESSAGES.generic);
  return res.data;
}

export async function fetchProgress() {
  const res = await authed("/progress");
  return res.status === 200 ? res.data.progress || {} : {};
}

/** The class packs of this student: questions, deadlines and the markdown of each pack. */
export async function fetchSchedule() {
  const res = await authed("/schedule");
  return res.status === 200 ? res.data : { classCode: "", packs: [] };
}

const TEHRAN_TIME = new Intl.DateTimeFormat("fa-IR-u-ca-persian", {
  timeZone: "Asia/Tehran", weekday: "long", day: "numeric", month: "long", year: "numeric",
  hour: "2-digit", minute: "2-digit", hourCycle: "h23",
});

/** A UTC timestamp as a Jalali date and time in Tehran, for example شنبه ۳۰ آبان ۱۴۰۵ ساعت ۲۲:۰۰. */
export function jalaliText(iso) {
  return iso ? TEHRAN_TIME.format(new Date(iso)) : "";
}

/** The solution material of a question, once the student has passed it; null before that. */
export async function fetchGuide(problemId) {
  const res = await authed(`/guide?problemId=${encodeURIComponent(problemId)}`);
  return res.status === 200 ? res.data : null;
}

/** Records what the editor did, for the teacher's check (typing is expected; insertion is not). */
export function noteTyping(problemId, change) {
  if (!ONLINE || !problemId || !change || change.origin === "setValue") return;
  const count = (typing[problemId] ||= { typed: 0, inserted: 0 });
  const size = (change.text || []).join("\n").length;
  if (change.origin === "+input") count.typed += size;
  else if (change.origin === "paste" || change.origin === "drop" || change.origin === "drag") count.inserted += size;
}

/** Saves the code a moment after the student stops typing. */
export function scheduleDraft({ problemId, code, revision, hintLevel }) {
  if (!ONLINE || !problemId) return;
  draftPending = { problemId, code, revision, hintLevel };
  clearTimeout(draftTimer);
  draftTimer = setTimeout(flushDraft, DRAFT_DELAY_MS);
}

export function flushDraft() {
  if (!draftPending) return;
  const draft = draftPending;
  draftPending = null;
  clearTimeout(draftTimer);
  const count = typing[draft.problemId] || { typed: 0, inserted: 0 };
  authed("/draft", {
    method: "POST",
    body: {
      problemId: draft.problemId,
      code: draft.code,
      revision: draft.revision,
      hintLevel: draft.hintLevel || 0,
      typed: count.typed,
      inserted: count.inserted,
    },
  });
}

/**
 * Sends one run to the server. Returns { solved, solvedNow, flags }, or { stale: true } when
 * the question changed since the page loaded, so the caller can reload the list.
 */
export async function sendAttempt({ problemId, code, revision, total, passed, blocked }) {
  flushDraft();
  const count = typing[problemId] || { typed: 0, inserted: 0 };
  const res = await authed("/attempt", {
    method: "POST",
    body: {
      problemId,
      code,
      revision,
      total,
      passed,
      blocked: Boolean(blocked),
      typed: count.typed,
      inserted: count.inserted,
    },
  });
  if (res.status === 409) return { stale: true };
  if (res.status !== 200) return null;
  return res.data;
}
