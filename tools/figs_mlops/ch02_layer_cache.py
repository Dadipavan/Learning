import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

B, O, T, R = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"
fig, axes = plt.subplots(1, 2, figsize=(8, 4.2))
cases = [("BAD order: COPY . . first", [("FROM base", "cached", "0 s"), ("COPY . .", "rebuilt", "2 s"), ("RUN pip install", "rebuilt", "240 s")]),
         ("GOOD order: lock file first", [("FROM base", "cached", "0 s"), ("COPY lock", "cached", "0 s"), ("RUN pip install", "cached", "0 s"), ("COPY code", "rebuilt", "1 s")])]
for ax, (title, layers) in zip(axes, cases):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.6); ax.axis("off"); ax.set_title(title, fontsize=10.5, fontweight="bold")
    for i, (name, state, t) in enumerate(layers):
        y = 0.6 + i * 1.35
        c = T if state == "cached" else O
        ax.add_patch(Rectangle((0.5, y), 9, 1.15, fc=c, ec="white", lw=2, alpha=.92))
        ax.text(1, y + .57, name, color="white", va="center", fontsize=10, fontweight="bold")
        ax.text(9.2, y + .57, f"{state}, {t}", color="white", va="center", ha="right", fontsize=9)
    ax.text(5, 0.05, "after a one-line code edit", ha="center", fontsize=9, style="italic")
axes[0].text(5, 6.2, "total 242 s", ha="center", fontsize=11, color=R, fontweight="bold")
axes[1].text(5, 6.2, "total 1 s", ha="center", fontsize=11, color=T, fontweight="bold")
fig.tight_layout(); fig.savefig("ch02d_layer_cache.png", dpi=110)
