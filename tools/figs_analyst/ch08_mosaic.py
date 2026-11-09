import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
months = pd.period_range("2024-01", "2025-06", freq="M").to_timestamp()
monthly = pd.Series([310, 295, 340, 360, 385, 400, 380, 410, 430, 470, 560, 620,
                     350, 330, 375, 405, 430, 455], index=months, name="sales_k")
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
import matplotlib.dates as mdates
fig, axd = plt.subplot_mosaic("AAB;AAC;DDD", figsize=(8, 5.2), layout="constrained")
axd["A"].plot(monthly.index, monthly.values, color=BLUE, lw=2.5)
axd["A"].set_title("A: wide panel"); axd["A"].set_ylim(0, 700)
axd["A"].xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
axd["A"].xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
city = orders.groupby("city")["amount"].sum().sort_values()
axd["B"].barh(city.index, city.values / 1000, color=GREY); axd["B"].set_title("B")
axd["C"].hist(orders["amount"], bins=15, color=TEAL); axd["C"].set_title("C")
yoy = (monthly.pct_change(12) * 100).dropna()
axd["D"].bar(yoy.index.strftime("%b"), yoy.values, color=ORANGE); axd["D"].set_title("D: full-width strip: YoY growth, %")
for ax in axd.values(): ax.tick_params(labelsize=9)
print("panels:", list(axd), "| A size (inches):", np.round(axd["A"].get_figure().get_size_inches(), 1))
fig.savefig("ch08v_mosaic.png", dpi=110)
print("saved")
