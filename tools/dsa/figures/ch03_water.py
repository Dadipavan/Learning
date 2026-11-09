from ch03_common import *
from matplotlib.patches import Rectangle
h = [3, 9, 2, 6, 8, 4, 7, 5]
best = max(((min(h[i], h[j]) * (j - i), i, j) for i in range(8) for j in range(i + 1, 8)))
fig, ax = new_fig(8, 4.6)
for i, v in enumerate(h):
    ax.add_patch(Rectangle((i + 0.3, 0), 0.4, v, fc="#555555", ec="none"))
    ax.text(i + 0.5, -0.5, str(i), ha="center", fontsize=12, color="#666666")
    ax.text(i + 0.5, v + 0.15, str(v), ha="center", fontsize=13)
area, bi, bj = best
ax.add_patch(Rectangle((bi + 0.5, 0), bj - bi, min(h[bi], h[bj]), fc=BLUE, alpha=0.25, ec=BLUE, lw=2))
ax.text((bi + bj) / 2 + 0.5, 11.2, f"best water = {min(h[bi], h[bj])} x {bj - bi} = {area}",
        ha="center", fontsize=14, color=BLUE, fontweight="bold")
ax.add_patch(Rectangle((0.5, 0), 7, 3, fc=ORANGE, alpha=0.18, ec=ORANGE, lw=2, ls="--"))
ax.text(0.6, 0.3, "start: L=0, R=7, 3 x 7 = 21", fontsize=12, color=ORANGE, fontweight="bold", bbox=dict(fc="white", ec="none", pad=1.5))
ax.annotate("", xy=(0.5, 9.9), xytext=(0.5, 11), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.4))
ax.text(0.5, 11.1, "L", ha="center", fontsize=15, color=ORANGE, fontweight="bold")
ax.annotate("", xy=(7.5, 5.9), xytext=(7.5, 7.1), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.4))
ax.text(7.5, 7.2, "R", ha="center", fontsize=15, color=ORANGE, fontweight="bold")
ax.set_aspect("auto"); ax.set_xlim(-0.3, 8.5); ax.set_ylim(-1, 12.2)
ax.set_title("Container with most water: width times the shorter wall", fontsize=15)
save(fig, "dsa3_water.png")
