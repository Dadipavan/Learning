#!/usr/bin/env python3
"""Fill tpl/chNN.tpl into src/chNN.html: runs @@py blocks (real output), shows @@sql/@@text blocks,
evaluates ~~expr::fmt~~ against the cleaned data namespace. Usage: python3 tools/ways/fill.py 01"""
import sys, re, os, html, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/c2487352/Personal/Career/final/study/ways/data/"
sys.path.insert(0, DATA)
import numpy as np, pandas as pd, prep, sqlite3
o, c, p = prep.load_clean(DATA)
raw, _, _ = prep.load_raw(DATA)
ns = dict(np=np, pd=pd, o=o, c=c, p=p, raw=raw, DATA=DATA, con=prep.clean_db(DATA))
extra = os.path.join(HERE, "ns_extra.py")
if os.path.exists(extra): exec(open(extra).read(), ns)
def run(code):
    full = "import matplotlib\nmatplotlib.use('Agg')\n" + code
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write(full)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode: raise SystemExit("BLOCK FAILED:\n" + code + "\n" + r.stderr[-800:])
    return r.stdout.strip()
def pre(lang, txt): return f'<pre class="code lang-{lang}"><code>{html.escape(txt, quote=False)}</code></pre>'
def main(n):
    s = open(os.path.join(HERE, "tpl", f"ch{n}.tpl")).read()
    def block(m):
        kind, arg, body = m.group(1), m.group(2).strip(), m.group(3).strip("\n")
        if kind in ("red", "blue", "green", "cream"):
            lab = {"red": "COMMON MISTAKE", "blue": "INTUITION", "green": "KEY IDEA", "cream": "REAL JOB"}[kind]
            if body.startswith("["): lab, body = body[1:].split("] ", 1)
            return f'<div class="callout {kind}"><div class="lab">{lab}</div><div class="txt">{body}</div></div>'
        if kind == "prompt":
            return ('<div class="prompt"><div class="ph"><span>\u2728 AI prompt: copy and paste into any AI</span>'
                    '<button type="button" class="copy">Copy</button></div><pre>' + html.escape(body, quote=False) + '</pre></div>')
        if kind == "steps":
            rows = "".join(f"<tr><th>{a.strip()}</th><td>{b.strip()}</td></tr>" for a, b in (l.split("|", 1) for l in body.split("\n")))
            return f'<table class="steps">{rows}</table>'
        if kind == "table":
            ls = [[x.strip() for x in l.split("|")] for l in body.split("\n")]
            th = "".join(f"<th>{x}</th>" for x in ls[0]); tb = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in ls[1:])
            return f'<div class="tablewrap"><table class="data"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'
        if kind == "python-not-run":
            return pre("pyshown", body + "\n# not run here")
        if kind == "prob":
            return f'<p class="problem"><span class="pl">Problem {arg}</span> {body}</p>'
        if kind == "qa":
            out = []
            for k, (q, a) in enumerate(re.findall(r"Q: (.*?)\nA: (.*?)(?=\nQ: |\Z)", body, re.S), 1):
                out.append(f'<p class="problem"><span class="pl">Problem {arg}.{k}</span> {q}</p>\n<p><strong>Answer:</strong> {a}</p>')
            return "\n".join(out)
        if kind == "py":
            code = f'DATA = "{DATA}"\n' + body
            out = run(code)
            return pre("python", code) + ("\n" + pre("text", out) if out else "")
        return pre(kind, body)
    def ev(m):
        t = m.group(1)
        mm = re.match(r"(.*?)::?([,.\d]*[fd%]?)$", t) if re.search(r":[,.\d]*[fd%]?$", t) and not t.endswith("[:") else None
        e, f = (mm.group(1), mm.group(2)) if mm else (t, "")
        v = eval(e, ns)
        return format(v, f) if f else str(v)
    s = re.sub(r"~~(.*?)~~", ev, s)
    s = re.sub(r"^@@([\w-]+)([^\n]*)\n(.*?)\n@@$", block, s, flags=re.S | re.M)
    open(os.path.join(HERE, "src", f"ch{n}.html" if n.isdigit() else f"{n}.html"), "w").write(s)
    print("written", n)
main(sys.argv[1])
