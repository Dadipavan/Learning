#!/usr/bin/env python3
"""Assemble parts/*.html into src/ch22.html. <py>code</py> is run and its output pasted;
<py quiet> is shown with no output block; <np> is shown labelled not-run; <txt> is a static text block."""
import re, glob, html, subprocess, sys, tempfile, os
here = os.path.dirname(os.path.abspath(__file__))
src = "\n".join(open(f).read() for f in sorted(glob.glob(here + "/parts/*.html")))
esc = lambda s: html.escape(s.strip("\n"), quote=False)
def run(code):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode: sys.exit("FAILED:\n" + code[:300] + "\n" + r.stderr[-800:])
    return r.stdout.strip("\n")
def py(m):
    code = m.group(2)
    out = f'\n<pre class="code lang-text"><code>{esc(run(code))}</code></pre>' if not m.group(1) else ""
    return f'<pre class="code lang-python"><code>{esc(code)}</code></pre>{out}'
src = re.sub(r"<py( quiet)?>(.*?)</py>", py, src, flags=re.S)
src = re.sub(r"<np>(.*?)</np>", lambda m: f'<pre class="code lang-python notrun"><code># NOT RUN HERE (library not installed)\n{esc(m.group(1))}</code></pre>', src, flags=re.S)
src = re.sub(r"<txt>(.*?)</txt>", lambda m: f'<pre class="code lang-text"><code>{esc(m.group(1))}</code></pre>', src, flags=re.S)
open(here + "/src/ch22.html", "w").write(src)
print("written", len(src.split()))
