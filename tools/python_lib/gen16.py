#!/usr/bin/env python3
"""Assemble src/ch16.html from src/parts/*.html. <py>code</py> blocks are run; their stdout is pasted
as the lang-text block, and the code is HTML-escaped. Not a site build tool."""
import re, sys, glob, html, subprocess, tempfile, os
here = os.path.dirname(os.path.abspath(__file__))
src = "".join(open(f).read() for f in sorted(glob.glob(here + "/src/parts/p*.html")))
bad = 0
def run(m):
    global bad
    code = m.group(1).strip("\n")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode:
        bad += 1; print("FAILED block:\n", code[:200], "\n", r.stderr[-600:], file=sys.stderr); out = "ERROR"
    else: out = r.stdout.strip("\n")
    s = f'<pre class="code lang-python"><code>{html.escape(code, quote=False)}</code></pre>\n'
    if out.strip():
        s += f'<pre class="code lang-text"><code>{html.escape(out, quote=False)}</code></pre>'
    return s
out = re.sub(r"<py>(.*?)</py>", run, src, flags=re.S)
open(here + "/src/ch16.html", "w").write(out)
print("blocks failed:", bad)
