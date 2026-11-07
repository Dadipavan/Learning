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
