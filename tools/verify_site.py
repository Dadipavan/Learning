#!/usr/bin/env python3
"""Whole-site sanity checks. Usage (project root): python3 tools/verify_site.py
Checks: index.html data parses; lesson numbering; every plan/lesson link target (file + anchor) exists; resources exist;
chapter registry matches files; decks/catalog/notebook manifests are valid JS; inline + asset JavaScript passes `node --check`."""
import glob, json, os, re, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
errs, warns = [], []


def err(m):
    errs.append(m)


def anchors(path, cache={}):
    if path not in cache:
        cache[path] = set(re.findall(r'id="([^"]+)"', open(path, encoding="utf-8", errors="ignore").read()))
    return cache[path]


def check_target(where, href):
    if not href or href.startswith("#") or href.startswith("http"):
        return
    f, _, a = href.partition("#")
    p = os.path.join(ROOT, f)
    if not os.path.exists(p):
        return err(f"{where}: missing file {f}")
    if a and f.endswith(".html") and a not in anchors(p):
        err(f"{where}: anchor #{a} not in {f}")


def main():
    h = open(os.environ.get("SITE_INDEX") or os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    i = h.index("const D = ") + len("const D = ")
    D, _ = json.JSONDecoder().raw_decode(h[i:])
    res = {r["id"] for g in D["resources"] for r in g["items"]}
    n = 0
    for w in D["weeks"]:
        if w["n"] != D["weeks"].index(w) + 1:
            err(f"week numbering broken at {w['n']}")
        days = [l["day"] for l in w["lessons"]]
        if days != list(range(1, len(days) + 1)) or len(days) != 7:
            err(f"week {w['n']}: days {days}")
        for l in w["lessons"]:
            if l["n"] != n:
                err(f"lesson index {l['n']} expected {n} (week {w['n']})")
            n += 1
            if l["week"] != w["n"]:
                err(f"lesson {l['n']} week mismatch")
            for r in l.get("res", []):
                if r not in res:
                    err(f"lesson {l['n']}: unknown resource {r}")
            check_target(f"lesson {l['n']}", l.get("ch"))
            for k in ("title", "build", "ask", "learn"):
                if not l.get(k):
                    err(f"lesson {l['n']}: empty {k}")
    print("weeks", len(D["weeks"]), "lessons", n)
    for w in D["plan"]:
        ids = [t["id"] for t in w["tasks"]]
        if len(ids) != len(set(ids)):
            err(f"plan week {w['n']}: duplicate task ids")
        for t in w["tasks"]:
            check_target(f"plan week {w['n']}", t.get("href"))
    print("plan weeks", len(D["plan"]), "phases", len(D["phases"]))
    for s in D["study"]:
        for c in s["chapters"]:
            if not os.path.exists(os.path.join(ROOT, "study", s["key"], c["page"])):
                err(f"study {s['key']}: {c['page']} missing")
    # javascript syntax
    scripts = re.findall(r"<script>(.*?)</script>", h, re.S)
    for k, code in enumerate(scripts):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as t:
            t.write(code)
        r = subprocess.run(["node", "--check", t.name], capture_output=True, text=True)
        os.unlink(t.name)
        if r.returncode:
            err(f"index.html inline script {k}: {r.stderr.strip().splitlines()[-3:]}")
    for p in sorted(glob.glob(os.path.join(ROOT, "assets", "**", "*.js"), recursive=True)) + [os.path.join(ROOT, "lab.html")]:
        if not os.path.exists(p):
            continue
        if p.endswith(".html"):
            m = re.findall(r"<script>(.*?)</script>", open(p, encoding="utf-8").read(), re.S)
            code = "\n;\n".join(m)
            tmp = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False)
            tmp.write(code); tmp.close(); p2 = tmp.name
        else:
            p2 = p
        r = subprocess.run(["node", "--check", p2], capture_output=True, text=True)
        if p.endswith(".html"):
            os.unlink(p2)
        if r.returncode:
            err(f"{os.path.relpath(p, ROOT)}: {r.stderr.strip().splitlines()[:3]}")
    # referenced assets in index.html
    for m in re.findall(r'(?:src|href)="((?:assets|data)/[^"#?]+)"', h):
        if not os.path.exists(os.path.join(ROOT, m)):
            err(f"index.html references missing {m}")
    if errs:
        print(f"{len(errs)} PROBLEMS:")
        for e in errs[:80]:
            print(" -", e)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
