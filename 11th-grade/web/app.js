(function () {
  var KEY = "grade11-lang";

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

  // Narrow window (any pointer): the sidebar collapses into the hamburger.
  // Display scaling or zoom can make a PC's CSS width narrow; there the
  // hamburger is the visible replacement, so the spot is never empty.
  var toc = document.querySelector("details.toc");
  var lessonNav = document.getElementById("lesson-nav");
  var navBackdrop = document.getElementById("nav-backdrop");
  var phone = window.matchMedia("(max-width: 699px)");

  function placeNav() {
    var header = document.querySelector(".top");
    if (header) {
      document.documentElement.style.setProperty("--header-h", header.offsetHeight + "px");
    }
  }

  function syncNav() {
    if (toc && !phone.matches) toc.open = true;
    var show = !!(toc && toc.open && phone.matches);
    document.body.classList.toggle("nav-open", show);
    if (navBackdrop) navBackdrop.hidden = !show;
    if (show) placeNav();
  }

  if (toc && phone.matches) toc.open = false;
  syncNav();
  if (toc) toc.addEventListener("toggle", syncNav);
  if (phone.addEventListener) phone.addEventListener("change", syncNav);
  if (navBackdrop) {
    navBackdrop.addEventListener("click", function () {
      if (toc) toc.open = false;
    });
  }
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
      if (phone.matches && link && toc) {
        toc.open = false;
      }
    });
  }
  window.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toc && phone.matches) toc.open = false;
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

  document.addEventListener("click", function (event) {
    var box = document.getElementById("results");
    var input = document.getElementById("q");
    if (box && input && !event.target.closest(".search-wrap")) box.hidden = true;
  });

  var input = document.getElementById("q");
  var box = document.getElementById("results");
  if (input && box) {
    input.addEventListener("input", function () {
      var q = input.value.trim();
      box.innerHTML = "";
      if (q.length < 2 || !window.BOOK_SEARCH) {
        box.hidden = true;
        return;
      }
      var lang = current();
      var needle = q.toLowerCase();
      var hits = [];
      var rows = window.BOOK_SEARCH;
      for (var i = 0; i < rows.length && hits.length < 8; i++) {
        var row = rows[i];
        var faAt = (row.titleFa + "\n" + row.textFa).toLowerCase().indexOf(needle);
        var enAt = (row.titleEn + "\n" + row.textEn).toLowerCase().indexOf(needle);
        if (faAt < 0 && enAt < 0) continue;
        var useEn = lang === "en" ? enAt >= 0 : faAt < 0;
        var source = useEn ? row.textEn : row.textFa;
        var at = useEn ? enAt : faAt;
        if (at < 0) at = 0;
        var from = Math.max(0, at - 40);
        var excerpt = source.slice(from, from + 110).replace(/\s+/g, " ");
        hits.push({ row: row, excerpt: excerpt, useEn: useEn });
      }
      if (!hits.length) {
        box.hidden = false;
        var empty = document.createElement("div");
        empty.style.padding = "0.5rem 0.7rem";
        empty.textContent = lang === "en" ? "No matches" : "چیزی پیدا نشد";
        box.appendChild(empty);
        return;
      }
      var root = document.body.getAttribute("data-root") || "";
      for (var h = 0; h < hits.length; h++) {
        var a = document.createElement("a");
        a.href = root + hits[h].row.href;
        var title = document.createElement("strong");
        title.textContent = lang === "en" ? hits[h].row.titleEn : hits[h].row.titleFa;
        var snip = document.createElement("span");
        snip.textContent = hits[h].excerpt;
        a.appendChild(title);
        a.appendChild(snip);
        box.appendChild(a);
      }
      box.hidden = false;
    });
  }

  apply(current());
})();
