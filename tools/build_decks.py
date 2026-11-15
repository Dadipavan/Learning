#!/usr/bin/env python3
"""Build assets/decks/<key>.js and assets/decks/index.js from tools/decks/<key>.json (flashcards + quizzes).

Usage (from the project root):  python3 tools/build_decks.py
Validates every deck (ids, options, answer index, lengths) and exits non-zero on problems.
Output format (loaded lazily by the app with a <script> tag, so it also works from file://):
  assets/decks/<key>.js     window.DECKS=window.DECKS||{};window.DECKS["<key>"]={...};
  assets/decks/index.js     window.DECK_INDEX=[{"key","title","cards","quiz"},...];
"""
import json, os, re, sys, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "decks")


def site_data():
    text = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    i = text.index("const D = ") + len("const D = ")
    return json.JSONDecoder().raw_decode(text[i:])[0]


def check(key, deck, chapters):
    errs = []
    ids = set()
    for c in deck.get("cards", []):
        for f in ("id", "q", "a", "ch"):
            if not c.get(f):
                errs.append(f"{key}: card missing {f}: {c}")
        if c.get("id") in ids:
            errs.append(f"{key}: duplicate id {c.get('id')}")
        ids.add(c.get("id"))
        if len(c.get("q", "").split()) > 40:
            errs.append(f"{key}: card question too long: {c['id']}")
        if len(c.get("a", "").split()) > 70:
            errs.append(f"{key}: card answer too long: {c['id']}")
        if c.get("ch") and c["ch"] not in chapters:
            errs.append(f"{key}: card {c['id']} chapter {c['ch']} not found")
    for q in deck.get("quiz", []):
        for f in ("id", "q", "opts", "ans", "why", "ch"):
            if q.get(f) in (None, "", []):
                errs.append(f"{key}: quiz missing {f}: {q.get('id')}")
        if q.get("id") in ids:
            errs.append(f"{key}: duplicate id {q.get('id')}")
        ids.add(q.get("id"))
        o = q.get("opts", [])
        if len(o) != 4 or len(set(o)) != 4:
            errs.append(f"{key}: quiz {q.get('id')} needs 4 distinct options")
        if not isinstance(q.get("ans"), int) or not 0 <= q["ans"] < len(o):
            errs.append(f"{key}: quiz {q.get('id')} bad ans")
        if q.get("ch") and q["ch"] not in chapters:
            errs.append(f"{key}: quiz {q.get('id')} chapter {q['ch']} not found")
    pos = [q["ans"] for q in deck.get("quiz", []) if isinstance(q.get("ans"), int)]
    if pos and len(set(pos)) < 3:
        errs.append(f"{key}: answer positions are not balanced: {sorted(set(pos))}")
    return errs


def main():
    D = site_data()
    labels = {s["key"]: s["label"] for s in D["study"]}
    os.makedirs(OUT, exist_ok=True)
    index, errs = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, "tools", "decks", "*.json"))):
        key = os.path.basename(path)[:-5]
        deck = json.load(open(path, encoding="utf-8"))
        chapters = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, "study", key, "ch[0-9][0-9].html"))}
        errs += check(key, deck, chapters)
        deck["key"] = key
        deck["title"] = labels.get(key, key)
        js = "window.DECKS=window.DECKS||{};window.DECKS[%s]=%s;\n" % (json.dumps(key), json.dumps(deck, ensure_ascii=False, separators=(",", ":")))
        open(os.path.join(OUT, key + ".js"), "w", encoding="utf-8").write(js)
        index.append({"key": key, "title": labels.get(key, key), "cards": len(deck.get("cards", [])), "quiz": len(deck.get("quiz", []))})
        print(f"{key:8s} cards={len(deck.get('cards', [])):3d} quiz={len(deck.get('quiz', [])):3d}")
    open(os.path.join(OUT, "index.js"), "w", encoding="utf-8").write("window.DECK_INDEX=%s;\n" % json.dumps(index, ensure_ascii=False, separators=(",", ":")))
    print("decks:", len(index), "cards:", sum(i["cards"] for i in index), "quiz:", sum(i["quiz"] for i in index))
    if errs:
        print("PROBLEMS:\n- " + "\n- ".join(errs))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
