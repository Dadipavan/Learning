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
fig, axes = plt.subplots(1, 3, figsize=(14, 5), dpi=110)
orders = {"Preorder: root, left, right": [8, 3, 1, 6, 4, 7, 10, 14, 13],
          "Inorder: left, root, right": [1, 3, 4, 6, 7, 8, 10, 13, 14],
          "Postorder: left, right, root": [1, 4, 7, 6, 3, 13, 14, 10, 8]}
cols = [BLUE, ORANGE, TEAL]
for ax, (title, order), c in zip(axes, orders.items(), cols):
    pos = draw(ax, T, r=0.42, fs=14)
    for k, v in enumerate(order, 1):
        x, y = pos[v]
        ax.text(x + 0.45, y + 0.5, str(k), fontsize=13, color=c, fontweight="bold", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.1", fc="white", ec=c, lw=2), zorder=5)
    ax.set_title(title, fontsize=14, color=c)
    ax.text(4.0, -5.3, "Output: " + " ".join(map(str, order)), ha="center", fontsize=11)
    ax.set_ylim(-5.8, 1.0)
fig.tight_layout(); fig.savefig("dsa7_traversals.png")
