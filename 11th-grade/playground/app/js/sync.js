/**
 * The offline copy's link to the teacher: a queue of results, the state the server last reported,
 * the tutorials kept on the device, and the sync itself.
 *
 * Everything works without internet. A result is checked on the device and put in a queue; when
 * there is a connection (and the student is signed in) the queue is sent to the accounts service.
 * The service decides what counts: a result counts when it reaches the server before the deadline.
 * So the student always sees, for each solved problem, whether it has reached the teacher yet.
 */
import { apiRequest, getSession, clearSession, updateStudent } from "./account.js?v=5";
import { setServerTime } from "./countdown.js?v=2";
import { define, t } from "./i18n.js?v=5";

define({
  "sync.synced": { fa: "ارسال‌شده", en: "Sent" },
  "sync.pending": { fa: "منتظر ارسال", en: "Waiting to send" },
  "sync.unsent": { fa: "ارسال نشده", en: "Not sent" },
  "sync.outdated": { fa: "نسخه‌ی قدیمی", en: "Old version" },
  "sync.tip.synced": { fa: "حل شده و به معلم ارسال شده است", en: "Solved, and sent to the teacher" },
  "sync.tip.pending": { fa: "حل شده، اما هنوز به معلم نرسیده است", en: "Solved, but it has not reached the teacher yet" },
  "sync.tip.unsent": { fa: "حل شده؛ برای ارسال به معلم وارد شو", en: "Solved; sign in to send it to the teacher" },
  "sync.tip.outdated": { fa: "این مسئله در سایت تغییر کرده است؛ برنامه را به‌روز کن", en: "This problem changed on the website; update this copy" },
  "chip.signedout": { fa: "وارد نشده‌ای؛ پیشرفت فقط روی این دستگاه است", en: "Not signed in; progress stays on this device only" },
  "chip.syncing": { fa: "در حال ارسال…", en: "Sending…" },
  "chip.offline": { fa: "بدون اینترنت", en: "No internet" },
  "chip.pending": { fa: "{n} مسئله‌ی حل‌شده هنوز ارسال نشده", en: "{n} solved problem(s) not sent yet" },
  "chip.queue": { fa: "{n} تلاش منتظر ارسال", en: "{n} attempt(s) waiting to send" },
  "chip.synced": { fa: "همه‌ی نتیجه‌ها به معلم رسیده است ✓", en: "Everything has reached the teacher ✓" },
  "chip.outdated": { fa: "{n} مسئله در سایت تغییر کرده؛ برنامه را به‌روز کن", en: "{n} problem(s) changed on the website; update this copy" },
});

const QUEUE_KEY = "teacher-sync-queue-v1";
const STATE_KEY = "teacher-sync-state-v1";
const GUIDES_KEY = "teacher-sync-guides-v1";
const TYPING_KEY = "teacher-sync-typing-v1";
const MAX_QUEUE = 400;
const MAX_BYTES = 1_500_000;
const BATCH = 20;
const BATCH_BYTES = 400_000;
const AUTO_EVERY_MS = 60_000;
const STALE_MS = 10 * 60_000;

function read(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key) || "null") ?? fallback;
  } catch {
    return fallback;
  }
}

function write(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false; // storage full or blocked: the copy in memory still works for this visit
  }
}

let queue = read(QUEUE_KEY, []);
let server = read(STATE_KEY, { progress: {}, packs: [], classCode: "", revisions: {}, guidesVersion: "", at: "" });
let guides = read(GUIDES_KEY, { version: "", guides: {} });
const typing = read(TYPING_KEY, {});
let busy = false;
let lastError = "";
let sequence = Date.now();
const listeners = new Set();

export function onSyncChange(fn) {
  listeners.add(fn);
}

function changed() {
  for (const fn of listeners) {
    try {
      fn();
    } catch {
      /* one listener must not stop the others */
    }
  }
}

// ---- typing counts, kept across visits so the teacher's check sees the whole story -----------

export function noteSyncTyping(problemId, change) {
  if (!problemId || !change || change.origin === "setValue") return;
  const count = (typing[problemId] ||= { typed: 0, inserted: 0 });
  const size = (change.text || []).join("\n").length;
  if (change.origin === "+input") count.typed += size;
  else if (change.origin === "paste" || change.origin === "drop" || change.origin === "drag") count.inserted += size;
  else return;
  write(TYPING_KEY, typing);
}

export function typingFor(problemId) {
  return typing[problemId] || { typed: 0, inserted: 0 };
}

// ---- the queue --------------------------------------------------------------------------------

const solving = (r) => !r.blocked && r.total > 0 && r.passed === r.total;

function trimQueue() {
  const size = () => JSON.stringify(queue).length;
  while (queue.length > MAX_QUEUE || size() > MAX_BYTES) {
    // Drop the oldest result that did not solve the problem; a solving result goes last.
    const at = queue.findIndex((r) => !solving(r));
    queue.splice(at === -1 ? 0 : at, 1);
  }
}

export function queueResult(result) {
  queue.push({ _id: ++sequence, clientAt: new Date().toISOString(), ...result });
  trimQueue();
  write(QUEUE_KEY, queue);
  changed();
  scheduleSync();
}

/** Results of problems solved on this device before there was a queue or an account. */
export function backfill(problems, progress, codes) {
  for (const problem of problems) {
    const local = progress[problem.id];
    if (!local?.solved) continue;
    if (server.progress[problem.id]?.solved && server.progress[problem.id].revision === local.revision) continue;
    if (queue.some((r) => r.problemId === problem.id && solving(r) && r.revision === local.revision)) continue;
    queueResult({
      problemId: problem.id, revision: local.revision, code: codes[problem.id] || "",
      passed: problem.tests.length, total: problem.tests.length, blocked: false, typed: 0, inserted: 0,
      clientAt: local.at || new Date().toISOString(),
    });
  }
}

export const queueLength = () => queue.length;
export const serverState = () => server;
export const lastSyncAt = () => server.at || "";

// ---- what the student sees ----------------------------------------------------------------------

/** For a problem solved on this device: "synced", "pending", "unsent" (not signed in) or "outdated". */
export function solvedStatus(problemId, local, localRevision) {
  if (!local?.solved) return null;
  const serverRevision = server.revisions[problemId];
  if (serverRevision && serverRevision !== localRevision) return "outdated";
  const known = server.progress[problemId];
  if (known?.solved && known.revision === local.revision) return "synced";
  return getSession() ? "pending" : "unsent";
}

export function statusText(status) {
  return status ? t(`sync.${status}`) : "";
}

export function statusTip(status) {
  return status ? t(`sync.tip.${status}`) : "";
}

/** Counts for the summary, and the state and sentence of the chip in the bar. */
export function summarize(problems, progress, revisionOf) {
  let solved = 0, synced = 0, pending = 0, outdated = 0;
  for (const problem of problems) {
    const status = solvedStatus(problem.id, progress[problem.id], revisionOf(problem));
    if (!status) continue;
    solved += 1;
    if (status === "synced") synced += 1;
    else if (status === "outdated") outdated += 1;
    else pending += 1;
  }
  let state = "synced";
  let text = t("chip.synced");
  const signedIn = Boolean(getSession());
  if (!signedIn) {
    state = "signedout";
    text = t("chip.signedout");
  } else if (busy) {
    state = "syncing";
    text = t("chip.syncing");
  } else if (outdated) {
    state = "outdated";
    text = t("chip.outdated", { n: outdated });
  } else if (pending || queue.length) {
    state = lastError === "offline" || navigator.onLine === false ? "offline" : "pending";
    text = pending ? t("chip.pending", { n: pending }) : t("chip.queue", { n: queue.length });
    if (state === "offline") text = `${t("chip.offline")} — ${text}`;
  }
  return { solved, synced, pending, outdated, queue: queue.length, state, text, lastSyncAt: server.at };
}

// ---- tutorials kept on the device ---------------------------------------------------------------

export const guideFor = (problemId) => guides.guides?.[problemId] || null;
export const hasGuides = () => Boolean(guides.version);

async function refreshGuides() {
  if (!getSession()) return;
  if (guides.version && guides.version === server.guidesVersion) return;
  const res = await apiRequest("/guides");
  if (res.status === 200 && res.data.guides) {
    guides = { version: res.data.version, guides: res.data.guides };
    write(GUIDES_KEY, guides);
    changed();
  }
}

// ---- the sync ---------------------------------------------------------------------------------

function takeBatch() {
  const batch = [];
  let bytes = 0;
  for (const item of queue) {
    const size = JSON.stringify(item).length;
    if (batch.length && (batch.length >= BATCH || bytes + size > BATCH_BYTES)) break;
    batch.push(item);
    bytes += size;
  }
  return batch;
}

function acceptState(data) {
  server = {
    progress: data.progress || {}, packs: data.packs || [], classCode: data.classCode || "",
    revisions: data.revisions || {}, guidesVersion: data.guidesVersion || "", at: new Date().toISOString(),
    serverTime: data.serverTime || "",
  };
  write(STATE_KEY, server);
  if (data.serverTime) setServerTime(data.serverTime);
  if (data.student) updateStudent(data.student);
}

/** Sends the queue and refreshes the server's state. Returns "ok", "offline", "signed-out", "busy" or "error". */
export async function syncNow() {
  if (busy) return "busy";
  if (!getSession()) {
    lastError = "signed-out";
    changed();
    return "signed-out";
  }
  busy = true;
  changed();
  try {
    for (;;) {
      const batch = takeBatch();
      const res = batch.length
        ? await apiRequest("/sync", { method: "POST", body: { results: batch.map(({ _id, ...rest }) => rest) } })
        : await apiRequest("/me");
      if (res.status === 0) return (lastError = "offline");
      if (res.status === 401) {
        clearSession();
        return (lastError = "signed-out");
      }
      if (res.status === 429) return (lastError = "busy");
      if (res.status !== 200) return (lastError = "error");
      if (batch.length) {
        const sent = new Set(batch.map((r) => r._id));
        queue = queue.filter((r) => !sent.has(r._id));
        write(QUEUE_KEY, queue);
      }
      acceptState(res.data);
      if (!queue.length) break;
    }
    lastError = "";
    await refreshGuides();
    return "ok";
  } finally {
    busy = false;
    changed();
  }
}

let soon = null;
/** A short pause after a run, so a burst of runs is one request. */
export function scheduleSync(delay = 1500) {
  clearTimeout(soon);
  soon = setTimeout(() => {
    if (getSession()) syncNow();
  }, delay);
}

let started = false;
/** Syncs on start, when the connection comes back, when the tab is shown again, and every minute if needed. */
export function startAutoSync() {
  if (started) return;
  started = true;
  const trySync = () => getSession() && syncNow();
  window.addEventListener("online", trySync);
  document.addEventListener("visibilitychange", () => document.visibilityState === "visible" && trySync());
  setInterval(() => {
    const stale = !server.at || Date.now() - Date.parse(server.at) > STALE_MS;
    if (queue.length || stale) trySync();
  }, AUTO_EVERY_MS);
  trySync();
}
