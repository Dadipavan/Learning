import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
n = 200_000
x = rng.normal(0, 1, n)
y = 0.6 * x + rng.normal(0, 0.8, n)
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), sharex=True, sharey=True)
a.scatter(x, y, s=4, color=BLUE)
a.set_title("200,000 points: a blob")
hb = b.hexbin(x, y, gridsize=40, cmap="Blues", mincnt=1, bins="log")
b.set_title("Hexbin: density is visible")
fig.colorbar(hb, ax=b, label="points per cell (log scale)")
for ax in (a, b): ax.set_xlabel("x"); ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4.5, 4.5)
fig.tight_layout()
fig.savefig("ch08v_hexbin.png", dpi=110)
counts = hb.get_array()
print("points:", n, "| occupied hexagons:", len(counts), "| busiest 40 x 40 square bin holds", int(np.histogram2d(x, y, bins=40)[0].max()), "points")
print("correlation:", round(float(np.corrcoef(x, y)[0, 1]), 3))
print("saved")
