#!/usr/bin/env python3
"""Assemble ch17.html from parts/*.txt. Blocks between @@CODE and @@END are run and their output pasted."""
import glob, html, os, re, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
src = "\n".join(open(f).read() for f in sorted(glob.glob(os.path.join(here, "parts", "p*.txt"))))
def run(m):
    code = m.group(1).strip("\n")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode:
        print("FAILED BLOCK:\n", code[:300], "\n", r.stderr[-800:]); out = "ERROR"
    else: out = r.stdout.rstrip("\n")
    pass
    s = f'<pre class="code lang-python"><code>{html.escape(code, quote=False)}</code></pre>\n'
    if out.strip(): s += f'<pre class="code lang-text"><code>{html.escape(out, quote=False)}</code></pre>'
    return s
store = {}
def prun(m):
    name, code = m.group(1), m.group(2).strip("\n")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode: print("FAILED PBLOCK", name, r.stderr[-500:])
    store[name] = "\n".join(l.rstrip() for l in r.stdout.rstrip("\n").split("\n"))
    return f'<pre class="code lang-python"><code>{html.escape(code, quote=False)}</code></pre>'
src = re.sub(r"@@PCODE (\w+)\n(.*?)\n@@END", prun, src, flags=re.S)
src = re.sub(r"\{\{(\w+)\}\}", lambda m: f'<pre class="code lang-text"><code>{html.escape(store[m.group(1)], quote=False)}</code></pre>', src)
res = re.sub(r"@@CODE\n(.*?)\n@@END", run, src, flags=re.S)
open(os.path.join(here, "src", "ch17.html"), "w").write(res)
print("written", len(res.split()))
