/*
 * The teacher's panel: students, their progress, the submission log, the class schedules, and the
 * report of actions. Everything the server sends is written with textContent, never as HTML.
 * Dates are shown in the Jalali calendar and Tehran time.
 */

// ---- two languages: the choice is shared with the rest of the site -------------------------------
const LANG_KEY = "grade11-lang-v2";
let lang = "fa";
try {
  lang = localStorage.getItem(LANG_KEY) === "en" ? "en" : "fa";
} catch {
  lang = "fa";
}
/** The Persian or the English text, by the chosen language. */
const x = (fa, en) => (lang === "en" ? en : fa);

const FLAG_TEXT = {
  inserted: ["متن بدون تایپ وارد شده", "Text entered without typing"],
  no_typing: ["کد بدون تایپ نوشته شده", "Code written without typing"],
  quick_pass: ["قبول شدن خیلی سریع", "Passed very quickly"],
};
/** The server's messages are Persian; in English the panel shows its own text for the known codes. */
const SERVER_TEXT_EN = {
  network: "Could not connect to the server.",
  rate_limited: "Too many attempts. Try again in a moment.",
  not_configured: "The admin password has not been set yet.",
  locked: "Too many wrong passwords. Try again later.",
  invalid: "Wrong password.",
  admin_required: "Enter the admin password to open the panel.",
  login_required: "Sign in to continue.",
  not_found: "This student was not found.",
  class_invalid: "Set the class to 201 or 202.",
  bad_origin: "This request did not come from this site.",
  bad_length: "The request is not valid.",
  bad_json: "The request is not valid.",
  too_large: "The request is too big.",
  unsupported_media: "The request must be JSON.",
};
const timeFormat = () =>
  new Intl.DateTimeFormat(lang === "en" ? "en-GB" : "fa-IR-u-ca-persian", {
    timeZone: "Asia/Tehran", dateStyle: "medium", timeStyle: "short", hourCycle: "h23",
  });
/** The text of a failed answer in the chosen language (the server's Persian text is the fallback). */
function failure(res, fallbackFa, fallbackEn) {
  if (lang === "en") return SERVER_TEXT_EN[res.data.code] || fallbackEn;
  return res.data.message || fallbackFa;
}
const SESSION_ENDED = () => x("نشست مدیر تمام شده است. دوباره وارد شو.", "The admin session has ended. Sign in again.");
let currentView = "students";

function applyStatic() {
  const html = document.documentElement;
  html.lang = lang;
  html.dir = lang === "fa" ? "rtl" : "ltr";
  for (const el of document.querySelectorAll("[data-fa][data-en]")) el.textContent = el.getAttribute(`data-${lang}`);
  for (const [attr, name] of [["placeholder", "placeholder"], ["aria-label", "aria"]]) {
    for (const el of document.querySelectorAll(`[data-fa-${name}]`)) el.setAttribute(attr, el.getAttribute(`data-${lang}-${name}`) ?? "");
  }
  const toggle = document.getElementById("lang-toggle");
  if (toggle) toggle.setAttribute("data-lang", lang);
}

const $ = (id) => document.getElementById(id);
let currentId = null;
let currentStudent = null;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined && text !== null) element.textContent = String(text);
  if (className) element.className = className;
  return element;
}

function when(iso) {
  return iso ? timeFormat().format(new Date(iso)) : "—";
}

function setStatus(text) {
  $("status").textContent = text || "";
}

async function api(path, { method = "GET", body } = {}) {
  let res;
  try {
    res = await fetch("/api/admin" + path, {
      method,
      credentials: "same-origin",
      cache: "no-store",
      headers: body !== undefined ? { "Content-Type": "application/json" } : {},
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    return { status: 0, data: { code: "network", message: "اتصال به سرور برقرار نشد." } };
  }
  let data = {};
  try {
    data = await res.json();
  } catch {
    data = {};
  }
  return { status: res.status, data };
}

function showLogin(message = "") {
  $("login-view").hidden = false;
  $("app-view").hidden = true;
  $("logout").hidden = true;
  $("login-error").textContent = message;
  $("login-error").hidden = !message;
}

function showApp() {
  $("login-view").hidden = true;
  $("app-view").hidden = false;
  $("logout").hidden = false;
}

function statusText(s) {
  if (s.disabled) return x("غیرفعال", "Disabled");
  if (s.needsPassword) return x("منتظر انتخاب رمز تازه", "Waiting for a new password");
  if (s.locked) return x("قفل موقت", "Temporarily locked");
  return x("فعال", "Active");
}

function flagsText(flags) {
  const label = (f) => (FLAG_TEXT[f] ? x(...FLAG_TEXT[f]) : f);
  return flags && flags.length ? flags.map(label).join(x("، ", ", ")) : "—";
}

// ---- switching between the parts of the panel --------------------------------------------------

const VIEWS = ["students", "submissions", "schedule", "audit"];

function showView(name) {
  currentView = name;
  setStatus("");
  for (const view of VIEWS) {
    $(`view-${view}`).hidden = view !== name;
    $(`tab-${view}`).classList.toggle("active", view === name);
  }
  if (name === "students") loadStudents();
  if (name === "submissions") loadSubmissions();
  if (name === "schedule") loadSchedule();
  if (name === "audit") showAudit();
}

// ---- students ------------------------------------------------------------------------------

async function loadStudents() {
  const q = encodeURIComponent($("search").value.trim());
  const res = await api(`/students?q=${q}`);
  if (res.status === 401) return showLogin(SESSION_ENDED());
  if (res.status !== 200) return setStatus(failure(res, "خواندن فهرست انجام نشد.", "The list could not be read."));
  renderStudents(res.data.students, res.data.problemCount);
  setStatus(x(`${res.data.students.length} دانش‌آموز`, `${res.data.students.length} students`));
}

function renderStudents(students, total) {
  const body = $("students");
  body.replaceChildren();
  if (!students.length) {
    const cell = node("td", x("دانش‌آموزی پیدا نشد.", "No student found."));
    cell.colSpan = 10;
    const row = node("tr");
    row.append(cell);
    body.append(row);
    return;
  }
  for (const s of students) {
    const name = node("td");
    const link = node("button", s.fullName, "link-button");
    link.type = "button";
    link.addEventListener("click", () => openStudent(s.id));
    name.append(link);
    const row = node("tr");
    row.append(
      name,
      node("td", s.classCode || "—"),
      node("td", s.phone, "ltr"),
      node("td", s.nationalCode, "ltr"),
      node("td", x(`${s.solved} از ${total}`, `${s.solved} of ${total}`)),
      node("td", s.scored),
      node("td", s.attempts),
      node("td", s.flagged),
      node("td", statusText(s)),
      node("td", when(s.lastLoginAt)),
    );
    body.append(row);
  }
}

// ---- one student ---------------------------------------------------------------------------

async function openStudent(id) {
  currentId = id;
  const res = await api(`/students/${id}`);
  if (res.status === 401) return showLogin(SESSION_ENDED());
  if (res.status !== 200) return setStatus(failure(res, "این دانش‌آموز پیدا نشد.", "This student was not found."));
  renderDetail(res.data);
  $("detail").hidden = false;
  $("detail").scrollIntoView({ behavior: "smooth", block: "start" });
}

function fact(list, label, value, className) {
  list.append(node("dt", label), node("dd", value, className));
}

function scoreText(p) {
  if (!p.solved) return "—";
  if (p.scored) return x("در مهلت (نمره)", "On time (scored)");
  return p.deadline ? x("پس از مهلت (تمرین)", "After the deadline (practice)") : x("بدون نمره (تمرین)", "No score (practice)");
}

function renderDetail(data) {
  const s = data.student;
  currentStudent = s;
  $("detail-name").textContent = s.fullName;
  const facts = $("detail-facts");
  facts.replaceChildren();
  fact(facts, x("کلاس", "Class"), s.classCode || "—");
  fact(facts, x("موبایل", "Mobile"), s.phone, "ltr");
  fact(facts, x("کد ملی", "National code"), s.nationalCode, "ltr");
  fact(facts, x("ثبت‌نام", "Signed up"), when(s.createdAt));
  fact(facts, x("آخرین ورود", "Last sign-in"), when(s.lastLoginAt));
  fact(facts, x("وضعیت", "Status"), statusText(s));
  fact(facts, x("مسئله‌های قبول‌شده", "Problems passed"), x(`${s.solved} از ${data.problemCount}`, `${s.solved} of ${data.problemCount}`));
  fact(facts, x("نمره (قبول در مهلت)", "Score (passed on time)"), x(`${s.scored} از ${data.problemCount}`, `${s.scored} of ${data.problemCount}`));
  $("detail-toggle").textContent = s.disabled ? x("فعال کردن حساب", "Enable the account") : x("غیرفعال کردن حساب", "Disable the account");
  $("detail-class").value = ["201", "202"].includes(s.classCode) ? s.classCode : "201";

  const rows = $("detail-progress");
  rows.replaceChildren();
  if (!data.progress.length) {
    const cell = node("td", x("هنوز کاری ثبت نشده است.", "Nothing has been recorded yet."));
    cell.colSpan = 7;
    const row = node("tr");
    row.append(cell);
    rows.append(row);
  }
  for (const p of data.progress) {
    const code = node("td");
    if (p.lastCode) {
      const details = node("details");
      details.append(node("summary", x("نمایش کد", "Show the code")), node("pre", p.lastCode, "admin-code"));
      code.append(details);
    } else {
      code.textContent = "—";
    }
    const row = node("tr");
    row.append(
      node("td", `${p.number}. ${(lang === "en" && p.titleEn) || p.title}`),
      node("td", p.solved ? x("قبول شد", "Passed") : x("هنوز قبول نشده", "Not passed yet")),
      node("td", scoreText(p)),
      node("td", p.attempts),
      node("td", p.revision),
      node("td", flagsText(p.flags)),
      code,
    );
    rows.append(row);
  }

  const list = $("detail-attempts");
  list.replaceChildren();
  if (!data.attempts.length) list.append(node("p", x("هنوز ثبتی نیست.", "No submissions yet."), "admin-status"));
  for (const a of data.attempts) {
    const item = node("div", null, "attempt");
    item.append(
      node("p", x(`${when(a.at)} · ${a.problemId} · ${a.percent}٪ درست (${a.passed} از ${a.total}) · نسخه ${a.revision}` +
        ` · ${a.onTime ? "در مهلت" : "پس از مهلت یا بدون مهلت"}` + (a.solved ? " · قبول" : ""),
        `${when(a.at)} · ${a.problemId} · ${a.percent}% correct (${a.passed} of ${a.total}) · revision ${a.revision}` +
        ` · ${a.onTime ? "on time" : "after the deadline or no deadline"}` + (a.solved ? " · passed" : "")), "attempt-head"),
    );
    if (a.flags.length) item.append(node("p", flagsText(a.flags), "flag-line"));
    item.append(node("pre", a.code, "admin-code"));
    list.append(item);
  }
}

async function resetPassword() {
  if (!currentStudent) return;
  const ok = confirm(x(
    "رمز این دانش‌آموز پاک می‌شود. در ورود بعدی باید با شماره و کد ملی‌اش رمز تازه انتخاب کند. ادامه بدهم؟",
    "This student's password will be erased. At the next sign-in they must choose a new password with their number and national code. Continue?"
  ));
  if (!ok) return;
  const res = await api(`/students/${currentId}/reset-password`, { method: "POST", body: {} });
  if (res.status === 200) {
    await openStudent(currentId);
    await loadStudents();
  }
  // Set last, so the list reload above does not hide the result of the action.
  setStatus(res.status === 200 ? x("رمز بازنشانی شد.", "The password was reset.") : failure(res, "انجام نشد.", "It was not done."));
}

async function toggleAccount() {
  if (!currentStudent) return;
  const disabling = !currentStudent.disabled;
  if (disabling && !confirm(x("با غیرفعال کردن، این دانش‌آموز نمی‌تواند وارد شود تا دوباره فعالش کنی. ادامه بدهم؟",
      "If you disable the account, this student cannot sign in until you enable it again. Continue?"))) {
    return;
  }
  const path = `/students/${currentId}/${disabling ? "disable" : "enable"}`;
  const res = await api(path, { method: "POST", body: {} });
  if (res.status === 200) {
    await openStudent(currentId);
    await loadStudents();
  }
  setStatus(res.status === 200 ? (disabling ? x("حساب غیرفعال شد.", "The account was disabled.") : x("حساب فعال شد.", "The account was enabled.")) : failure(res, "انجام نشد.", "It was not done."));
}

async function changeClass() {
  if (!currentStudent) return;
  const target = $("detail-class").value;
  if (target === (currentStudent.classCode || "")) return setStatus(x("این دانش‌آموز از پیش در این کلاس است.", "This student is already in this class."));
  if (!confirm(x(`کلاس این دانش‌آموز به ${target} تغییر کند؟ از این پس نمره‌ها و مهلت‌ها بر اساس سری‌های کلاس ${target} حساب می‌شود.`,
      `Change this student's class to ${target}? From now on, scores and deadlines are calculated by the series of class ${target}.`))) {
    return;
  }
  const res = await api(`/students/${currentId}/class`, { method: "POST", body: { classCode: target } });
  if (res.status === 200) {
    await openStudent(currentId);
    await loadStudents();
  }
  setStatus(res.status === 200 ? x(`کلاس به ${target} تغییر کرد.`, `The class was changed to ${target}.`) : failure(res, "تغییر کلاس انجام نشد.", "The class change was not done."));
}

// ---- the submission log ----------------------------------------------------------------------

function submissionFilters() {
  const params = new URLSearchParams();
  if ($("sub-class").value) params.set("class", $("sub-class").value);
  if ($("sub-search").value.trim()) params.set("q", $("sub-search").value.trim());
  return params.toString();
}

async function loadSubmissions() {
  const query = submissionFilters();
  $("sub-csv").href = "/api/admin/submissions.csv" + (query ? `?${query}` : "");
  const res = await api(`/submissions${query ? `?${query}` : ""}`);
  if (res.status === 401) return showLogin(SESSION_ENDED());
  if (res.status !== 200) return setStatus(failure(res, "ثبت‌ها خوانده نشد.", "The submissions could not be read."));
  renderSubmissions(res.data.submissions);
  setStatus(x(`${res.data.submissions.length} ثبت (حداکثر ۵۰۰ تای آخر)`, `${res.data.submissions.length} submissions (at most the last 500)`));
}

function renderSubmissions(items) {
  const body = $("sub-rows");
  body.replaceChildren();
  if (!items.length) {
    const cell = node("td", x("ثبتی پیدا نشد.", "No submission found."));
    cell.colSpan = 7;
    const row = node("tr");
    row.append(cell);
    body.append(row);
    return;
  }
  for (const s of items) {
    const code = node("td");
    const details = node("details");
    details.append(node("summary", x("نمایش کد", "Show the code")), node("pre", s.code, "admin-code"));
    code.append(details);
    const scoreCell = !s.deadline ? x("بدون مهلت", "No deadline") : s.onTime ? x("در مهلت", "On time") : x("پس از مهلت", "After the deadline");
    const row = node("tr");
    row.append(
      node("td", when(s.at)),
      node("td", s.class || "—"),
      node("td", s.studentName),
      node("td", `${s.number}. ${s.title}`),
      node("td", x(`${s.percent}٪ (${s.passed} از ${s.total})`, `${s.percent}% (${s.passed} of ${s.total})`)),
      node("td", scoreCell),
      code,
    );
    body.append(row);
  }
}

// ---- the schedule of the classes -------------------------------------------------------------

async function loadSchedule() {
  const res = await api("/schedule");
  if (res.status !== 200) return setStatus(failure(res, "برنامه خوانده نشد.", "The schedule could not be read."));
  const box = $("schedule-box");
  box.replaceChildren();
  const classes = Object.keys(res.data.classes).sort();
  if (!classes.length) box.append(node("p", x("برنامه‌ای برای کلاس‌ها تعریف نشده است.", "No schedule is defined for the classes."), "admin-status"));
  const text = (pack, field) => (lang === "en" && pack.en?.[field]) || pack[field];
  for (const cls of classes) {
    box.append(node("h3", x(`کلاس ${cls}`, `Class ${cls}`)));
    for (const pack of res.data.classes[cls]) {
      const section = node("section", null, "pack");
      section.append(node("h4", `${text(pack, "title")} · ${x("مهلت", "Deadline")}: ${text(pack, "untilText")}`));
      section.append(node("p", x(`${pack.questions.length} مسئله: `, `${pack.questions.length} problems: `) +
        pack.questions.map((q) => q.number).join(x("، ", ", ")), "admin-status"));
      section.append(node("pre", text(pack, "markdown") || x("(بدون متن)", "(no text)"), "admin-code"));
      box.append(section);
    }
  }
}

// ---- the report of actions -------------------------------------------------------------------

async function showAudit() {
  const res = await api("/audit");
  if (res.status !== 200) return setStatus(failure(res, "گزارش خوانده نشد.", "The report could not be read."));
  const rows = $("audit-rows");
  rows.replaceChildren();
  for (const e of res.data.entries) {
    const row = node("tr");
    row.append(node("td", when(e.at)), node("td", e.actor, "ltr"), node("td", e.action), node("td", e.target));
    rows.append(row);
  }
}

// ---- wiring ------------------------------------------------------------------------------------

$("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const res = await api("/login", { method: "POST", body: { password: $("admin-password").value } });
  $("admin-password").value = "";
  if (res.status === 200) {
    showApp();
    showView("students");
  } else {
    showLogin(failure(res, "ورود انجام نشد.", "Sign-in was not done."));
  }
});

$("logout").addEventListener("click", async () => {
  await api("/logout", { method: "POST", body: {} });
  showLogin();
});

for (const view of VIEWS) {
  $(`tab-${view}`).addEventListener("click", () => showView(view));
}

let searchTimer = null;
$("search").addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadStudents, 300);
});
$("refresh").addEventListener("click", () => loadStudents());
$("sub-class").addEventListener("change", loadSubmissions);
$("sub-search").addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadSubmissions, 300);
});
$("sub-refresh").addEventListener("click", () => loadSubmissions());
$("detail-close").addEventListener("click", () => {
  $("detail").hidden = true;
  currentId = null;
});
$("detail-reset").addEventListener("click", resetPassword);
$("detail-toggle").addEventListener("click", toggleAccount);
$("detail-class-save").addEventListener("click", changeClass);

$("lang-toggle").addEventListener("click", () => {
  lang = lang === "fa" ? "en" : "fa";
  try {
    localStorage.setItem(LANG_KEY, lang);
  } catch {
    /* the choice lasts for this visit */
  }
  applyStatic();
  // Draw what the scripts built again in the new language.
  if (!$("app-view").hidden) {
    showView(currentView);
    if (currentId && !$("detail").hidden) openStudent(currentId);
  }
});

async function start() {
  applyStatic();
  const session = await api("/session");
  if (session.status === 200) {
    showApp();
    showView("students");
  } else {
    showLogin();
  }
}
start();
