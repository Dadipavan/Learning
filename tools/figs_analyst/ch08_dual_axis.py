import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
sales = np.array([350, 330, 375, 405, 430, 455])
returns = np.array([52, 55, 49, 58, 54, 57])
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
print(f"sales change Jan to Jun: {sales[-1] / sales[0] - 1:+.1%}; returns change: {returns[-1] / returns[0] - 1:+.1%}")

def dual(ax, lim, title):
    ax.plot(months, sales, color=BLUE, lw=2.5, marker="o")
    ax.set_ylim(0, 500); ax.set_ylabel("Sales (Rs thousand)", color=BLUE)
    ax2 = ax.twinx()
    ax2.plot(months, returns, color=RED, lw=2.5, marker="s")
    ax2.set_ylim(*lim); ax2.set_ylabel("Returns (count)", color=RED)
    ax2.spines["right"].set_visible(True)
    ax.set_title(title, fontsize=12)

fig = plt.figure(figsize=(11, 4.4), layout="constrained")
gs = fig.add_gridspec(2, 3, width_ratios=[1.3, 1.3, 1])
dual(fig.add_subplot(gs[:, 0]), (0, 100), "A: returns look flat")
dual(fig.add_subplot(gs[:, 1]), (45, 60), "B: returns 'chase' sales")
top = fig.add_subplot(gs[0, 2]); bot = fig.add_subplot(gs[1, 2], sharex=top)
top.plot(months, sales, color=BLUE, lw=2.5, marker="o"); top.set_ylim(0, 500); top.set_title("C: separate panels", fontsize=12)
top.set_ylabel("Sales (k)"); top.tick_params(labelbottom=False)
bot.plot(months, returns, color=RED, lw=2.5, marker="s"); bot.set_ylim(0, 100); bot.set_ylabel("Returns")
fig.savefig("ch08v_dual_axis.png", dpi=110)
print("saved")
