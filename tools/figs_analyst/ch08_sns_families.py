import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
n = 300
category = rng.choice(["Electronics", "Home", "Fashion", "Grocery"], n, p=[0.2, 0.25, 0.3, 0.25])
mu = pd.Series({"Electronics": 7.4, "Home": 6.8, "Fashion": 6.4, "Grocery": 5.6})[category].to_numpy()
orders = pd.DataFrame({
    "date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
    "city": rng.choice(["Delhi", "Mumbai", "Pune"], n, p=[0.40, 0.35, 0.25]),
    "category": category,
    "channel": rng.choice(["App", "Web"], n, p=[0.6, 0.4]),
    "amount": np.round(rng.lognormal(mu, 0.6)).astype(int)})
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
fig, axs = plt.subplots(1, 3, figsize=(12, 3.9), layout="constrained")
# Relational: x, y, plus colour (hue) and area (size) for two more variables
sns.scatterplot(data=weekly, x="ad_spend", y="revenue_k", hue="discount", size="orders", sizes=(15, 110),
                palette="viridis", legend=False, ax=axs[0])
axs[0].set(title="Relational: scatterplot", xlabel="Ad spend (Rs thousand)", ylabel="Revenue (Rs thousand)")
# Distribution: empirical cumulative distribution, one line per channel
sns.ecdfplot(data=orders, x="amount", hue="channel", palette={"App": BLUE, "Web": ORANGE}, linewidth=2.5, ax=axs[1])
axs[1].set(title="Distribution: ecdfplot", xlabel="Order amount (Rs)", ylabel="Share of orders up to this amount")
# Categorical: mean per category with a 95% bootstrap interval
sns.pointplot(data=orders, x="category", y="amount", hue="channel", palette={"App": BLUE, "Web": ORANGE},
              order=["Electronics", "Home", "Fashion", "Grocery"], hue_order=["App", "Web"], dodge=0.3, errorbar=("ci", 95), seed=8, ax=axs[2])
axs[2].set(title="Categorical: pointplot", xlabel="", ylabel="Average order (Rs)")
sns.move_legend(axs[1], "lower right", title=None, frameon=False)
sns.move_legend(axs[2], "upper right", title=None, frameon=False)
fig.savefig("ch08v_sns_families.png", dpi=110)
print(type(axs[0]).__name__, "| median App:", orders.loc[orders.channel == "App", "amount"].median(),
      "| median Web:", orders.loc[orders.channel == "Web", "amount"].median())
print("saved")
