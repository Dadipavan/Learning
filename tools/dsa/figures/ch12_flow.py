from ch12_common import *
rows = [
 ("sorted array, pair or triple", "Two pointers", B),
 ("contiguous substring, longest or shortest", "Sliding window", B),
 ("seen before? count? duplicates?", "Hash map or set", B),
 ("many range-sum queries", "Prefix sums", B),
 ("sorted, or 'smallest value that works'", "Binary search", B),
 ("next greater, matching brackets", "Stack", T),
 ("tree, parent and child", "Tree DFS or BFS", T),
 ("grid, network, fewest steps, order", "Graph BFS, DFS, topo", T),
 ("top K, k-th largest, stream", "Heap", O),
 ("all subsets, permutations, arrangements", "Backtracking", O),
 ("count ways, min cost, overlapping choices", "Dynamic programming", P),
 ("intervals, one local best choice", "Greedy and sorting", P),
]
fig, ax = plt.subplots(figsize=(8, 6.6))
ax.set_xlim(0, 10); ax.set_ylim(-0.3, 12.8); ax.axis("off")
ax.text(2.6, 12.45, "Signal in the statement", ha="center", fontsize=15, fontweight="bold")
ax.text(8.0, 12.45, "Pattern to try", ha="center", fontsize=15, fontweight="bold")
for i, (s, p, c) in enumerate(rows):
    y = 11.2 - i * 1.0
    ax.add_patch(FancyBboxPatch((0.05, y - 0.38), 5.5, 0.76, boxstyle="round,pad=0.02", fc="white", ec=c, lw=2))
    ax.text(0.25, y, s, va="center", fontsize=12.5)
    ax.annotate("", xy=(6.1, y), xytext=(5.6, y), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.5, mutation_scale=20))
    ax.add_patch(FancyBboxPatch((6.15, y - 0.38), 3.75, 0.76, boxstyle="round,pad=0.02", fc=c, ec=c))
    ax.text(8.02, y, p, va="center", ha="center", fontsize=13, color="white", fontweight="bold")
plt.tight_layout(); plt.savefig("dsa12_flow.png", dpi=110)
