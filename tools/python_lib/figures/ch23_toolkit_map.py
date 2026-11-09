import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
items = [("Write", "pathlib\ndataclasses\ntyping", B), ("Test", "pytest\nunittest\nmock", O), ("Package", "venv, uv\npyproject\npre-commit", T),
         ("Serve", "argparse\nFastAPI", P), ("Ship", "Docker\nsecrets", R)]
for i, (h, body, c) in enumerate(items):
    x = 0.3 + i * 2.35
    ax.add_patch(FancyBboxPatch((x, 2.6), 1.95, 2.4, boxstyle="round,pad=0.05", fc="white", ec=c, lw=2.5))
    ax.text(x + 0.97, 4.5, h, ha="center", va="center", fontsize=15, fontweight="bold", color=c)
    ax.text(x + 0.97, 3.4, body, ha="center", va="center", fontsize=11.5)
    if i < 4:
        ax.annotate("", xy=(x + 2.33, 3.8), xytext=(x + 1.99, 3.8), arrowprops=dict(arrowstyle="->", lw=2))
ax.add_patch(FancyBboxPatch((0.3, 0.5), 11.3, 1.3, boxstyle="round,pad=0.05", fc="#eef2fc", ec=B, lw=2))
ax.text(5.95, 1.15, "Track and orchestrate: logging, JSON metrics, MLflow, DVC, Airflow / Prefect", ha="center", va="center", fontsize=12)
ax.set_title("The engineering toolkit around a model", fontsize=15)
fig.tight_layout(); fig.savefig("lib23_toolkit_map.png")
