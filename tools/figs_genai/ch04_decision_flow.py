import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

fig, ax = plt.subplots(figsize=(8, 4.2)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 56)
def box(x, y, w, h, t, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=c, ec="none"))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
def arr(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color="#444", lw=1.4))
box(35, 46, 30, 8, "Define one failing case\nand the metric", B)
box(2, 28, 22, 10, "Format wrong?\nschema, examples,\nvalidate + retry", O)
box(27, 28, 22, 10, "Reasoning wrong?\nCoT, decompose,\ncode for maths", T)
box(52, 28, 22, 10, "Facts invented?\ngrounding, quotes,\nretrieve, check", R)
box(77, 28, 21, 10, "Too big or slow?\ntrim, cache,\nsmaller model", P)
box(10, 8, 36, 10, "Change ONE thing,\nrerun the dev eval set", B)
box(54, 8, 36, 10, "Better beyond the margin of\nerror? Check held-out set", B)
for x in [13, 38, 63, 87.5]: arr(50, 45.5, x, 38.6)
for x in [13, 38]: arr(x, 27.5, 28 if x == 13 else 32, 18.6)
for x in [63, 87.5]: arr(x, 27.5, 28, 18.6) if False else None
arr(63, 27.5, 40, 18.6); arr(87.5, 27.5, 46, 16)
arr(46.5, 13, 53.5, 13)
ax.set_title("Prompt problem decision flow")
fig.tight_layout(); fig.savefig("ch04d_decision_flow.png", dpi=110)
