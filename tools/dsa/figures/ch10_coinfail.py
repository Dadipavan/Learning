import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
def coin(x, y, v, c):
    ax.add_patch(Circle((x, y), 0.45, color=c, ec="black"))
    ax.text(x, y, str(v), ha="center", va="center", color="white", fontsize=18, fontweight="bold")
ax.text(5, 5.5, "Coins {1, 3, 4}, make 6", ha="center", fontsize=17, fontweight="bold")
ax.text(0.2, 4.0, "Greedy\n(biggest first)", fontsize=14, va="center")
for i, v in enumerate([4, 1, 1]):
    coin(4.0 + i * 1.1, 4.0, v, RED)
ax.text(7.7, 4.0, "3 coins", fontsize=15, va="center", color=RED, fontweight="bold")
ax.text(0.2, 2.2, "Best\n(found by DP)", fontsize=14, va="center")
for i, v in enumerate([3, 3]):
    coin(4.0 + i * 1.1, 2.2, v, TEAL)
ax.text(7.7, 2.2, "2 coins", fontsize=15, va="center", color=TEAL, fontweight="bold")
ax.text(5, 0.8, "Taking 4 first locks you out of 3 + 3.", ha="center", fontsize=14)
plt.tight_layout()
plt.savefig("dsa10_coinfail.png", dpi=110)
