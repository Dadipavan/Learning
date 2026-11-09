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
peak = monthly.idxmax()
baseline = monthly.loc["2024-01":"2024-10"].mean()
print(f"peak {monthly.max()}k in {peak:%b %Y}; Jan to Oct 2024 average {baseline:.0f}k; peak / average = {monthly.max() / baseline:.2f}")
fig, ax = plt.subplots()
ax.plot(monthly.index, monthly.values, color=BLUE, lw=2.5, marker="o", ms=5)
ax.annotate(f"{peak:%b %Y}: {monthly.max()}k", xy=(peak, monthly.max()), xytext=(pd.Timestamp("2024-04-15"), 630),
            arrowprops=dict(arrowstyle="->", color="#333"), va="center")
ax.axvspan(pd.Timestamp("2024-10-20"), pd.Timestamp("2024-12-31"), color=ORANGE, alpha=0.12)
ax.text(pd.Timestamp("2024-11-25"), 80, "festive\nseason", ha="center", color=ORANGE)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_ylim(0, 700)
ax.set_ylabel("Sales (Rs thousand)")
ax.set_title("The festive season lifted sales to 620k in Dec 2024")
fig.tight_layout()
fig.savefig("ch08v_line.png", dpi=110)
print("saved")
