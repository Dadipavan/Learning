import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

fig, axes = plt.subplots(2, 1, figsize=(8, 5))
def draw(ax, nums, title, reach_marks):
    for i, v in enumerate(nums):
        col = TEAL if i <= reach_marks else GREY
        ax.add_patch(Rectangle((i, 0), 0.9, 0.9, fc=col, ec="black"))
        ax.text(i + 0.45, 0.45, str(v), ha="center", va="center", fontsize=18, color="white" if i <= reach_marks else "black", fontweight="bold")
        ax.text(i + 0.45, -0.35, f"i={i}", ha="center", fontsize=12)
    ax.set_xlim(-0.3, len(nums) + 0.2); ax.set_ylim(-0.8, 3.0); ax.axis("off")
    ax.set_title(title, fontsize=14)
nums1 = [2, 3, 1, 1, 4]
draw(axes[0], nums1, "[2,3,1,1,4]: furthest reach grows 2, 4, 4, 4: last index reachable", 4)
ax = axes[0]
for i, r in [(0, 2), (1, 4)]:
    ax.add_patch(FancyArrowPatch((i + 0.45, 0.95), (r + 0.45, 0.95), connectionstyle="arc3,rad=-0.3", arrowstyle="-|>", mutation_scale=18, color=BLUE, lw=2))
nums2 = [3, 2, 1, 0, 4]
draw(axes[1], nums2, "[3,2,1,0,4]: reach is stuck at 3: index 4 is never reached", 3)
ax = axes[1]
for i, r in [(0, 3), (1, 3), (2, 3)]:
    ax.add_patch(FancyArrowPatch((i + 0.45, 0.95), (r + 0.45, 0.95), connectionstyle="arc3,rad=-0.3", arrowstyle="-|>", mutation_scale=18, color=ORANGE, lw=2))
ax.text(3.45, 2.2, "wall", color=RED, ha="center", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("dsa10_jump.png", dpi=110)
