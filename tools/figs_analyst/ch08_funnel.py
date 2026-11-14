import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
steps = pd.DataFrame({"step": ["Visited site", "Added to cart", "Started checkout", "Paid"],
                      "users": [10000, 3800, 1900, 1330]})
steps["step_conv"] = (steps["users"] / steps["users"].shift(1) * 100).round(1)
steps["overall"] = (steps["users"] / steps["users"].iloc[0] * 100).round(1)
print(steps.to_string(index=False))
fig, ax = plt.subplots()
y = np.arange(len(steps))[::-1]
ax.barh(y, steps["users"], color=[GREY, GREY, GREY, BLUE], height=0.7)
ax.barh(y, -steps["users"], color=[GREY, GREY, GREY, BLUE], height=0.7)       # mirror for the funnel look
for yi, u, c in zip(y, steps["users"], steps["step_conv"]):
    ax.text(0, yi, f"{u:,}", ha="center", va="center", color="white", fontweight="bold")
    if not np.isnan(c):
        ax.text(u + 250, yi, f"{c:.0f}% of previous step", va="center", color="#333")
ax.set_yticks(y, steps["step"])
ax.set_xlim(-5200, 8800); ax.set_xticks([])
ax.spines[["left", "bottom"]].set_visible(False); ax.tick_params(length=0)
ax.set_title("Cart to checkout loses half of shoppers (50%)")
fig.tight_layout()
fig.savefig("ch08v_funnel.png", dpi=110)
print("saved")
