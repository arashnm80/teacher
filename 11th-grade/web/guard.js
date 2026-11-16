/*
 * Keeps the lesson texts, the guides and the AI answers from being copied, and stops text being
 * pasted or dropped into the code editor, so that students type the code themselves.
 *
 * This is a deterrent, not a lock. A page cannot stop someone who reads its source, takes a
 * screenshot or saves the files. It stops the everyday ways of copying text from a page.
 */
(function () {
  "use strict";

  function inEditor(node) {
    var el = node && node.nodeType === 1 ? node : node && node.parentElement;
    return !!(el && el.closest && el.closest(".CodeMirror"));
  }

  // Native form fields keep their own copy and paste (the search box, the API key).
  function ownField() {
    var a = document.activeElement;
    return !!a && (a.tagName === "INPUT" || (a.tagName === "TEXTAREA" && !inEditor(a)));
  }

  function stop(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Copy and cut: nothing reaches the clipboard. This covers Ctrl+C, the menu and long-press.
  document.addEventListener("copy", function (e) { if (!ownField()) stop(e); }, true);
  document.addEventListener("cut", function (e) { if (!ownField()) stop(e); }, true);

  // Dragging selected text out of the page.
  document.addEventListener("dragstart", function (e) { if (!ownField()) stop(e); }, true);

  // Pasting or dropping text into the code editor.
  document.addEventListener("paste", function (e) { if (inEditor(e.target)) stop(e); }, true);
  document.addEventListener("drop", function (e) { if (inEditor(e.target)) stop(e); }, true);
  document.addEventListener("beforeinput", function (e) {
    if (inEditor(e.target) && /^insertFrom(Paste|Drop)/.test(e.inputType || "")) e.preventDefault();
  }, true);
})();
