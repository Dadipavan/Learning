import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
city = pd.Series({"Delhi": 3298, "Mumbai": 3047, "Pune": 2995})
start = 2900
visual = (city["Delhi"] - start) / (city["Pune"] - start)
real = city["Delhi"] / city["Pune"]
print(f"visible bar heights with axis starting at {start}: Delhi {city['Delhi'] - start}, Pune {city['Pune'] - start}")
print(f"visual ratio = {visual:.2f}; real ratio = {real:.2f}; lie factor = {visual / real:.1f}")
fig, (a, b) = plt.subplots(1, 2, figsize=(9, 4.2))
a.bar(city.index, city.values, color=[BLUE, GREY, GREY], width=0.6)
a.set_ylim(start, 3400); a.set_title("Misleading: axis starts at 2,900")
a.text(0.97, 0.93, "Delhi looks 4.2x Pune", transform=a.transAxes, ha="right", va="top", color=RED, fontweight="bold")
b.bar(city.index, city.values, color=[BLUE, GREY, GREY], width=0.6)
b.set_ylim(0, 4000); b.set_title("Honest: axis starts at 0")
b.text(0.97, 0.93, "Delhi is really 1.10x Pune", transform=b.transAxes, ha="right", va="top", color=TEAL, fontweight="bold")
for ax in (a, b):
    ax.set_yticks(ax.get_yticks()[ax.get_yticks() >= ax.get_ylim()[0]])
    ax.bar_label(ax.containers[0], fmt="{:,.0f}", padding=3, fontsize=11)
fig.tight_layout()
fig.savefig("ch08v_lie_truncated.png", dpi=110)
print("saved")
