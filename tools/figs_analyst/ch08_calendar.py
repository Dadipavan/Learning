import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
rng = np.random.default_rng(8)
days = pd.date_range("2025-01-01", "2025-06-30")
base = np.where(days.dayofweek >= 5, 15, 9.5)                      # weekends are busier
orders_per_day = rng.poisson(base)
daily = pd.Series(orders_per_day, index=days, name="orders")
print(daily.groupby(daily.index.dayofweek).mean().round(1).rename(index=dict(enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))).to_string())
first_monday = days[0] - pd.Timedelta(days=days[0].dayofweek)
week = ((days - first_monday).days // 7).to_numpy()
grid = np.full((7, week.max() + 1), np.nan)
grid[days.dayofweek, week] = daily.values
fig, ax = plt.subplots(figsize=(9, 3.4))
im = ax.imshow(grid, cmap="Blues", aspect="equal", vmin=0)
ax.set_yticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
month_start = [(d - first_monday).days // 7 for d in pd.date_range("2025-01-01", "2025-06-01", freq="MS")]
ax.set_xticks(month_start, ["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
cb = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02); cb.set_label("Orders per day")
ax.set_title("Saturdays and Sundays are the busiest days")
fig.tight_layout()
fig.savefig("ch08v_calendar.png", dpi=110)
print("saved")
