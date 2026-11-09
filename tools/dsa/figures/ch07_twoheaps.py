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
fig = plt.figure(figsize=(9, 5), dpi=110)
a1 = fig.add_axes([0.0, 0.3, 0.5, 0.52]); a2 = fig.add_axes([0.5, 0.3, 0.5, 0.52])
draw(a1, (3, 2, 1), fill={3: BLUE}, r=0.4)
draw(a2, (5, 8, 9), fill={5: ORANGE}, r=0.4)
a1.set_title("Lower half: max-heap\n(top = biggest of the small ones)", fontsize=13, color=BLUE)
a2.set_title("Upper half: min-heap\n(top = smallest of the big ones)", fontsize=13, color=ORANGE)
nl = fig.add_axes([0.05, 0.0, 0.9, 0.28]); nl.set_xlim(0, 7); nl.set_ylim(-0.3, 1.0); nl.axis("off")
vals = [1, 2, 3, 5, 8, 9]
for i, v in enumerate(vals):
    c = BLUE if i < 3 else ORANGE
    nl.add_patch(plt.Rectangle((0.5 + i, 0.15), 1, 0.7, fc=c, ec="#222222", lw=2))
    nl.text(1.0 + i, 0.5, str(v), ha="center", va="center", fontsize=16, color="white", fontweight="bold")
nl.plot([3.5, 3.5], [0.05, 0.95], color=RED, lw=3)
nl.text(3.5, -0.2, "median = (3 + 5) / 2 = 4.0", ha="center", fontsize=14, color=RED)
fig.savefig("dsa7_twoheaps.png")
