import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(-0.5, 6)
nodes = {
 "root": (3.0, 5.2, "100"), "a": (1.0, 4.0, "a:45"), "n55": (5.0, 4.0, "55"),
 "n25": (3.2, 2.7, "25"), "n30": (7.2, 2.7, "30"), "c": (2.2, 1.4, "c:12"), "b": (4.2, 1.4, "b:13"),
 "n14": (6.2, 1.4, "14"), "d": (8.2, 1.4, "d:16"), "f": (5.5, 0.1, "f:5"), "e": (6.9, 0.1, "e:9")}
edges = [("root","a","0"),("root","n55","1"),("n55","n25","0"),("n55","n30","1"),("n25","c","0"),("n25","b","1"),
         ("n30","n14","0"),("n30","d","1"),("n14","f","0"),("n14","e","1")]
for p, c, lab in edges:
    x1, y1, _ = nodes[p]; x2, y2, _ = nodes[c]
    ax.plot([x1, x2], [y1, y2], color="black", lw=1.5, zorder=1)
    ax.text((x1 + x2) / 2 - 0.15, (y1 + y2) / 2 + 0.1, lab, color=ORANGE, fontsize=15, fontweight="bold")
for k, (x, y, t) in nodes.items():
    leaf = ":" in t
    ax.add_patch(Circle((x, y), 0.42, fc=TEAL if leaf else BLUE, ec="black", zorder=2))
    ax.text(x, y, t, ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=3)
ax.text(7.2, 5.0, "a=0  c=100  b=101\nd=111  f=1100  e=1101", fontsize=14, va="center", color="#222")
plt.tight_layout()
plt.savefig("dsa10_huffman.png", dpi=110)
