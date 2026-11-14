import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
price = pd.Series({"Wireless earbuds": 2500, "Smart watch": 4500, "Air fryer": 3500, "Yoga mat": 800, "Backpack": 1200,
                   "Desk lamp": 900, "Water bottle": 400, "Phone case": 300, "Notebook": 150, "Pen set": 120})
revenue_k = pd.Series({"Wireless earbuds": 412, "Smart watch": 388, "Air fryer": 301, "Yoga mat": 187, "Backpack": 176,
                       "Desk lamp": 152, "Water bottle": 129, "Phone case": 96, "Notebook": 64, "Pen set": 41})
units = (revenue_k * 1000 / price).round().astype(int)
df = pd.DataFrame({"price": price, "units": units, "revenue_k": revenue_k})
print(df.sort_values("revenue_k", ascending=False).head(4).to_string())
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.scatter(df["price"], df["units"], s=df["revenue_k"] * 5, color=BLUE, alpha=0.55, edgecolor="white", linewidth=1.5)
offsets = {"Wireless earbuds": (-8, 46), "Smart watch": (22, 44), "Air fryer": (-26, 42), "Yoga mat": (0, 28),
           "Backpack": (0, -34), "Desk lamp": (30, 26), "Water bottle": (0, 24), "Phone case": (40, -14),
           "Notebook": (0, 22), "Pen set": (0, -28)}
for name, (dx, dy) in offsets.items():
    ax.annotate(name, (df.loc[name, "price"], df.loc[name, "units"]), xytext=(dx, dy), textcoords="offset points",
                ha="center", va="center", fontsize=10)
ax.set_xscale("log"); ax.set_xlim(80, 7000)
ax.set_xticks([100, 300, 1000, 3000], ["100", "300", "1,000", "3,000"])
ax.set_ylim(0, 520)
ax.set_xlabel("Unit price (Rs, log scale)"); ax.set_ylabel("Units sold")
ax.set_title("Cheap items sell most units; pricey ones earn most revenue")
ax.text(0.99, 0.97, "bubble area = revenue", transform=ax.transAxes, ha="right", va="top", color="#555")
fig.tight_layout()
fig.savefig("ch08v_bubble.png", dpi=110)
print("saved")
