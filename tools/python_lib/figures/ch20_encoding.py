import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

text = "café déjà vu, Zürich, naïve"
encs = ["ascii", "latin-1", "utf-8", "utf-16", "utf-32"]
sizes = []
for e in encs:
    try:
        sizes.append(len(text.encode(e)))
    except UnicodeEncodeError:
        sizes.append(0)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
cols = [R if s == 0 else B for s in sizes]
bars = ax.bar(encs, [max(s, 0.5) for s in sizes], color=cols)
for b, s, e in zip(bars, sizes, encs):
    ax.text(b.get_x() + b.get_width() / 2, max(s, 0.5), "fails" if s == 0 else f"{s} bytes", ha="center", va="bottom")
ax.set_ylabel(f"bytes for a {len(text)}-character string")
ax.set_title("Same text, different bytes: you must pick the right codec")
fig.tight_layout(); fig.savefig("lib20_encoding.png")
