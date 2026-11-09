import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
months = np.arange(12)
walks = 100 + rng.normal(1.0, 3.5, (8, 12)).cumsum(axis=1)
sales = pd.DataFrame(walks.T, columns=[f"Region {c}" for c in "ABCDEFGH"])
growth = (sales.iloc[-1] / sales.iloc[0] - 1)
best = growth.idxmax()
print(growth.round(3).to_string())
print(f"best: {best} {growth[best]:+.0%}; median of the others: {growth.drop(best).median():+.0%}")
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
a.plot(months, sales.values)                                   # BEFORE: default colours, one legend entry per line
a.legend(sales.columns, fontsize=8, loc="upper left", ncol=2); a.set_title("Sales by region", fontsize=12, fontweight="normal", loc="center")
for col in sales.columns:                                      # AFTER
    if col != best:
        b.plot(months, sales[col], color="#cccccc", lw=1.8)
b.plot(months, sales[best], color=BLUE, lw=3.2)
b.text(11.2, sales[best].iloc[-1], f"{best}\n{growth[best]:+.0%}", color=BLUE, fontweight="bold", va="center")
b.text(11.2, sales.drop(columns=best).iloc[-1].median(), "other seven\n(grey)", color="#666", va="center", fontsize=10.5)
b.set_xlim(0, 13.5); b.set_xticks([0, 3, 6, 9, 11], ["Jan", "Apr", "Jul", "Oct", "Dec"])
b.set_ylabel(""); a.set_ylabel("Sales index (Jan = 100)")
b.set_title(f"{best} grew {growth[best]:.0%}\nthe other seven: {growth.drop(best).median():.0%} (median)", fontsize=13)
fig.text(0.01, 0.97, "BEFORE", color=RED, fontweight="bold", fontsize=13, va="top")
fig.text(0.50, 0.97, "AFTER", color=TEAL, fontweight="bold", fontsize=13, va="top")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("ch08v_makeover2.png", dpi=110)
print("saved")
