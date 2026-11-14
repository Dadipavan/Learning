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
fig, ax = plt.subplots(figsize=(8, 4.8))
fig.subplots_adjust(left=0.15, right=0.96, top=0.78, bottom=0.2)
x = np.arange(6)
ax.plot(x, monthly.iloc[:6].values, color=GREY, marker="o", lw=2.5, label="Jan to Jun 2024")
ax.plot(x, monthly.iloc[12:18].values, color=BLUE, marker="o", lw=2.5, label="Jan to Jun 2025")
ax.set_xticks(x, ["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
ax.set_ylim(250, 500)
ax.set_ylabel("Sales (Rs thousand)")
ax.set_title("Sales ran 10% to 14% above last year", pad=30)
ax.text(0, 1.04, "Monthly sales, Rs thousand, first half of each year", transform=ax.transAxes, color="#555")
ax.grid(axis="y", color="#dddddd", lw=0.8); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower right")
ax.annotate("Jun 2025: 455\n(+13.7% on Jun 2024)", xy=(5, 455), xytext=(2.6, 465),
            arrowprops=dict(arrowstyle="->", color="#333"), color="#333")
fig.text(0.15, 0.04, "Source: monthly sales table, Chapter 2", color="#666", fontsize=10)

def badge(n, xy, coords="figure fraction"):
    ax.annotate(str(n), xy=xy, xycoords=coords, ha="center", va="center", fontsize=10, color="white",
                fontweight="bold", bbox=dict(boxstyle="circle,pad=0.25", fc=RED, ec="none"), zorder=10)
badge(1, (0.095, 0.877)); badge(2, (0.69, 0.81)); badge(3, (0.08, 0.27)); badge(4, (0.118, 0.745))
badge(5, (1.5, 400), "data"); badge(6, (1.0, 351), "data"); badge(7, (0.705, 0.29)); badge(8, (2.3, 470), "data")
badge(9, (2, 0.105), ("data", "figure fraction")); badge(10, (0.125, 0.045)); badge(11, (4.5, 250), "data")
fig.savefig("ch08v_anatomy.png", dpi=110)
print("jun growth:", round((455 / 400 - 1) * 100, 1), "| jan growth:", round((350 / 310 - 1) * 100, 1))
print("saved")
