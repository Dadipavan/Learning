import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
region = pd.DataFrame({"orders_k": [640, 60, 570, 330, 250, 540], "pop_m": [320, 46, 190, 280, 250, 270]},
                      index=["North", "Northeast", "West", "Central", "East", "South"])
region["per_1000"] = (region["orders_k"] / region["pop_m"]).round(2)
print(region.to_string())
print("rank by count :", region["orders_k"].sort_values(ascending=False).index.tolist())
print("rank by rate  :", region["per_1000"].sort_values(ascending=False).index.tolist())
pos = {"North": (1, 0), "Northeast": (2, 0), "West": (0, 1), "Central": (1, 1), "East": (2, 1), "South": (1, 2)}
fig, axs = plt.subplots(1, 2, figsize=(9, 4.2))
for ax, col, title, cmap, fmt in [(axs[0], "orders_k", "Orders (thousand): maps population", "Greys", "{:.0f}"),
                                  (axs[1], "per_1000", "Orders per 1,000 residents", "Blues", "{:.1f}")]:
    vals = region[col]
    for name, (cx, cy) in pos.items():
        shade = plt.get_cmap(cmap)(0.15 + 0.7 * (vals[name] - vals.min()) / (vals.max() - vals.min()))
        ax.add_patch(plt.Rectangle((cx, cy), 0.95, 0.95, color=shade))
        dark = (vals[name] - vals.min()) / (vals.max() - vals.min()) > 0.55
        ax.text(cx + 0.475, cy + 0.6, name, ha="center", va="center", fontsize=10, color="white" if dark else "#222")
        ax.text(cx + 0.475, cy + 0.32, fmt.format(vals[name]), ha="center", va="center", fontsize=13,
                fontweight="bold", color="white" if dark else "#222")
    ax.set(xlim=(0, 3), ylim=(3, 0), aspect="equal", title=title); ax.axis("off")
    ax.set_title(title, fontsize=12, loc="left")
fig.tight_layout()
fig.savefig("ch08v_tilemap.png", dpi=110)
print("saved")
