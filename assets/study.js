// Study page helpers: copy buttons for prompts, "mark as read" shared with the tracker.
(function () {
  var KEY = "career-tracker-v1";
  try { var _s = JSON.parse(localStorage.getItem(KEY) || "{}"); if (_s.theme === "sepia") document.documentElement.setAttribute("data-theme", "sepia"); if (_s.fontScale) document.documentElement.style.setProperty("--fs", String(_s.fontScale)); } catch (e) {}
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }

  document.addEventListener("click", function (e) {
    var b = e.target.closest(".prompt .copy");
    if (b) {
      var txt = b.closest(".prompt").querySelector("pre").textContent;
      var done = function () { var o = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = o; }, 1400); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, done);
      else { var t = document.createElement("textarea"); t.value = txt; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); done(); }
      return;
    }
    var r = e.target.closest("[data-read]");
    if (r) {
      var s = load(); s.done = s.done || {};
      var id = r.getAttribute("data-read");
      if (s.done[id]) delete s.done[id]; else s.done[id] = true;
      save(s); paint();
    }
  });

  function paint() {
    var s = load(); var d = s.done || {};
    document.querySelectorAll("[data-read]").forEach(function (b) {
      var on = !!d[b.getAttribute("data-read")];
      b.classList.toggle("done", on);
      b.textContent = on ? "✓ Chapter marked as read (click to undo)" : "Mark this chapter as read";
    });
    document.querySelectorAll("[data-tile]").forEach(function (a) {
      var on = !!d[a.getAttribute("data-tile")];
      var m = a.querySelector("i"); if (m) m.textContent = on ? " ✓" : "";
    });
    var pr = document.getElementById("readprog");
    if (pr) {
      var ids = JSON.parse(pr.getAttribute("data-ids")); var n = ids.filter(function (i) { return d[i]; }).length;
      pr.textContent = n + " of " + ids.length + " chapters read";
    }
  }
  paint();
})();

// Compact site search in the topbar: loads assets/search-index.js lazily on first focus.
(function () {
  var bar = document.querySelector(".topbar .in");
  if (!bar) return;
  var sp = bar.querySelector(".sp");
  var wrap = document.createElement("div"); wrap.className = "ssearch";
  wrap.innerHTML = '<input type="search" placeholder="Search all docs ( / )" aria-label="Search all study documents" autocomplete="off"><div class="sdrop" hidden></div>';
  if (sp && sp.nextSibling) bar.insertBefore(wrap, sp.nextSibling); else bar.appendChild(wrap);
  var inp = wrap.querySelector("input"), drop = wrap.querySelector(".sdrop"), loading = false, timer = 0;
  var base = (function () { var s = document.querySelector('script[src*="study.js"]'); return s ? s.src.replace(/assets\/study\.js.*$/, "") : "../../"; })();
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function load(cb) {
    if (window.SEARCH_INDEX) return cb();
    if (loading) return; loading = true;
    var s = document.createElement("script"); s.src = base + "assets/search-index.js"; s.onload = function () { loading = false; cb(); };
    s.onerror = function () { loading = false; drop.hidden = false; drop.innerHTML = '<div class="snone">Search index not found.</div>'; };
    document.head.appendChild(s);
  }
  function toks(q) { return q.toLowerCase().split(/[^a-z0-9+#]+/).filter(Boolean).map(function (w) { return w.length > 4 && w.slice(-1) === "s" ? w.slice(0, -1) : w; }); }
  function run() {
    var q = inp.value.trim(); if (!q) { drop.hidden = true; return; }
    var T = toks(q), docs = {}, res = [];
    (window.SEARCH_DOCS || []).forEach(function (d) { docs[d.k] = d; });
    window.SEARCH_INDEX.forEach(function (r) {
      var h = r.h.toLowerCase(), b = r.s || (h + " " + (r.b || "").toLowerCase()), sc = 0;
      for (var i = 0; i < T.length; i++) {
        var inH = h.indexOf(T[i]) >= 0, inB = b.indexOf(T[i]) >= 0;
        if (!inH && !inB) return; sc += (inH ? 10 : 0) + (inB ? 2 : 0);
      }
      if (h.indexOf(T.join(" ")) >= 0) sc += 40;
      res.push([sc, r]);
    });
    res.sort(function (a, b) { return b[0] - a[0]; });
    drop.hidden = false;
    drop.innerHTML = res.length ? res.slice(0, 8).map(function (x) {
      var r = x[1], d = docs[r.k] || { i: "", d: r.k };
      return '<a href="' + base + esc(r.u) + '"><b>' + esc(r.h.slice(0, 90)) + '</b><small>' + d.i + " " + esc(d.d) + (r.c ? " · " + esc(r.c) : "") + "</small></a>";
    }).join("") + '<a class="sall" href="' + base + 'index.html">Open the full search on the home page</a>' : '<div class="snone">No results</div>';
  }
  inp.addEventListener("focus", function () { load(run); });
  inp.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(function () { load(run); }, 120); });
  document.addEventListener("keydown", function (e) {
    var typing = /INPUT|TEXTAREA|SELECT/.test(e.target.tagName || "");
    if ((e.key === "/" && !typing && !e.metaKey && !e.ctrlKey) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k")) { e.preventDefault(); inp.focus(); inp.select(); }
    else if (e.key === "Escape" && document.activeElement === inp) { inp.blur(); drop.hidden = true; }
    else if (e.key === "Enter" && document.activeElement === inp) { var a = drop.querySelector("a"); if (a) location.href = a.href; }
  });
  document.addEventListener("click", function (e) { if (!wrap.contains(e.target)) drop.hidden = true; });
})();
