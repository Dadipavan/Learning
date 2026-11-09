import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
c = Counter("mississippi")
items = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
cols = [T if v == 1 else B for _, v in items]
ax.bar([k for k, _ in items], [v for _, v in items], color=cols, edgecolor="black")
for i, (k, v) in enumerate(items): ax.text(i, v + 0.1, str(v), ha="center", fontsize=16, fontweight="bold")
ax.set_ylim(0, 5.2); ax.tick_params(labelsize=16); ax.set_yticks([0, 1, 2, 3, 4])
ax.set_title("Counter('mississippi'): teal = count 1, the non-repeating letter", fontsize=13)
ax.set_xlabel("letter", fontsize=14); ax.set_ylabel("count", fontsize=14)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("dsa2_freq_bars.png")
