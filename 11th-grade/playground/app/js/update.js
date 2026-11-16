/**
 * The update notice of the offline copy. The launcher (which serves this page from the student's
 * own computer) can compare this copy with the website and replace what changed. This module asks
 * it, shows a notice when there is something new, and starts the update on a click.
 * Opened without the launcher, the addresses do not exist and nothing is shown.
 */
import { define, t } from "./i18n.js?v=5";

define({
  "update.available": { fa: "نسخه‌ی تازه‌ی برنامه آماده است ({files} فایل، حدود {mb} مگابایت).", en: "A new version is ready ({files} files, about {mb} MB)." },
  "update.apply": { fa: "به‌روزرسانی", en: "Update now" },
  "update.later": { fa: "بعداً", en: "Later" },
  "update.running": { fa: "در حال به‌روزرسانی… {done} از {total}", en: "Updating… {done} of {total}" },
  "update.done": { fa: "به‌روزرسانی انجام شد. صفحه دوباره باز می‌شود.", en: "Updated. The page will reload." },
  "update.failed": { fa: "به‌روزرسانی انجام نشد ({why}). دوباره امتحان کن.", en: "The update did not work ({why}). Try again." },
  "update.version": { fa: "نسخه‌ی این برنامه", en: "Version of this copy" },
});

const CHECK_EVERY_MS = 30 * 60_000;
let banner = null;

function $(id) {
  return document.getElementById(id);
}

async function getJson(path, options) {
  try {
    const res = await fetch(path, { cache: "no-store", ...options });
    return res.ok ? await res.json() : null;
  } catch {
    return null;
  }
}

function show(text, { apply = false, later = false } = {}) {
  banner.hidden = false;
  $("update-text").textContent = text;
  $("update-apply").hidden = !apply;
  $("update-later").hidden = !later;
}

async function applyUpdate() {
  $("update-apply").disabled = true;
  const started = await getJson("/__update/apply", { method: "POST", headers: { "X-Teacher-Update": "1" } });
  if (!started?.ok) {
    $("update-apply").disabled = false;
    return show(t("update.failed", { why: "?" }), { apply: true, later: true });
  }
  for (;;) {
    await new Promise((resolve) => setTimeout(resolve, 700));
    const status = await getJson("/__update/status");
    if (!status?.ok) continue;
    if (status.state === "running") show(t("update.running", { done: status.done, total: status.total }));
    else if (status.state === "done") {
      show(t("update.done"));
      return setTimeout(() => location.reload(), 1200);
    } else if (status.state === "error") {
      $("update-apply").disabled = false;
      return show(t("update.failed", { why: status.message || "?" }), { apply: true, later: true });
    }
  }
}

export async function checkForUpdate() {
  const answer = await getJson("/__update/check");
  if (!answer?.ok) return null; // no launcher, no internet, or the website is unreachable: stay quiet
  if (answer.update) {
    show(t("update.available", { files: answer.files, mb: Math.max(1, Math.round(answer.bytes / 1048576)) }), { apply: true, later: true });
  }
  return answer;
}

export function initUpdateNotice() {
  banner = $("update-banner");
  if (!banner) return;
  $("update-apply").addEventListener("click", applyUpdate);
  $("update-later").addEventListener("click", () => (banner.hidden = true));
  setTimeout(checkForUpdate, 4000);
  setInterval(checkForUpdate, CHECK_EVERY_MS);
  window.addEventListener("online", () => setTimeout(checkForUpdate, 2000));
}
