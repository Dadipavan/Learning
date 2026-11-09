import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
months = np.arange(0, 11)
signups = 100 * 2 ** months                       # doubles every month
print("signups:", signups.tolist())
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 3.8), layout="constrained")
ax1.plot(months, signups, color=BLUE, lw=2.5, marker="o"); ax1.set_title("Linear axis")
ax1.yaxis.set_major_formatter("{x:,.0f}")
ax2.plot(months, signups, color=BLUE, lw=2.5, marker="o"); ax2.set_yscale("log"); ax2.set_title("Log axis: a straight line")
ax2.set_yticks([100, 1000, 10000, 100000], ["100", "1,000", "10,000", "100,000"]); ax2.minorticks_off()
rs = np.array([350, 330, 375, 405, 430, 455])
ax3.plot(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], rs, color=ORANGE, lw=2.5, marker="o")
ax3.set_title("Second axis, other unit"); ax3.set_ylabel("Rs thousand"); ax3.set_ylim(300, 500)
sec = ax3.secondary_yaxis("right", functions=(lambda r: r / 84, lambda d: d * 84))      # illustrative rate: Rs 84 per US dollar
sec.set_ylabel("US dollars thousand (at Rs 84)"); sec.spines["right"].set_visible(True)
for ax in (ax1, ax2):
    ax.set_xlabel("Months since launch"); ax.set_ylabel("Signups"); ax.set_xticks(range(0, 11, 2))
fig.savefig("ch08v_scales.png", dpi=110)
print("log10 of the values:", np.round(np.log10(signups[[0, 5, 10]]), 2).tolist())
print("saved")
