import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
vals = [1, 2, 3, 4, 100, 200]
xs = [0, 1.3, 2.6, 3.9, 6.6, 7.9]
starts = {1, 100, 200}
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for x, v in zip(xs, vals):
    f = T if v in starts else B
    ax.add_patch(Rectangle((x, 2), 1.1, 1.0, fc=f, ec="black", lw=1.5))
    ax.text(x + 0.55, 2.5, str(v), ha="center", va="center", fontsize=18, color="white", fontweight="bold")
for a, b in zip(xs[:3], xs[1:4]):
    ax.annotate("", xy=(b + 0.55, 3.1), xytext=(a + 0.55, 3.1), arrowprops=dict(arrowstyle="-|>", color=O, lw=2.5, connectionstyle="arc3,rad=-0.6"))
ax.text(2.2, 4.1, "n+1 is in the set: keep walking, run length 4", ha="center", fontsize=13, color=O, fontweight="bold")
ax.text(5.75, 2.5, "...", fontsize=24, ha="center", va="center")
ax.text(0.55, 1.4, "start\n(0 not in set)", ha="center", va="top", fontsize=12, color=T, fontweight="bold")
ax.text(7.15, 1.4, "start\n(99 not in set)", ha="center", va="top", fontsize=11, color=T, fontweight="bold")
ax.text(8.45, 0.5, "start\n(199 not in set)", ha="center", va="top", fontsize=11, color=T, fontweight="bold")
ax.text(2.8, -0.1, "2, 3, 4 are NOT starts: 1, 2, 3 are in the set, so skip them", ha="center", fontsize=12, color=R)
ax.set_xlim(-0.3, 9.6); ax.set_ylim(-0.8, 4.6); ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_consecutive.png")
