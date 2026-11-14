#!/usr/bin/env python3
"""Builds study/analyst/ch08.html from tools/figs_analyst/ch08_src/p*.txt.
Each @@PY block is written to tools/figs_analyst/ch08_<name>.py, run from study/analyst/images,
and its real stdout is pasted under it. Run: python3 tools/figs_analyst/ch08_build.py"""
import os, re, sys, glob, json, hashlib, html, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "tools/figs_analyst/ch08_src")
FIGS = os.path.join(ROOT, "tools/figs_analyst")
IMG = os.path.join(ROOT, "study/analyst/images")
OUT = os.path.join(ROOT, "study/analyst/ch08.html")
CACHE = os.path.join(SRC, ".cache"); os.makedirs(CACHE, exist_ok=True)

HEADER = '''import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"'''
HEADER_S = '''import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"'''
ORDERS = '''rng = np.random.default_rng(8)
n = 300
category = rng.choice(["Electronics", "Home", "Fashion", "Grocery"], n, p=[0.2, 0.25, 0.3, 0.25])
mu = pd.Series({"Electronics": 7.4, "Home": 6.8, "Fashion": 6.4, "Grocery": 5.6})[category].to_numpy()
orders = pd.DataFrame({
    "date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
    "city": rng.choice(["Delhi", "Mumbai", "Pune"], n, p=[0.40, 0.35, 0.25]),
    "category": category,
    "channel": rng.choice(["App", "Web"], n, p=[0.6, 0.4]),
    "amount": np.round(rng.lognormal(mu, 0.6)).astype(int)})'''
SALES = '''sales = pd.DataFrame({
    "city":   ["Pune", "Pune", "Pune", "Mumbai", "Mumbai", "Mumbai", "Delhi", "Delhi"],
    "status": ["Delivered", "Delivered", "Returned", "Delivered", "Delivered", "Cancelled", "Delivered", "Delivered"],
    "amount": [998, 1400, 597, 1299, 1298, 450, 799, 2499]})'''
MONTHLY = '''months = pd.period_range("2024-01", "2025-06", freq="M").to_timestamp()
monthly = pd.Series([310, 295, 340, 360, 385, 400, 380, 410, 430, 470, 560, 620,
                     350, 330, 375, 405, 430, 455], index=months, name="sales_k")'''
WEEKLY = '''rng = np.random.default_rng(8)
n = 52
ad_spend = rng.uniform(20, 100, n).round(1)                                   # Rs thousand per week
visits = (900 + 25 * ad_spend + rng.normal(0, 250, n)).round()
discount = rng.uniform(0, 25, n).round(1)                                      # average discount, %
orders_n = (0.05 * visits + 0.6 * discount + rng.normal(0, 8, n)).round()
revenue_k = (0.9 * orders_n * (1 - discount / 200) + rng.normal(0, 4, n)).round(1)
returns = (0.04 * orders_n + 0.25 * discount + rng.normal(0, 2, n)).round().clip(0)
weekly = pd.DataFrame({"ad_spend": ad_spend, "visits": visits, "discount": discount,
                       "orders": orders_n, "revenue_k": revenue_k, "returns": returns})'''
SUBS = {"#WEEKLY": WEEKLY, "#H": HEADER, "#HS": HEADER_S, "#ORD": ORDERS, "#SALES": SALES, "#MONTHLY": MONTHLY}

def esc(s): return html.escape(s, quote=False)
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def run_block(name, code):
    code = "\n".join(SUBS.get(l.strip(), l) if l.strip() in SUBS else l for l in code.split("\n"))
    full = 'import matplotlib\nmatplotlib.use("Agg")\n' + code + "\n"
    open(os.path.join(FIGS, f"ch08_{name}.py"), "w").write(full)
    h = hashlib.md5(full.encode()).hexdigest()
    cf = os.path.join(CACHE, name + ".json")
    if os.path.exists(cf):
        c = json.load(open(cf))
        if c["h"] == h and all(os.path.exists(os.path.join(IMG, f)) for f in c.get("imgs", [])):
            return code, c["out"]
    before = set(os.listdir(IMG))
    r = subprocess.run([sys.executable, os.path.join(FIGS, f"ch08_{name}.py")], capture_output=True, text=True, cwd=IMG, timeout=300)
    if r.returncode:
        print(f"!! block {name} FAILED\n{r.stderr[-1500:]}"); sys.exit(1)
    out = r.stdout.rstrip("\n")
    imgs = re.findall(r"ch08v_\w+\.png", full)
    json.dump({"h": h, "out": out, "imgs": imgs}, open(cf, "w"))
    return code, out

def main():
    shell = open(os.path.join(SRC, "orig_ch08.html")).read()
    head = shell[:shell.index('<details class="toc"')]
    tail = shell[shell.index('<div class="readbtn">'):]
    body = []; toc = []; h2n = 0
    lines = []
    for f in sorted(glob.glob(os.path.join(SRC, "p*.txt"))):
        lines += open(f).read().split("\n")
    i = 0
    names = set()
    while i < len(lines):
        L = lines[i]; i += 1
        if L.startswith("@@PY ") or L.startswith("@@NORUN"):
            norun = L.startswith("@@NORUN")
            name = L.split()[1] if not norun else None
            buf = []
            while not lines[i].startswith("@@END"): buf.append(lines[i]); i += 1
            i += 1
            code = "\n".join(buf)
            if norun:
                code = "\n".join(SUBS.get(l.strip(), l) if l.strip() in SUBS else l for l in code.split("\n"))
                body.append(f'<pre class="code lang-plotly"><code>{esc(code)}</code></pre>')
            else:
                assert name not in names, name; names.add(name)
                code, out = run_block(name, code)
                body.append(f'<pre class="code lang-python"><code>{esc(code)}</code></pre>')
                body.append(f'<pre class="code lang-text"><code>{esc(out)}</code></pre>')
        elif L.startswith("@@H2 "):
            t = L[5:].strip(); h2n += 1
            sid = f"s{h2n}-{slug(t)}"; toc.append((sid, t))
            body.append(f'<h2 id="{sid}">{t}</h2>')
        elif L.startswith("@@CALL "):
            k, lab, txt = [x.strip() for x in L[7:].split("|", 2)]
            body.append(f'<div class="callout {k}"><div class="lab">{lab}</div><div class="txt">{txt}</div></div>')
        elif L.startswith("@@FIG "):
            fn, alt, cap = [x.strip() for x in L[6:].split("|", 2)]
            assert os.path.exists(os.path.join(IMG, f"ch08v_{fn}.png")), "missing image " + fn
            body.append(f'<figure><img src="images/ch08v_{fn}.png" alt="{alt}" loading="lazy"/><figcaption>{cap}</figcaption></figure>')
        elif L.startswith("@@TABLE"):
            rows = []
            while not lines[i].startswith("@@END"): rows.append([c.strip() for c in lines[i].split(" | ")]); i += 1
            i += 1
            t = "<div class=\"tablewrap\"><table class=\"data\"><thead><tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr></thead><tbody>"
            for r in rows[1:]: t += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
            body.append(t + "</tbody></table></div>")
        elif L.startswith("@@PROBLEM "):
            lab, txt = [x.strip() for x in L[10:].split("|", 1)]
            body.append(f'<p class="problem"><span class="pl">Problem {lab}</span> {txt}</p>')
        elif L.startswith("@@STEPS"):
            t = '<table class="steps">'
            while not lines[i].startswith("@@END"):
                a, b = lines[i].split(" ## ", 1); t += f"<tr><th>{a.strip()}</th><td>{b.strip()}</td></tr>"; i += 1
            i += 1; body.append(t + "</table>")
        elif L.startswith("@@Q "):
            lab, txt = [x.strip() for x in L[4:].split("|", 1)]
            body.append(f'<p class="problem"><span class="pl">Problem {lab}</span> {txt}</p>')
        elif L.startswith("@@QA "):
            lab, q, a = [x.strip() for x in L[5:].split("|", 2)]
            body.append(f'<p class="problem"><span class="pl">Problem {lab}</span> {q} <strong>Answer:</strong> {a}</p>')
        elif L.startswith("@@A "):
            body.append(f'<p><strong>Answer:</strong> {L[4:].strip()}</p>')
        elif L.startswith("@@PROMPT "):
            body.append('<div class="prompt"><div class="ph"><span>✨ AI prompt: copy and paste into any AI</span><button type="button" class="copy">Copy</button></div><pre>' + L[9:].strip() + '</pre></div>')
        else:
            body.append(L)
    tocs = '<details class="toc" open><summary>In this chapter</summary><ol>' + "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in toc) + '</ol></details>'
    open(OUT, "w").write(head + tocs + "\n".join(b for b in body if b.strip() != "") + tail)
    print("built", OUT, "h2:", h2n)
main()
