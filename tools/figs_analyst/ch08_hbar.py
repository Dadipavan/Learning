import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
revenue = pd.Series({"Wireless earbuds": 412, "Smart watch": 388, "Air fryer": 301, "Yoga mat": 187,
                     "Backpack": 176, "Desk lamp": 152, "Water bottle": 129, "Phone case": 96,
                     "Notebook": 64, "Pen set": 41}, name="revenue_k").sort_values()
top3 = revenue.nlargest(3).sum() / revenue.sum()
print("total (Rs thousand):", revenue.sum(), "| top-3 share:", f"{top3:.1%}")
fig, ax = plt.subplots(figsize=(8, 4.6))
colors = [BLUE if v >= revenue.nlargest(3).min() else GREY for v in revenue]
bars = ax.barh(revenue.index, revenue.values, color=colors, height=0.7)
ax.bar_label(bars, padding=4)
ax.set_title(f"Three products bring in {top3:.0%} of revenue")
ax.set_xlabel("Revenue (Rs thousand)")
ax.set_xlim(0, 470)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("ch08v_hbar.png", dpi=110)
print("saved")
