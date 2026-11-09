#!/usr/bin/env python3
"""Assemble tpl/ch21_*.tpl into src/ch21.html, running %%PY blocks to paste real output.
%%PY ... %%END   runnable python (output pasted)
%%NORUN ... %%END  code not run here (class lang-torch)
%%ERR ... %%END   plain text block (class lang-text, only after a prose line)"""
import glob, html, os, subprocess, sys, tempfile, re
here = os.path.dirname(os.path.abspath(__file__))
out = []
cache_bad = []
for f in sorted(glob.glob(os.path.join(here, "tpl", "ch21_*.tpl"))):
    lines = open(f).read().split("\n"); i = 0; buf = []
    while i < len(lines):
        l = lines[i]
        if l.strip() in ("%%PY", "%%NORUN", "%%ERR"):
            kind = l.strip(); j = i + 1; code = []
            while lines[j].strip() != "%%END": code.append(lines[j]); j += 1
            code = "\n".join(code)
            esc = html.escape(code, quote=False)
            if kind == "%%PY":
                with tempfile.TemporaryDirectory() as d:
                    p = os.path.join(d, "b.py")
                    open(p, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
                    r = subprocess.run([sys.executable, p], capture_output=True, text=True, cwd=d, timeout=300)
                if r.returncode:
                    cache_bad.append(f"{os.path.basename(f)}:{i+1}: {r.stderr.strip().splitlines()[-1]}")
                o = html.escape(r.stdout.strip("\n"), quote=False)
                buf.append(f'<pre class="code lang-python"><code>{esc}</code></pre>')
                if o.strip(): buf.append(f'<pre class="code lang-text"><code>{o}</code></pre>')
            elif kind == "%%NORUN":
                buf.append(f'<pre class="code lang-torch"><code>{esc}</code></pre>')
            else:
                buf.append(f'<pre class="code lang-text"><code>{esc}</code></pre>')
            i = j + 1
        else:
            buf.append(l); i += 1
    out.append("\n".join(buf))
open(os.path.join(here, "src", "ch21.html"), "w").write("\n".join(out) + "\n")
print("built; failures:", *cache_bad, sep="\n  " if cache_bad else " none")
