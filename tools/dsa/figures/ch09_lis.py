import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
TB, TO, TT, TR, TP = "#dfe6fb", "#f6e3da", "#d9ece8", "#f3d9d7", "#e6dcf8"


def cell(ax, x, y, txt, fc="white", ec="#333333", w=1.0, h=1.0, fs=16, color="black", bold=False, lw=1.5):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal")


def arrow(ax, p, q, color=BLUE, rad=0.0, lw=2.4, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=20, color=color, lw=lw,
                                 connectionstyle="arc3,rad=%s" % rad, shrinkA=0, shrinkB=0))


def grid(ax, data, rows=None, cols=None, fill=None, edge=None, fs=15, x0=0.0, y0=0.0, cw=1.0, ch=1.0, lfs=13):
    """Draw a table. Data row r sits at y0 - (r+1)*ch. fill/edge map (r, c) to a colour."""
    fill = fill or {}
    edge = edge or {}
    for r, row in enumerate(data):
        for c, v in enumerate(row):
            if v is None:
                continue
            e = edge.get((r, c))
            cell(ax, x0 + c * cw, y0 - (r + 1) * ch, str(v), fc=fill.get((r, c), "white"),
                 ec=e or "#333333", w=cw, h=ch, fs=fs, lw=3.6 if e else 1.5)
    if cols:
        for c, t in enumerate(cols):
            ax.text(x0 + c * cw + cw / 2, y0 + 0.35 * ch, str(t), ha="center", va="center", fontsize=lfs, color="#555555")
    if rows:
        for r, t in enumerate(rows):
            ax.text(x0 - 0.15 * cw, y0 - (r + 1) * ch + ch / 2, str(t), ha="right", va="center", fontsize=lfs, color="#555555")


def finish(name, ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(name, dpi=110)
fig, ax = plt.subplots(figsize=(8, 4.2))
a = [10, 9, 2, 5, 3, 7, 101, 18]
dp = [1] * len(a)
for i in range(len(a)):
    for j in range(i):
        if a[j] < a[i]:
            dp[i] = max(dp[i], dp[j] + 1)
chain = [2, 3, 5, 6]
for i, v in enumerate(a):
    ch = i in chain
    cell(ax, i * 1.2, 1.5, v, fc=TT if ch else "white", ec=TEAL if ch else "#333333", w=1.1, lw=3 if ch else 1.5, fs=15)
    cell(ax, i * 1.2, 0, dp[i], fc=TB if ch else "white", ec=BLUE if ch else "#333333", w=1.1, lw=3 if ch else 1.5, fs=15)
for p, q in zip(chain, chain[1:]):
    arrow(ax, (p * 1.2 + 0.55, 2.7), (q * 1.2 + 0.55, 2.7), color=TEAL, rad=-0.5)
ax.text(-0.2, 2.0, "value", ha="right", va="center", fontsize=13, color=TEAL)
ax.text(-0.2, 0.5, "dp", ha="right", va="center", fontsize=13, color=BLUE)
ax.text(5.0, -0.9, "dp[i] = length of the longest rising chain that ENDS at i", ha="center", fontsize=13)
ax.text(5.0, -1.6, "chain 2 -> 5 -> 7 -> 101 has length 4 = max(dp)", ha="center", fontsize=13, color=TEAL)
finish("dsa9_lis.png", ax, (-1.6, 10.2), (-2.2, 4.2))
