import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

fig, axes = plt.subplots(2, 1, figsize=(8, 4.6), sharex=True)
def draw(ax, ivs, cols, title):
    for k, (s, e) in enumerate(ivs):
        ax.barh(0, e - s, left=s, height=0.5, color=cols[k], ec="black", alpha=0.9)
        ax.text((s + e) / 2, 0, f"[{s},{e}]", ha="center", va="center", color="white", fontweight="bold", fontsize=13)
    ax.set_yticks([]); ax.set_ylim(-0.5, 0.5); ax.set_title(title, fontsize=14)
orig = [(1, 3), (2, 6), (8, 10), (15, 18)]
axes[0].barh(0.18, 2, left=1, height=0.3, color=BLUE, ec="black")
axes[0].text(2, 0.18, "[1,3]", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
axes[0].set_yticks([]); axes[0].set_ylim(-0.5, 0.5)
axes[0].barh(-0.18, 4, left=2, height=0.3, color=ORANGE, ec="black")
axes[0].text(4, -0.18, "[2,6]", ha="center", va="center", color="white", fontweight="bold", fontsize=13)
axes[0].barh(0, 2, left=8, height=0.5, color=TEAL, ec="black")
axes[0].text(9, 0, "[8,10]", ha="center", va="center", color="white", fontweight="bold", fontsize=13)
axes[0].barh(0, 3, left=15, height=0.5, color=PURPLE, ec="black")
axes[0].text(16.5, 0, "[15,18]", ha="center", va="center", color="white", fontweight="bold", fontsize=13)
axes[0].set_title("Sorted by start: [1,3] and [2,6] overlap because 2 <= 3", fontsize=14)
draw(axes[1], [(1, 6), (8, 10), (15, 18)], [BLUE, TEAL, PURPLE], "After merging: 3 blocks")
axes[1].set_xticks(range(0, 20, 2))
axes[1].set_xlabel("time")
plt.tight_layout()
plt.savefig("dsa10_merge.png", dpi=110)
