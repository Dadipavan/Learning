"""Insert a teaching fragment into a dl chapter. Usage: dl_add.py chNN main.html [practice.html]
Python blocks in the fragment are executed and the real output replaces @@OUT@@ in the following lang-text block.
Main fragment goes before the 'Chapter recap' h2; practice fragment before the 'Prompt pack' h2."""
import re, sys, subprocess, html, tempfile, os
ch, main = sys.argv[1], sys.argv[2]
prac = sys.argv[3] if len(sys.argv) > 3 else None
path = f"/Users/c2487352/Personal/Career/final/study/dl/{ch}.html"
def fill(frag):
    pat = re.compile(r'(<pre class="code lang-python"><code>)(.*?)(</code></pre>\s*<pre class="code lang-text"><code>)@@OUT@@(</code></pre>)', re.S)
    def rep(m):
        code = html.unescape(m.group(2))
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "s.py"); open(f, "w").write(code)
            r = subprocess.run(["python3", f], capture_output=True, text=True, cwd=d)
        if r.returncode: sys.exit("FAILED:\n" + code + r.stderr)
        return m.group(1) + m.group(2) + m.group(3) + html.escape(r.stdout.rstrip("\n"), quote=False) + m.group(4)
    return pat.sub(rep, frag)
s = open(path).read()
def ins(s, frag, marker_re):
    m = re.search(marker_re, s)
    if not m: sys.exit("marker not found " + marker_re)
    return s[:m.start()] + fill(open(frag).read()).rstrip("\n") + "\n" + s[m.start():]
s = ins(s, main, r'<h2 id="[^"]*chapter-recap">')
if prac: s = ins(s, prac, r'<h2 id="[^"]*prompt-pack">')
assert "@@OUT@@" not in s
open(path, "w").write(s)
print("ok")
