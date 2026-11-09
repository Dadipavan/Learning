import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

gas = [1, 2, 3, 4, 5]; cost = [3, 4, 5, 1, 2]
net = [g - c for g, c in zip(gas, cost)]
pref = [0]
for v in net:
    pref.append(pref[-1] + v)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(range(6), pref, "-o", color=BLUE, lw=3, ms=9)
m = pref.index(min(pref))
ax.plot([m], [pref[m]], "o", color=RED, ms=16)
ax.annotate("lowest point: start at the next station (3)", (m, pref[m]), (0.2, -4.6), fontsize=13, arrowprops=dict(arrowstyle="->", color=RED, lw=2))
ax.axhline(0, color="black", lw=1)
ax.set_xlabel("stations passed, starting at station 0")
ax.set_ylabel("running gas minus cost")
ax.set_title("net = gas - cost = " + str(net), fontsize=14)
ax.set_ylim(-7.5, 1.5)
plt.tight_layout()
plt.savefig("dsa10_gas.png", dpi=110)
