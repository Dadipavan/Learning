#!/usr/bin/env python3
"""Assemble src/parts/*.txt into src/ch19.html. Blocks:
@@PY ... @@END   -> run, show code + real output
@@NORUN ... @@END -> show code only (not run)
@@TXT ... @@END  -> plain text block
Usage: python3 tools/python_lib/gen19.py [--show]"""
import re, sys, os, glob, html, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
base = os.path.dirname(os.path.abspath(__file__))
src = "\n".join(open(f).read() for f in sorted(glob.glob(base + "/src/parts/*.txt")))
pat = re.compile(r"@@(PY|NORUN|TXT|QPY)\n(.*?)\n@@END", re.S)
items = list(pat.finditer(src))
def run(code):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode: return "ERROR: " + r.stderr.strip()
    return r.stdout.strip()
with ThreadPoolExecutor(4) as ex:
    outs = list(ex.map(lambda m: run(m.group(2)) if m.group(1) in ("PY", "QPY") else None, items))
res = {}; i = 0; bad = 0; qouts = []
def rep(m):
    global i, bad
    kind, code = m.group(1), m.group(2); out = outs[i]; i += 1
    e = html.escape(code, quote=False)
    if kind == "TXT": return f'<pre class="code lang-text"><code>{e}</code></pre>'
    if kind == "QPY":
        if out.startswith("ERROR"):
            bad += 1; print("BLOCK", i, out[-600:])
        qouts.append(out)
        return f'<pre class="code lang-python norun"><code>{e}</code></pre>'
    if kind == "NORUN": return f'<pre class="code lang-python norun"><code>{e}</code></pre>'
    s = f'<pre class="code lang-python"><code>{e}</code></pre>'
    if out.startswith("ERROR"):
        bad += 1; print("BLOCK", i, out[-600:]); 
    if out: s += f'\n<pre class="code lang-text"><code>{html.escape(out, quote=False)}</code></pre>'
    if "--show" in sys.argv: print(f"--- block {i} ---\n{code}\n>>>\n{out}\n")
    return s
final = pat.sub(rep, src)
for o in qouts:
    assert '[[OUT]]' in final, 'missing [[OUT]]'
    final = final.replace('[[OUT]]', f'<pre class="code lang-text"><code>{html.escape(o, quote=False)}</code></pre>', 1)
assert '[[OUT]]' not in final, 'extra [[OUT]]'
open(base + "/src/ch19.html", "w").write(final)
print("blocks", len(items), "errors", bad)
