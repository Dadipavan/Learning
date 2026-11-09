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
words = ["car", "cat", "cap", "do", "dog"]
root = {}
for w in words:
    n = root
    for ch in w:
        n = n.setdefault(ch, {})
    n["$"] = True
fig, ax = plt.subplots(figsize=(8.4, 4.8), dpi=110)
cnt = [0]
nodes = []
def go(n, ch, d, end, parent):
    kids = [(k, v) for k, v in sorted(n.items()) if k != "$"]
    if not kids:
        x = cnt[0]; cnt[0] += 1
        me = len(nodes); nodes.append([ch, x, -d, end, parent]); return me
    me = len(nodes); nodes.append([ch, 0, -d, "$" in n, parent])
    xs = [nodes[go(v, k, d + 1, "$" in v, me)][1] for k, v in kids]
    nodes[me][1] = sum(xs) / len(xs)
    return me
go(root, "root", 0, False, None)
for ch, x, y, end, p in nodes:
    if p is not None:
        ax.plot([nodes[p][1], x], [nodes[p][2], y], color="#555555", lw=2, zorder=1)
for ch, x, y, end, p in nodes:
    f = TEAL if end else ("white" if p is not None else BLUE)
    ax.add_patch(plt.Circle((x, y), 0.3, fc=f, ec="#222222", lw=2, zorder=2))
    ax.text(x, y, "" if ch == "root" else ch, ha="center", va="center", fontsize=17, fontweight="bold", color="white" if end else "#111111", zorder=3)
ax.text(nodes[0][1] + 0.4, 0.05, "root (empty)", fontsize=12, color=BLUE, va="center")
ax.text(3.2, -0.8, "green = a word ends here\nwords: car, cat, cap, do, dog", fontsize=13, color=TEAL)
ax.text(1.45, -4.1, "prefix 'ca' ends at the 'a' node:\nits subtree holds car, cat, cap", ha="center", fontsize=12, color=ORANGE)
ax.set_xlim(-0.8, 5.0); ax.set_ylim(-4.8, 0.7); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout(); fig.savefig("dsa7_trie.png")
