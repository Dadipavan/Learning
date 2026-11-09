import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
n = 2500
hours = np.arange(8, 24)
w = np.exp(-0.5 * ((hours - 20) / 3.0) ** 2)                             # evening peak around 8 pm
hour = rng.choice(hours, n, p=w / w.sum())
weekday = rng.choice(7, n, p=[0.12, 0.12, 0.12, 0.13, 0.14, 0.19, 0.18])
tbl = pd.crosstab(weekday, hour).reindex(index=range(7), columns=range(8, 24), fill_value=0)
tbl.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print("busiest cell:", tbl.stack().idxmax(), "with", tbl.stack().max(), "orders")
ax = sns.heatmap(tbl, cmap="Blues", cbar_kws={"label": "Orders"}, linewidths=0.5, linecolor="white")
ax.set(xlabel="Hour of day (24-hour clock)", ylabel="", title="Orders peak around 8 pm, strongest on Saturday")
ax.tick_params(length=0)
ax.figure.tight_layout()
ax.figure.savefig("ch08v_timeheat_sns.png", dpi=110)
print("saved")
