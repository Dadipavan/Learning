import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
vals = np.array([1, 2, 3])
years = np.array([2019, 2020, 2021, 2024]); sales = np.array([100, 120, 140, 160])
fig, (a, b, c) = plt.subplots(1, 3, figsize=(11, 3.8))
for i, v in enumerate(vals):                         # radius proportional to value: area grows with the SQUARE
    a.add_patch(plt.Circle((i * 2.2 + 1, 2.9), 0.3 * v, color=RED))
    a.add_patch(plt.Circle((i * 2.2 + 1, 0.85), 0.3 * np.sqrt(v) * 1.15, color=TEAL))
a.set(xlim=(0, 7), ylim=(-0.4, 4.2), aspect="equal"); a.axis("off")
a.text(3.5, 4.0, "Radius = value (wrong)", ha="center", color=RED, fontweight="bold")
a.text(3.5, -0.2, "Area = value (right)", ha="center", color=TEAL, fontweight="bold")
b.plot(range(4), sales, color=RED, lw=2.8, marker="o")             # categories equally spaced although years are not
b.set_xticks(range(4), years); b.set_title("Wrong: 2021 to 2024 squeezed", fontsize=12); b.set_ylim(80, 180)
c.plot(years, sales, color=TEAL, lw=2.8, marker="o")
c.set_xticks(years); c.set_title("Right: true time axis", fontsize=12); c.set_ylim(80, 180)
for ax in (b, c): ax.set_ylabel("Sales index")
fig.tight_layout()
fig.savefig("ch08v_lie_scales.png", dpi=110)
print("area ratio when radius is proportional to value (3 vs 1):", (3 / 1) ** 2)
print("growth per year:", [round(float(g), 1) for g in np.diff(sales) / np.diff(years)])
print("saved")
