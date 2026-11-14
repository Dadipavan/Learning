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
fig, ax = plt.subplots(figsize=(8, 4.6))
a, b = "horse", "ros"
n, m = len(a), len(b)
dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(n + 1):
    dp[i][0] = i
for j in range(m + 1):
    dp[0][j] = j
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
i, j = n, m
path = [(i, j)]
while i > 0 or j > 0:
    if i > 0 and j > 0 and a[i - 1] == b[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
        i, j = i - 1, j - 1
    elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
        i, j = i - 1, j - 1
    elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
        i -= 1
    else:
        j -= 1
    path.append((i, j))
fill = {p: TB for p in path}
fill.update({(r, 0): TO for r in range(n + 1)})
fill.update({(0, c): TO for c in range(m + 1)})
edge = {p: BLUE for p in path}
grid(ax, dp, rows=["''"] + list(a), cols=["''"] + list(b), fill=fill, edge=edge, fs=20, x0=0, cw=1.2, ch=1.0, lfs=15)
ax.text(5.6, -2.0, "orange: turning a prefix\ninto '' costs its length", fontsize=12, color=ORANGE, va="center")
ax.text(5.6, -3.7, "blue path: the edits.\nhorse -> ros costs %d" % dp[n][m], fontsize=14, color=BLUE, va="center")
finish("dsa9_edit.png", ax, (-1.2, 10.0), (-6.5, 1.2))
