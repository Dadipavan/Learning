from ch12_common import *
pos = {"[]": (4, 3.2), "[1]": (1.5, 2.0), "[2]": (4.5, 2.0), "[3]": (7, 2.0),
       "[1,2]": (0.7, 0.8), "[1,3]": (2.6, 0.8), "[2,3]": (4.5, 0.8), "[1,2,3]": (0.7, -0.4)}
E = [("[]","[1]"),("[]","[2]"),("[]","[3]"),("[1]","[1,2]"),("[1]","[1,3]"),("[2]","[2,3]"),("[1,2]","[1,2,3]")]
fig, ax = plt.subplots(figsize=(8, 4.4)); ax.axis("off"); ax.set_xlim(-0.8, 8.2); ax.set_ylim(-1.2, 3.9)
for a, b in E: line(ax, pos[a], pos[b], r=0.3)
for k, p in pos.items():
    ax.add_patch(FancyBboxPatch((p[0]-0.55, p[1]-0.3), 1.1, 0.6, boxstyle="round,pad=0.03", fc="white", ec=B if len(k) < 6 else O, lw=2.5, zorder=3))
    ax.text(p[0], p[1], k, ha="center", va="center", fontsize=14, fontweight="bold", zorder=4)
ax.text(5.4, 3.0, "Every node IS an answer.\nA child adds one later number.", fontsize=13, color=T, fontweight="bold")
ax.text(5.4, -0.2, "8 nodes = 2^3 subsets", fontsize=14, color=R, fontweight="bold")
ax.set_title("Backtracking for subsets of [1, 2, 3]", fontsize=15)
plt.tight_layout(); plt.savefig("dsa12_subsets.png", dpi=110)
