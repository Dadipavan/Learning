import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
sales = pd.DataFrame({
    "city":   ["Pune", "Pune", "Pune", "Mumbai", "Mumbai", "Mumbai", "Delhi", "Delhi"],
    "status": ["Delivered", "Delivered", "Returned", "Delivered", "Delivered", "Cancelled", "Delivered", "Delivered"],
    "amount": [998, 1400, 597, 1299, 1298, 450, 799, 2499]})
by_city = sales.groupby("city", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
palette = {c: BLUE if c == "Delhi" else GREY for c in by_city["city"]}
ax = sns.barplot(data=by_city, x="city", y="amount", hue="city", palette=palette, legend=False)
ax.bar_label(ax.containers[0], fmt="{:,.0f}", padding=3)
ax.set(ylim=(0, 3800), yticks=[], xlabel="", ylabel="Sales (Rs)", title="Delhi sold the most: Rs 3,298 of Rs 9,340")
sns.despine(left=True)
ax.figure.tight_layout()
ax.figure.savefig("ch08v_bar_sns.png", dpi=110)
print(by_city.to_string(index=False))
print("saved")
