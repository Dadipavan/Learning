import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 14, "font.family": "DejaVu Sans"})

def layout(t):
    """Return nodes [(val, x, y)] and edges [(i, j)] for a tuple tree (int = leaf)."""
    nodes, edges, cnt = [], [], [0]
    def go(t, d):
        if t is None:
            return None
        if isinstance(t, int):
            t = (t, None, None)
        v, l, r = t
        li = go(l, d + 1)
        i = len(nodes)
        nodes.append((v, cnt[0], -d * 1.4))
        cnt[0] += 1
        ri = go(r, d + 1)
        for c in (li, ri):
            if c is not None:
                edges.append((i, c))
        return i
    go(t, 0)
    return nodes, edges

def draw(ax, t, fill=None, edgecol=None, ecolor="#555555", r=0.36, fs=15, bold=()):
    fill = fill or {}
    edgecol = edgecol or {}
    nodes, edges = layout(t)
    for i, j in edges:
        a, b = nodes[i], nodes[j]
        col, lw = ecolor, 2
        if (a[0], b[0]) in edgecol:
            col, lw = edgecol[(a[0], b[0])], 4
        ax.plot([a[1], b[1]], [a[2], b[2]], color=col, lw=lw, zorder=1)
    for v, x, y in nodes:
        f = fill.get(v, "white")
        ax.add_patch(plt.Circle((x, y), r, fc=f, ec="#222222", lw=2, zorder=2))
        tc = "white" if f not in ("white", "#f3f3f3") else "#111111"
        ax.text(x, y, str(v), ha="center", va="center", fontsize=fs, color=tc, zorder=3, fontweight="bold")
    xs = [n[1] for n in nodes]; ys = [n[2] for n in nodes]
    ax.set_xlim(min(xs) - 0.8, max(xs) + 0.8)
    ax.set_ylim(min(ys) - 0.8, max(ys) + 0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    return {v: (x, y) for v, x, y in nodes}

T = (8, (3, 1, (6, 4, 7)), (10, None, (14, 13, None)))
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=110)
pos = draw(ax, T, fill={8: BLUE, 1: TEAL, 4: TEAL, 7: TEAL, 13: TEAL})
for d in range(4):
    ax.text(-0.9, -d * 1.4, f"depth {d}", ha="right", va="center", fontsize=13, color="#444444")
ax.annotate("root: no parent", xy=(5.4, 0), xytext=(6.4, 0.1), fontsize=13, color=BLUE, va="center", arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))
ax.annotate("leaf: no children", xy=(6.65, -4.3), xytext=(5.2, -5.3), fontsize=13, color=TEAL, va="center", arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
ax.annotate("6 is the parent of 4 and 7\n(4 and 7 are siblings)", xy=(3.4, -2.95), xytext=(3.9, -3.2), fontsize=12, color=ORANGE, va="center", arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
ax.text(2.6, 0.1, "height of this tree = 3 edges\n(longest root-to-leaf path)", fontsize=12, color=PURPLE, ha="center", va="center")
ax.set_xlim(-3.2, 10); ax.set_ylim(-5.9, 0.9)
fig.tight_layout(); fig.savefig("dsa7_anatomy.png")
