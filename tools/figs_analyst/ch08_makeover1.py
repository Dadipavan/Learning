import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rev = pd.Series({"Wireless earbuds": 412, "Smart watch": 388, "Air fryer": 301, "Yoga mat": 187,
                 "Backpack": 176, "Desk lamp": 152, "Water bottle": 129}).sort_values(ascending=False)
top2 = rev.iloc[:2].sum() / rev.sum()
print(f"top two products: {rev.iloc[:2].sum()} of {rev.sum()} = {top2:.1%}")
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1, 1.1]})
# BEFORE
a.pie(rev, colors=plt.cm.rainbow(np.linspace(0, 1, len(rev))), autopct="%1.1f%%", textprops={"fontsize": 8})
a.legend(rev.index, loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=9)
a.set_title("Revenue share by product", fontsize=12, fontweight="normal", loc="center")
# AFTER
s = rev.sort_values()
bars = b.barh(s.index, s.values, color=[GREY] * 5 + [BLUE] * 2, height=0.7)
b.bar_label(bars, labels=[f"{v}  ({v / rev.sum():.0%})" for v in s.values], padding=4)
b.set_xlim(0, 560); b.set_xlabel("Revenue (Rs thousand)"); b.tick_params(axis="y", length=0)
b.set_title(f"Two products bring in {top2:.0%} of revenue")
fig.text(0.01, 0.97, "BEFORE", color=RED, fontweight="bold", fontsize=13, va="top")
fig.text(0.52, 0.97, "AFTER", color=TEAL, fontweight="bold", fontsize=13, va="top")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("ch08v_makeover1.png", dpi=110)
print("saved")
