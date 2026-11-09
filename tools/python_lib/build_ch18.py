#!/usr/bin/env python3
"""Assemble tools/python_lib/parts/ch18_*.src into src/ch18.html.
@@PY ... @@END   -> python block, run, real stdout pasted as lang-text block
@@PYQ ... @@END  -> python block, run, no output block
@@NORUN ... @@END -> code shown as lang-text (not executed; library not installed)
"""
import re, subprocess, sys, tempfile, os, html, glob
here = os.path.dirname(os.path.abspath(__file__))
src = "".join(open(p).read() for p in sorted(glob.glob(os.path.join(here, "parts", "ch18_*.src"))))
def esc(s): return html.escape(s, quote=False)
def run(code):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode: sys.exit("BLOCK FAILED:\n" + code + "\n" + r.stderr)
    return r.stdout.strip()
import numpy as np
from scipy import stats, optimize, integrate, interpolate, linalg, sparse
state = {"last": ""}
def sub(m):
    if m.group(3) is not None:                    # {{=expr}}
        return esc(str(eval(m.group(3), {"np": np, "stats": stats, "optimize": optimize, "integrate": integrate, "linalg": linalg, "sparse": sparse})))
    if m.group(4) is not None:                    # {{LAST}}
        return esc(state["last"].replace("\n", " / "))
    kind, code = m.group(1), m.group(2).strip("\n")
    if kind == "NORUN":
        return '<pre class="code lang-text"><code>%s</code></pre>' % esc(code)
    out = run(code)
    state["last"] = out
    s = '<pre class="code lang-python"><code>%s</code></pre>' % esc(code)
    if kind == "PY": s += '\n<pre class="code lang-text"><code>%s</code></pre>' % esc(out)
    return s
res = re.sub(r"@@(PYQ|PY|NORUN)\n(.*?)\n@@END|\{\{=(.*?)\}\}|\{\{(LAST)\}\}", sub, src, flags=re.S)
open(os.path.join(here, "src", "ch18.html"), "w").write(res)
print("words", len(re.sub(r"<[^>]+>", " ", res).split()))
