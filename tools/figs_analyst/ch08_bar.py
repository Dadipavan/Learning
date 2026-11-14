import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
sales = pd.DataFrame({
    "city":   ["Pune", "Pune", "Pune", "Mumbai", "Mumbai", "Mumbai", "Delhi", "Delhi"],
    "status": ["Delivered", "Delivered", "Returned", "Delivered", "Delivered", "Cancelled", "Delivered", "Delivered"],
    "amount": [998, 1400, 597, 1299, 1298, 450, 799, 2499]})
by_city = sales.groupby("city")["amount"].sum().sort_values(ascending=False)
print(by_city.to_string())
print("grand total:", by_city.sum())
colors = [BLUE if c == by_city.idxmax() else GREY for c in by_city.index]
fig, ax = plt.subplots()
bars = ax.bar(by_city.index, by_city.values, color=colors, width=0.6)
ax.bar_label(bars, labels=[f"{v:,}" for v in by_city.values], padding=3)
ax.set_title("Delhi sold the most: Rs 3,298 of Rs 9,340")
ax.set_ylabel("Sales (Rs)")
ax.set_ylim(0, 3800)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
fig.tight_layout()
fig.savefig("ch08v_bar.png", dpi=110)
print("saved")
