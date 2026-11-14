import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
x = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
x4 = np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8])
ys = [np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
      np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
      np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
      np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])]
xs = [x, x, x, x4]
fig, axs = plt.subplots(2, 2, figsize=(8, 5.2), sharex=True, sharey=True)
for k, (ax, xx, yy) in enumerate(zip(axs.ravel(), xs, ys), start=1):
    r = np.corrcoef(xx, yy)[0, 1]
    slope, icpt = np.polyfit(xx, yy, 1)
    ax.scatter(xx, yy, color=BLUE, s=40, zorder=3)
    ax.plot([3, 20], [icpt + slope * 3, icpt + slope * 20], color=ORANGE, lw=2)
    ax.set_title(f"Set {k}", fontsize=12)
    print(f"set {k}: mean x {xx.mean():.2f}, mean y {yy.mean():.2f}, r {r:.3f}, line y = {icpt:.2f} + {slope:.2f}x")
fig.supxlabel("x"); fig.supylabel("y")
fig.suptitle("Four data sets, one set of summary statistics", x=0.02, ha="left", fontweight="bold")
fig.tight_layout()
fig.savefig("ch08v_anscombe.png", dpi=110)
print("saved")
