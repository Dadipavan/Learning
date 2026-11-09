import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
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
r = np.corrcoef(weekly["ad_spend"], weekly["revenue_k"])[0, 1]
slope, intercept = np.polyfit(weekly["ad_spend"], weekly["revenue_k"], 1)
print(f"r = {r:.2f}   revenue = {intercept:.1f} + {slope:.2f} x ad_spend   r squared = {r ** 2:.2f}")
resid = weekly["revenue_k"] - (intercept + slope * weekly["ad_spend"])
worst = resid.abs().idxmax()
print(f"biggest miss: week {worst}, ad spend {weekly.loc[worst, 'ad_spend']}, revenue {weekly.loc[worst, 'revenue_k']}, "
      f"expected {intercept + slope * weekly.loc[worst, 'ad_spend']:.1f}")
fig, ax = plt.subplots()
ax.scatter(weekly["ad_spend"], weekly["revenue_k"], s=45, color=BLUE, alpha=0.75, edgecolor="white", linewidth=0.8)
xs = np.array([weekly["ad_spend"].min(), weekly["ad_spend"].max()])
ax.plot(xs, intercept + slope * xs, color=ORANGE, lw=2.5)
ax.annotate(f"week {worst}", xy=(weekly.loc[worst, "ad_spend"], weekly.loc[worst, "revenue_k"]),
            xytext=(weekly.loc[worst, "ad_spend"] + 14, weekly.loc[worst, "revenue_k"] - 10),
            arrowprops=dict(arrowstyle="->", color="#333"))
ax.text(24, 155, f"r = {r:.2f}\n+Rs {slope:.1f}k revenue per Rs 1k ads", color=ORANGE, fontweight="bold", va="top")
ax.set_xlabel("Weekly ad spend (Rs thousand)"); ax.set_ylabel("Weekly revenue (Rs thousand)")
ax.set_title("Weeks with more ad spend had more revenue")
fig.tight_layout()
fig.savefig("ch08v_scatter.png", dpi=110)
print("saved")
