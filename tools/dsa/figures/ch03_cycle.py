from ch03_common import *
from matplotlib.patches import Circle, FancyArrowPatch
pos = {1: (0, 0), 2: (1.6, 0), 3: (3.2, 0), 4: (4.6, 1.3), 5: (6.0, 0), 6: (4.6, -1.3)}
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)]
fig, ax = new_fig()
for a, b in edges:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=22, lw=2.2,
                                 color="#444444", shrinkA=20, shrinkB=20,
                                 connectionstyle="arc3,rad=0.0" if (a, b) != (6, 3) else "arc3,rad=-0.2"))
for n, (x, y) in pos.items():
    face = LIGHT[PURPLE] if n == 5 else "white"
    ax.add_patch(Circle((x, y), 0.45, fc=face, ec="#333333", lw=2))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=18)
ax.text(0, 0.9, "head", ha="center", fontsize=14, color="#555555")
ax.text(6.0, 0.85, "slow and fast\nmeet at 5", ha="center", fontsize=14, color=PURPLE, fontweight="bold")
ax.text(1.6, -1.6, "slow: 1, 2, 3, 4, 5\nfast: 1, 3, 5, 3, 5", ha="center", fontsize=14, color=BLUE)
ax.text(3.8, -2.4, "cycle: 3 to 4 to 5 to 6 to 3", ha="center", fontsize=13, color=RED)
ax.set_xlim(-0.8, 7.0); ax.set_ylim(-2.9, 2.2)
ax.set_title("Fast and slow pointers on a list with a cycle", fontsize=15)
save(fig, "dsa3_cycle.png")
