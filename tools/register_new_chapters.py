#!/usr/bin/env python3
"""Register the new chapters written in tools/new_chapters/ with their study documents.

Usage (from the project root):  python3 tools/register_new_chapters.py [--no-pdf] [key ...]
For every meta_<key>_chNN.json whose fragment exists, writes tools/new_chapters/add_<key>.json and runs
tools/add_chapters.py (creates study/<key>/chNN.html, then rebuilds index tiles, pager, full.html, .docx, .pdf and the registry).
Run it only when no other process is editing index.html. Safe to re-run (the page is simply regenerated)."""
import glob, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main(args):
    no_pdf = "--no-pdf" in args
    only = [a for a in args if not a.startswith("--")]
    groups = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "tools", "new_chapters", "meta_*_ch*.json"))):
        m = json.load(open(p, encoding="utf-8"))
        src = f"tools/new_chapters/{m['key']}_ch{m['num']:02d}.html"
        if not os.path.exists(os.path.join(ROOT, src)):
            print("skip (no fragment):", src)
            continue
        if only and m["key"] not in only:
            continue
        groups.setdefault(m["key"], []).append({"num": m["num"], "title": m["title"], "sub": m["sub"], "src": src, "color": m["color"]})
    for key, chs in groups.items():
        cfg = os.path.join(ROOT, "tools", "new_chapters", f"add_{key}.json")
        json.dump({"key": key, "chapters": sorted(chs, key=lambda c: c["num"])}, open(cfg, "w"), indent=1)
        cmd = [sys.executable, os.path.join(ROOT, "tools", "add_chapters.py"), cfg] + (["--no-pdf"] if no_pdf else [])
        print("==>", " ".join(cmd))
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode:
            print("FAILED for", key)
            sys.exit(r.returncode)


if __name__ == "__main__":
    main(sys.argv[1:])
