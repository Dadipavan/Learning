import re, json, os
import sys
base = os.path.abspath(sys.argv[1]) if len(sys.argv)>1 else os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(base, "doc.json")))
out = ['<p>Use this page for revision, not for first learning. Each block is the recap table of one chapter.</p>']
for ch in cfg["chapters"]:
    p = os.path.join(base, "src", f"ch{ch['num']:02d}.html")
    if not os.path.exists(p): continue
    h = open(p).read()
    m = re.search(r'<h2[^>]*>\s*Chapter recap\s*</h2>(.*?)(?=<h2)', h, re.S)
    if not m: continue
    t = re.findall(r'<div class="tablewrap">.*?</div>', m.group(1), re.S)
    out.append(f'<h2>Chapter {ch["num"]}: {ch["title"]}</h2>' + "".join(t))
open(os.path.join(base, "src", "appendix.html"), "w").write("\n".join(out))
print(len(out) - 1, "chapters in appendix")
