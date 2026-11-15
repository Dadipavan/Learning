#!/usr/bin/env python3
"""Merge the daily lessons written for weeks 14-156 (tools/lessons/weeks_*.json) and the elective weeks 157-164
(tools/new_chapters/week_*.json + meta_*.json) into the site data in index.html.

Usage (from the project root):  python3 tools/add_lessons.py [--dry-run]
Idempotent: D.weeks is cut back to the original 13 weeks and D.plan to the original 156 before merging.
 - D.weeks gets one entry per week with lessons {n,week,day,title,build,ask,learn,res,rest[,ch]}; n = global lesson index
 - D.plan: every week 14-156 gets the "Finish this week's 7 daily lessons" task first; plan_title replaces placeholder titles
 - elective weeks 157-164 are added to D.plan (phase p16) and phase p16 is added to D.phases
Run it only when no other process is editing index.html."""
import glob, hashlib, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IDX = os.environ.get("SITE_INDEX") or os.path.join(ROOT, "index.html")
LESSON_TASK = "Finish this week's 7 daily lessons on the Today page (6 study days and one review day)"
ELECTIVE_ORDER = {157: ("ml", 19), 158: ("ds", 17), 159: ("stats", 16), 160: ("ds", 18), 161: ("ml", 20), 162: ("genai", 17), 163: ("dl", 17), 164: ("ds", 19)}


def tid(prefix, text):
    return f"{prefix}:" + hashlib.md5(text.encode()).hexdigest()[:8]


def main(dry):
    h = open(IDX, encoding="utf-8").read()
    i = h.index("const D = ") + len("const D = ")
    D, end = json.JSONDecoder().raw_decode(h[i:])
    study = {s["key"]: s for s in D["study"]}

    weeks = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "tools", "lessons", "weeks_*.json"))):
        for w in json.load(open(p, encoding="utf-8"))["weeks"]:
            assert w["n"] not in weeks, f"week {w['n']} defined twice ({p})"
            weeks[w["n"]] = w
    missing = [n for n in range(14, 157) if n not in weeks]
    if missing:
        print("WARNING: no lessons for weeks:", missing[:10], "... (%d weeks). Merging only the contiguous prefix 14..%d" % (len(missing), missing[0] - 1))
        weeks = {n: w for n, w in weeks.items() if n < missing[0]}
    electives = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "tools", "new_chapters", "week_*.json"))):
        for w in json.load(open(p, encoding="utf-8"))["weeks"]:
            electives[w["n"]] = w
    # --- weeks
    D["weeks"] = [w for w in D["weeks"] if w["n"] <= 13]
    nxt = sum(len(w["lessons"]) for w in D["weeks"])
    for n in sorted(list(weeks) + list(electives)):
        w = weeks.get(n) or electives[n]
        out = {"n": n, "theme": w["theme"], "goal": w["goal"], "lessons": []}
        assert n == len(D["weeks"]) + 1, f"weeks must be contiguous; got {n} after {len(D['weeks'])}"
        for l in sorted(w["lessons"], key=lambda x: x["day"]):
            item = {"n": nxt, "week": n, "day": l["day"], "title": l["title"], "build": l["build"], "ask": l["ask"], "learn": l["learn"],
                    "res": l.get("res", []), "rest": bool(l.get("rest", False))}
            if l.get("ch"):
                item["ch"] = l["ch"]
            out["lessons"].append(item)
            nxt += 1
        D["weeks"].append(out)
    # --- plan
    plan = {w["n"]: w for w in D["plan"] if w["n"] <= 156}
    for n, w in weeks.items():
        pw = plan[n]
        if w.get("plan_title"):
            pw["title"] = w["plan_title"]
        if not any(t["text"] == LESSON_TASK for t in pw["tasks"]):
            pw["tasks"].insert(0, {"text": LESSON_TASK, "href": "#/today", "id": tid(f"w{n}", LESSON_TASK)})
    phase_tasks = []
    for n, (key, num) in ELECTIVE_ORDER.items():
        mp = os.path.join(ROOT, "tools", "new_chapters", f"meta_{key}_ch{num:02d}.json")
        if n not in electives or not os.path.exists(mp):
            print(f"note: elective week {n} ({key} ch{num}) not ready; skipped")
            continue
        meta = json.load(open(mp, encoding="utf-8"))
        label = study[key]["label"]
        page = f"study/{key}/ch{num:02d}.html"
        texts = [
            (LESSON_TASK, "#/today"),
            (f"Elective. Read {label}, Chapter {num}: {meta['title']}", page),
            ("Type and run every code example yourself (do not paste). Predict each output first.", None),
            ("Do the chapter Practice set, then check your answers", None),
            ("Use one prompt from the chapter's Prompt pack to quiz or challenge yourself", None),
            ("Open the Review page and the Quiz page and do today's cards plus one quiz", "#/review"),
            ("Weekly review: 3 honest lines in your learning log (done / hardest / change)", "#/progress"),
        ]
        plan[n] = {"n": n, "phase": "p16", "title": meta["title"], "tasks": [{"text": t, "href": hr, "id": tid(f"w{n}", t)} for t, hr in texts], "projects": []}
        phase_tasks.append({"id": tid("p16", meta["title"]), "text": f"Elective: {label}, Chapter {num}: {meta['title']}"})
    D["plan"] = [plan[n] for n in sorted(plan)]
    # --- phase p16
    D["phases"] = [p for p in D["phases"] if p["id"] != "p16"]
    if phase_tasks:
        D["phases"].append({"id": "p16", "months": [37, 38], "stage": 3, "title": "Frontier electives (optional, any order)",
                            "goal": "Go deeper where your job or curiosity points: graphs, modern forecasting, geospatial, econometrics, responsible AI, LLM engineering, frontier deep learning, domain playbooks.",
                            "tasks": phase_tasks, "maps": ["ml", "ds", "ai", "math", "pro"], "project": "Pick one elective and build its suggested mini project",
                            "exit": "You can read, implement and explain advanced topics on your own."})
    total = sum(len(w["lessons"]) for w in D["weeks"])
    print(f"weeks={len(D['weeks'])} lessons={total} plan weeks={len(D['plan'])} phases={len(D['phases'])}")
    if dry:
        return
    out = json.dumps(D, ensure_ascii=False).replace("</", "<\\/")
    open(IDX, "w", encoding="utf-8").write(h[:i] + out + h[i + end:])
    print("index.html updated")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
