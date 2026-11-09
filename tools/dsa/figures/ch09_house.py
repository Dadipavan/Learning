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
money = [2, 7, 9, 3, 1]
best = []
for i, m in enumerate(money):
    best.append(max(best[i - 1] if i >= 1 else 0, (best[i - 2] if i >= 2 else 0) + m))
for i in range(5):
    cell(ax, i * 1.3, 1.4, money[i], fc=TO, ec=ORANGE, w=1.1)
    cell(ax, i * 1.3, 0, best[i], fc=TT if i == 4 else ("white" if i != 2 else TB), ec=TEAL if i == 4 else (BLUE if i == 2 else "#333333"),
         w=1.1, lw=3 if i in (2, 4) else 1.5)
    ax.text(i * 1.3 + 0.55, 2.7, "house %d" % i, ha="center", fontsize=12, color="#555555")
ax.text(-0.2, 1.9, "money", ha="right", va="center", fontsize=13, color=ORANGE)
ax.text(-0.2, 0.5, "best", ha="right", va="center", fontsize=13, color=BLUE)
arrow(ax, (0.55, -0.05), (3.4, -0.05), color=ORANGE, rad=0.3)
arrow(ax, (1.85, -0.05), (3.0, -0.05), color=BLUE, rad=0.6)
ax.text(1.55, -1.9, "take house 2: best[0] + 9 = 11", ha="center", fontsize=12, color=ORANGE)
ax.text(1.8, -2.5, "skip house 2: best[1] = 7", ha="center", fontsize=12, color=BLUE)
ax.text(5.0, -1.75, "best[2] = max(7, 11) = 11\nanswer = best[4] = 12", ha="left", fontsize=13)
finish("dsa9_house.png", ax, (-1.6, 7.2), (-3.0, 3.2))
