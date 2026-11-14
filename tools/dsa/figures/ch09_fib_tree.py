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
leaf = [0]


def build(n, d):
    node = {"n": n, "d": d, "kids": []}
    if n >= 2:
        node["kids"] = [build(n - 1, d + 1), build(n - 2, d + 1)]
        node["x"] = sum(k["x"] for k in node["kids"]) / 2
    else:
        node["x"] = leaf[0]
        leaf[0] += 1
    return node


root = build(5, 0)
order = []


def walk(nd):
    order.append(nd)
    for k in nd["kids"]:
        walk(k)


walk(root)
seen = set()
for nd in order:
    nd["rep"] = nd["n"] in seen
    seen.add(nd["n"])
for nd in order:
    for k in nd["kids"]:
        ax.plot([nd["x"], k["x"]], [-nd["d"], -k["d"]], color="#999999", lw=1.6, zorder=1)
for nd in order:
    fc, ec = (TO, ORANGE) if nd["rep"] else (TB, BLUE)
    ax.text(nd["x"], -nd["d"], "fib(%d)" % nd["n"], ha="center", va="center", fontsize=12, zorder=3,
            bbox=dict(boxstyle="round,pad=0.3", fc=fc, ec=ec, lw=2))
ax.text(3.5, -5.0, "Blue: computed for the first time.  Orange: the same work done again.",
        ha="center", fontsize=12)
ax.text(3.5, -5.6, "15 calls, but only 6 different answers (fib 0 to fib 5).", ha="center", fontsize=12, color=RED)
finish("dsa9_fib_tree.png", ax, (-0.8, 7.8), (-6.1, 0.6))
