import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

fig, ax = plt.subplots(figsize=(8, 4.2))
parts = ["answer reserve", "system + examples", "history", "question", "retrieved chunks", "unused"]
cols = [R, B, O, P, T, "#cfcfcf"]
rows = {"history kept (3,000)": [800, 700, 3000, 100, 3200, 392],
        "history compressed (600)": [800, 700, 600, 100, 5600, 392]}
for y, (lab, vals) in enumerate(rows.items()):
    left = 0
    for v, c, p in zip(vals, cols, parts):
        ax.barh(y, v, left=left, color=c, edgecolor="white", label=p if y == 0 else None)
        if v >= 500: ax.text(left + v / 2, y, f"{v:,}", ha="center", va="center", color="white" if c != "#cfcfcf" else "black", fontsize=9)
        left += v
ax.set_yticks([0, 1]); ax.set_yticklabels(list(rows)); ax.invert_yaxis()
ax.set_xlim(0, 8192); ax.set_xlabel("tokens in an 8,192-token window")
ax.set_title("Same window, different packing: 8 chunks vs 14 chunks")
ax.legend(ncol=3, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.18))
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_window_budget.png", dpi=110)
