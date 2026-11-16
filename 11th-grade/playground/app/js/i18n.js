/**
 * Two languages. The choice is shared with the lesson site (same storage key); Persian is the default.
 *
 * Static texts in the page carry both languages: data-fa / data-en (text), data-fa-placeholder /
 * data-en-placeholder, data-fa-title / data-en-title (tooltips), data-fa-aria / data-en-aria. Texts built
 * by scripts are defined with `define` and read with `t(key, params)`. `onLangChange` lets a module
 * draw its parts again when the language is switched.
 */
const KEY = "grade11-lang-v2";
const DICT = {};
const listeners = new Set();

function stored() {
  try {
    return localStorage.getItem(KEY) === "en" ? "en" : "fa";
  } catch {
    return "fa";
  }
}

let current = stored();

export const lang = () => current;
export const has = (key) => key in DICT;
export const isEnglish = () => current === "en";

export function define(entries) {
  Object.assign(DICT, entries);
}

/** A text by key, with {name} placeholders filled from `params`. Falls back to Persian, then the key. */
export function t(key, params = {}) {
  const entry = DICT[key];
  const text = (entry && (entry[current] || entry.fa)) || key;
  return text.replace(/\{(\w+)\}/g, (match, name) => (params[name] ?? match));
}

/** Both languages for one text, when a script needs to choose between two ready strings. */
export const pick = (fa, en) => (current === "en" ? en || fa : fa);

export function onLangChange(fn) {
  listeners.add(fn);
}

/** Puts the current language on the page: direction, static texts, placeholders, tooltips. */
export function applyStatic(root = document) {
  const html = document.documentElement;
  html.lang = current;
  html.dir = current === "fa" ? "rtl" : "ltr";
  for (const node of root.querySelectorAll("[data-fa][data-en]")) node.textContent = node.getAttribute(`data-${current}`);
  for (const attr of ["placeholder", "title", "aria-label"]) {
    const name = attr === "aria-label" ? "aria" : attr;
    for (const node of root.querySelectorAll(`[data-fa-${name}]`)) node.setAttribute(attr, node.getAttribute(`data-${current}-${name}`) ?? "");
  }
  for (const node of root.querySelectorAll("[data-lang-block]")) node.hidden = node.getAttribute("data-lang-block") !== current;
  for (const toggle of document.querySelectorAll("#lang-toggle, [data-lang-toggle]")) toggle.setAttribute("data-lang", current);
  const title = document.querySelector("title");
  if (title?.getAttribute("data-fa")) title.textContent = title.getAttribute(`data-${current}`);
}

export function setLang(next) {
  current = next === "en" ? "en" : "fa";
  try {
    localStorage.setItem(KEY, current);
  } catch {
    /* the choice lasts for this visit */
  }
  applyStatic();
  for (const fn of listeners) {
    try {
      fn(current);
    } catch {
      /* one listener must not stop the others */
    }
  }
}

/** Applies the stored language and wires the switch in the header. Call once at start-up. */
export function initLang() {
  applyStatic();
  // The header's switch, and the one inside the sign-in window (a modal window covers the header).
  for (const toggle of document.querySelectorAll("#lang-toggle, [data-lang-toggle]")) {
    toggle.addEventListener("click", () => setLang(current === "fa" ? "en" : "fa"));
  }
}
