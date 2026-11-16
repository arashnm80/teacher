/* Search for every page: the header box, the index in window.BOOK_SEARCH. */
(function () {
  var input = document.getElementById("q");
  var box = document.getElementById("search-results");
  if (!input || !box) return;
  var root = document.body.getAttribute("data-root") || "";

  function currentLang() {
    return document.documentElement.lang === "en" ? "en" : "fa";
  }

  input.addEventListener("input", function () {
    var q = input.value.trim();
    box.innerHTML = "";
    if (q.length < 2 || !window.BOOK_SEARCH) {
      box.hidden = true;
      return;
    }
    var lang = currentLang();
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
    box.hidden = false;
    if (!hits.length) {
      var empty = document.createElement("div");
      empty.className = "search-empty";
      empty.textContent = lang === "en" ? "No matches" : "چیزی پیدا نشد";
      box.appendChild(empty);
      return;
    }
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
  });

  document.addEventListener("click", function (event) {
    if (!event.target.closest(".search-wrap")) box.hidden = true;
  });
})();
