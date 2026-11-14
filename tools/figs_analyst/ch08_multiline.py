import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
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
orders["month"] = orders["date"].dt.to_period("M").dt.to_timestamp()
city_m = orders.pivot_table(index="month", columns="city", values="amount", aggfunc="sum") / 1000
city_m = city_m.round(1)
print(city_m.to_string())
colors = {"Delhi": BLUE, "Mumbai": ORANGE, "Pune": GREY}
fig, ax = plt.subplots()
for city in city_m.columns:
    ax.plot(city_m.index, city_m[city], color=colors[city], lw=2.8, marker="o")
    ax.text(city_m.index[-1] + pd.Timedelta(days=6), city_m[city].iloc[-1], city,
            color="#666" if city == "Pune" else colors[city], va="center", fontweight="bold")
ax.set_xticks(city_m.index, [d.strftime("%b") for d in city_m.index])
ax.set_xlim(city_m.index[0] - pd.Timedelta(days=8), city_m.index[-1] + pd.Timedelta(days=30))
ax.set_ylim(0, 35)
ax.set_ylabel("Sales (Rs thousand)")
ax.set_title("Delhi climbed to 30k in June while Mumbai fell")
fig.tight_layout()
fig.savefig("ch08v_multiline.png", dpi=110)
print("saved")
