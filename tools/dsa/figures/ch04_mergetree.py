import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
LT = {"blue": "#d6defa", "orange": "#f3d9cc", "teal": "#cfe5e0", "red": "#f1cfcc", "purple": "#e0d4f7", "grey": "#e4e4ea", "white": "#ffffff"}
plt.rcParams.update({"font.size": 14})

def cells(ax, vals, x0=0.0, y=0.0, fc=None, fs=16, idx=True, w=1.0, h=0.8):
    for i, v in enumerate(vals):
        c = LT[fc[i]] if fc and fc[i] else LT["white"]
        ax.add_patch(Rectangle((x0 + i * w, y), w, h, fc=c, ec="#333333", lw=1.5))
        ax.text(x0 + i * w + w / 2, y + h / 2, str(v), ha="center", va="center", fontsize=fs, color="#111111")
        if idx:
            ax.text(x0 + i * w + w / 2, y - 0.08, str(i), ha="center", va="top", fontsize=11, color="#666666")

def below(ax, x, y, label, color, fs=13):
    ax.annotate(label, xy=(x, y - 0.3), xytext=(x, y - 0.95), ha="center", va="top", fontsize=fs, color=color,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=color, lw=2))

def above(ax, x, y, label, color, fs=13):
    ax.annotate(label, xy=(x, y + 0.05), xytext=(x, y + 0.65), ha="center", va="bottom", fontsize=fs, color=color,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=color, lw=2))

def save(fig, name):
    fig.savefig(name, dpi=110, bbox_inches="tight", facecolor="white")
fig, ax = plt.subplots(figsize=(8, 4.8))
nodes = {
 "R": (3.25, 3, "[38,27,43,3,9,82,10]", "[3,9,10,27,38,43,82]"),
 "A": (1.5, 2, "[38,27,43,3]", "[3,27,38,43]"),
 "B": (5.0, 2, "[9,82,10]", "[9,10,82]"),
 "C": (0.5, 1, "[38,27]", "[27,38]"),
 "D": (2.5, 1, "[43,3]", "[3,43]"),
 "E": (4.0, 1, "[9]", "[9]"),
 "F": (5.75, 1, "[82,10]", "[10,82]"),
 "c1": (0, 0, "[38]", None), "c2": (1, 0, "[27]", None), "c3": (2, 0, "[43]", None),
 "c4": (3, 0, "[3]", None), "c5": (5.25, 0, "[82]", None), "c6": (6.25, 0, "[10]", None)}
edges = [("R","A"),("R","B"),("A","C"),("A","D"),("B","E"),("B","F"),("C","c1"),("C","c2"),("D","c3"),("D","c4"),("F","c5"),("F","c6")]
for a, b in edges:
    ax.plot([nodes[a][0], nodes[b][0]], [nodes[a][1] * 1.5 - 0.35, nodes[b][1] * 1.5 + 0.35], color="#888888", lw=1.5, zorder=1)
for k, (x, lv, a, b) in nodes.items():
    y = lv * 1.5
    txt = a if b is None else a + "\n" + b
    ax.text(x, y, txt, ha="center", va="center", fontsize=11, zorder=3,
            bbox=dict(boxstyle="round,pad=0.3", fc=LT["blue"] if b else LT["grey"], ec=BLUE, lw=1.5))
    if b: ax.text(x, y - 0.0, "", fontsize=1)
ax.set_xlim(-0.8, 7.2); ax.set_ylim(-0.9, 5.1); ax.axis("off")
ax.text(3.2, -0.5, "top line = split input, bottom line = merged output", ha="center", va="center", fontsize=11, color=TEAL)
ax.set_title("Merge sort: split down to size 1, then merge back up", fontsize=14)
save(fig, "dsa4_mergetree.png")
