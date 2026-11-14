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
s = "AXBYBA"
n = len(s)
dp = [[0] * n for _ in range(n)]
for i in range(n - 1, -1, -1):
    dp[i][i] = 1
    for j in range(i + 1, n):
        if s[i] == s[j]:
            dp[i][j] = dp[i + 1][j - 1] + 2
        else:
            dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
data = [[dp[i][j] if j >= i else None for j in range(n)] for i in range(n)]
pal = [TB, TT, TO, TP, TR, "#eeeeee"]
fill = {(i, j): pal[(j - i) % 6] for i in range(n) for j in range(n) if j >= i}
edge = {(0, n - 1): BLUE}
grid(ax, data, rows=["i=%d '%s'" % (i, s[i]) for i in range(n)], cols=["j=%d '%s'" % (j, s[j]) for j in range(n)],
     fill=fill, edge=edge, fs=18, x0=1.8, cw=1.15, ch=0.95, lfs=11)
ax.text(8.9, -1.7, "each colour = one\ninterval length;\nfill the diagonals\nshort to long", fontsize=12, va="center")
ax.text(8.9, -4.6, "answer dp[0][5] = %d\n(ABYBA)" % dp[0][n - 1], fontsize=13, color=BLUE, va="center")
finish("dsa9_interval.png", ax, (-1.0, 11.8), (-6.4, 1.0))
