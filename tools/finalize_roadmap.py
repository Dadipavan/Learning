#!/usr/bin/env python3
"""Add tasks for the new documents/chapters (python 16-23, dsa, ways) to the 156-week roadmap in index.html."""
import json, hashlib
p = "index.html"; h = open(p).read(); s = h.split("<script>")[-1]; i = s.find("const D = ") + 10
D, end = json.JSONDecoder().raw_decode(s[i:])
S = {x["key"]: x for x in D["study"]}; plan = {w["n"]: w for w in D["plan"]}
def add(wn, key, page, verb="Read"):
    st = S.get(key)
    if not st: return
    ch = next((c for c in st["chapters"] if c["page"] == page), None)
    if not ch: return
    text = f'{verb} {st["label"]}, {ch["label"].title()}: {ch["title"]}'
    t = plan[wn]["tasks"]
    if any(x["text"] == text for x in t): return
    j = next((k for k, x in enumerate(t) if x["href"] == "#/progress"), len(t))
    t[j:j] = [{"text": text, "href": f"study/{key}/{page}", "id": f"w{wn}:" + hashlib.md5(text.encode()).hexdigest()[:8]},
              {"text": "Do the chapter Practice set and check your answers (code every example yourself)", "href": None, "id": f"w{wn}:" + hashlib.md5((text + "p").encode()).hexdigest()[:8]}]
PY = {16: 13, 17: 16, 18: 21, 19: 54, 20: 44, 21: 83, 22: 66, 23: 30}
for c, w in PY.items(): add(w, "python", f"ch{c}.html", "Library Handbook. Read")
DSA = {1: 26, 2: 27, 3: 28, 4: 29, 5: 31, 6: 32, 7: 33, 8: 34, 9: 35, 10: 36, 11: 37, 12: 38}
for c, w in DSA.items(): add(w, "dsa", f"ch{c:02d}.html")
WAYS = {1: 14, 2: 15, 3: 16, 4: 18, 5: 22, 6: 58, 7: 98, 8: 123}
for c, w in WAYS.items(): add(w, "ways", f"ch{c:02d}.html")
D["plan"] = [plan[n] for n in sorted(plan)]
out = json.dumps(D, ensure_ascii=False).replace("</", "<\\/")
open(p, "w").write(h.replace(s, s[:i] + out + s[i + end:]))
print("roadmap updated")
