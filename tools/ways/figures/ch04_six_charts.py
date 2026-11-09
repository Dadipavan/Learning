import sys, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, pandas as pd, numpy as np
DATA = "/Users/c2487352/Personal/Career/final/study/ways/data/"
sys.path.insert(0, DATA); import prep
o, c, p = prep.load_clean(DATA)
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(2, 3, figsize=(11, 6.2))
m = o.groupby(o.order_date.dt.month).revenue.sum() / 1e6
ax[0, 0].plot(m.index, m.values, color=B, marker="o"); ax[0, 0].set_title("1 Line: revenue by month (millions)"); ax[0, 0].set_xticks(range(1, 13))
k = o.groupby("category").revenue.sum().sort_values() / 1e6
ax[0, 1].barh(k.index, k.values, color=T); ax[0, 1].set_title("2 Bar: revenue by category (millions)")
city = o.groupby("city").revenue.sum().sort_values(ascending=False) / 1e6
ax[0, 2].bar(city.index, city.values, color=B); ax[0, 2].set_title("3 Column: revenue by city (millions)"); ax[0, 2].tick_params(axis="x", rotation=30)
ax[1, 0].hist(o.delivery_minutes.dropna(), bins=40, color=O, edgecolor="white"); ax[1, 0].set_title("4 Histogram: delivery minutes"); ax[1, 0].set_xlabel("minutes")
r = o.groupby("category").apply(lambda d: (d.status == "returned").mean(), include_groups=False).sort_values() * 100
ax[1, 1].barh(r.index, r.values, color=R); ax[1, 1].set_title("5 Bar: return rate by category (%)")
s = o.dropna(subset=["delivery_minutes"]).sample(1500, random_state=1)
ax[1, 2].scatter(s.order_hour + np.random.default_rng(1).uniform(-.3, .3, len(s)), s.delivery_minutes, s=6, alpha=.4, color=P)
ax[1, 2].set_title("6 Scatter: hour vs delivery minutes"); ax[1, 2].set_xlabel("order hour"); ax[1, 2].set_ylim(0, 150)
fig.tight_layout(); fig.savefig("ch04_six_charts.png", dpi=110)
