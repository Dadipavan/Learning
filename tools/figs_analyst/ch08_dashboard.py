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
orders["quarter"] = np.where(orders["date"] < "2025-04-01", "Q1", "Q2")
q = orders.groupby("quarter")["amount"].sum()
kpi = {"Sales": f"Rs {orders['amount'].sum() / 1000:,.1f}k", "Orders": f"{len(orders):,}",
       "Average order": f"Rs {orders['amount'].mean():,.0f}", "Q2 vs Q1": f"{q['Q2'] / q['Q1'] - 1:+.1%}"}
monthly = orders.groupby("month")["amount"].sum() / 1000
by_city = (orders.groupby("city")["amount"].sum() / 1000).sort_values()
by_cat = orders.groupby("category")["amount"].mean().sort_values()
chg_city = (orders.pivot_table(index="city", columns="quarter", values="amount", aggfunc="sum").diff(axis=1)["Q2"] / 1000)
chg_cat = (orders.pivot_table(index="category", columns="quarter", values="amount", aggfunc="sum").diff(axis=1)["Q2"] / 1000)
worst_city, worst_cat = chg_city.idxmin(), chg_cat.idxmin()

def tile(ax, label, value, color="#222"):
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="#f3f5fa", zorder=0))
    ax.text(0.06, 0.74, label, transform=ax.transAxes, fontsize=12, color="#555")
    ax.text(0.06, 0.22, value, transform=ax.transAxes, fontsize=24, fontweight="bold", color=color)

def bars(ax, s, title, highlight, fmt, xlabel):
    colors = [BLUE if i == highlight else GREY for i in s.index]
    b = ax.barh(s.index, s.values, color=colors, height=0.65)
    ax.bar_label(b, labels=[fmt.format(v) for v in s.values], padding=4, fontsize=11)
    ax.set_title(title, fontsize=13); ax.set_xlabel(xlabel, fontsize=11)
    ax.set_xlim(0, s.max() * 1.22); ax.tick_params(axis="y", length=0, labelsize=11); ax.tick_params(axis="x", labelsize=10)

fig = plt.figure(figsize=(12, 7), layout="constrained")
gs = fig.add_gridspec(3, 4, height_ratios=[0.75, 2.3, 2.3])
for j, (label, value) in enumerate(kpi.items()):
    tile(fig.add_subplot(gs[0, j]), label, value, RED if label == "Q2 vs Q1" else "#222")
ax = fig.add_subplot(gs[1, :3])                                         # trend
ax.plot(monthly.index, monthly.values, color=BLUE, lw=3, marker="o")
ax.set_xticks(monthly.index, [d.strftime("%b") for d in monthly.index])
ax.set_ylim(0, 70); ax.set_ylabel("Rs thousand", fontsize=11); ax.set_title("Monthly sales", fontsize=13)
ax.annotate("April dip", xy=(monthly.index[3], monthly.iloc[3]), xytext=(monthly.index[3], 12), ha="center",
            arrowprops=dict(arrowstyle="->", color="#444"), fontsize=11, color="#444")
bars(fig.add_subplot(gs[1, 3]), by_city, "Sales by city\n(blue: biggest Q2 fall)", worst_city, "{:,.0f}k", "Rs thousand")
bars(fig.add_subplot(gs[2, :2]), by_cat, "Average order by category\n(blue: biggest Q2 fall in sales)", worst_cat, "Rs {:,.0f}", "Rs")
ax = fig.add_subplot(gs[2, 2:])
ax.hist(orders["amount"], bins=np.arange(0, 5800, 250), color=TEAL, edgecolor="white")
ax.axvline(orders["amount"].median(), color=ORANGE, lw=2.5)
ax.text(orders["amount"].median() + 80, ax.get_ylim()[1] * 0.9, f"median Rs {orders['amount'].median():,.0f}", color=ORANGE, fontweight="bold")
ax.set_title("Order size", fontsize=13); ax.set_xlabel("Rs per order", fontsize=11); ax.set_ylabel("Orders", fontsize=11)
fig.suptitle(f"Sales fell {abs(q['Q2'] / q['Q1'] - 1):.0%} in Q2: {worst_city} ({chg_city.min():+.1f}k) and {worst_cat} ({chg_cat.min():+.1f}k) lead the drop",
             x=0.01, ha="left", fontsize=17, fontweight="bold")
fig.savefig("ch08v_dashboard.png", dpi=110)
print(kpi)
print("worst city:", worst_city, round(chg_city.min(), 1), "| worst category:", worst_cat, round(chg_cat.min(), 1))
print("saved")
