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
weekly["season"] = np.where(weekly["discount"] > 12.5, "High discount", "Low discount")
ax = sns.scatterplot(data=weekly, x="ad_spend", y="revenue_k", hue="season", style="season",
                     palette={"High discount": ORANGE, "Low discount": BLUE}, s=60)
sns.regplot(data=weekly, x="ad_spend", y="revenue_k", scatter=False, color="#444", ci=95, line_kws={"lw": 2})
ax.set(xlabel="Weekly ad spend (Rs thousand)", ylabel="Weekly revenue (Rs thousand)",
       title="Revenue rises with ad spend in both discount groups")
sns.move_legend(ax, "lower right", frameon=False, title=None)
ax.figure.tight_layout()
ax.figure.savefig("ch08v_scatter_sns.png", dpi=110)
print(weekly.groupby("season")[["ad_spend", "revenue_k"]].mean().round(1).to_string())
print("saved")
