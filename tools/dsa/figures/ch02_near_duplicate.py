import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
nums = [4, 1, 2, 4, 5]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for i, v in enumerate(nums):
    f = R if v == 4 else B
    ax.add_patch(Rectangle((i * 1.2, 1), 1.0, 1.0, fc=f, ec="black", lw=1.5))
    ax.text(i * 1.2 + 0.5, 1.5, str(v), ha="center", va="center", fontsize=22, color="white", fontweight="bold")
    ax.text(i * 1.2 + 0.5, 0.6, str(i), ha="center", fontsize=14, color="#444")
arc = FancyArrowPatch((0.5, 2.05), (3 * 1.2 + 0.5, 2.05), connectionstyle="arc3,rad=-0.45", arrowstyle="<|-|>", mutation_scale=22, lw=3, color=O)
ax.add_patch(arc)
ax.text(2.0, 3.35, "same value 4 at index 0 and 3: distance 3", ha="center", fontsize=14, color=O, fontweight="bold")
ax.text(2.4, 0.0, "k = 3, distance 3 <= 3, so answer is True", ha="center", fontsize=14)
ax.text(2.4, -0.6, "keep last_seen = {4: 0, 1: 1, 2: 2}, then see 4 again at 3", ha="center", fontsize=12, color=T)
ax.set_xlim(-0.5, 6.5); ax.set_ylim(-1, 4); ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_near_duplicate.png")
