import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
revenue = pd.Series({"Wireless earbuds": 412, "Smart watch": 388, "Air fryer": 301, "Yoga mat": 187,
                     "Backpack": 176, "Desk lamp": 152, "Water bottle": 129, "Phone case": 96,
                     "Notebook": 64, "Pen set": 41}, name="revenue_k")
df = revenue.sort_values(ascending=False).rename_axis("product").reset_index()
df["top3"] = np.where(df.index < 3, "top", "rest")
ax = sns.barplot(data=df, y="product", x="revenue_k", hue="top3", palette={"top": BLUE, "rest": GREY},
                 dodge=False, legend=False, orient="h")
ax.bar_label(ax.containers[0], padding=4); ax.bar_label(ax.containers[1], padding=4)
ax.set(xlabel="Revenue (Rs thousand)", ylabel="", xlim=(0, 470))
ax.figure.tight_layout()
ax.figure.savefig("ch08v_hbar_sns.png", dpi=110)
print(df.head(3).to_string(index=False))
print("saved")
