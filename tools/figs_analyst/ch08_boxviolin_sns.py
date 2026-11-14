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
order = ["Electronics", "Home", "Fashion", "Grocery"]
pal = [BLUE, TEAL, ORANGE, PURPLE]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
sns.boxplot(data=orders, x="amount", y="category", order=order, hue="category", hue_order=order, palette=pal,
            log_scale=True, legend=False, fliersize=3, saturation=1, ax=ax1)
ax1.set(title="Box plot", xlabel="Order amount (Rs, log scale)", ylabel="")
sns.violinplot(data=orders, x="amount", y="category", order=order, hue="category", hue_order=order, palette=pal,
               log_scale=True, cut=0, inner="quartile", legend=False, saturation=1, ax=ax2)
sns.stripplot(data=orders, x="amount", y="category", order=order, color="black", size=2, alpha=0.35, ax=ax2)
ax2.set(title="Violin + every order", xlabel="Order amount (Rs, log scale)", ylabel="")
for ax in (ax1, ax2):
    ax.set_xticks([100, 300, 1000, 3000], ["100", "300", "1,000", "3,000"]); ax.minorticks_off()
fig.tight_layout()
fig.savefig("ch08v_boxviolin_sns.png", dpi=110)
print(orders.groupby("category")["amount"].describe()[["count", "25%", "50%", "75%"]].round(0).loc[order].to_string())
print("saved")
