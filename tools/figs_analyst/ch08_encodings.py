import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
vals = np.array([50, 46, 40, 30, 20])
names = list("ABCDE")
fig, axs = plt.subplots(2, 2, figsize=(8, 5.4))
axs[0, 0].bar(names, vals, color=BLUE)
axs[0, 0].set_title("Length (bars)")
axs[0, 0].set_yticks([])
axs[0, 1].pie(vals, labels=names, colors=[BLUE, ORANGE, TEAL, RED, PURPLE],
              startangle=90, counterclock=False, wedgeprops={"edgecolor": "white"})
axs[0, 1].set_title("Angle (pie)")
radius = np.sqrt(vals / np.pi)                       # area proportional to value
for i, (r, nm) in enumerate(zip(radius, names)):
    axs[1, 0].add_patch(plt.Circle((i * 2 + 1, 0), r * 0.17, color=BLUE))
    axs[1, 0].text(i * 2 + 1, -1.15, nm, ha="center")
axs[1, 0].set(xlim=(-0.2, 10.2), ylim=(-1.5, 1.2), aspect="equal"); axs[1, 0].axis("off")
axs[1, 0].set_title("Area (bubbles)", loc="left")
axs[1, 1].imshow(vals[None, :], cmap="Blues", vmin=0, vmax=55, aspect=1.0)
axs[1, 1].set_xticks(range(5), names); axs[1, 1].set_yticks([])
axs[1, 1].set_title("Shade (colour)")
for ax in axs.ravel(): ax.spines[["left", "bottom"]].set_visible(False)
fig.tight_layout()
fig.savefig("ch08v_encodings.png", dpi=110)
print("values:", vals.tolist())
print("A/B by length:", round(vals[0] / vals[1], 3))
print("pie angle of A and B (degrees):", np.round(360 * vals[:2] / vals.sum(), 1).tolist())
print("A/B radius ratio when area is proportional:", round(np.sqrt(vals[0] / vals[1]), 3))
print("saved")
