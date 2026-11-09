"""Helper for generating verified SQL teaching snippets (inserted before 'Chapter recap')."""
import re, sqlite3, html, os
ROOT = "/Users/c2487352/Personal/Career/final/study/sql/"
def shop_sql():
    s = open(ROOT + "ch02.html").read()
    m = re.search(r'<pre class="code lang-sql"><code>(CREATE TABLE customers.*?)</code></pre>', s, re.S)
    return html.unescape(m.group(1))
def shop():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.executescript(shop_sql()); return db
def fmt(cur_rows, cols):
    rows = [[("NULL" if v is None else str(v)) for v in r] for r in cur_rows]
    w = [max(len(c), *(len(r[i]) for r in rows)) if rows else len(c) for i, c in enumerate(cols)]
    L = ["  ".join(c.ljust(w[i]) for i, c in enumerate(cols)), "  ".join("-" * x for x in w)]
    L += ["  ".join(r[i].ljust(w[i]) for i in range(len(cols))) for r in rows]
    return "\n".join(x.rstrip() for x in L)
def run(db, sql):
    """run statements; return text of results of every SELECT-like statement (sqlite3 -column style)"""
    out = []
    for st in split(sql):
        cur = db.execute(st)
        if cur.description:
            out.append(fmt(cur.fetchall(), [d[0] for d in cur.description]))
    return "\n".join(out)
def split(sql):
    parts, buf = [], ""
    for line in sql.split("\n"):
        buf += line + "\n"
        if sqlite3.complete_statement(buf):
            if buf.strip(): parts.append(buf.strip())
            buf = ""
    if buf.strip(): parts.append(buf.strip())
    return parts
e = lambda s: html.escape(s, quote=False)
def sql(code): return '<pre class="code lang-sql"><code>%s</code></pre>' % e(code.strip("\n"))
def text(t): return '<pre class="code lang-text"><code>%s</code></pre>' % e(t.strip("\n"))
def py(code): return '<pre class="code lang-python"><code>%s</code></pre>' % e(code.strip("\n"))
def exec_sql(db, code):
    """show sql + its real output"""
    o = run(db, code)
    return sql(code) + ("\n" + text(o) if o else "")
def P(code, t): return '<p class="problem"><span class="pl">Problem %s</span> %s</p>' % (code, t)
def steps(rows): return '<table class="steps">' + "".join("<tr><th>%s</th><td>%s</td></tr>" % r for r in rows) + "</table>"
def co(color, lab, txt): return '<div class="callout %s"><div class="lab">%s</div><div class="txt">%s</div></div>' % (color, lab, txt)
def tbl(head, rows):
    return '<div class="tablewrap"><table class="data"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        "".join("<th>%s</th>" % h for h in head), "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows))
def fig(name, alt, cap, how):
    return '<figure><img src="images/%s" alt="%s" loading="lazy"/><figcaption>%s</figcaption></figure>\n<p><strong>How to read it:</strong> %s</p>' % (name, alt, cap, how)
def qa(code, q, a): return P(code, q) + "\n<p><strong>Answer:</strong> %s</p>" % a
def insert(ch, key, body):
    """insert body before the Chapter recap h2 (replace if marker exists)"""
    path = ROOT + "ch%s.html" % ch
    s = open(path).read()
    mark_a, mark_b = "<!-- gen:%s -->" % key, "<!-- /gen:%s -->" % key
    blk = mark_a + "\n" + body.strip() + "\n" + mark_b + "\n"
    if mark_a in s:
        s = re.sub(re.escape(mark_a) + ".*?" + re.escape(mark_b) + "\n", lambda m: blk, s, flags=re.S)
    else:
        m = list(re.finditer(r'<h2 id="s\d+-chapter-recap">', s))
        assert len(m) == 1, "recap anchor"
        s = s[:m[0].start()] + blk + s[m[0].start():]
    open(path, "w").write(s)
    print("inserted", ch, key, len(re.sub(r"<[^>]+>", " ", body).split()), "words")
import subprocess, sys, tempfile
def pyrun(code):
    with tempfile.TemporaryDirectory() as d:
        f = d + "/b.py"; open(f, "w").write(code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    assert r.returncode == 0, r.stderr
    return r.stdout
def pyblock(code):
    return py(code) + "\n" + text(pyrun(code.strip("\n") + "\n"))
