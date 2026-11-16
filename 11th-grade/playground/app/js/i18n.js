/**
 * Texts in both languages. The language is the one chosen on the lesson site (same storage key);
 * Persian is the default. New texts are defined here with `define`, and read with `t(key, params)`.
 */
const KEY = "grade11-lang-v2";
const DICT = {};

export function lang() {
  try {
    return localStorage.getItem(KEY) === "en" ? "en" : "fa";
  } catch {
    return "fa";
  }
}

export function define(entries) {
  Object.assign(DICT, entries);
}

/** A text by key, with {name} placeholders filled from `params`. Falls back to Persian, then the key. */
export function t(key, params = {}) {
  const entry = DICT[key];
  const text = (entry && (entry[lang()] || entry.fa)) || key;
  return text.replace(/\{(\w+)\}/g, (match, name) => (params[name] ?? match));
}
