import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
names = ["Earbuds", "Watch", "Air fryer", "Yoga mat", "Backpack", "Lamp"]
level = np.array([70, 65, 50, 30, 28, 25])
trend = np.array([4, 1, -1, 0.5, 0, -2])
units = pd.DataFrame(level + np.outer(np.arange(6), trend) + rng.normal(0, 2.5, (6, 6)), columns=names).round(0)
units.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
change = (units.iloc[-1] - units.iloc[0]).astype(int)
print(change.to_string())
fig = plt.figure(figsize=(11, 5.2))
a = fig.add_axes([0.04, 0.12, 0.30, 0.74])
units.plot.bar(stacked=True, ax=a, width=0.8, legend=False)                 # BEFORE: six default colours stacked
a.legend(names, fontsize=8, bbox_to_anchor=(1.0, 1), loc="upper left"); a.set_title("Units by product", fontsize=12, fontweight="normal", loc="center")
plt.setp(a.get_xticklabels(), rotation=0)
gs = fig.add_gridspec(2, 3, left=0.50, right=0.98, bottom=0.12, top=0.84, hspace=0.45, wspace=0.12)
for k, name in enumerate(names):                                           # AFTER: small multiples, same scale
    ax = fig.add_subplot(gs[k // 3, k % 3])
    color = BLUE if name == change.idxmax() else GREY
    ax.plot(range(6), units[name], color=color, lw=3)
    ax.set_ylim(0, 95); ax.set_title(f"{name}  ({change[name]:+d})", fontsize=11, color="#222" if color == BLUE else "#555", loc="left")
    ax.set_xticks([0, 5], ["Jan", "Jun"]); ax.tick_params(labelsize=9)
    if k % 3: ax.set_yticklabels([])
grew = change[change > 10]
assert len(grew) == 1                                                      # the title below claims exactly one
fig.text(0.50, 0.90, f"Only {grew.index[0]} grew by more than 10 units", fontsize=14, fontweight="bold")
fig.text(0.01, 0.97, "BEFORE", color=RED, fontweight="bold", fontsize=13, va="top")
fig.text(0.46, 0.97, "AFTER", color=TEAL, fontweight="bold", fontsize=13, va="top")
fig.savefig("ch08v_makeover5.png", dpi=110)
print("saved")
