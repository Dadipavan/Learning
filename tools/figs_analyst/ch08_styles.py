import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
import matplotlib as mpl
print("styles that ship with matplotlib:", len(plt.style.available))
print([s for s in plt.style.available if s in ("ggplot", "fivethirtyeight", "bmh", "seaborn-v0_8-whitegrid", "classic", "dark_background")])
x = np.arange(1, 7); y1 = np.array([350, 330, 375, 405, 430, 455]); y2 = np.array([310, 295, 340, 360, 385, 400])
fig = plt.figure(figsize=(9, 5))
for k, style in enumerate(["default", "ggplot", "seaborn-v0_8-whitegrid", "bmh"], start=1):
    with plt.style.context(style):
        ax = fig.add_subplot(2, 2, k)
        ax.plot(x, y1, lw=2.5, label="2025"); ax.plot(x, y2, lw=2.5, label="2024")
        ax.set_title(style, fontsize=11); ax.legend(fontsize=9, loc="lower right")
fig.tight_layout()
fig.savefig("ch08v_styles.png", dpi=110)
print("saved")
