(function () {
  var KEY = "grade11-lang-v2"; // Persian is the default; the key changed so earlier English choices do not override it

  function current() {
    try {
      return localStorage.getItem(KEY) === "en" ? "en" : "fa";
    } catch (e) {
      return "fa";
    }
  }

  function apply(next) {
    lang = next;
    document.documentElement.lang = next;
    document.documentElement.dir = next === "fa" ? "rtl" : "ltr";
    var nodes = document.querySelectorAll("[data-fa][data-en]");
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].textContent = nodes[i].getAttribute("data-" + next);
    }
    var fields = document.querySelectorAll("[data-fa-placeholder]");
    for (var j = 0; j < fields.length; j++) {
      fields[j].placeholder = fields[j].getAttribute("data-" + next + "-placeholder");
    }
    var labelled = document.querySelectorAll("[data-fa-aria]");
    for (var a = 0; a < labelled.length; a++) {
      labelled[a].setAttribute("aria-label", labelled[a].getAttribute("data-" + next + "-aria"));
    }
    var blocks = document.querySelectorAll("[data-lang-block]");
    for (var k = 0; k < blocks.length; k++) {
      blocks[k].hidden = blocks[k].getAttribute("data-lang-block") !== next;
    }
    var toggle = document.getElementById("lang-toggle");
    if (toggle) toggle.setAttribute("data-lang", next);
    var title = document.querySelector("title");
    if (title && title.getAttribute("data-fa")) {
      title.textContent = title.getAttribute("data-" + next);
    }
    try { localStorage.setItem(KEY, next); } catch (e) {}
  }

  // Up to 980px wide, the lesson list is a bar above the lesson: it starts
  // closed and the bar opens it. Wider, the list is always beside the lesson.
  var toc = document.querySelector("details.toc");
  var lessonNav = document.getElementById("lesson-nav");
  var narrow = window.matchMedia("(max-width: 980px)");

  function syncNav() {
    if (toc && !narrow.matches) toc.open = true;
  }

  if (toc && narrow.matches) toc.open = false;
  syncNav();
  if (narrow.addEventListener) narrow.addEventListener("change", syncNav);
  // Keep the lesson list scrolled where the reader left it across full
  // page loads. Without this, every click jumps the sidebar back to top.
  var SIDE_SCROLL_KEY = "grade11-side-scroll";
  var side = lessonNav || document.querySelector(".side");

  function saveSideScroll() {
    if (!side) return;
    try {
      sessionStorage.setItem(SIDE_SCROLL_KEY, String(side.scrollTop));
    } catch (e) {}
  }

  function restoreSideScroll() {
    if (!side) return;
    var raw = null;
    try {
      raw = sessionStorage.getItem(SIDE_SCROLL_KEY);
    } catch (e) {}
    if (raw == null || raw === "") return;
    var top = parseInt(raw, 10);
    if (isNaN(top)) return;
    side.scrollTop = top;
  }

  if (side) {
    side.addEventListener("scroll", function () {
      saveSideScroll();
    }, { passive: true });
    // Restore after layout; a second pass catches late font/sticky height.
    restoreSideScroll();
    requestAnimationFrame(restoreSideScroll);
    window.addEventListener("load", restoreSideScroll);
  }

  if (lessonNav) {
    lessonNav.addEventListener("click", function (event) {
      var link = event.target.closest && event.target.closest("a");
      if (link) saveSideScroll();
      if (narrow.matches && link && toc) {
        toc.open = false;
      }
    });
  }
  window.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toc && narrow.matches) toc.open = false;
  });

  var lang = current();
  var toggle = document.getElementById("lang-toggle");
  if (toggle) {
    toggle.addEventListener("click", function (event) {
      event.preventDefault();
      lang = lang === "fa" ? "en" : "fa";
      apply(lang);
    });
  }

  apply(current());
})();
