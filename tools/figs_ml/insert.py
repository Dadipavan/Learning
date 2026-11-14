"""Usage: python3 insert.py chNN src_fragment.html [--practice practice_fragment.html]
Expands @@CODE name.py@@ into a python block plus its real output (from code/name.py),
inserts the fragment before the chapter's 'Chapter recap' h2, and practice items before the Prompt pack h2.
Idempotent guard: refuses if the fragment's first line is already in the chapter."""
import sys, re, subprocess, html, os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", ".."))
def expand(t):
    def rep(m):
        p = os.path.join(here, "code", m.group(1))
        code = open(p).read().rstrip("\n")
        out = subprocess.run(["python3", p], capture_output=True, text=True, cwd=os.path.join(root, "study/ml/images"))
        if out.returncode: sys.exit("FAIL " + p + out.stderr)
        o = out.stdout.rstrip("\n")
        return ('<pre class="code lang-python"><code>%s</code></pre>\n<pre class="code lang-text"><code>%s</code></pre>' % (html.escape(code, quote=False), html.escape(o, quote=False)))
    return re.sub(r"@@CODE (\S+?)@@", rep, t)
ch = sys.argv[1]; frag = expand(open(sys.argv[2]).read().strip("\n"))
path = os.path.join(root, "study/ml", ch + ".html"); s = open(path).read()
first = frag.split("\n")[0]
if first in s: sys.exit("already inserted: " + first[:60])
m = re.search(r'<h2 id="s\d+-chapter-recap">', s); assert m
s = s[:m.start()] + frag + "\n" + s[m.start():]
if "--practice" in sys.argv:
    pr = open(sys.argv[sys.argv.index("--practice") + 1]).read().strip("\n")
    m = re.search(r'<h2 id="s\d+-prompt-pack">', s); assert m
    pm = re.search(r'<h2 id="s\d+-practice-set">', s)
    sect = s[pm.end():m.start()]
    if sect.lstrip().startswith("<ol>"):   # numbered-list style practice set: append <li> items
        pr = re.sub(r'<p><strong>\d+\. \((.*?)\)</strong> (.*?)</p>', lambda q: "<li>(%s) %s</li>" % (q.group(1), q.group(2)), pr)
        k = s.rindex("</ol>", pm.end(), m.start())
        s = s[:k] + pr.replace("\n", "") + s[k:]
    else:
        s = s[:m.start()] + pr + "\n" + s[m.start():]
open(path, "w").write(s)
print("inserted into", path)
