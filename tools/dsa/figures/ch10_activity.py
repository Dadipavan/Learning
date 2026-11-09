import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

acts = [("A",1,4),("B",3,5),("C",0,6),("D",5,7),("E",3,9),("F",5,9),("G",6,10),("H",8,11),("I",8,12),("J",2,14),("K",12,16)]
acts.sort(key=lambda a: a[2])
last = -1
fig, ax = plt.subplots(figsize=(8, 4.8))
for row, (n, s, e) in enumerate(acts):
    pick = s >= last
    if pick:
        last = e
    ax.barh(len(acts) - row, e - s, left=s, height=0.7, color=BLUE if pick else GREY, edgecolor="black")
    ax.text(s + (e - s) / 2, len(acts) - row, n, ha="center", va="center", color="white" if pick else "black", fontweight="bold")
ax.set_yticks([])
ax.set_xticks(range(0, 17, 2))
ax.set_xlabel("time")
ax.set_title("Sorted by END time: blue = picked, grey = clashes")
for s in (0,):
    pass
plt.tight_layout()
plt.savefig("dsa10_activity.png", dpi=110)
