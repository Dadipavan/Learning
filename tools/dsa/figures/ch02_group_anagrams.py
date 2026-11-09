import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
cmap = {"aet": B, "ant": O, "abt": T}
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ys = {}
for i, w in enumerate(words):
    y = 5 - i * 0.95
    k = "".join(sorted(w)); c = cmap[k]
    ax.add_patch(Rectangle((0, y), 1.3, 0.7, fc=c, ec="black", lw=1.5))
    ax.text(0.65, y + 0.35, w, ha="center", va="center", fontsize=17, color="white", fontweight="bold")
    ax.annotate("", xy=(3.3, y + 0.35), xytext=(1.35, y + 0.35), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.5))
    ax.text(3.35, y + 0.35, k, ha="left", va="center", fontsize=17, color=c, fontweight="bold")
ax.text(0.65, 6.1, "word", ha="center", fontsize=14); ax.text(3.6, 6.1, "key = sorted letters", ha="center", fontsize=14)
ax.text(7.0, 6.1, "groups", ha="center", fontsize=14)
groups = {"aet": ["eat", "tea", "ate"], "ant": ["tan", "nat"], "abt": ["bat"]}
y = 4.8
for k, g in groups.items():
    ax.add_patch(Rectangle((5.0, y), 3.9, 0.9, fc="white", ec=cmap[k], lw=3))
    ax.text(6.95, y + 0.45, str(g).replace("'", ""), ha="center", va="center", fontsize=16, color=cmap[k], fontweight="bold")
    y -= 1.5
ax.set_xlim(-0.3, 9.2); ax.set_ylim(-0.2, 6.6); ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_group_anagrams.png")
