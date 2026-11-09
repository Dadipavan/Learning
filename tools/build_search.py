#!/usr/bin/env python3
"""Build assets/search-index.js (window.SEARCH_INDEX) from study pages + index.html data.

Run from anywhere:  python3 tools/build_search.py
Record fields: k doc key (label/icon live in window.SEARCH_DOCS), c chapter label, t chapter title,
h heading, a anchor id, u url (relative to site root), b display body (<=600 chars, snippet only),
s lowercase searchable text (<=4000 chars; absent on site-data records, client uses h+b), l level (1 chapter intro, 2 h2, 3 h3, 0 site data).
"""
import json, re, sys, glob, os
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BODY_CAP, SEARCH_CAP, MAX_BYTES = 320, 4000, 12 * 1024 * 1024
WS = re.compile(r"\s+")


def clean(s):
    return WS.sub(" ", s).strip()


def load_site_data():
    text = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    i = text.index("const D = ") + len("const D = ")
    return json.JSONDecoder().raw_decode(text[i:])[0]


def plain(s):
    return clean(re.sub(r"[*`_]+", "", s or ""))


def page_records(path, doc, label, icon):
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    eb = soup.select_one(".banner .eyebrow")
    h1 = soup.select_one(".banner h1") or soup.find("h1")
    title = clean(h1.get_text()) if h1 else clean(soup.title.get_text() if soup.title else rel)
    base = os.path.basename(path)
    if base == "index.html":
        clabel = "Contents"
    elif base == "appendix.html":
        clabel = "Appendix"
    else:
        clabel = clean(eb.get_text()).title() if eb else base
    recs = []

    def new(heading, anchor, level):
        r = {"k": doc, "c": clabel, "t": title, "h": heading, "a": anchor,
             "u": rel + ("#" + anchor if anchor else ""), "l": level, "_p": []}
        recs.append(r)
        return r

    cur = new(title, "", 1)
    h2id = ""
    root = soup.body or soup
    for node in list(root.descendants):
        if isinstance(node, NavigableString):
            if isinstance(node, Comment):
                continue
            skip = False
            for p in node.parents:
                if p.name in ("script", "style") or (p.name == "details" and "toc" in (p.get("class") or [])) \
                        or "topbar" in (p.get("class") or []) or "pager" in (p.get("class") or []):
                    skip = True
                    break
                if p.name in ("h2", "h3"):
                    skip = True
                    break
            if not skip and str(node).strip():
                cur["_p"].append(str(node))
        elif node.name in ("h2", "h3"):
            hid = node.get("id") or ""
            if node.name == "h2":
                h2id = hid
                cur = new(clean(node.get_text()), hid, 2)
            else:
                cur = new(clean(node.get_text()), hid or h2id, 3)
    out = []
    for r in recs:
        body = clean(" ".join(r.pop("_p")))
        if not body and r["l"] == 1:
            continue
        r["b"] = body[:BODY_CAP]
        r["s"] = body[:SEARCH_CAP].lower()
        out.append(r)
    return out


def site_records(D):
    out = []
    for d in D["domains"]:
        for sec in d["sections"]:
            for it in sec["items"]:
                txt = plain(it["text"])
                out.append({"k": "skills", "c": d["title"], "t": sec["title"],
                            "h": txt[:160], "a": "", "u": "index.html#/skills/" + d["key"], "l": 0,
                            "b": clean((it.get("sub") or "") + " " + txt)[:BODY_CAP]})
    for g in D["topicMap"]:
        for it in g["items"]:
            out.append({"k": "topics", "c": g["domain"], "t": "98-topic map",
                        "h": "%s. %s" % (it["n"], it["name"]), "a": "", "u": "index.html#/map", "l": 0,
                        "b": g["domain"]})
    return out


def main():
    D = load_site_data()
    meta = {s["key"]: s for s in D["study"]}
    recs = []
    for key in sorted(meta):
        s = meta[key]
        files = sorted(glob.glob(os.path.join(ROOT, "study", key, "ch*.html")))
        files = [os.path.join(ROOT, "study", key, "index.html")] + files
        ap = os.path.join(ROOT, "study", key, "appendix.html")
        if os.path.exists(ap):
            files.append(ap)
        for f in files:
            if os.path.exists(f):
                recs += page_records(f, key, s["label"], s["icon"])
    # unknown study dirs
    recs += site_records(D)
    docs = [{"k": k, "d": s["label"], "i": s["icon"]} for k, s in meta.items()]
    docs += [{"k": "skills", "d": "Skill map", "i": "🧭"}, {"k": "topics", "d": "Topic map", "i": "🗺️"}]

    def dump():
        return "window.SEARCH_INDEX=" + json.dumps(recs, ensure_ascii=False, separators=(",", ":")) + \
               ";\nwindow.SEARCH_DOCS=" + json.dumps(docs, ensure_ascii=False, separators=(",", ":")) + ";\n"

    js = dump()
    cap = SEARCH_CAP
    while len(js.encode("utf-8")) > MAX_BYTES and cap > 500:
        cap = int(cap * 0.7)
        for r in recs:
            if "s" in r:
                r["s"] = r["s"][:cap]
        js = dump()
    with open(os.path.join(ROOT, "assets", "search-index.js"), "w", encoding="utf-8") as fh:
        fh.write(js)
    print("records: %d  size: %.2f MB" % (len(recs), len(js.encode("utf-8")) / 1048576))


if __name__ == "__main__":
    sys.exit(main())
