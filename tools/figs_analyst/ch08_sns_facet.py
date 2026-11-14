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
g = sns.displot(data=orders, x="amount", col="city", row="channel", col_order=["Delhi", "Mumbai", "Pune"], row_order=["App", "Web"], binwidth=400, binrange=(0, 5600),
                color=BLUE, height=2.0, aspect=1.5, facet_kws={"margin_titles": True})
g.set_axis_labels("Order amount (Rs)", "Orders")
g.set_titles(col_template="{col_name}", row_template="{row_name}")
g.set(xticks=[0, 2000, 4000])
g.figure.suptitle("Order sizes have the same shape in every city and channel", x=0.02, ha="left", fontweight="bold", y=1.04)
g.figure.savefig("ch08v_sns_facet.png", dpi=110, bbox_inches="tight")
print(type(g).__name__, "| panels:", g.axes.shape, "| figure size (in):", np.round(g.figure.get_size_inches(), 1).tolist())
print(orders.groupby(["channel", "city"]).size().unstack().to_string())
print("saved")
