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
vals = [0, 1, 1, 2, 3, 5, 8, 13, 21]
for i, v in enumerate(vals):
    fc = TT if i in (5, 6) else ("white" if i != 7 else TB)
    cell(ax, i, 0, v, fc=fc, ec=TEAL if i in (5, 6) else (BLUE if i == 7 else "#333333"),
         lw=3 if i in (5, 6, 7) else 1.5)
    ax.text(i + 0.5, -0.4, "i=%d" % i, ha="center", va="center", fontsize=12, color="#555555")
arrow(ax, (5.5, 1.05), (7.35, 1.05), color=TEAL, rad=-0.35)
arrow(ax, (6.5, 1.05), (7.55, 1.05), color=TEAL, rad=-0.35)
ax.text(6.5, 2.3, "fib(7) = fib(6) + fib(5) = 8 + 5 = 13", ha="center", fontsize=14, color=BLUE)
ax.add_patch(Rectangle((4.9, -0.95), 2.2, 0.0, fc="none"))
ax.annotate("", xy=(5.0, -1.0), xytext=(7.0, -1.0), arrowprops=dict(arrowstyle="-", color=TEAL, lw=3))
ax.text(6.0, -1.6, "O(1) space: keep only these two (a, b)", ha="center", fontsize=13, color=TEAL)
ax.text(2.0, -2.2, "Table: keep all n + 1 boxes", ha="center", fontsize=13, color=BLUE)
finish("dsa9_fib_table.png", ax, (-0.6, 9.4), (-2.1, 3.0))
