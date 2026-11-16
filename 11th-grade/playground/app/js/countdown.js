/**
 * Remaining time to a deadline, for the problem view and the problem list.
 *
 * The time comes from the server's clock: every answer that carries `serverTime` sets an offset
 * from this computer's clock, so a wrong clock on the student's computer does not mislead. The
 * offset is kept, so the offline copy can still count down between syncs. The server alone
 * decides what counts; this is only for showing the time left.
 */

import { define, isEnglish, t } from "./i18n.js?v=5";

define({
  "cd.late": { fa: "مهلت گذشته", en: "Deadline passed" },
  "cd.short.late": { fa: "گذشته", en: "passed" },
  "cd.days_clock": { fa: "{d} روز و {clock}", en: "{d} d {clock}" },
  "cd.day": { fa: "{n} روز", en: "{n} d" },
  "cd.hour": { fa: "{n} ساعت", en: "{n} h" },
  "cd.minute": { fa: "{n} دقیقه", en: "{n} min" },
});

const FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const OFFSET_KEY = "teacher-clock-offset-v1";

/** Digits in the chosen language: Persian digits in Persian, plain digits in English. */
export const fa = (value) => (isEnglish() ? String(value) : String(value).replace(/\d/g, (d) => FA_DIGITS[d]));

let offset = 0;
try {
  offset = Number(localStorage.getItem(OFFSET_KEY)) || 0;
} catch {
  offset = 0;
}

/** Remembers how far the server's clock is from this computer's. */
export function setServerTime(iso) {
  const server = Date.parse(iso);
  if (Number.isNaN(server)) return;
  offset = server - Date.now();
  try {
    localStorage.setItem(OFFSET_KEY, String(offset));
  } catch {
    /* the offset still works for this visit */
  }
}

export const nowMs = () => Date.now() + offset;

/** Milliseconds left until the ISO time `until` (negative once it has passed). */
export const remainingMs = (until) => Date.parse(until) - nowMs();

const pad = (n) => String(n).padStart(2, "0");

/** Exact: "۱ روز و ۰۳:۲۴:۱۰", or "۰۳:۲۴:۱۰" under a day; "مهلت گذشته" after the deadline. */
export function longText(ms) {
  if (ms <= 0) return t("cd.late");
  const total = Math.floor(ms / 1000);
  const days = Math.floor(total / 86400);
  const clock = `${pad(Math.floor((total % 86400) / 3600))}:${pad(Math.floor((total % 3600) / 60))}:${pad(total % 60)}`;
  return fa(days ? t("cd.days_clock", { d: days, clock }) : clock);
}

/** Compact, for the list: "۲ روز", "۵ ساعت", "۱۲ دقیقه"; "گذشته" after the deadline. */
export function shortText(ms) {
  if (ms <= 0) return t("cd.short.late");
  const minutes = Math.floor(ms / 60000);
  if (minutes >= 1440) return t("cd.day", { n: fa(Math.floor(minutes / 1440)) });
  if (minutes >= 60) return t("cd.hour", { n: fa(Math.floor(minutes / 60)) });
  return t("cd.minute", { n: fa(Math.max(1, minutes)) });
}

/** How urgent: late (passed), urgent (under 3 hours), soon (under a day), ok. */
export function level(ms) {
  if (ms <= 0) return "late";
  if (ms < 3 * 3600 * 1000) return "urgent";
  if (ms < 24 * 3600 * 1000) return "soon";
  return "ok";
}
