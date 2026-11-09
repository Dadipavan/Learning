import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
n = 300
category = rng.choice(["Electronics", "Home", "Fashion", "Grocery"], n, p=[0.2, 0.25, 0.3, 0.25])
mu = pd.Series({"Electronics": 7.4, "Home": 6.8, "Fashion": 6.4, "Grocery": 5.6})[category].to_numpy()
orders = pd.DataFrame({
    "date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
    "city": rng.choice(["Delhi", "Mumbai", "Pune"], n, p=[0.40, 0.35, 0.25]),
    "category": category,
    "channel": rng.choice(["App", "Web"], n, p=[0.6, 0.4]),
    "amount": np.round(rng.lognormal(mu, 0.6)).astype(int)})
order = ["Electronics", "Home", "Fashion", "Grocery"]
grid = orders.pivot_table(index="category", columns="city", values="amount", aggfunc="mean").loc[order, ["Delhi", "Mumbai", "Pune"]]
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2))
im = a.imshow(grid.values, cmap="jet", aspect="auto")                      # BEFORE: rainbow, no numbers
a.set_xticks(range(3), grid.columns); a.set_yticks(range(4), grid.index); a.set_title("Average order", fontsize=12, fontweight="normal", loc="center")
fig.colorbar(im, ax=a)
im2 = b.imshow(grid.values, cmap="Blues", vmin=0, vmax=2500, aspect="auto")      # AFTER
b.set_xticks(range(3), grid.columns); b.set_yticks(range(4), grid.index); b.xaxis.tick_top(); b.tick_params(length=0)
for i in range(4):
    for j in range(3):
        v = grid.values[i, j]
        b.text(j, i, f"{v:,.0f}", ha="center", va="center", fontweight="bold", fontsize=12, color="white" if v > 1250 else "#222")
for sp in b.spines.values(): sp.set_visible(False)
ratio = grid.loc["Electronics"] / grid.drop("Electronics").max(axis=0)       # Electronics vs the next-largest category
b.set_title(f"Electronics orders are {ratio.min():.1f} to {ratio.max():.1f}\ntimes the next category", pad=30, loc="left", fontsize=13)
fig.colorbar(im2, ax=b, label="Average order (Rs)")
fig.text(0.01, 0.97, "BEFORE", color=RED, fontweight="bold", fontsize=13, va="top")
fig.text(0.50, 0.97, "AFTER", color=TEAL, fontweight="bold", fontsize=13, va="top")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("ch08v_makeover4.png", dpi=110)
print(ratio.round(1).to_string())
print("saved")
