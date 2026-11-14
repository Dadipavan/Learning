import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

fig, ax = plt.subplots(figsize=(8, 4.2)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 52)
def box(x, y, w, h, t, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=c, ec="none", alpha=0.95))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", color="white", fontsize=9, fontweight="bold")
def arr(x1, y1, x2, y2, t="", c="#444", dy=1.5):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, color=c, lw=1.6))
    if t: ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, t, ha="center", fontsize=8, color=c)
box(2, 21, 16, 10, "build prompt\n(v3 + input)", B)
box(26, 21, 16, 10, "call model\n(temp 0)", B)
box(50, 21, 16, 10, "parse JSON\n+ schema check", O)
box(76, 36, 20, 10, "accept\n(log version)", T)
box(76, 6, 20, 10, "give up:\nquarantine row", R)
box(40, 4, 28, 9, "retry: append error\nmessage to prompt", P)
arr(18.5, 26, 25.5, 26); arr(42.5, 26, 49.5, 26); arr(66.5, 28, 75.5, 40); ax.text(66, 36, "valid", color=T, fontsize=9)
arr(66.5, 24, 75.5, 11); ax.text(70, 21, "invalid and\ntries used up", color=R, fontsize=8)
arr(58, 20.5, 54, 13.5); ax.text(59, 15.5, "invalid, tries left", color=P, fontsize=8)
arr(40, 8.5, 34, 20.5, "", P)
ax.set_title("Validate, repair, then fail gracefully")
fig.tight_layout(); fig.savefig("ch04d_repair_flow.png", dpi=110)
