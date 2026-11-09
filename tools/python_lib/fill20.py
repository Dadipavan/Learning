#!/usr/bin/env python3
"""Assemble parts20/p*.html into src/ch20.html: escape code blocks, run python blocks, paste real output.
Markers: output placeholder  <pre class="code lang-text"><code>@@</code></pre>  (right after a python block)
         '# id: name' first line in a python block stores its stdout; '@@name@@' in later text inserts it inline."""
import re, subprocess, sys, tempfile, os, glob, html
here = os.path.dirname(os.path.abspath(__file__))
src = "".join(open(p).read() for p in sorted(glob.glob(os.path.join(here, "parts20", "p*.html"))))
blk = re.compile(r'<pre class="code (lang-python|lang-text)"><code>(.*?)</code></pre>', re.S)
saved = {}
out, pos, last_run = [], 0, None
def run(code):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py")
        open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=180)
    if r.returncode:
        print("FAILED block:\n", code[:300], "\n", r.stderr[-600:]); sys.exit(1)
    return r.stdout.strip()
for m in blk.finditer(src):
    out.append(src[pos:m.start()]); pos = m.end()
    kind, body = m.group(1), html.unescape(m.group(2))
    if kind == "lang-python":
        mid = re.match(r"# id: (\w+)\n", body)
        stdout = run(body)
        if mid: saved[mid.group(1)] = stdout; body = body[mid.end():]
        last_run = stdout
        out.append(f'<pre class="code lang-python"><code>{html.escape(body, quote=False)}</code></pre>')
    else:
        if body.strip() == "@@":
            assert last_run is not None
            out.append(f'<pre class="code lang-text"><code>{html.escape(last_run, quote=False)}</code></pre>'); last_run = None
        else:
            last_run = None
            out.append(f'<pre class="code lang-text"><code>{html.escape(body, quote=False)}</code></pre>')
out.append(src[pos:])
res = "".join(out)
def inline(m):
    return html.escape(saved[m.group(1)].replace("\n", " / "), quote=False)
res = re.sub(r"@@(\w+)@@", inline, res)
open(os.path.join(here, "src", "ch20.html"), "w").write(res)
print("written", len(res))
