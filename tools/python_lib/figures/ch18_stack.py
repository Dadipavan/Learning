import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, text, c, tc="white", fs=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="none"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=tc, fontsize=fs, fontweight="bold")
box(0.2, 0.2, 9.6, 0.9, "NumPy arrays (ndarray): the shared data format", T)
mods = ["stats", "optimize", "integrate", "interpolate", "linalg", "sparse", "signal", "fft", "spatial", "cluster"]
for i, m in enumerate(mods):
    box(0.2 + (i % 5) * 1.95, 1.5 + (i // 5) * 0.95, 1.8, 0.75, "scipy." + m, B, fs=11)
box(0.2, 3.5, 9.6, 0.1, "", "white")
box(0.2, 3.65, 4.7, 0.9, "statsmodels: models + tables", O)
box(5.1, 3.65, 4.7, 0.9, "scikit-learn: prediction", P)
box(0.2, 4.85, 4.7, 0.9, "pandas: labelled tables in and out", R)
box(5.1, 4.85, 4.7, 0.9, "matplotlib: plots of any result", "#444444")
fig.tight_layout(); fig.savefig("lib18_stack.png"); 
