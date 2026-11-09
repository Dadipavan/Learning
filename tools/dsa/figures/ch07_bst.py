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
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.8), dpi=110, gridspec_kw={"width_ratios": [1.5, 1]})
path = {(8, 3): ORANGE, (3, 6): ORANGE, (6, 7): ORANGE}
pos = draw(a1, T, fill={8: ORANGE, 3: ORANGE, 6: ORANGE, 7: TEAL}, edgecol=path, r=0.4)
a1.set_title("Valid BST: search for 7", fontsize=15)
notes = [(8, "7 < 8: go left"), (3, "7 > 3: go right"), (6, "7 > 6: go right")]
for v, s in notes:
    x, y = pos[v]
    if v == 6:
        a1.text(x + 0.55, y + 0.1, s, ha="left", va="center", fontsize=12, color=ORANGE)
    else:
        a1.text(x - 0.55, y + 0.05, s, ha="right", va="center", fontsize=12, color=ORANGE)
a1.text(pos[7][0] + 0.5, pos[7][1] - 0.05, "found", fontsize=13, color=TEAL, ha="left", va="center")
a1.set_xlim(-5.5, 9)
B = (5, 1, (8, 4, 9))
pos2 = draw(a2, B, fill={4: RED}, r=0.4)
a2.set_title("NOT a BST", fontsize=15, color=RED)
a2.text(pos2[4][0], pos2[4][1] - 0.85, "4 sits in the right\nsubtree of 5, but 4 < 5", ha="center", va="top", fontsize=12, color=RED)
a2.set_ylim(-4.6, 0.9)
fig.tight_layout(); fig.savefig("dsa7_bst.png")
