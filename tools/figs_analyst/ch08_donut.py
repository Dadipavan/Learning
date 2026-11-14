import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
channel = pd.Series({"App": 180.658, "Web": 95.579})
share = channel / channel.sum()
print((share * 100).round(1).to_string())
revenue = pd.Series({"Wireless earbuds": 412, "Smart watch": 388, "Air fryer": 301, "Yoga mat": 187,
                     "Backpack": 176, "Desk lamp": 152, "Water bottle": 129}).sort_values(ascending=False)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.2))
ax1.pie(channel, colors=[BLUE, GREY], startangle=90, counterclock=False, wedgeprops={"width": 0.38, "edgecolor": "white"})
ax1.text(0, 0, f"{share['App']:.0%}\nvia app", ha="center", va="center", fontsize=15, fontweight="bold")
ax1.set_title("Acceptable: 2 parts")
ax1.text(0, -1.3, f"Web: {share['Web']:.0%}", ha="center", color="#555")
ax2.pie(revenue, labels=revenue.index, startangle=90, counterclock=False, textprops={"fontsize": 9},
        colors=[BLUE, ORANGE, TEAL, RED, PURPLE, GREY, "#d9a400"], wedgeprops={"edgecolor": "white"})
ax2.set_title("Avoid: 7 close slices")
fig.tight_layout()
fig.savefig("ch08v_donut.png", dpi=110)
print("saved")
