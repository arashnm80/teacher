/**
 * The online playground: sign-in, progress kept on the server, and solution material released
 * only after a pass. The answers are still checked in this browser, where Python runs; the
 * server keeps what the browser reports and checks what it can.
 *
 * The offline copy (meta pg-mode="offline") uses the same dialog and the same questions about the
 * student, but talks to the teacher's server with a token instead of a cookie (pages on the
 * student's own computer cannot share the website's cookies). Signing in there is optional: without
 * it, progress stays on the device. See sync.js for what is sent.
 */

const MODE = document.querySelector('meta[name="pg-mode"]')?.content;
export const ONLINE = MODE === "online";
export const OFFLINE = MODE === "offline";

import { define, has, onLangChange, t } from "./i18n.js?v=5";

define({
  "acct.network": { fa: "اتصال به سرور برقرار نشد. اینترنت را بررسی کن و دوباره امتحان کن.", en: "Could not reach the server. Check your internet and try again." },
  "acct.mismatch": { fa: "رمزها یکی نیستند. هر دو را یکسان بنویس.", en: "The passwords do not match. Type the same one in both." },
  "acct.generic": { fa: "این کار انجام نشد. دوباره امتحان کن.", en: "That did not work. Try again." },
  "acct.login.title": { fa: "ورود به زمین بازی", en: "Sign in to the playground" },
  "acct.login.submit": { fa: "ورود", en: "Sign in" },
  "acct.register.title": { fa: "ثبت‌نام", en: "Sign up" },
  "acct.register.submit": { fa: "ثبت‌نام و شروع", en: "Sign up and start" },
  "acct.reset.title": { fa: "انتخاب رمز تازه", en: "Choose a new password" },
  "acct.reset.submit": { fa: "ذخیره رمز تازه", en: "Save the new password" },
  "err.phone_invalid": { fa: "شماره موبایل معتبر نیست. مثل 09123456789 بنویس.", en: "The mobile number is not valid. Write it like 09123456789." },
  "err.national_code_invalid": { fa: "کد ملی معتبر نیست. ده رقم را دوباره بررسی کن.", en: "The national code is not valid. Check the ten digits again." },
  "err.name_invalid": { fa: "نام و نام خانوادگی را با حروف فارسی و حداقل دو کلمه بنویس.", en: "Write your full name in Persian letters, at least two words." },
  "err.class_invalid": { fa: "کلاس را انتخاب کن: ۲۰۱ یا ۲۰۲.", en: "Choose your class: 201 or 202." },
  "err.password_length": { fa: "رمز باید بین ۸ تا ۱۲۸ نویسه باشد.", en: "The password must be 8 to 128 characters." },
  "err.password_mix": { fa: "رمز باید هم حرف و هم عدد داشته باشد.", en: "The password must have both a letter and a number." },
  "err.password_weak": { fa: "رمز نباید همان شماره موبایل یا کد ملی باشد.", en: "The password must not be your mobile number or national code." },
  "err.invalid": { fa: "شماره موبایل یا رمز درست نیست.", en: "The mobile number or the password is not right." },
  "err.locked": { fa: "چند بار رمز اشتباه وارد شده است. ۱۵ دقیقه صبر کن و دوباره امتحان کن.", en: "The password was wrong several times. Wait 15 minutes and try again." },
  "err.exists": { fa: "این شماره موبایل یا کد ملی قبلاً ثبت شده است. اگر حساب خودت است، با همان رمز وارد شو. اگر رمزت را گم کرده‌ای، از معلم بخواه آن را بازنشانی کند.", en: "This mobile number or national code is already registered. If it is your account, sign in with your password. If you lost it, ask the teacher to reset it." },
  "err.disabled": { fa: "این حساب غیرفعال شده است. با معلم صحبت کن.", en: "This account has been disabled. Talk to the teacher." },
  "err.reset_required": { fa: "رمزت را معلم بازنشانی کرده است. با همین شماره و کد ملی، رمز جدید انتخاب کن.", en: "The teacher reset your password. Choose a new one with the same number and national code." },
  "err.rate_limited": { fa: "تعداد تلاش‌ها زیاد است. کمی بعد دوباره امتحان کن.", en: "Too many attempts. Try again in a little while." },
  "err.login_required": { fa: "برای ادامه وارد شو.", en: "Sign in to continue." },
  "err.problem_updated": { fa: "این مسئله به‌روز شده است. صفحه را دوباره باز کن تا نسخه‌ی تازه را ببینی.", en: "This problem was updated. Reload the page to see the new version." },
  "err.total_mismatch": { fa: "تعداد آزمون‌ها با نسخه‌ی این مسئله نمی‌خواند. صفحه را دوباره باز کن.", en: "The number of tests does not match this version of the problem. Reload the page." },
});

/** The text of a server error in the chosen language (the server answers in Persian). */
export function errorText(data) {
  const key = `err.${data?.error}`;
  return has(key) ? t(key) : data?.message || t("acct.generic");
}

const API = "/api/student";
// The offline copy reaches the teacher's server at this address (a test can point it elsewhere).
const SYNC_BASE = window.__teacherSyncBase || "https://teacher.arashnm80.ir/api/offline";
const SESSION_KEY = "teacher-sync-session-v1";
const DRAFT_DELAY_MS = 2500;
const MESSAGES = {
  get network() { return t("acct.network"); },
  get mismatch() { return t("acct.mismatch"); },
  get generic() { return t("acct.generic"); },
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

// ---- the offline copy's session: a token kept on the device ---------------------------------

const sessionListeners = new Set();

/** { token, student } of the signed-in student of the offline copy, or null. */
export function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY) || "null");
  } catch {
    return null;
  }
}

function saveSession(session) {
  try {
    if (session) localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    else localStorage.removeItem(SESSION_KEY);
  } catch {
    /* without storage the sign-in lasts for this visit only */
  }
}

/** Called when the student signs in or out (not on every start). */
export function onSessionChange(fn) {
  sessionListeners.add(fn);
}

function announceSession() {
  paintStudentBar();
  for (const fn of sessionListeners) {
    try {
      fn(student);
    } catch {
      /* a listener must not break the sign-in */
    }
  }
}

export function clearSession() {
  saveSession(null);
  student = null;
  announceSession();
}

/** The server's latest view of the student (for example a new class) after a sync. */
export function updateStudent(fresh) {
  const session = getSession();
  if (!session || !fresh) return;
  saveSession({ ...session, student: fresh });
  student = fresh;
  paintStudentBar();
}

export async function apiRequest(path, options) {
  return request(path, options);
}

async function request(path, { method = "GET", body } = {}) {
  let res;
  const headers = body !== undefined ? { "Content-Type": "application/json" } : {};
  if (OFFLINE) {
    const token = getSession()?.token;
    if (token) headers.Authorization = `Bearer ${token}`;
  }
  try {
    res = await fetch((OFFLINE ? SYNC_BASE : API) + path, {
      method,
      credentials: OFFLINE ? "omit" : "same-origin",
      cache: "no-store",
      headers,
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
  if (result.status === 401 && OFFLINE) {
    clearSession(); // the offline copy goes on working; the student signs in again when they want to
    return result;
  }
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
  phone: { modes: ["login", "register", "reset"] },
  nationalCode: { modes: ["register", "reset"] },
  fullName: { modes: ["register"] },
  classCode: { modes: ["register"] },
  password: { modes: ["login", "register", "reset"] },
  password2: { modes: ["register", "reset"] },
};
const MODE_TEXT = {
  get login() { return { title: t("acct.login.title"), submit: t("acct.login.submit") }; },
  get register() { return { title: t("acct.register.title"), submit: t("acct.register.submit") }; },
  get reset() { return { title: t("acct.reset.title"), submit: t("acct.reset.submit") }; },
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
  if (OFFLINE && data.token) saveSession({ token: data.token, student });
  $("auth-password").value = "";
  $("auth-password2").value = "";
  $("auth-dialog").close();
  const resolve = resolveSignIn;
  pendingSignIn = null;
  resolveSignIn = null;
  if (resolve) resolve(student);
  announceSession();
}

let resolveSignIn = null;

/** Opens the sign-in dialog (once) and resolves with the student when they are signed in. */
export function requireSignIn() {
  if (!ONLINE && !OFFLINE) return Promise.resolve(null);
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
        setMode("reset", errorText(res.data));
        return;
      }
      return showError(errorText(res.data));
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
      return showError(errorText(res.data));
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
    return showError(errorText(res.data));
  } finally {
    submit.disabled = false;
  }
}

function paintStudentBar() {
  const bar = $("student-bar");
  if (!bar) return;
  if (OFFLINE) {
    // The bar is always there offline: a sign-in button, or the name with the sync state.
    bar.hidden = false;
    $("student-who").hidden = !student;
    $("student-logout").hidden = !student;
    $("student-signin").hidden = Boolean(student);
  } else if (!student) {
    return;
  }
  if (student) {
    $("student-name").textContent = student.fullName;
    $("student-class").textContent = student.classCode || "—";
  }
  bar.hidden = false;
}

export async function logout() {
  if (OFFLINE) {
    await request("/logout", { method: "POST", body: {} }); // best effort: it may be offline
    clearSession();
    return;
  }
  flushDraft();
  await request("/logout", { method: "POST", body: {} });
  location.reload();
}

/** Wires the dialog and the sign-in bar. Call once at start-up. */
export function initAccountUi() {
  if (!ONLINE && !OFFLINE) return;
  const dialog = $("auth-dialog");
  onLangChange(() => {
    $("auth-title").textContent = MODE_TEXT[formMode].title;
    $("auth-submit").textContent = MODE_TEXT[formMode].submit;
  });
  $("auth-form").addEventListener("submit", submitAuth);
  $("auth-tab-login").addEventListener("click", () => setMode("login"));
  $("auth-tab-register").addEventListener("click", () => setMode("register"));
  $("student-logout").addEventListener("click", logout);
  if (OFFLINE) {
    // Optional offline: the student can close the dialog and keep working on this device.
    $("auth-later").hidden = false;
    $("auth-later").addEventListener("click", () => dialog.close());
    $("student-signin").addEventListener("click", () => requireSignIn());
    dialog.addEventListener("close", () => {
      if (pendingSignIn && !student) {
        const resolve = resolveSignIn;
        pendingSignIn = null;
        resolveSignIn = null;
        if (resolve) resolve(null);
      }
    });
    student = getSession()?.student || null;
    paintStudentBar();
    return;
  }
  dialog.addEventListener("cancel", (event) => event.preventDefault()); // the sign-in cannot be skipped
  // Offline-only controls: the server keeps the progress, so these do not apply.
  document.querySelector(".backup")?.setAttribute("hidden", "");
  $("btn-clear-progress")?.setAttribute("hidden", "");
}

/** Resolves the signed-in student for the first time. Opens the dialog when there is none. */
export async function ensureStudent() {
  if (OFFLINE) return student; // from the stored session: no network needed
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
