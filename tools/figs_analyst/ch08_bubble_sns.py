import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
price = pd.Series({"Wireless earbuds": 2500, "Smart watch": 4500, "Air fryer": 3500, "Yoga mat": 800, "Backpack": 1200,
                   "Desk lamp": 900, "Water bottle": 400, "Phone case": 300, "Notebook": 150, "Pen set": 120})
revenue_k = pd.Series({"Wireless earbuds": 412, "Smart watch": 388, "Air fryer": 301, "Yoga mat": 187, "Backpack": 176,
                       "Desk lamp": 152, "Water bottle": 129, "Phone case": 96, "Notebook": 64, "Pen set": 41})
df = pd.DataFrame({"price": price, "revenue_k": revenue_k})
df["units"] = (df["revenue_k"] * 1000 / df["price"]).round().astype(int)
ax = sns.scatterplot(data=df, x="price", y="units", size="revenue_k", sizes=(60, 1800), color=BLUE, alpha=0.55,
                     legend="brief")
ax.set(xscale="log", xlabel="Unit price (Rs, log scale)", ylabel="Units sold", title="Cheap items sell most units")
sns.move_legend(ax, "upper right", title="Revenue (Rs thousand)", frameon=False, labelspacing=1.4)
ax.figure.tight_layout()
ax.figure.savefig("ch08v_bubble_sns.png", dpi=110)
print(df.loc[["Smart watch", "Pen set"]].to_string())
print("saved")
