import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
n = 52
ad_spend = rng.uniform(20, 100, n).round(1)                                   # Rs thousand per week
visits = (900 + 25 * ad_spend + rng.normal(0, 250, n)).round()
discount = rng.uniform(0, 25, n).round(1)                                      # average discount, %
orders_n = (0.05 * visits + 0.6 * discount + rng.normal(0, 8, n)).round()
revenue_k = (0.9 * orders_n * (1 - discount / 200) + rng.normal(0, 4, n)).round(1)
returns = (0.04 * orders_n + 0.25 * discount + rng.normal(0, 2, n)).round().clip(0)
weekly = pd.DataFrame({"ad_spend": ad_spend, "visits": visits, "discount": discount,
                       "orders": orders_n, "revenue_k": revenue_k, "returns": returns})
corr = weekly.corr().round(2)
print(corr.to_string())
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)          # hide the mirror-image upper triangle
ax = sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, center=0,
                 square=True, linewidths=1, linecolor="white", cbar_kws={"label": "Correlation (r)", "shrink": 0.8})
ax.set(title="Visits and orders move with revenue; discount links to returns")
ax.tick_params(length=0)
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
ax.figure.savefig("ch08v_corr_sns.png", dpi=110, bbox_inches="tight")
print("saved")
