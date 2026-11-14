#!/usr/bin/env python3
"""Assemble parts/*.txt into src/ch23.html. Blocks:
@@py ... @@end   run it, show code + real output
@@np ... @@end   python shown, labelled not run (no output block)
@@file LANG ... @@end   non-python listing (bash, toml, yaml, dockerfile)
Everything else is raw HTML."""
import glob, html, os, re, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
out, fails = [], 0
open("/tmp/ch23_ex.log", "w").close()
def esc(s): return html.escape(s, quote=False)
for part in sorted(glob.glob(os.path.join(here, "parts", "ch23_*.txt"))):
    lines = open(part).read().split("\n"); i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r"@@(py|np|ex|file)\s*(\S*)", l)
        if not m:
            out.append(l); i += 1; continue
        j = i + 1; body = []
        while lines[j] != "@@end": body.append(lines[j]); j += 1
        code = "\n".join(body); kind = m.group(1)
        if kind in ("py", "ex"):
            with tempfile.TemporaryDirectory() as d:
                f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
                r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=180)
            if r.returncode:
                fails += 1; print(f"FAIL {part} line {i+1}:\n{r.stderr[-800:]}", file=sys.stderr)
            out.append(f'<pre class="code lang-python"><code>{esc(code)}</code></pre>')
            if kind == "ex":
                open("/tmp/ch23_ex.log", "a").write(f"--- {os.path.basename(part)}:{i+1}\n{r.stdout}{('ERR: ' + r.stderr[-300:]) if r.stderr.strip() else ''}\n")
            elif r.stdout.strip():
                out.append(f'<pre class="code lang-text"><code>{esc(r.stdout.rstrip())}</code></pre>')
        elif kind == "np":
            out.append(f'<pre class="code lang-python norun"><code>{esc(code)}</code></pre>')
        else:
            out.append(f'<pre class="code lang-{m.group(2) or "bash"}"><code>{esc(code)}</code></pre>')
        i = j + 1
open(os.path.join(here, "src", "ch23.html"), "w").write("\n".join(out) + "\n")
print("built, failures:", fails)
