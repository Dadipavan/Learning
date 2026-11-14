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
fig, ax = plt.subplots(figsize=(8, 4.0))
g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
R = C = 3
dp = [[0] * C for _ in range(R)]
for r in range(R):
    for c in range(C):
        opts = ([dp[r - 1][c]] if r else []) + ([dp[r][c - 1]] if c else [])
        best = min(opts, default=0)
        dp[r][c] = g[r][c] + best
r, c = R - 1, C - 1
path = [(r, c)]
while (r, c) != (0, 0):
    if r == 0:
        c -= 1
    elif c == 0:
        r -= 1
    elif dp[r - 1][c] <= dp[r][c - 1]:
        r -= 1
    else:
        c -= 1
    path.append((r, c))
fill = {p: TT for p in path}
edge = {p: TEAL for p in path}
grid(ax, g, rows=["r0", "r1", "r2"], cols=["c0", "c1", "c2"], fill={p: TO for p in path}, edge={p: ORANGE for p in path}, fs=20, cw=1.2, ch=1.1)
grid(ax, dp, rows=None, cols=["c0", "c1", "c2"], fill=fill, edge=edge, fs=20, x0=5.0, cw=1.2, ch=1.1)
ax.text(1.8, 1.5, "cost grid", ha="center", fontsize=14, color=ORANGE)
ax.text(6.8, 1.5, "dp = cheapest total to reach the cell", ha="center", fontsize=14, color=TEAL)
ax.text(6.8, -4.1, "walk back from the corner: 7 -> 6 -> 5 -> 4 -> 1", ha="center", fontsize=12)
finish("dsa9_grid_cost.png", ax, (-1.2, 9.6), (-4.6, 2.2))
