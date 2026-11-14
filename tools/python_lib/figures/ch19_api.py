import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, text, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="none", alpha=0.9))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", fontsize=13, weight="bold")
def arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=2, color="#333"))
    if label: ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.25, label, ha="center", fontsize=12)
box(0.2, 4.2, 2.0, 1.2, "X, y\ntrain data", P)
box(3.6, 4.2, 2.6, 1.2, "estimator\n(hyper-params)", B)
box(7.4, 4.2, 2.3, 1.2, "fitted\nattributes_", T)
arrow(2.3, 4.8, 3.5, 4.8); arrow(6.3, 4.8, 7.3, 4.8, "fit")
box(0.2, 0.5, 2.0, 1.2, "new X", P)
box(3.6, 0.5, 2.6, 1.2, "predict /\ntransform", O)
box(7.4, 0.5, 2.3, 1.2, "output\ny_hat or X'", R)
arrow(2.3, 1.1, 3.5, 1.1); arrow(6.3, 1.1, 7.3, 1.1)
arrow(8.5, 4.1, 5.5, 1.8, "learned state")
ax.text(5, 3.0, "same object, two phases", ha="center", fontsize=13, style="italic")
plt.tight_layout(); plt.savefig("lib19_api.png")
