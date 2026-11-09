import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
items = [("Code", "git commit", B), ("Data", "content hash", O), ("Config", "YAML, logged", T),
         ("Environment", "lock file + image", R), ("Seeds, hardware", "every RNG, GPU type", P)]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
for i, (name, how, c) in enumerate(items):
    x = 0.2 + i * 1.95
    ax.add_patch(FancyBboxPatch((x, 3.4), 1.7, 1.5, boxstyle="round,pad=0.05", fc=c, ec="none", alpha=0.92))
    ax.text(x + 0.85, 4.35, name, ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")
    ax.text(x + 0.85, 3.8, how, ha="center", va="center", color="white", fontsize=8.5)
    ax.add_patch(FancyArrowPatch((x + 0.85, 3.35), (5, 2.35), arrowstyle="-|>", mutation_scale=14, color="#555", lw=1.2))
ax.add_patch(FancyBboxPatch((3.6, 1.55), 2.8, 0.8, boxstyle="round,pad=0.05", fc="#f3f1ea", ec="#333", lw=1.4))
ax.text(5, 1.95, "one training run", ha="center", va="center", fontsize=11, fontweight="bold")
ax.add_patch(FancyArrowPatch((5, 1.5), (5, 0.85), arrowstyle="-|>", mutation_scale=14, color="#555", lw=1.2))
ax.text(5, 0.5, "metrics + model file  (same five inputs  =>  same result)", ha="center", va="center", fontsize=10.5)
ax.text(5, 5.55, "Miss any one ingredient and the result can change", ha="center", fontsize=12, fontweight="bold")
fig.tight_layout(); fig.savefig("ch02d_five_ingredients.png", dpi=110)
