import re, subprocess, sys, os, tempfile, html, glob
parts = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch06_part*.txt")))
src = "".join(open(p).read() for p in parts)
def run(code):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write(code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=120)
    if r.returncode:
        print("FAILED block:\n", code[:300], "\n", r.stderr[-800:]); sys.exit(1)
    return r.stdout
def sub(m):
    code = m.group(1).strip("\n")
    out = run(code + "\n").strip("\n")
    e = lambda s: html.escape(s, quote=False)
    return f'<pre class="code lang-python"><code>{e(code)}</code></pre>\n<pre class="code lang-text"><code>{e(out)}</code></pre>'
hidden = {}
def subh(m):
    key = m.group(1); code = m.group(2).strip("\n")
    hidden[key] = run(code + "\n").strip("\n")
    return f'<pre class="code lang-python"><code>{html.escape(code, quote=False)}</code></pre>'
def show(m):
    return f'<pre class="code lang-text"><code>{html.escape(hidden[m.group(1)], quote=False)}</code></pre>'
res = re.sub(r"@@PYH (\w+)\n(.*?)\n@@END", subh, src, flags=re.S)
res = re.sub(r"@@SHOW (\w+)", show, res)
res = re.sub(r"@@PY\n(.*?)\n@@END", sub, res, flags=re.S)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "ch06.html"), "w").write(res)
print("built")
