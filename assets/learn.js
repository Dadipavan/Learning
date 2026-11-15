/* Career Journey: Review (spaced repetition), Quiz and Datasets pages.
   Loaded with a plain <script> BEFORE the main inline script in index.html, so these page functions exist when the app first renders.
   Everything is inside one function scope. It uses the app's globals (S, D, R, PLAN, esc, fmt, pct, pbar, callout, today, save, toast,
   rerender, streak, currentWeekIdx, currentLessonIdx, LESSONS) only when a function is CALLED, never while this file loads.

   State added to the app's localStorage object S (all created lazily, old exports without these fields import fine):
     S.sr      = { cards:{<id>:{ease,interval,due,reps,lapses,last,lrn,k[,src,q,a,opts,ch]}}, days:{<iso date>:{n,ok,nw}}, newPerDay:10, enabled:{<key>:true|false} }
     S.quizlog = [{date,key,score,total,missed:[ids]}]            (last 200)
     S.mastery = { <doc key>:{seen,correct,recent:"1101..."} }     (recent = last 30 answers, newest last)
   Data files (built by the lead): assets/decks/index.js, assets/decks/<key>.js, assets/data-catalog.js (all loaded lazily). */
(function () {
  "use strict";
  const DAY = 86400000, MIN = 60000, LEARN_MIN = 10, AHEAD = 20 * MIN, MATURE = 21;
  const LET = ["A", "B", "C", "D", "E", "F"];
  const SITE = "https://dadipavan.github.io/Learning/";

  /* ---------- helpers ---------- */
  const now = () => Date.now();
  const dayStart = (t, plus = 0) => { const d = new Date(t); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + plus); return d.getTime(); };
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const own = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
  const safe = (name, fn) => function () {
    try { return fn.apply(null, arguments); }
    catch (e) { console.error(name, e); return `<div class="card">Something went wrong on this page (${esc((e && e.message) || e)}). Try reloading the site.</div>`; }
  };
  const noDecks = () => callout("NO FLASHCARD DECKS YET", "The flashcard decks are not on this site yet. Build them with <code>python3 tools/build_decks.py</code>, upload the <code>assets/decks</code> folder and reload this page.", "cream");

  /* ---------- state (created lazily) ---------- */
  function sr() {
    let s = S.sr;
    if (!s || typeof s !== "object" || Array.isArray(s)) s = S.sr = {};
    if (!s.cards || typeof s.cards !== "object") s.cards = {};
    if (!s.days || typeof s.days !== "object") s.days = {};
    if (!s.enabled || typeof s.enabled !== "object") s.enabled = {};
    if (typeof s.newPerDay !== "number" || !(s.newPerDay >= 0)) s.newPerDay = 10;
    return s;
  }
  const qlog = () => Array.isArray(S.quizlog) ? S.quizlog : (S.quizlog = []);
  const mast = () => (S.mastery && typeof S.mastery === "object" && !Array.isArray(S.mastery)) ? S.mastery : (S.mastery = {});
  const dayGet = () => sr().days[today()] || { n: 0, ok: 0, nw: 0 };
  /* called after an import or a reset: repairs the saved shapes and forgets any half-finished session */
  window.learnFix = function () { sr(); qlog(); mast(); if (S.quizlog.length > 200) S.quizlog = S.quizlog.slice(-200); view.mode = "home"; view.cur = null; view.shown = false; view.undo = []; sess = { n: 0, ok: 0 }; qz.mode = "menu"; };

  /* ---------- documents ---------- */
  function docInfo(key) { return D.study.find(d => d.key === key) || { key, label: key, icon: "📘", chapters: [] }; }
  const docLabel = key => docInfo(key).label || key;
  const docName = key => { const d = docInfo(key); return (d.icon ? d.icon + " " : "") + (d.label || key); };
  const readDoc = key => (docInfo(key).chapters || []).some(c => S.done[c.readid]);
  function chLink(k, ch) {
    const c = (docInfo(k).chapters || []).find(x => x.page === ch + ".html");
    return `<a href="study/${esc(k)}/${esc(ch)}.html" target="_blank" rel="noopener">📖 ${c ? "Chapter " + c.num + ": " + esc(c.title) : esc(ch)} ↗</a>`;
  }
  /* A document is switched on by default when you have marked a chapter as read or it is in this week's plan; you can override it. */
  function isOn(key) {
    const e = sr().enabled;
    if (own(e, key)) return !!e[key];
    if (readDoc(key)) return true;
    const w = PLAN[currentWeekIdx()];
    return !!(w && w.tasks.some(t => t.href && t.href.indexOf("study/" + key + "/") === 0));
  }

  /* ---------- lazy loading of decks and the catalog (script injection, works from file://) ---------- */
  let idx = null, idxSt = "idle", catSt = "idle", bumpT = 0;
  const deckSt = {}, CARD = {}, QUIZ = {};
  const bump = () => { clearTimeout(bumpT); bumpT = setTimeout(() => { if (["review", "quiz", "home", "data"].indexOf(R.page) >= 0) rerender(); }, 40); };
  function loadJs(src, done) { const s = document.createElement("script"); s.src = src; s.async = true; s.onload = () => done(true); s.onerror = () => { s.remove(); done(false); }; document.head.appendChild(s); }
  function ensureIndex() {
    if (idxSt !== "idle") return;
    idxSt = "loading";
    loadJs("assets/decks/index.js", ok => { idx = ok && Array.isArray(window.DECK_INDEX) ? window.DECK_INDEX : []; idxSt = idx.length ? "ok" : "missing"; bump(); });
  }
  function ensureDeck(key) {
    if (deckSt[key]) return;
    deckSt[key] = "loading";
    loadJs("assets/decks/" + encodeURIComponent(key) + ".js", ok => {
      const d = window.DECKS && window.DECKS[key];
      deckSt[key] = ok && d ? "ok" : "missing";
      if (deckSt[key] === "ok") { (d.cards || []).forEach(c => { CARD[c.id] = Object.assign({ k: key }, c); }); (d.quiz || []).forEach(q => { QUIZ[q.id] = Object.assign({ k: key }, q); }); }
      bump();
    });
  }
  const deck = key => (window.DECKS && window.DECKS[key]) || null;
  function wantDecks() { ensureIndex(); if (idxSt === "ok") idx.forEach(x => { if (isOn(x.key)) ensureDeck(x.key); }); }
  const loadingDecks = () => (idx || []).filter(x => isOn(x.key) && deckSt[x.key] === "loading").length;
  function loadCatalog() {
    if (catSt !== "idle") return;
    if (Array.isArray(window.DATA_CATALOG)) { catSt = "ok"; return; }
    catSt = "loading";
    loadJs("assets/data-catalog.js", ok => { catSt = ok && Array.isArray(window.DATA_CATALOG) && window.DATA_CATALOG.length ? "ok" : "missing"; bump(); });
  }

  /* ---------- the scheduler ----------
     SM-2 style, close to Anki's defaults. Grades: 0 Again, 1 Hard, 2 Good, 3 Easy.
     Card record: ease (starts 2.5, never below 1.3), interval (days; 0 = learning), due (ms timestamp), reps (times remembered),
     lapses (times forgotten after learning), last (ms of the last review), lrn (1 = failed recently), k (document key).
     Learning (a new card, or a card you forgot):  Again = again in 10 minutes;  Hard = tomorrow;  Good = in 3 days (2 if you failed it before);
       Easy = in 7 days (4 if you failed it before).
     Review (interval >= 1 day):  Again = forgotten: ease -0.2, back to learning (10 minutes);  Hard = interval x1.2 (ease -0.15);
       Good = interval x ease, plus half of the days you were late;  Easy = interval x ease x1.3 (ease +0.15).
       Whole days only, each grade at least 1 day longer than the one before it, capped at one year.
     A card whose interval is in days is due at the START of that day, so it is available all day (no waiting for the clock time).
     Cards still in learning that are due within 20 minutes are shown at the end of a session instead of making you wait. */
  function nextState(r, g, t) {
    const ease = r.ease || 2.5, iv = r.interval || 0, lrn = r.lrn || 0;
    if (!iv) {
      if (g === 0) return { interval: 0, ease, lrn: 1, due: t + LEARN_MIN * MIN, mins: LEARN_MIN, lapse: false };
      const days = (lrn ? [0, 1, 2, 4] : [0, 1, 3, 7])[g];
      return { interval: days, ease, lrn: 0, due: dayStart(t, days), mins: 0, lapse: false };
    }
    if (g === 0) return { interval: 0, ease: Math.max(1.3, ease - 0.2), lrn: 1, due: t + LEARN_MIN * MIN, mins: LEARN_MIN, lapse: true };
    const late = Math.max(0, Math.floor((t - (r.due || t)) / DAY));
    const hard = Math.max(iv + 1, Math.round(iv * 1.2));
    const good = Math.max(hard + 1, Math.round((iv + late / 2) * ease));
    const easy = Math.max(good + 1, Math.round((iv + late) * ease * 1.3));
    const days = Math.min(365, [0, hard, good, easy][g]);
    const e2 = g === 1 ? Math.max(1.3, ease - 0.15) : g === 3 ? ease + 0.15 : ease;
    return { interval: days, ease: e2, lrn: 0, due: dayStart(t, days), mins: 0, lapse: false };
  }
  function applyGrade(r, g, t) {
    const n = nextState(r, g, t);
    r.ease = Math.round(n.ease * 100) / 100; r.interval = n.interval; r.due = n.due; r.lrn = n.lrn;
    if (g > 0) r.reps = (r.reps || 0) + 1;
    if (n.lapse) r.lapses = (r.lapses || 0) + 1;
    r.last = t;
  }
  function ivLabel(n) {
    if (!n.interval) return n.mins >= 60 ? Math.round(n.mins / 60) + "h" : n.mins + "m";
    const d = n.interval;
    return d < 30 ? d + "d" : d < 365 ? (Math.round(d / 30 * 10) / 10) + "mo" : (Math.round(d / 365 * 10) / 10) + "y";
  }

  /* ---------- queues ---------- */
  function content(id) {
    const r = sr().cards[id];
    if (r && r.src === "quiz") return { id, k: r.k, q: r.q, a: r.a, ch: r.ch, opts: r.opts, tag: "missed in a quiz" };
    return CARD[id] || null;
  }
  const live = r => r.src === "quiz" || isOn(r.k);
  function dueIds(t) {
    const c = sr().cards, out = [];
    Object.keys(c).forEach(id => { const r = c[id]; if (r.due <= t && live(r) && content(id)) out.push(id); });
    return out.sort((a, b) => c[a].due - c[b].due);
  }
  function aheadIds(t) {
    const c = sr().cards, out = [];
    Object.keys(c).forEach(id => { const r = c[id]; if (!r.interval && r.due > t && r.due <= t + AHEAD && live(r) && content(id)) out.push(id); });
    return out.sort((a, b) => c[a].due - c[b].due);
  }
  /* New cards: one pool per switched-on document (cards not started yet). Inside a pool, cards from chapters you marked as read come
     first, then the deck order. Cards are interleaved by document: the next new card always comes from the document that has had the
     fewest new cards started today (ties: list order). At most newPerDay new cards are started per day. */
  function newPools() {
    const s = sr(), pools = [];
    if (!idx) return pools;
    idx.forEach(x => {
      const d = isOn(x.key) && deck(x.key); if (!d) return;
      const l = (d.cards || []).map((c, i) => [S.done["study:" + x.key + ":" + c.ch] ? 0 : 1, i, CARD[c.id]]).filter(a => a[2] && !s.cards[a[2].id]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).map(a => a[2]);
      if (l.length) pools.push({ key: x.key, cards: l });
    });
    return pools;
  }
  const newLeft = () => Math.max(0, sr().newPerDay - (dayGet().nw || 0));
  const newAvail = () => Math.min(newLeft(), newPools().reduce((a, p) => a + p.cards.length, 0));
  function nextNew() {
    if (!newLeft()) return null;
    const nk = dayGet().nk || {};
    let best = null;
    newPools().forEach(p => { const c = nk[p.key] || 0; if (!best || c < best.c) best = { c, card: p.cards[0] }; });
    return best && best.card;
  }
  function nextItem() {
    const t = now(), d = dueIds(t);
    if (d.length) return { id: d[0], kind: "due" };
    const n = nextNew();
    if (n) return { id: n.id, kind: "new" };
    const a = aheadIds(t);
    return a.length ? { id: a[0], kind: "due" } : null;
  }
  function stats() {
    const s = sr(), t = now(), agg = {}, tot = { learned: 0, mature: 0 };
    Object.keys(s.cards).forEach(id => {
      const r = s.cards[id], k = r.k || id.split("-")[0], a = agg[k] || (agg[k] = { seen: 0, due: 0, learned: 0, mature: 0 });
      if (r.src !== "quiz") a.seen++;
      if (r.interval >= 1) { a.learned++; tot.learned++; }
      if (r.interval >= MATURE) { a.mature++; tot.mature++; }
      if (r.due <= t && live(r)) a.due++;
    });
    return { agg, tot };
  }
  function nextDueText() {
    const s = sr(), t = now();
    let best = Infinity;
    Object.keys(s.cards).forEach(id => { const r = s.cards[id]; if (r.due > t && live(r) && r.due < best) best = r.due; });
    if (best === Infinity) return "";
    const d = best - t;
    if (best < dayStart(t, 1)) return d < 60 * MIN ? `in ${Math.max(1, Math.round(d / MIN))} min` : `in about ${Math.round(d / (60 * MIN))} h`;
    if (best < dayStart(t, 2)) return "tomorrow";
    return new Date(best).toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" });
  }
  const dueBetween = (a, b) => { const c = sr().cards; return Object.keys(c).filter(id => c[id].due >= a && c[id].due < b && live(c[id])).length; };

  /* ---------- Review page ---------- */
  const view = { mode: "home", cur: null, shown: false, undo: [], auto: false };
  let sess = { n: 0, ok: 0 };
  const validCur = c => !!(c && content(c.id) && (c.kind === "new" ? !sr().cards[c.id] : !!sr().cards[c.id]));
  function pickNext() { view.cur = nextItem(); view.shown = false; }
  function startSession() { view.mode = "study"; sess = { n: 0, ok: 0 }; view.undo = []; pickNext(); if (!view.cur) view.mode = "done"; }

  function grade(g) {
    const cur = view.cur;
    if (!cur || !view.shown) return;
    const s = sr(), id = cur.id, t = now(), info = content(id);
    if (!info) return;
    const isNew = !s.cards[id], old = isNew ? null : JSON.stringify(s.cards[id]);
    const r = s.cards[id] || { ease: 2.5, interval: 0, due: 0, reps: 0, lapses: 0, last: 0, lrn: 0, k: info.k };
    applyGrade(r, g, t); s.cards[id] = r;
    const key = today(), dd = s.days[key] || (s.days[key] = { n: 0, ok: 0, nw: 0 });
    const snap = { n: dd.n, ok: dd.ok, nw: dd.nw || 0, nk: dd.nk ? Object.assign({}, dd.nk) : null };
    dd.n++; if (g > 0) dd.ok++;
    if (isNew) { dd.nw = (dd.nw || 0) + 1; dd.nk = dd.nk || {}; dd.nk[info.k] = (dd.nk[info.k] || 0) + 1; }
    const hb = S.habits[key] || (S.habits[key] = {}), hadRev = !!hb.review;
    if (dd.n >= 5) hb.review = true;           /* a day counts for the streak after 5 reviewed cards */
    view.undo.push({ id, old, snap, key, hadRev, kind: cur.kind, g });
    if (view.undo.length > 30) view.undo.shift();
    sess.n++; if (g > 0) sess.ok++;
    pickNext(); if (!view.cur) view.mode = "done";
    save(); render(); window.scrollTo(0, 0);
  }
  function undo() {
    const u = view.undo.pop(); if (!u) return;
    const s = sr();
    if (u.old) s.cards[u.id] = JSON.parse(u.old); else delete s.cards[u.id];
    const dd = s.days[u.key];
    if (dd) { dd.n = u.snap.n; dd.ok = u.snap.ok; dd.nw = u.snap.nw; if (u.snap.nk) dd.nk = u.snap.nk; else delete dd.nk; }
    if (!u.hadRev && S.habits[u.key] && (!dd || dd.n < 5)) delete S.habits[u.key].review;
    sess.n = Math.max(0, sess.n - 1); if (u.g > 0) sess.ok = Math.max(0, sess.ok - 1);
    view.cur = { id: u.id, kind: u.kind }; view.shown = true; view.mode = "study";
    save(); rerender();
  }

  window.pageReview = safe("review", function () {
    wantDecks();
    const head = `<div class="phead"><div class="eyebrow">Spaced repetition</div><h1>Review</h1><p>Flashcards come back just before you forget them. Ten minutes a day is enough.</p></div>`;
    if (idxSt === "idle" || idxSt === "loading") return head + `<div class="empty">Loading your flashcards…</div>`;
    if (idxSt === "missing") return head + noDecks();
    if (view.auto && !loadingDecks()) { view.auto = false; startSession(); }
    if (view.mode === "study") { if (!validCur(view.cur)) pickNext(); if (!view.cur) view.mode = "done"; }
    if (view.mode === "study") return studyHtml();
    if (view.mode === "done") return doneHtml(head);
    return overviewHtml(head);
  });

  function studyHtml() {
    const cur = view.cur, c = content(cur.id), r = sr().cards[cur.id], t = now();
    const left = dueIds(t).length + newAvail() + aheadIds(t).length, total = sess.n + left;
    const st = r || { ease: 2.5, interval: 0, lrn: 0, due: t };
    const state = !r ? ["New", "warn"] : r.interval ? ["Review", ""] : ["Learning", "warn"];
    const names = ["Again", "Hard", "Good", "Easy"];
    const opts = c.opts ? `<ul class="rv-opts">${c.opts.map((o, i) => `<li><b>${LET[i]}</b>${fmt(o)}</li>`).join("")}</ul>` : "";
    const back = view.shown ? `<div class="rv-a">${fmt(c.a)}</div><div class="note">${chLink(c.k, c.ch)}</div>` : "";
    const act = view.shown
      ? `<div class="rv-grades" role="group" aria-label="How well did you remember?">${[0, 1, 2, 3].map(g => `<button class="rv-g g${g}" data-lx="grade" data-v="${g}" aria-label="${names[g]}, next review in ${ivLabel(nextState(st, g, t))}"><span>${names[g]}<span class="rv-key">${g + 1}</span></span><small>${ivLabel(nextState(st, g, t))}</small></button>`).join("")}</div>`
      : `<button class="btn bigbtn" data-lx="show">Show answer <span class="rv-key" style="color:#fff;border-color:#fff8;background:none">Space</span></button>`;
    return `<div class="rv-top"><div style="flex:1">${pbar(pct(sess.n, total))}<div class="pmeta"><span>${sess.n} done · ${left} left</span><span>${view.shown ? "How well did you remember?" : "Say the answer in your head first"}</span></div></div>
      <button class="btn ghost sm" data-lx="stop" aria-label="Finish this session">Finish</button></div>
      <div class="card rv-card" aria-live="polite"><div class="rv-meta"><span class="pill">${esc(docName(c.k))}</span><span class="pill ${state[1]}">${state[0]}</span>${c.tag ? `<span class="pill mut">${esc(c.tag)}</span>` : ""}</div>
      <div class="rv-q">${fmt(c.q)}</div>${opts}${back}</div>${act}
      <div class="row" style="margin-top:10px"><button class="btn ghost sm" data-lx="undo" ${view.undo.length ? "" : "disabled"} aria-label="Undo the last grade">↶ Undo <span class="rv-key">U</span></button></div>`;
  }

  function doneHtml(head) {
    const t = now(), acc = sess.n ? Math.round(100 * sess.ok / sess.n) : null, nd = nextDueText(), tom = dueBetween(dayStart(t, 1), dayStart(t, 2)), s = sr();
    const nl = Math.max(0, s.newPerDay - (dayGet().nw || 0));
    return `${head}<div class="card"><p class="label">${sess.n ? "Session complete" : "All done for now"}</p>
      <div class="rv-stats"><div class="card"><div class="n">${sess.n}</div><div class="l">cards this session</div></div>
      <div class="card"><div class="n">${acc === null ? "–" : acc + "%"}</div><div class="l">remembered (not Again)</div></div>
      <div class="card"><div class="n">${streak()} 🔥</div><div class="l">day streak</div></div>
      <div class="card"><div class="n">${dayGet().n}</div><div class="l">cards today in total</div></div></div>
      <p style="margin:6px 0">${nd ? `Next card is due <b>${esc(nd)}</b>.` : "No cards are waiting."}${tom ? ` About <b>${tom}</b> card${tom === 1 ? "" : "s"} will be due tomorrow.` : ""}</p>
      ${!nl && s.newPerDay ? `<p class="note">You have started all ${s.newPerDay} new cards allowed today. Change this in the document list below.</p>` : ""}
      <div class="row"><button class="btn" data-lx="home">Back to Review</button><a class="btn ghost" href="#/quiz">📝 Take a quiz</a><a class="btn ghost" href="#/today">▶ Today's lesson</a></div></div>`;
  }

  function overviewHtml(head) {
    const t = now(), st = stats(), due = dueIds(t).length, nl = newAvail(), s = sr(), day = dayGet(), load = loadingDecks();
    const total = due + nl;
    const msg = s.newPerDay === 0 ? "New cards are paused (0 per day)." : (day.nw || 0) >= s.newPerDay ? `You already started your ${s.newPerDay} new cards today.` : "No new cards: switch on a document below, or mark a chapter as read.";
    const nd = nextDueText();
    const go = total ? `<button class="btn bigbtn" data-lx="start">▶ Start review · ${due} due${nl ? ` + ${nl} new` : ""}</button>`
      : callout("NOTHING DUE", `${nd ? `The next card is due <b>${esc(nd)}</b>. ` : ""}${esc(msg)}`, "green");
    const rows = idx.map(x => {
      const a = st.agg[x.key] || { seen: 0, due: 0, learned: 0, mature: 0 }, on = isOn(x.key);
      return `<tr><td><input type="checkbox" class="chk" data-lx="tog" data-v="${esc(x.key)}" ${on ? "checked" : ""} aria-label="Use ${esc(docLabel(x.key))} in my reviews"></td><td>${esc(docName(x.key))}${deckSt[x.key] === "missing" && on ? ' <span class="pill warn">deck file missing</span>' : ""}</td><td class="num">${x.cards}</td><td class="num">${Math.max(0, x.cards - a.seen)}</td><td class="num">${on ? a.due : "·"}</td><td class="num">${a.learned}</td><td class="num">${a.mature}</td></tr>`;
    }).join("");
    return `${head}${load ? `<p class="note">Loading ${load} deck${load === 1 ? "" : "s"}…</p>` : ""}
      <div class="rv-stats"><div class="card"><div class="n">${due}</div><div class="l">due now</div></div><div class="card"><div class="n">${nl}</div><div class="l">new cards today</div></div>
      <div class="card"><div class="n">${st.tot.learned}</div><div class="l">learned</div></div><div class="card"><div class="n">${st.tot.mature}</div><div class="l">mature (21+ days)</div></div>
      <div class="card"><div class="n">${day.n}</div><div class="l">reviewed today</div></div></div>${go}
      <h2>Documents in my reviews</h2><p class="note" style="margin:0 0 8px">Tick the documents you are studying. A document is on when you have marked a chapter as read or it is in this week's plan. Your choice always wins.</p>
      <div class="card"><div class="rv-wrap"><table class="rv-t"><thead><tr><th></th><th>Document</th><th class="num">Cards</th><th class="num">New</th><th class="num">Due</th><th class="num">Learned</th><th class="num">Mature</th></tr></thead><tbody>${rows}</tbody></table></div>
      <div class="row" style="margin-top:12px"><label for="npd" class="note">New cards per day:</label>${npdSelect()}<span class="note">Keys: Space shows the answer, 1 to 4 grades, U undoes.</span></div></div>`;
  }
  const npdSelect = () => `<select id="npd" data-lx="npd" style="width:auto" aria-label="New cards per day">${[0, 5, 10, 15, 20, 30, 40].map(n => `<option value="${n}" ${sr().newPerDay === n ? "selected" : ""}>${n === 0 ? "0 (paused)" : n}</option>`).join("")}</select>`;
  window.learnSettings = () => `<div class="card"><p class="label">Review: new cards per day</p><p class="note" style="margin-top:0">How many brand-new flashcards you start each day on the Review page. Reviews of old cards are not limited.</p>${npdSelect()}</div>`;

  /* ---------- Quiz ---------- */
  const qz = { mode: "menu", scope: "mix", len: 10, list: [], i: 0, picked: -1, res: [], argSeen: "", err: "", added: 0 };
  function masteryPct(k) {   /* weighted mean of the last 30 answers: the newest answer counts 1, each older one 7% less */
    const m = mast()[k]; if (!m || !m.recent || m.recent.length < 3) return null;
    let num = 0, den = 0, w = 1;
    for (let i = m.recent.length - 1; i >= 0; i--) { num += w * (+m.recent[i]); den += w; w *= 0.93; }
    return Math.round(100 * num / den);
  }
  const withK = (k, q) => QUIZ[q.id] || Object.assign({ k }, q);
  function roundRobin(lists, n) {
    const out = [];
    for (let i = 0; out.length < n; i++) { let any = false; for (let j = 0; j < lists.length && out.length < n; j++) if (i < lists[j].length) { out.push(lists[j][i]); any = true; } if (!any) break; }
    return out;
  }
  function mixPool(n) {
    const have = idx.map(x => x.key).filter(k => deck(k));
    let keys = have.filter(readDoc);
    if (!keys.length) keys = have.filter(isOn);
    if (!keys.length) keys = have;
    const lists = shuffle(keys).map(k => {
      const all = (deck(k).quiz || []).map(q => withK(k, q)), rd = all.filter(q => S.done["study:" + k + ":" + q.ch]);
      return shuffle(rd.length >= 5 ? rd : all);
    });
    return roundRobin(lists, n);
  }
  function weakPool(n) {
    const s = sr(), out = [], seen = {};
    shuffle(Object.keys(s.cards)).forEach(id => { const r = s.cards[id]; if (r.src === "quiz" && (r.interval || 0) < MATURE && QUIZ[id]) { out.push(QUIZ[id]); seen[id] = 1; } });
    const ks = idx.map(x => x.key).filter(k => deck(k) && masteryPct(k) !== null && masteryPct(k) < 85).sort((a, b) => masteryPct(a) - masteryPct(b));
    const lists = ks.map(k => shuffle((deck(k).quiz || []).map(q => withK(k, q)).filter(q => !seen[q.id])));
    return out.concat(roundRobin(lists, n)).slice(0, n);
  }
  function prep(q) {
    const order = shuffle(q.opts.map((_, i) => i));
    return { id: q.id, k: q.k, q: q.q, why: q.why, ch: q.ch, opts: order.map(i => q.opts[i]), ans: order.indexOf(q.ans), right: q.opts[q.ans], orig: q.opts, origAns: q.ans };
  }
  function startQuiz() {
    let pool;
    if (qz.scope === "weak") pool = weakPool(qz.len);
    else if (qz.scope === "mix") pool = mixPool(qz.len);
    else pool = shuffle(((deck(qz.scope) || {}).quiz || []).map(q => withK(qz.scope, q))).slice(0, qz.len);
    if (!pool.length) { qz.err = qz.scope === "weak" ? "No weak spots yet. Take a mixed quiz first; the questions you miss will appear here." : "No questions found for this choice."; rerender(); return; }
    qz.err = ""; qz.list = pool.map(prep); qz.i = 0; qz.picked = -1; qz.res = []; qz.mode = "run"; render(); window.scrollTo(0, 0);
  }
  function pick(i) {
    if (qz.mode !== "run" || qz.picked >= 0) return;
    const q = qz.list[qz.i]; if (i < 0 || i >= q.opts.length) return;
    qz.picked = i; qz.res.push({ id: q.id, k: q.k, ok: i === q.ans, picked: q.opts[i], q });
    rerender();
    const fb = document.querySelector("#main .callout"); if (fb && fb.scrollIntoView) fb.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }
  function nextQ() {
    if (qz.picked < 0) return;
    if (qz.i + 1 < qz.list.length) { qz.i++; qz.picked = -1; } else finishQuiz();
    render(); window.scrollTo(0, 0);
  }
  function addMissed(q) {   /* a missed quiz question becomes a review card with the same id, so it is never duplicated */
    const s = sr(), r = s.cards[q.id], t = now();
    if (r) { if (r.interval > 0) { r.interval = 0; r.lrn = 1; r.due = t; r.ease = Math.max(1.3, (r.ease || 2.5) - 0.2); r.lapses = (r.lapses || 0) + 1; } return false; }
    s.cards[q.id] = { ease: 2.5, interval: 0, due: t, reps: 0, lapses: 0, last: t, lrn: 1, k: q.k, src: "quiz", ch: q.ch, q: q.q, opts: q.orig, a: `**${LET[q.origAns]}: ${q.right}.** ${q.why}` };
    return true;
  }
  function finishQuiz() {
    const res = qz.res, miss = res.filter(r => !r.ok), t = today();
    qz.added = 0; miss.forEach(r => { if (addMissed(r.q)) qz.added++; });
    const log = qlog(); log.push({ date: t, key: qz.scope, score: res.length - miss.length, total: res.length, missed: miss.map(r => r.id) });
    if (log.length > 200) S.quizlog = log.slice(-200);
    const m = mast();
    res.forEach(r => { const o = m[r.k] || (m[r.k] = { seen: 0, correct: 0, recent: "" }); o.seen++; if (r.ok) o.correct++; o.recent = ((o.recent || "") + (r.ok ? "1" : "0")).slice(-30); });
    S.habits[t] = S.habits[t] || {}; S.habits[t].quiz = true;
    qz.mode = "done"; save();
  }

  window.pageQuiz = safe("quiz", function () {
    ensureIndex();
    const head = `<div class="phead"><div class="eyebrow">Practice</div><h1>Quiz</h1><p>Short multiple-choice questions with an explanation after every answer. Missed questions go to your Review queue.</p></div>`;
    if (idxSt === "idle" || idxSt === "loading") return head + `<div class="empty">Loading the question bank…</div>`;
    if (idxSt === "missing") return head + noDecks();
    idx.forEach(x => ensureDeck(x.key));
    if (qz.mode === "run") return quizRunHtml();
    if (qz.mode === "done") return quizDoneHtml(head);
    return quizMenuHtml(head);
  });

  function quizMenuHtml(head) {
    if (!R.arg) qz.argSeen = "";
    else if (R.arg !== qz.argSeen) { qz.argSeen = R.arg; if (R.arg === "mix" || R.arg === "weak" || idx.some(x => x.key === R.arg)) qz.scope = R.arg; }
    const ready = idx.every(x => deckSt[x.key] === "ok" || deckSt[x.key] === "missing");
    const choices = [["mix", "Mixed from documents I have read"], ["weak", "My weak spots"]].concat(idx.map(x => [x.key, `${docLabel(x.key)} (${x.quiz} questions)`]));
    const rows = idx.map(x => { const p = masteryPct(x.key), m = mast()[x.key]; return `<tr><td>${esc(docName(x.key))}</td><td>${p === null ? '<span class="note">not enough answers yet</span>' : `<span class="rv-mini"><i style="width:${p}%;${p < 60 ? "background:var(--warn)" : ""}"></i></span><b>${p}%</b>`}</td><td class="num">${m ? m.seen : 0}</td></tr>`; }).join("");
    const hist = qlog().slice(-5).reverse().map(h => `<tr><td>${esc(h.date)}</td><td>${esc(h.key === "mix" ? "Mixed" : h.key === "weak" ? "Weak spots" : docLabel(h.key))}</td><td class="num">${h.score}/${h.total}</td></tr>`).join("");
    return `${head}${qz.err ? callout("NOTE", esc(qz.err), "cream") : ""}
      <div class="card"><label class="label" for="qscope">What do you want to be quizzed on?</label>
      <select id="qscope" data-lx="qscope">${choices.map(([k, t]) => `<option value="${esc(k)}" ${qz.scope === k ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>
      <div class="row" style="margin:12px 0 4px"><span class="note">Length:</span><div class="seg">${[10, 20].map(n => `<button data-lx="len" data-v="${n}" class="${qz.len === n ? "on" : ""}">${n} questions</button>`).join("")}</div></div>
      <button class="btn bigbtn" data-lx="qstart" ${ready ? "" : "disabled"}>${ready ? "▶ Start quiz" : "Loading questions…"}</button></div>
      <h2>Mastery by document</h2><p class="note" style="margin:0 0 8px">Your last answers count most. A score shows after 3 answers in a document.</p>
      <div class="card"><div class="rv-wrap"><table class="rv-t"><thead><tr><th>Document</th><th>Mastery</th><th class="num">Answered</th></tr></thead><tbody>${rows}</tbody></table></div></div>
      ${hist ? `<h2>Recent quizzes</h2><div class="card"><table class="rv-t"><tbody>${hist}</tbody></table></div>` : ""}`;
  }

  function quizRunHtml() {
    const q = qz.list[qz.i], n = qz.list.length, ans = qz.picked >= 0;
    const opts = q.opts.map((o, i) => `<button class="qz-opt ${ans ? (i === q.ans ? "ok" : i === qz.picked ? "bad" : "") : ""}" data-lx="pick" data-v="${i}" aria-label="Option ${LET[i]}"><span class="qz-let">${LET[i]}</span><span>${fmt(o)}</span></button>`).join("");
    const ok = qz.picked === q.ans;
    const fb = ans ? callout(ok ? "CORRECT" : "NOT QUITE", `${ok ? "" : `The right answer is <b>${LET[q.ans]}</b>. `}${fmt(q.why)}<br>${chLink(q.k, q.ch)}`, ok ? "green" : "red")
      + `<button class="btn bigbtn" data-lx="next">${qz.i + 1 < n ? "Next question →" : "See my score"} <span class="rv-key" style="color:#fff;border-color:#fff8;background:none">Space</span></button>` : "";
    return `<div class="rv-top"><div style="flex:1">${pbar(pct(qz.i + (ans ? 1 : 0), n))}<div class="pmeta"><span>Question ${qz.i + 1} of ${n}</span><span>${esc(docLabel(q.k))} · keys 1 to ${q.opts.length}</span></div></div><button class="btn ghost sm" data-lx="qmenu">Quit</button></div>
      <div class="card qz-card"><div class="qz-q">${fmt(q.q)}</div><div class="qz-opts" role="group" aria-label="Answer options">${opts}</div></div>${fb}`;
  }

  function quizDoneHtml(head) {
    const n = qz.res.length, good = qz.res.filter(r => r.ok).length, miss = qz.res.filter(r => !r.ok), p = pct(good, n);
    return `${head}<div class="card"><p class="label">Your score</p><div class="qz-score">${good} / ${n} <span style="font-size:22px;color:var(--muted)">(${p}%)</span></div>
      <p>${p >= 80 ? "Strong work." : p >= 60 ? "Good progress. Look at the misses below." : "This is how you find gaps. Read the explanations, then try again."}${qz.added ? ` <b>${qz.added}</b> missed question${qz.added === 1 ? " was" : "s were"} added to your Review queue.` : ""}</p>
      <div class="row"><button class="btn" data-lx="qstart">Try again</button><button class="btn ghost" data-lx="qmenu">Back to quiz menu</button><a class="btn ghost" href="#/review">🧠 Go to Review</a></div></div>
      ${miss.length ? `<h2>Questions to revisit</h2>` + miss.map(r => `<div class="card" style="margin-bottom:10px"><div class="rv-meta"><span class="pill">${esc(docName(r.k))}</span></div><p style="margin:8px 0"><b>${fmt(r.q.q)}</b></p>
        <p style="margin:4px 0" class="note">Your answer: ${fmt(r.picked)}</p><p style="margin:4px 0"><b>Right answer:</b> ${fmt(r.q.right)}</p><p style="margin:4px 0">${fmt(r.q.why)}</p><p style="margin:4px 0">${chLink(r.k, r.q.ch)}</p></div>`).join("") : ""}`;
  }

  /* ---------- Datasets ---------- */
  const dsf = { q: "", level: "", domain: "", topic: "" };
  const catalog = () => Array.isArray(window.DATA_CATALOG) ? window.DATA_CATALOG : [];
  function dsMatch(d) {
    if (dsf.level && d.level !== dsf.level) return false;
    if (dsf.domain && d.domain !== dsf.domain) return false;
    if (dsf.topic && (d.topics || []).indexOf(dsf.topic) < 0) return false;
    if (dsf.q) { const h = [d.title, d.domain, d.summary, d.id, (d.topics || []).join(" ")].join(" ").toLowerCase(); return dsf.q.toLowerCase().split(/\s+/).filter(Boolean).every(w => h.indexOf(w) >= 0); }
    return true;
  }
  const lvlCls = l => l === "beginner" ? "ok" : l === "advanced" ? "warn" : "";
  function dsGrid() {
    const l = catalog().filter(dsMatch);
    return l.length ? l.map(d => `<a class="card ds-card" href="#/data/${esc(d.id)}"><div class="row"><span class="pill ${lvlCls(d.level)}">${esc(d.level || "")}</span><span class="pill mut">${esc(d.domain || "")}</span><div class="sp"></div><span class="note">${d.rows ? Number(d.rows).toLocaleString() + " rows" : ""}</span></div>
      <h3>${esc(d.title)}</h3><p>${esc(d.summary || "")}</p><div class="row">${(d.topics || []).slice(0, 4).map(t => `<span class="tag mine" style="margin:0">${esc(t)}</span>`).join("")}</div></a>`).join("")
      : `<div class="empty" style="grid-column:1/-1">No dataset matches these filters.</div>`;
  }
  function snippets(file, many) {
    const url = SITE + "data/" + encodeURI(file), loc = "data/" + file, base = file.split("/").pop(), ext = (base.split(".").pop() || "").toLowerCase();
    const nm = many ? base.replace(/\.[^.]+$/, "").replace(/[^a-z0-9]+/gi, "_").toLowerCase() : "df", v = /^[a-z_]/.test(nm) ? nm : "df";
    const rd = { csv: "read_csv", json: "read_json", parquet: "read_parquet", xlsx: "read_excel", xls: "read_excel" }[ext];
    if (rd) return [`import pandas as pd\n${v} = pd.${rd}("${url}")`, `import pandas as pd\n${v} = pd.${rd}("${loc}")`];
    if (/^(db|sqlite|sqlite3)$/.test(ext)) return [`import sqlite3, urllib.request\nurllib.request.urlretrieve("${url}", "${base}")\ncon = sqlite3.connect("${base}")`, `import sqlite3\ncon = sqlite3.connect("${loc}")`];
    return [`# download this file:\n# ${url}`, `# local copy:\n# ${loc}`];
  }
  function usedIn(u) {
    let m = /^study\/([a-z0-9]+)\/(ch\d+)\.html(#.*)?$/.exec(u);
    if (m) { const d = docInfo(m[1]), c = (d.chapters || []).find(x => x.page === m[2] + ".html"); return `<li><a href="${esc(u)}">${esc(d.label || m[1])}${c ? ", chapter " + c.num + ": " + esc(c.title) : ""}</a></li>`; }
    m = /^project:(\d+)$/.exec(u);
    if (m) { const p = D.projects.find(x => String(x.n) === m[1]); return `<li><a href="#/projects">Project ${m[1]}${p ? ": " + esc(p.title) : ""}</a></li>`; }
    return `<li>${esc(u)}</li>`;
  }
  const list = (a, ord) => `<${ord ? "ol" : "ul"} class="ds-list">${(a || []).map(x => `<li>${fmt(x)}</li>`).join("")}</${ord ? "ol" : "ul"}>`;
  function dsDetail(d) {
    const files = d.files || [], many = files.length > 1;
    const sn = files.map(f => snippets(f, many));
    const snip = (txt, label) => `<div class="row" style="margin-top:8px"><b style="font-size:13.5px">${label}</b><div class="sp"></div><button class="btn ghost sm" data-lx="copy" data-v="${esc(txt)}">📋 Copy</button></div><div class="ds-snip">${esc(txt)}</div>`;
    return `<p><a href="#/data">← All datasets</a></p>
      <div class="phead"><div class="eyebrow">${esc(d.domain || "Dataset")}</div><h1>${esc(d.title)}</h1><p><span class="pill ${lvlCls(d.level)}">${esc(d.level || "")}</span> ${d.rows ? Number(d.rows).toLocaleString() + " rows · " : ""}${files.length} file${files.length === 1 ? "" : "s"}</p></div>
      <div class="card"><p style="margin:0">${fmt(d.summary || "")}</p><div class="row" style="margin-top:10px">${(d.topics || []).map(t => `<span class="tag mine" style="margin:0">${esc(t)}</span>`).join("")}</div></div>
      <div class="ds-sec"><h2>Download</h2><div class="card"><div class="row">${files.map(f => `<a class="btn ghost sm" href="data/${encodeURI(f)}" download>⬇ ${esc(f)}</a>`).join("")}</div>
        ${files.map((f, i) => `<div style="margin-top:12px"><b>${esc(f)}</b>${snip(sn[i][0], "Load it from the website (Colab, Jupyter)")}${snip(sn[i][1], "Load it from a local folder")}</div>`).join("")}</div></div>
      <div class="ds-sec"><h2>Data dictionary</h2><div class="card"><div class="rv-wrap"><table class="rv-t"><thead><tr><th>Column</th><th>Type</th><th>Meaning</th></tr></thead><tbody>${(d.dictionary || []).map(c => `<tr><td><code>${esc(c.col)}</code></td><td>${esc(c.type || "")}</td><td>${fmt(c.meaning || "")}</td></tr>`).join("")}</tbody></table></div></div></div>
      <div class="ds-sec"><h2>Suggested tasks</h2><div class="card">${list(d.tasks, true)}</div></div>
      <div class="ds-sec"><details><summary><span class="sm1">Hints: problems hidden in this data</span><span class="cnt">${(d.gotchas || []).length} to find</span></summary><div class="in"><p class="note" style="margin:0 6px">Open this only after you tried on your own. Each line is a planted problem to look for.</p>${list(d.gotchas)}</div></details>
        <details><summary><span class="sm1">Show answer key (spoiler)</span></summary><div class="in"><p style="margin:0 6px">${fmt(d.answer_key || "No answer key for this dataset.")}</p></div></details></div>
      ${(d.used_in || []).length ? `<div class="ds-sec"><h2>Used in</h2><div class="card"><ul class="ds-list" style="margin:0 0 0 20px">${d.used_in.map(usedIn).join("")}</ul></div></div>` : ""}`;
  }
  window.pageData = safe("data", function () {
    loadCatalog();
    const head = `<div class="phead"><div class="eyebrow">Practice data</div><h1>Datasets</h1><p>Realistic data with planted problems to find. Download one, explore it, then check yourself against the answer key.</p></div>`;
    if (catSt === "idle" || catSt === "loading") return head + `<div class="empty">Loading the dataset catalog…</div>`;
    if (catSt === "missing") return head + callout("NO CATALOG YET", "The dataset catalog is not on this site yet. Build it with <code>python3 tools/build_data_catalog.py</code>, upload <code>assets/data-catalog.js</code> and the <code>data</code> folder, then reload.", "cream");
    const cat = catalog(), one = R.arg && cat.find(d => d.id === R.arg);
    if (one) return dsDetail(one);
    const uniq = f => [...new Set(cat.flatMap(d => f(d)).filter(Boolean))].sort();
    const sel = (id, label, vals, cur) => `<select id="${id}" data-lx="${id}" aria-label="${label}"><option value="">${label}</option>${vals.map(v => `<option ${v === cur ? "selected" : ""}>${esc(v)}</option>`).join("")}</select>`;
    return `${head}<div class="ds-filters"><input type="search" id="dsq" data-lx="dsq" placeholder="Search datasets…" value="${esc(dsf.q)}" aria-label="Search datasets">
      ${sel("dsLevel", "All levels", ["beginner", "intermediate", "advanced"], dsf.level)}${sel("dsDomain", "All domains", uniq(d => [d.domain]), dsf.domain)}${sel("dsTopic", "All topics", uniq(d => d.topics || []), dsf.topic)}</div>
      <div class="grid g2" id="dgrid">${dsGrid()}</div>`;
  });

  /* ---------- Home card ---------- */
  function quizSuggest() {
    const w = PLAN[currentWeekIdx()];
    if (w) for (const t of w.tasks) { const m = t.href && /^study\/([a-z0-9]+)\//.exec(t.href); if (m && (idx ? idx.some(x => x.key === m[1]) : true)) return m[1]; }
    const k = D.study.find(d => d.status === "ready" && readDoc(d.key));
    return k ? k.key : "";
  }
  window.learnHome = safe("home", function () {
    wantDecks();
    if (idxSt === "missing" && !Object.keys(sr().cards).length) return "";
    const t = now(), due = dueIds(t).length, nl = newAvail(), cur = currentLessonIdx(), l = cur === null ? null : LESSONS[cur], qk = quizSuggest();
    const stuff = idxSt === "ok" && loadingDecks() ? " (loading…)" : "";
    return `<div class="card pt-card"><div class="row"><div><p class="label">Practice today</p><h3 style="margin:0">${due} card${due === 1 ? "" : "s"} to review${nl ? ` · ${nl} new` : ""}${stuff}</h3></div><div class="sp"></div>
      <button class="btn" data-lx="gostart">▶ Start review</button></div>
      <div class="row" style="margin-top:10px">${qk ? `<a class="btn ghost sm" href="#/quiz/${esc(qk)}">📝 Quiz: ${esc(docLabel(qk))}</a>` : `<a class="btn ghost sm" href="#/quiz">📝 Take a quiz</a>`}
      ${l ? `<a class="btn ghost sm" href="#/today">▶ Lesson: Day ${l.n + 1}</a>` : ""}<span class="note">🔥 ${streak()}-day streak</span></div></div>`;
  });

  /* ---------- events ---------- */
  function copyText(txt) {
    const done = () => toast("Copied. Paste it into your notebook.");
    const fallback = () => { const ta = document.createElement("textarea"); ta.value = txt; ta.style.cssText = "position:fixed;opacity:0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (e) { /* ignore */ } ta.remove(); done(); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, fallback); else fallback();
  }
  /* leaving a finished session or quiz shows the start screen next time (this listener runs before the app's own hashchange render) */
  window.addEventListener("hashchange", () => {
    const p = parseRoute();
    if (view.mode === "done") view.mode = "home";
    if (qz.mode === "done") qz.mode = "menu";
    if (p.page === "quiz" && p.arg && p.arg !== qz.argSeen && qz.mode === "run") qz.mode = "menu";
  });
  document.addEventListener("click", e => {
    const el = e.target.closest && e.target.closest("[data-lx]"); if (!el || el.tagName === "SELECT" || el.tagName === "INPUT") return;
    const a = el.getAttribute("data-lx"), v = el.getAttribute("data-v");
    if (a === "start") { startSession(); render(); window.scrollTo(0, 0); }
    else if (a === "gostart") { if (R.page === "review") { startSession(); rerender(); } else { view.auto = true; view.mode = "home"; location.hash = "#/review"; } }
    else if (a === "show") { view.shown = true; rerender(); }
    else if (a === "grade") grade(+v);
    else if (a === "undo") undo();
    else if (a === "stop") { view.mode = "done"; rerender(); }
    else if (a === "home") { view.mode = "home"; rerender(); }
    else if (a === "len") { qz.len = +v; rerender(); }
    else if (a === "qstart") startQuiz();
    else if (a === "pick") pick(+v);
    else if (a === "next") nextQ();
    else if (a === "qmenu") { qz.mode = "menu"; rerender(); }
    else if (a === "copy") copyText(v);
  });
  document.addEventListener("change", e => {
    const t = e.target, a = t.getAttribute && t.getAttribute("data-lx"); if (!a) return;
    if (a === "tog") { sr().enabled[t.getAttribute("data-v")] = t.checked; save(); wantDecks(); rerender(); }
    else if (a === "npd") { sr().newPerDay = +t.value; save(); rerender(); }
    else if (a === "qscope") { qz.scope = t.value; rerender(); }
    else if (a === "dsLevel" || a === "dsDomain" || a === "dsTopic") { dsf[a === "dsLevel" ? "level" : a === "dsDomain" ? "domain" : "topic"] = t.value; const g = document.getElementById("dgrid"); if (g) g.innerHTML = dsGrid(); }
  });
  document.addEventListener("input", e => {
    const t = e.target;
    if (t.getAttribute && t.getAttribute("data-lx") === "dsq") { dsf.q = t.value.trim(); const g = document.getElementById("dgrid"); if (g) g.innerHTML = dsGrid(); }
  });
  document.addEventListener("keydown", e => {
    if ((R.page !== "review" && R.page !== "quiz") || e.metaKey || e.ctrlKey || e.altKey) return;
    const tag = (e.target && e.target.tagName) || "";
    if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
    if ($("#smodal").classList.contains("open") || $("#modal").classList.contains("open")) return;
    const k = e.key, onBtn = /BUTTON|^A$/.test(tag), go = (k === " " || k === "Enter") && !onBtn;
    if (R.page === "review" && view.mode === "study" && view.cur) {
      if (go && !view.shown) { e.preventDefault(); view.shown = true; rerender(); }
      else if (view.shown && /^[1-4]$/.test(k)) { e.preventDefault(); grade(+k - 1); }
      else if (!view.shown && /^[1-4]$/.test(k)) { /* answer not shown yet: ignore */ }
      else if (k === "u" || k === "U") { e.preventDefault(); undo(); }
    } else if (R.page === "quiz" && qz.mode === "run") {
      if (qz.picked < 0 && /^[1-6]$/.test(k)) { e.preventDefault(); pick(+k - 1); }
      else if (qz.picked < 0 && /^[a-fA-F]$/.test(k) && !e.shiftKey) { e.preventDefault(); pick(k.toLowerCase().charCodeAt(0) - 97); }
      else if (qz.picked >= 0 && go) { e.preventDefault(); nextQ(); }
    }
  });
})();
