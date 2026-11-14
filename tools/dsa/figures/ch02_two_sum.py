import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
nums, target = [3, 8, 5, 2, 11], 16
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for i, v in enumerate(nums):
    f = {2: T, 4: T}.get(i, B)
    ax.add_patch(Rectangle((i * 1.3, 3), 1.1, 1.1, fc=f, ec="black", lw=1.5))
    ax.text(i * 1.3 + 0.55, 3.55, str(v), ha="center", va="center", fontsize=22, color="white", fontweight="bold")
    ax.text(i * 1.3 + 0.55, 2.65, str(i), ha="center", fontsize=14, color="#444")
ax.annotate("", xy=(4 * 1.3 + 0.55, 4.2), xytext=(4 * 1.3 + 0.55, 5.1), arrowprops=dict(arrowstyle="-|>", color=O, lw=3))
ax.text(4 * 1.3 + 0.55, 5.2, "i = 4", ha="center", fontsize=15, color=O, fontweight="bold")
ax.text(3.3, 6.0, "target = 16.  At i = 4: value 11, need 16 - 11 = 5", ha="center", fontsize=14)
ax.text(0, 1.9, "seen (value: index) before i = 4", fontsize=14, color=P, fontweight="bold")
for j, (k, v) in enumerate([(3, 0), (8, 1), (5, 2), (2, 3)]):
    c = T if k == 5 else "white"
    ax.add_patch(Rectangle((j * 1.55, 0.6), 1.4, 0.9, fc=c, ec=P, lw=2.5))
    ax.text(j * 1.55 + 0.7, 1.05, f"{k}: {v}", ha="center", va="center", fontsize=17, color="white" if k == 5 else P, fontweight="bold")
ax.text(3.3, 0.0, "5 is in seen at index 2, so the answer is [2, 4]", ha="center", fontsize=14, color=T, fontweight="bold")
ax.set_xlim(-0.3, 7); ax.set_ylim(-0.5, 6.5); ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_two_sum.png")
