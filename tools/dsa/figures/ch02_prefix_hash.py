import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
nums, k = [1, 2, 1, 2, 1], 3
pre = [0]
for v in nums: pre.append(pre[-1] + v)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(range(len(pre)), pre, "o-", color=B, lw=3, ms=11)
for i, p in enumerate(pre): ax.text(i, p + 0.45, str(p), ha="center", fontsize=15, fontweight="bold", color=B)
pairs = [(i, j) for j in range(len(pre)) for i in range(j) if pre[j] - pre[i] == k]
cols = [O, T, R, P]
for (i, j), c in zip(pairs, cols):
    ax.add_patch(FancyArrowPatch((i, -1.0 - 0.0), (j, -1.0), connectionstyle="arc3,rad=0.0", arrowstyle="<|-|>", mutation_scale=16, lw=2.5, color=c, alpha=0))
ys = [-0.9, -1.5, -2.1, -2.7]
for (i, j), c, y in zip(pairs, cols, ys):
    ax.annotate("", xy=(j, y), xytext=(i, y), arrowprops=dict(arrowstyle="<|-|>", color=c, lw=3))
    ax.text(j + 0.1, y, f"P[{j}] - P[{i}] = {pre[j]} - {pre[i]} = {k}", fontsize=11, va="center", color=c, fontweight="bold")
ax.set_xticks(range(len(pre))); ax.tick_params(labelsize=14)
ax.set_xlabel("prefix index j  (array = [1, 2, 1, 2, 1], k = 3)", fontsize=13)
ax.set_ylabel("prefix sum P[j]", fontsize=13)
ax.set_ylim(-3.2, 8.5); ax.set_xlim(-0.4, 8.5); ax.set_yticks([0, 2, 4, 6])
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_title("4 pairs of prefixes differ by k, so 4 subarrays sum to k", fontsize=13)
plt.tight_layout(); plt.savefig("dsa2_prefix_hash.png")
