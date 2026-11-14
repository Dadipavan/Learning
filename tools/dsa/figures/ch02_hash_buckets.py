import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
def h(k): return sum(ord(c) for c in k) % 8
keys = ["cat", "dog", "sun", "fig", "ant"]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for b in range(8):
    y = 7 - b
    ax.add_patch(Rectangle((4, y), 0.9, 0.8, fc="#eeeeee", ec="black", lw=1.5))
    ax.text(3.8, y + 0.4, str(b), ha="right", va="center", fontsize=14)
cols = [B, O, T, R, P]
chain = {}
for k, c in zip(keys, cols):
    b = h(k); n = chain.get(b, 0); chain[b] = n + 1
    y = 7 - b
    ax.add_patch(Rectangle((5.4 + 1.5 * n, y), 1.2, 0.8, fc=c, ec="black", lw=1.5))
    ax.text(6.0 + 1.5 * n, y + 0.4, k, ha="center", va="center", fontsize=15, color="white", fontweight="bold")
    ax.annotate("", xy=(4.95 if n == 0 else 5.35 + 1.5 * (n - 1) + 1.25, y + 0.4), xytext=(5.4 + 1.5 * n, y + 0.4),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2))
    ax.text(0.2, 7.2 - keys.index(k) * 1.1, f"hash('{k}') = {sum(ord(x) for x in k)} % 8 = {b}", fontsize=13, color=c, fontweight="bold")
ax.text(0.2, 1.2, "toy hash: sum of codes % 8", fontsize=12)
ax.text(0.2, 0.5, "sun, fig collide in bucket 6", fontsize=12, color=R)
ax.set_xlim(0, 9.5); ax.set_ylim(-0.3, 8.3); ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_hash_buckets.png")
