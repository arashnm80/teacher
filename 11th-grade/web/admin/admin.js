/*
 * The teacher's panel: students, their progress, the submission log, the class schedules, and the
 * report of actions. Everything the server sends is written with textContent, never as HTML.
 * Dates are shown in the Jalali calendar and Tehran time.
 */
const FLAG_TEXT = {
  inserted: "متن بدون تایپ وارد شده",
  no_typing: "کد بدون تایپ نوشته شده",
  quick_pass: "قبول شدن خیلی سریع",
};
const TIME = new Intl.DateTimeFormat("fa-IR-u-ca-persian", {
  timeZone: "Asia/Tehran", dateStyle: "medium", timeStyle: "short", hourCycle: "h23",
});

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
  return iso ? TIME.format(new Date(iso)) : "—";
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
    return { status: 0, data: { message: "اتصال به سرور برقرار نشد." } };
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
  if (s.disabled) return "غیرفعال";
  if (s.needsPassword) return "منتظر انتخاب رمز تازه";
  if (s.locked) return "قفل موقت";
  return "فعال";
}

function flagsText(flags) {
  return flags && flags.length ? flags.map((f) => FLAG_TEXT[f] || f).join("، ") : "—";
}

// ---- switching between the parts of the panel --------------------------------------------------

const VIEWS = ["students", "submissions", "schedule", "audit"];

function showView(name) {
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
  if (res.status === 401) return showLogin("نشست مدیر تمام شده است. دوباره وارد شو.");
  if (res.status !== 200) return setStatus(res.data.message || "خواندن فهرست انجام نشد.");
  renderStudents(res.data.students, res.data.problemCount);
  setStatus(`${res.data.students.length} دانش‌آموز`);
}

function renderStudents(students, total) {
  const body = $("students");
  body.replaceChildren();
  if (!students.length) {
    const cell = node("td", "دانش‌آموزی پیدا نشد.");
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
      node("td", `${s.solved} از ${total}`),
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
  if (res.status === 401) return showLogin("نشست مدیر تمام شده است. دوباره وارد شو.");
  if (res.status !== 200) return setStatus(res.data.message || "این دانش‌آموز پیدا نشد.");
  renderDetail(res.data);
  $("detail").hidden = false;
  $("detail").scrollIntoView({ behavior: "smooth", block: "start" });
}

function fact(list, label, value, className) {
  list.append(node("dt", label), node("dd", value, className));
}

function scoreText(p) {
  if (!p.solved) return "—";
  if (p.scored) return "در مهلت (نمره)";
  return p.deadline ? "پس از مهلت (تمرین)" : "بدون نمره (تمرین)";
}

function renderDetail(data) {
  const s = data.student;
  currentStudent = s;
  $("detail-name").textContent = s.fullName;
  const facts = $("detail-facts");
  facts.replaceChildren();
  fact(facts, "کلاس", s.classCode || "—");
  fact(facts, "موبایل", s.phone, "ltr");
  fact(facts, "کد ملی", s.nationalCode, "ltr");
  fact(facts, "ثبت‌نام", when(s.createdAt));
  fact(facts, "آخرین ورود", when(s.lastLoginAt));
  fact(facts, "وضعیت", statusText(s));
  fact(facts, "مسئله‌های قبول‌شده", `${s.solved} از ${data.problemCount}`);
  fact(facts, "نمره (قبول در مهلت)", `${s.scored} از ${data.problemCount}`);
  $("detail-toggle").textContent = s.disabled ? "فعال کردن حساب" : "غیرفعال کردن حساب";
  $("detail-class").value = ["201", "202"].includes(s.classCode) ? s.classCode : "201";

  const rows = $("detail-progress");
  rows.replaceChildren();
  if (!data.progress.length) {
    const cell = node("td", "هنوز کاری ثبت نشده است.");
    cell.colSpan = 7;
    const row = node("tr");
    row.append(cell);
    rows.append(row);
  }
  for (const p of data.progress) {
    const code = node("td");
    if (p.lastCode) {
      const details = node("details");
      details.append(node("summary", "نمایش کد"), node("pre", p.lastCode, "admin-code"));
      code.append(details);
    } else {
      code.textContent = "—";
    }
    const row = node("tr");
    row.append(
      node("td", `${p.number}. ${p.title}`),
      node("td", p.solved ? "قبول شد" : "هنوز قبول نشده"),
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
  if (!data.attempts.length) list.append(node("p", "هنوز ثبتی نیست.", "admin-status"));
  for (const a of data.attempts) {
    const item = node("div", null, "attempt");
    item.append(
      node("p", `${when(a.at)} · ${a.problemId} · ${a.percent}٪ درست (${a.passed} از ${a.total}) · نسخه ${a.revision}` +
        ` · ${a.onTime ? "در مهلت" : "پس از مهلت یا بدون مهلت"}` + (a.solved ? " · قبول" : ""), "attempt-head"),
    );
    if (a.flags.length) item.append(node("p", flagsText(a.flags), "flag-line"));
    item.append(node("pre", a.code, "admin-code"));
    list.append(item);
  }
}

async function resetPassword() {
  if (!currentStudent) return;
  const ok = confirm(
    "رمز این دانش‌آموز پاک می‌شود. در ورود بعدی باید با شماره و کد ملی‌اش رمز تازه انتخاب کند. ادامه بدهم؟"
  );
  if (!ok) return;
  const res = await api(`/students/${currentId}/reset-password`, { method: "POST", body: {} });
  if (res.status === 200) {
    await openStudent(currentId);
    await loadStudents();
  }
  // Set last, so the list reload above does not hide the result of the action.
  setStatus(res.status === 200 ? "رمز بازنشانی شد." : res.data.message || "انجام نشد.");
}

async function toggleAccount() {
  if (!currentStudent) return;
  const disabling = !currentStudent.disabled;
  if (disabling && !confirm("با غیرفعال کردن، این دانش‌آموز نمی‌تواند وارد شود تا دوباره فعالش کنی. ادامه بدهم؟")) {
    return;
  }
  const path = `/students/${currentId}/${disabling ? "disable" : "enable"}`;
  const res = await api(path, { method: "POST", body: {} });
  if (res.status === 200) {
    await openStudent(currentId);
    await loadStudents();
  }
  setStatus(res.status === 200 ? (disabling ? "حساب غیرفعال شد." : "حساب فعال شد.") : res.data.message || "انجام نشد.");
}

async function changeClass() {
  if (!currentStudent) return;
  const target = $("detail-class").value;
  if (target === (currentStudent.classCode || "")) return setStatus("این دانش‌آموز از پیش در این کلاس است.");
  if (!confirm(`کلاس این دانش‌آموز به ${target} تغییر کند؟ از این پس نمره‌ها و مهلت‌ها بر اساس سری‌های کلاس ${target} حساب می‌شود.`)) {
    return;
  }
  const res = await api(`/students/${currentId}/class`, { method: "POST", body: { classCode: target } });
  if (res.status === 200) {
    await openStudent(currentId);
    await loadStudents();
  }
  setStatus(res.status === 200 ? `کلاس به ${target} تغییر کرد.` : res.data.message || "تغییر کلاس انجام نشد.");
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
  if (res.status === 401) return showLogin("نشست مدیر تمام شده است. دوباره وارد شو.");
  if (res.status !== 200) return setStatus(res.data.message || "ثبت‌ها خوانده نشد.");
  renderSubmissions(res.data.submissions);
  setStatus(`${res.data.submissions.length} ثبت (حداکثر ۵۰۰ تای آخر)`);
}

function renderSubmissions(items) {
  const body = $("sub-rows");
  body.replaceChildren();
  if (!items.length) {
    const cell = node("td", "ثبتی پیدا نشد.");
    cell.colSpan = 7;
    const row = node("tr");
    row.append(cell);
    body.append(row);
    return;
  }
  for (const s of items) {
    const code = node("td");
    const details = node("details");
    details.append(node("summary", "نمایش کد"), node("pre", s.code, "admin-code"));
    code.append(details);
    const scoreCell = !s.deadline ? "بدون مهلت" : s.onTime ? "در مهلت" : "پس از مهلت";
    const row = node("tr");
    row.append(
      node("td", when(s.at)),
      node("td", s.class || "—"),
      node("td", s.studentName),
      node("td", `${s.number}. ${s.title}`),
      node("td", `${s.percent}٪ (${s.passed} از ${s.total})`),
      node("td", scoreCell),
      code,
    );
    body.append(row);
  }
}

// ---- the schedule of the classes -------------------------------------------------------------

async function loadSchedule() {
  const res = await api("/schedule");
  if (res.status !== 200) return setStatus(res.data.message || "برنامه خوانده نشد.");
  const box = $("schedule-box");
  box.replaceChildren();
  const classes = Object.keys(res.data.classes).sort();
  if (!classes.length) box.append(node("p", "برنامه‌ای برای کلاس‌ها تعریف نشده است.", "admin-status"));
  for (const cls of classes) {
    box.append(node("h3", `کلاس ${cls}`));
    for (const pack of res.data.classes[cls]) {
      const section = node("section", null, "pack");
      section.append(node("h4", `${pack.title} · مهلت: ${pack.untilText}`));
      section.append(node("p", `${pack.questions.length} مسئله: ` +
        pack.questions.map((q) => q.number).join("، "), "admin-status"));
      section.append(node("pre", pack.markdown || "(بدون متن)", "admin-code"));
      box.append(section);
    }
  }
}

// ---- the report of actions -------------------------------------------------------------------

async function showAudit() {
  const res = await api("/audit");
  if (res.status !== 200) return setStatus(res.data.message || "گزارش خوانده نشد.");
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
    showLogin(res.data.message || "ورود انجام نشد.");
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

async function start() {
  const session = await api("/session");
  if (session.status === 200) {
    showApp();
    showView("students");
  } else {
    showLogin();
  }
}
start();
