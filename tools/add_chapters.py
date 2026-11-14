#!/usr/bin/env python3
"""Add NEW chapter pages to an existing study document from HTML fragments, then sync everything.
Usage: python3 tools/add_chapters.py tools/<dir>/new_chapters.json
JSON: {"key":"python","chapters":[{"num":16,"title":"...","sub":"...","src":"tools/python_lib/src/ch16.html","color":"#2b4fd6"}]}
Creates study/<key>/chNN.html (banner, toc, body, read button, pager placeholders) and runs the sync in rebuild_doc.py."""
import json, os, sys, importlib.util
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
spec = importlib.util.spec_from_file_location("build_doc", os.path.join(ROOT, "tools", "build_doc.py"))
bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)

cfg = json.load(open(sys.argv[1])); key = cfg["key"]
import re
idx = open(os.path.join(ROOT, "study", key, "index.html")).read()
label = re.search(r'<span class="doc">(.*?)</span>', idx).group(1)
for c in cfg["chapters"]:
    src = open(os.path.join(ROOT, c["src"])).read()
    body, toc = bd.add_ids(src)
    tocs = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc)
    num = c["num"]; rid = f"study:{key}:ch{num:02d}"
    html = (bd.head(f'Chapter {num}: {c["title"]}') + f'<body style="--accent:{c["color"]}">' + bd.topbar(label) +
            f'<div class="page"><div class="banner"><div class="eyebrow">CHAPTER {num}</div><h1>{c["title"]}</h1><p>{c["sub"]}</p></div>'
            f'<details class="toc" open><summary>In this chapter</summary><ol>{tocs}</ol></details>{body}'
            f'<div class="readbtn"><button class="btn" data-read="{rid}">Mark this chapter as read</button></div>'
            f'<div class="pager"><span></span><span></span></div></div><script src="../../assets/study.js"></script></body></html>')
    open(os.path.join(ROOT, "study", key, f"ch{num:02d}.html"), "w").write(html)
    print("created", key, num)
os.execvp(sys.executable, [sys.executable, os.path.join(ROOT, "tools", "rebuild_doc.py"), key] + sys.argv[2:])
