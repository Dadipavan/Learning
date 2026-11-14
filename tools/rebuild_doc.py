#!/usr/bin/env python3
"""Rebuild derived files of an EXISTING study document after its chapter pages were edited.
Usage: python3 -I tools/rebuild_doc.py <key> [--no-pdf]
 - adds ids to any new <h2>, regenerates each chapter's "In this chapter" list
 - regenerates the chapter sections inside full.html
 - regenerates <key>.docx and <key>.pdf
 - updates the word counts in the main index.html registry"""
import sys, os, re, importlib.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
spec = importlib.util.spec_from_file_location("build_doc", os.path.join(ROOT, "tools", "build_doc.py"))
bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)


def split_page(h):
    m = re.search(r'(<div class="page">)(<div class="banner">.*?</div>)(<details class="toc".*?</details>)(.*?)(<div class="readbtn">.*)', h, re.S)
    return m


def sync(key, files):
    """Make index tiles, pagers, full.html and the registry agree with the chapter files on disk."""
    import json
    d = os.path.join(ROOT, "study", key)
    meta = []
    for f in files:
        h = open(os.path.join(d, f)).read()
        num = 99 if f == "appendix.html" else int(f[2:4])
        eb = re.search(r'<div class="eyebrow">(.*?)</div>', h).group(1)
        title = re.search(r"<h1>(.*?)</h1>", h).group(1)
        color = re.search(r'<body style="--accent:(#[0-9a-fA-F]+)"', h).group(1)
        meta.append(dict(num=num, page=f, label=eb, title=title, color=color, readid="study:%s:%s" % (key, f[:-5])))
    # pagers
    for i, m in enumerate(meta):
        p = os.path.join(d, m["page"]); h = open(p).read()
        prev = meta[i - 1] if i else None; nxt = meta[i + 1] if i + 1 < len(meta) else None
        def lab(x): return "Appendix" if x["label"] == "APPENDIX" else x["label"].title()
        pg = ('<div class="pager">' + (f'<a class="btn ghost" href="{prev["page"]}">\u2190 {lab(prev)}: {prev["title"]}</a>' if prev else '<a class="btn ghost" href="index.html">\u2190 Contents</a>') +
              (f'<a class="btn" href="{nxt["page"]}">{lab(nxt)}: {nxt["title"]} \u2192</a>' if nxt else '<span></span>') + '</div>')
        pg = pg.encode().decode("unicode_escape").encode("latin-1").decode("utf-8") if False else pg.replace("\\u2190", "\u2190").replace("\\u2192", "\u2192")
        h = re.sub(r'<div class="pager">.*?</div>(?=</div><script)', lambda _: pg, h, flags=re.S)
        open(p, "w").write(h)
    # index tiles + progress ids
    ip = os.path.join(d, "index.html"); ih = open(ip).read()
    tiles = "".join(f'<a href="{m["page"]}" data-tile="{m["readid"]}" style="background:{m["color"]}"><b>{m["label"]}<i></i></b>{m["title"]}</a>' for m in meta)
    ih = re.sub(r'<div class="tiles">.*?</div>(?=<div class="actions">)', lambda _: '<div class="tiles">' + tiles + '</div>', ih, flags=re.S)
    ih = re.sub(r"data-ids='\[.*?\]'", lambda _: "data-ids='" + json.dumps([m["readid"] for m in meta]) + "'", ih)
    open(ip, "w").write(ih)
    # registry
    p = os.path.join(ROOT, "index.html"); h = open(p).read()
    s = h.split("<script>")[-1]; i = s.find("const D = ") + 10
    D, end = json.JSONDecoder().raw_decode(s[i:])
    st = next(x for x in D["study"] if x["key"] == key)
    have = {c["readid"]: c for c in st["chapters"]}
    new = []
    for m in meta:
        c = have.get(m["readid"], {})
        new.append(dict(num=m["num"], title=m["title"], label=m["label"], page=m["page"], color=m["color"], words=c.get("words", 0), readid=m["readid"]))
    st["chapters"] = new
    out = json.dumps(D, ensure_ascii=False).replace("</", "<\\/")
    open(p, "w").write(h.replace(s, s[:i] + out + s[i + end:]))


def main(key, make_pdf):
    d = os.path.join(ROOT, "study", key)
    files = sorted((f for f in os.listdir(d) if re.fullmatch(r"ch\d\d\.html|appendix\.html", f)), key=lambda f: (f == "appendix.html", f))
    sync(key, files)
    secs, words = [], {}
    for f in files:
        h = open(os.path.join(d, f)).read()
        m = split_page(h)
        if not m:
            print("cannot parse", f); continue
        body, toc = bd.add_ids(m.group(4))
        tocs = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc)
        newtoc = f'<details class="toc" open><summary>In this chapter</summary><ol>{tocs}</ol></details>'
        h2 = h[:m.start(3)] + newtoc + body + m.group(5)
        open(os.path.join(d, f), "w").write(h2)
        secs.append((m.group(2), body))
        words[f] = bd.words(body)
    full_p = os.path.join(d, "full.html")
    full = open(full_p).read()
    first = full.find('<section class="chapter"'); last = full.rfind('</section>') + len('</section>')
    mm = re.findall(r'<div class="eyebrow">(.*?)</div>', "".join(b for b, _ in secs))
    accents = {}
    for f in files:
        accents[f] = re.search(r'<body style="--accent:(#[0-9a-fA-F]+)"', open(os.path.join(d, f)).read()).group(1)
    newsecs = "".join(f'<section class="chapter" style="--accent:{accents[f]}">{banner}{body}</section>' for f, (banner, body) in zip(files, secs))
    full = full[:first] + newsecs + full[last:]
    open(full_p, "w").write(full)

    # registry words
    p = os.path.join(ROOT, "index.html"); h = open(p).read(); tot = 0
    for f, w in words.items():
        rid = "study:%s:%s" % (key, f.replace(".html", ""))
        h, n = re.subn(r'"words": \d+(, "readid": "%s")' % re.escape(rid), r'"words": %d\1' % w, h)
        tot += w
    h = re.sub(r'"words": \d+(, "docx": "study/%s/)' % re.escape(key), r'"words": %d\1' % tot, h)
    open(p, "w").write(h)

    cfg = dict(label="")
    bd.to_docx(full, d, os.path.join(d, f"{key}.docx"), cfg)
    if make_pdf:
        bd.to_pdf(full_p, os.path.join(d, f"{key}.pdf"))
    print(f"rebuilt {key}: {len(files)} pages, {tot} words")


main(sys.argv[1], "--no-pdf" not in sys.argv)
