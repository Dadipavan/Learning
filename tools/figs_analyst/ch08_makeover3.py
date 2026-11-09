import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
stores = pd.Series({"Andheri": 3790, "Bandra": 4180, "Colaba": 3640, "Dadar": 3920, "Powai": 3705, "Thane": 3860})
lo, hi = stores.min(), stores.max()
print(f"largest / smallest = {hi / lo:.3f}; visual ratio on axis starting at 3,500: {(hi - 3500) / (lo - 3500):.1f}")
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.4))
a.bar(stores.index, stores.values, color="#4c72b0", label="Sales")        # BEFORE: alphabetical, truncated, grid, legend
a.set_ylim(3500, 4250); a.grid(True); a.legend(); a.set_title("Store sales", fontsize=12, fontweight="normal", loc="center")
plt.setp(a.get_xticklabels(), rotation=45)
s = stores.sort_values()                                                   # AFTER
bars = b.barh(s.index, s.values, color=GREY, height=0.7)
b.bar_label(bars, labels=[f"{v:,}" for v in s.values], padding=4)
b.set_xlim(0, 4700); b.set_xticks([]); b.spines["bottom"].set_visible(False); b.tick_params(axis="y", length=0)
b.set_title(f"All six stores sell within {hi / lo - 1:.0%} of each other")
b.set_xlabel("Sales (Rs thousand), axis starts at zero")
fig.text(0.01, 0.97, "BEFORE", color=RED, fontweight="bold", fontsize=13, va="top")
fig.text(0.50, 0.97, "AFTER", color=TEAL, fontweight="bold", fontsize=13, va="top")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("ch08v_makeover3.png", dpi=110)
print("saved")
