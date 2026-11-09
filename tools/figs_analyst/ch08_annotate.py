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
import matplotlib.dates as mdates
fig, ax = plt.subplots()
ax.plot(monthly.index, monthly.values, color=BLUE, lw=2.5)
target = 450
ax.axhline(target, color=GREY, ls="--", lw=1.5)
ax.text(monthly.index[0], target + 8, "target: 450k", color="#555")
ax.fill_between(monthly.index, monthly.values, target, where=monthly.values >= target, color=TEAL, alpha=0.35,
                interpolate=True)
peak = monthly.idxmax()
ax.annotate("Festive peak\n620k", xy=(peak, 620), xytext=(pd.Timestamp("2024-06-15"), 600),
            fontsize=12, ha="center", va="center", color=RED,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=RED),
            arrowprops=dict(arrowstyle="-|>", color=RED, connectionstyle="arc3,rad=-0.25", lw=1.8))
ax.set_ylim(250, 700); ax.set_ylabel("Sales (Rs thousand)")
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_title("Only four months beat the 450k target")
fig.tight_layout()
fig.savefig("ch08v_annotate.png", dpi=110)
print("months above target:", monthly[monthly >= target].index.strftime("%b %Y").tolist())
print("saved")
