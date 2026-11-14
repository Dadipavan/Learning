#!/usr/bin/env python3
"""Assemble new teaching content for study/stats/chNN.html from a compact template and insert it
before 'Chapter recap' (sections) and before 'Prompt pack' (extra practice).
Always starts from the pristine copy in tools/figs_stats/orig/, so it is safe to re-run.
Usage: python3 tools/figs_stats/build_insert.py NN [--relabel]
Template macros (one per line, blank line ends multi-line macros):
  @CODE name        run snip/name.py, emit code + real output
  @P id | text      worked problem statement
  @S                steps table: following lines 'Row | text'
  @A text           practice answer paragraph
  @T                data table: following lines 'a | b | c' (first = header)
  @C colour | LABEL | text   callout
  @FIG file | alt | caption | how to read
  other lines are passed through as HTML."""
import sys, re, os, subprocess, html, tempfile
R = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(R))
E = html.escape
def runcode(name):
    code = open(f"{R}/snip/{name}.py").read().rstrip("\n")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "b.py"); open(f, "w").write("import matplotlib\nmatplotlib.use('Agg')\n" + code)
        r = subprocess.run([sys.executable, f], capture_output=True, text=True, cwd=d, timeout=300)
    if r.returncode: sys.exit(f"snippet {name} failed:\n{r.stderr}")
    out = r.stdout.rstrip("\n")
    sys.stderr.write(f"--- {name}\n{out}\n")
    return (f'<pre class="code lang-python"><code>{E(code, quote=False)}</code></pre>\n'
            f'<pre class="code lang-text"><code>{E(out, quote=False)}</code></pre>')
def render(tpl):
    lines = tpl.split("\n"); out = []; i = 0
    while i < len(lines):
        l = lines[i]; i += 1
        if l.startswith("@CODE "): out.append(runcode(l[6:].strip()))
        elif l.startswith("@P "):
            a, b = l[3:].split("|", 1)
            out.append(f'<p class="problem"><span class="pl">Problem {a.strip()}</span> {b.strip()}</p>')
        elif l.startswith("@A "): out.append(f"<p><strong>Answer:</strong> {l[3:].strip()}</p>")
        elif l.startswith("@C "):
            c, lab, t = [x.strip() for x in l[3:].split("|", 2)]
            out.append(f'<div class="callout {c}"><div class="lab">{lab}</div><div class="txt">{t}</div></div>')
        elif l.startswith("@FIG "):
            f, alt, cap, how = [x.strip() for x in l[5:].split("|", 3)]
            out.append(f'<figure><img src="images/{f}" alt="{alt}" loading="lazy"/><figcaption>{cap}</figcaption></figure>\n<p><strong>How to read it:</strong> {how}</p>')
        elif l.strip() == "@S":
            rows = []
            while i < len(lines) and lines[i].strip() and lines[i][0] not in '@<':
                a, b = lines[i].split("|", 1); rows.append(f"<tr><th>{a.strip()}</th><td>{b.strip()}</td></tr>"); i += 1
            out.append('<table class="steps">' + "".join(rows) + "</table>")
        elif l.strip() == "@T":
            rows = []
            while i < len(lines) and lines[i].strip() and lines[i][0] not in '@<':
                rows.append([x.strip() for x in lines[i].split("|")]); i += 1
            h = "".join(f"<th>{x}</th>" for x in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tablewrap"><table class="data"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
        else: out.append(l)
    return "\n".join(out)
def main(nn, relabel):
    name = "appendix" if nn == "appendix" else f"ch{nn}"
    src = open(f"{R}/orig/{name}.html").read()
    sec = f"{R}/tpl/{name}_sections.txt"; pra = f"{R}/tpl/{name}_practice.txt"
    if relabel and nn != "appendix":
        # practice labels N.k.j (k = recap number + 1) -> N.P.j to avoid clashing with new sections
        m = re.search(r'<h2 id="s\d+-practice-set">', src)
        if m:
            head, tail = src[:m.end()], src[m.end():]
            n = int(nn)
            tail = re.sub(rf'Problem {n}\.\d+\.(\d+)', rf'Problem {n}.P.\1', tail, count=0)
            src = head + tail
    if os.path.exists(sec):
        new = render(open(sec).read())
        m = re.search(r'<h2 id="s\d+-chapter-recap">', src)
        if not m: sys.exit("no recap anchor")
        src = src[:m.start()] + new + "\n" + src[m.start():]
    if os.path.exists(pra):
        new = render(open(pra).read())
        m = re.search(r'<h2 id="s\d+-prompt-pack">', src)
        if not m: sys.exit("no prompt anchor")
        src = src[:m.start()] + new + "\n" + src[m.start():]
    open(f"{ROOT}/study/stats/{name}.html", "w").write(src)
if __name__ == "__main__": main(sys.argv[1], "--relabel" in sys.argv)
