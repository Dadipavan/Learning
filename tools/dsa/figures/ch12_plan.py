from ch12_common import *
rows = [("Big-O, Python, hashing", 1, 2, B), ("Two pointers, window, prefix", 2, 3, B), ("Sorting, binary search", 3, 4, B),
        ("Stack, queue, linked list", 4, 5, T), ("Recursion, backtracking", 5, 6, O), ("Trees, heaps", 6, 7, T),
        ("Graphs", 7, 8, T), ("Dynamic programming", 8, 10, P), ("Greedy, intervals, bits", 10, 10, P),
        ("Design problems", 10, 11, O), ("Mock interviews", 9, 12, R)]
fig, ax = plt.subplots(figsize=(8, 4.8)); ax.set_xlim(0.5, 12.5); ax.set_ylim(-0.7, len(rows) - 0.3)
for i, (n, s, e, c) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.add_patch(Rectangle((s - 0.45, y - 0.32), (e - s) + 0.9, 0.64, fc=c, ec="white", lw=2))
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=12)
ax.set_xticks(range(1, 13)); ax.set_xlabel("week", fontsize=14)
ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="x", color="#dddddd", zorder=0)
ax.set_title("12-week plan: learn a pattern, then keep it alive", fontsize=15)
plt.tight_layout(); plt.savefig("dsa12_plan.png", dpi=110)
