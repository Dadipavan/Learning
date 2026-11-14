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
grid = orders.pivot_table(index="category", columns="city", values="amount", aggfunc="mean").loc[order, ["Delhi", "Mumbai", "Pune"]]
ax = sns.heatmap(grid, annot=True, fmt=",.0f", cmap="Blues", vmin=0, vmax=2500, linewidths=1, linecolor="white",
                 annot_kws={"fontsize": 13, "fontweight": "bold"}, cbar_kws={"label": "Average order (Rs)"})
ax.set(xlabel="", ylabel="")
ax.figure.suptitle("Electronics orders are biggest in Delhi and Mumbai", x=0.02, ha="left", fontweight="bold", fontsize=14, y=1.03)
ax.xaxis.tick_top(); ax.tick_params(length=0)
ax.figure.savefig("ch08v_heatmap_sns.png", dpi=110, bbox_inches="tight")
print(grid.round(0).loc["Electronics"].to_string())
print("saved")
