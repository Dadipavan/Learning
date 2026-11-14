import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
from matplotlib.patches import Rectangle
rows = [("Categorical (max 5)", [BLUE, ORANGE, TEAL, RED, PURPLE], "name by direct label, not by memory"),
        ("Grey + accent", [GREY, GREY, GREY, GREY, BLUE], "the default for a single message"),
        ("Sequential: Blues", list(plt.cm.Blues(np.linspace(0.2, 0.95, 7))), "low to high, one hue"),
        ("Sequential: viridis", list(plt.cm.viridis(np.linspace(0, 1, 7))), "perceptually even, survives greyscale"),
        ("Diverging: RdBu_r", list(plt.cm.RdBu_r(np.linspace(0.05, 0.95, 7))), "centre = neutral (zero, target)"),
        ("Avoid: jet", list(plt.cm.jet(np.linspace(0, 1, 7))), "bright bands, false edges, not greyscale-safe")]
fig, ax = plt.subplots(figsize=(9, 4.2))
for i, (label, cols, note) in enumerate(rows):
    y = len(rows) - 1 - i
    for j, c in enumerate(cols):
        ax.add_patch(Rectangle((j * 1.05, y), 1, 0.8, color=c))
    ax.text(-0.2, y + 0.4, label, ha="right", va="center", fontsize=12, fontweight="bold", color=RED if label.startswith("Avoid") else "#222")
    ax.text(len(cols) * 1.05 + 0.2, y + 0.4, note, va="center", fontsize=11, color="#444")
ax.set(xlim=(-3.2, 15), ylim=(-0.1, len(rows)), aspect="auto"); ax.axis("off")
fig.tight_layout()
fig.savefig("ch08v_palettes.png", dpi=110)
print("house palette:", [BLUE, ORANGE, TEAL, RED, PURPLE])
print("saved")
