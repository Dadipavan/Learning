#!/usr/bin/env python3
"""Check a chapter fragment: balanced tags, required parts, every python block runs standalone,
and the printed output matches the following <pre class="code lang-text"> block (if any).
Usage: python3 -I tools/check_fragment.py tools/math/src/ch01.html [--run]"""
import sys, re, subprocess, tempfile, os, html
from html.parser import HTMLParser

VOID = {"br", "img", "hr", "meta", "link", "input"}

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st = []; s.err = []; s.h2 = []; s.cls = {}
    def handle_starttag(s, t, a):
        if t in VOID: return
        s.st.append((t, s.getpos()[0]))
        c = dict(a).get("class", "")
        for k in c.split(): s.cls[k] = s.cls.get(k, 0) + 1
        if t == "h2": s.cur = ""; s.in_h2 = True
    def handle_endtag(s, t):
        if t in VOID: return
        if not s.st or s.st[-1][0] != t:
            s.err.append(f"line {s.getpos()[0]}: </{t}> closes {s.st[-1] if s.st else None}")
            for i in range(len(s.st) - 1, -1, -1):
                if s.st[i][0] == t: del s.st[i:]; break
        else: s.st.pop()
        if t == "h2": s.in_h2 = False
    def handle_data(s, d):
        if getattr(s, "in_h2", False): s.h2.append(d)

def main(path, run, loose=False, doc="math"):
    src = open(path).read()
    p = P(); p.feed(src); p.close()
    errs = list(p.err) + [f"unclosed <{t}> from line {l}" for t, l in p.st]
    text = re.sub(r"<[^>]+>", " ", src)
    n_words = len(text.split())
    print(f"words={n_words}  h2={len(p.h2)}  classes={dict(sorted(p.cls.items()))}")
    heads = " | ".join(p.h2)
    for need in (() if loose else ("recap", "practice", "prompt")):
        if need not in heads.lower(): errs.append(f"missing h2 containing '{need}'")
    if not loose and p.cls.get("problem", 0) < 10: errs.append(f"only {p.cls.get('problem',0)} practice problems (<10)")
    if not loose and p.cls.get("prompt", 0) < 3: errs.append("fewer than 3 prompts")
    if not loose and p.cls.get("callout", 0) < 6: errs.append("fewer than 6 callouts")
    for m in re.finditer(r'<img src="images/([^"]+)"', src):
        e = os.path.join(os.path.dirname(os.path.abspath(path)), "..", "..", "..", "study", doc, "images", m.group(1))
        if not os.path.exists(e): errs.append(f"image missing: {m.group(1)} (run its figure script)")
    blocks = re.findall(r'<pre class="code lang-python"><code>(.*?)</code></pre>(\s*<pre class="code lang-text"><code>(.*?)</code></pre>)?', src, re.S)
    print("python blocks:", len(blocks))
    if run:
        for i, (code, _, out) in enumerate(blocks, 1):
            code = html.unescape(code); out = html.unescape(out or "")
            with tempfile.TemporaryDirectory() as d:
                f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
                r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=120)
            if r.returncode: errs.append(f"python block {i} FAILED: {r.stderr.strip().splitlines()[-1] if r.stderr else ''}")
            elif out.strip() and r.stdout.strip() != out.strip():
                errs.append(f"python block {i}: output differs from the shown output block.\n  actual:\n    " + r.stdout.strip().replace("\n", "\n    ")[:600])
    print("OK" if not errs else "PROBLEMS:\n- " + "\n- ".join(errs))
    sys.exit(1 if errs else 0)

doc = sys.argv[sys.argv.index("--doc") + 1] if "--doc" in sys.argv else "math"
main(sys.argv[1], "--run" in sys.argv, "--loose" in sys.argv, doc)
