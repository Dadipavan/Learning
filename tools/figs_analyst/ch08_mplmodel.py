import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
from matplotlib.patches import FancyBboxPatch
fig = plt.figure(figsize=(8, 4.4))
bg = fig.add_axes([0, 0, 1, 1]); bg.set(xlim=(0, 100), ylim=(-4, 55)); bg.axis("off")
def box(x, y, w, h, fc, ec, label, size=12, weight="bold", tc="#222"):
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=2))
    bg.text(x + 1.2, y + h - 2.4, label, fontsize=size, fontweight=weight, color=tc, va="center")
box(2, 2, 96, 50, "#f4f6fb", BLUE, "Figure   (the canvas: size, dpi, saving)    fig = plt.figure() or plt.subplots()")
box(6, 6, 58, 38, "white", TEAL, "Axes   (one plot)    ax = fig.add_subplot()")
box(10, 10, 24, 12, "#eef6f4", TEAL, "xaxis   (ticks)", 10)
box(38, 10, 24, 12, "#eef6f4", TEAL, "yaxis   (ticks)", 10)
box(10, 26, 24, 11, "#fbf1ec", ORANGE, "Line2D   ax.plot()", 10)
box(37, 26, 23, 11, "#fbf1ec", ORANGE, "Bars   ax.bar()", 10)
box(68, 24, 28, 12, "#f4f0fb", PURPLE, "Legend / Text / Annotation", 10)
box(68, 8, 28, 12, "#f4f0fb", PURPLE, "Second Axes   (subplots)", 10)
bg.text(50, -2, "Every box is an object. Methods on ax change one plot; methods on fig change the whole canvas.",
        ha="center", fontsize=10.5, color="#444")
fig.savefig("ch08v_mplmodel.png", dpi=110)
print("saved")
