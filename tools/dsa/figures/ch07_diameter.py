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
hl = {4: RED, 6: RED, 3: RED, 8: RED, 10: RED, 14: RED, 13: RED}
ec = {(8, 3): RED, (3, 6): RED, (6, 4): RED, (8, 10): RED, (10, 14): RED, (14, 13): RED}
pos = draw(ax, T, fill=hl, edgecol=ec, r=0.4)
hts = {1: 0, 4: 0, 7: 0, 13: 0, 6: 1, 14: 1, 3: 2, 10: 2, 8: 3}
for v, h in hts.items():
    x, y = pos[v]
    ax.text(x + 0.5, y + 0.28, f"h={h}", fontsize=12, color=BLUE, fontweight="bold")
ax.text(4.0, -5.4, "Diameter = longest path = 6 edges\nat node 8: (left height 2 + 1) + (right height 2 + 1) = 6", ha="center", fontsize=12)
ax.set_xlim(-1.2, 9.2); ax.set_ylim(-6.2, 0.9)
fig.tight_layout(); fig.savefig("dsa7_diameter.png")
