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
arr = [2, 5, 3, 9, 6, 8, 4]
def from_arr(a, i=0):
    if i >= len(a):
        return None
    return (a[i], from_arr(a, 2 * i + 1), from_arr(a, 2 * i + 2))
fig = plt.figure(figsize=(9, 5.4), dpi=110)
ax = fig.add_axes([0.02, 0.28, 0.96, 0.62])
pos = draw(ax, from_arr(arr), fill={2: BLUE}, r=0.42)
ax.set_title("Min-heap drawn as a tree (parent <= children)", fontsize=14)
for i, v in enumerate(arr):
    x, y = pos[v]
    ax.text(x, y - 0.62, f"i={i}", ha="center", fontsize=11, color=ORANGE)
bx = fig.add_axes([0.02, 0.0, 0.96, 0.27]); bx.axis("off"); bx.set_xlim(-1, 8); bx.set_ylim(-1.6, 1.1)
for i, v in enumerate(arr):
    bx.add_patch(plt.Rectangle((i, 0), 1, 0.9, fc="white", ec="#222222", lw=2))
    bx.text(i + 0.5, 0.45, str(v), ha="center", va="center", fontsize=16, fontweight="bold")
    bx.text(i + 0.5, -0.25, str(i), ha="center", va="center", fontsize=12, color=ORANGE)
bx.text(-0.8, 0.45, "array", fontsize=13, va="center")
bx.text(3.5, -1.0, "parent(i) = (i-1)//2    left(i) = 2i+1    right(i) = 2i+2", ha="center", fontsize=13, color=BLUE)
fig.savefig("dsa7_heap.png")
