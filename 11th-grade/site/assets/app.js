(function () {
  var KEY = "grade11-lang";

  function current() {
    try {
      return localStorage.getItem(KEY) === "en" ? "en" : "fa";
    } catch (e) {
      return "fa";
    }
  }

  function apply(lang) {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "fa" ? "rtl" : "ltr";
    var nodes = document.querySelectorAll("[data-fa][data-en]");
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].textContent = nodes[i].getAttribute("data-" + lang);
    }
    var fields = document.querySelectorAll("[data-fa-placeholder]");
    for (var j = 0; j < fields.length; j++) {
      fields[j].placeholder = fields[j].getAttribute("data-" + lang + "-placeholder");
    }
    var blocks = document.querySelectorAll("[data-lang-block]");
    for (var k = 0; k < blocks.length; k++) {
      blocks[k].hidden = blocks[k].getAttribute("data-lang-block") !== lang;
    }
    var buttons = document.querySelectorAll("[data-set-lang]");
    for (var b = 0; b < buttons.length; b++) {
      buttons[b].setAttribute("aria-pressed", buttons[b].getAttribute("data-set-lang") === lang ? "true" : "false");
    }
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }

  document.addEventListener("click", function (event) {
    var btn = event.target.closest ? event.target.closest("[data-set-lang]") : null;
    if (btn) apply(btn.getAttribute("data-set-lang"));
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
      for (var i = 0; i < rows.length && hits.length < 10; i++) {
        var row = rows[i];
        var hay = (row.titleFa + "\n" + row.titleEn + "\n" + row.text).toLowerCase();
        var at = hay.indexOf(needle);
        if (at < 0) continue;
        var from = Math.max(0, at - 40);
        var excerpt = row.text.slice(from, from + 110).replace(/\s+/g, " ");
        hits.push({ row: row, excerpt: excerpt });
      }
      if (!hits.length) {
        box.hidden = false;
        var empty = document.createElement("div");
        empty.style.padding = "0.5rem 0.7rem";
        empty.textContent = lang === "en" ? "No matches" : "چیزی پیدا نشد";
        box.appendChild(empty);
        return;
      }
      for (var h = 0; h < hits.length; h++) {
        var a = document.createElement("a");
        var root = document.body.getAttribute("data-root") || "";
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
