import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
s = "python"
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for i, c in enumerate(s):
    f = O if 1 <= i < 4 else B
    ax.add_patch(Rectangle((i, 1), 0.9, 0.9, fc=f, ec="black", lw=1.5))
    ax.text(i + 0.45, 1.45, c, ha="center", va="center", fontsize=24, color="white", fontweight="bold")
    ax.text(i + 0.45, 2.15, str(i), ha="center", fontsize=15, color=T, fontweight="bold")
    ax.text(i + 0.45, 0.6, str(i - 6), ha="center", fontsize=15, color=R, fontweight="bold")
ax.text(-0.2, 2.15, "index", ha="right", fontsize=13, color=T)
ax.text(-0.2, 0.6, "negative", ha="right", fontsize=13, color=R)
ax.annotate("", xy=(4.0, 2.85), xytext=(1.0, 2.85), arrowprops=dict(arrowstyle="<->", color=O, lw=2.5))
ax.text(2.5, 3.05, "s[1:4] = 'yth'  (start included, stop excluded)", ha="center", fontsize=14, color=O)
ax.text(3, 0.0, "s[-1] = 'n'     s[::-1] = 'nohtyp'", ha="center", fontsize=14)
ax.set_xlim(-2, 6.5); ax.set_ylim(-0.3, 3.6); ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_string_index.png")
