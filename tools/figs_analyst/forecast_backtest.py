import numpy as np, pandas as pd, itertools
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(11)
months = pd.period_range("2021-01", periods=48, freq="M")
season = np.array([-8, -10, -4, 0, 3, 5, 4, 6, 2, 10, 18, 22], dtype=float)
y = pd.Series((100 + 1.5*np.arange(48) + np.tile(season, 4) + rng.normal(0, 3, 48)).round(1), index=months)
train, test = y.iloc[:36], y.iloc[36:]
def hw(x, h, m, a, b, g):
    level = x[:m].mean(); trend = (x[m:2*m].mean()-x[:m].mean())/m
    seas = list(x[:m]-level); sse = 0.0
    for t in range(m, len(x)):
        pred = level + trend + seas[t-m]; sse += (x[t]-pred)**2
        prev = level
        level = a*(x[t]-seas[t-m]) + (1-a)*(level+trend)
        trend = b*(level-prev) + (1-b)*trend
        seas.append(g*(x[t]-level) + (1-g)*seas[t-m])
    return sse, np.array([level + (k+1)*trend + seas[len(x)-m+(k % m)] for k in range(h)])
grid = list(itertools.product((0.1,0.3,0.5), (0.05,0.1,0.2), (0.1,0.3,0.5)))
best = min(grid, key=lambda p: hw(train.values, 12, 12, *p)[0])
fc = {"naive": (np.repeat(train.iloc[-1],12), "#6a2fd0"), "seasonal naive": (train.iloc[-12:].values, "#357a70"),
      "3-month average": (np.repeat(train.iloc[-3:].mean(),12), "#aa2d26"), "Holt-Winters": (hw(train.values,12,12,*best)[1], "#b84a22")}
x = np.arange(48)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(x[:36], train.values, color="#2b4fd6", lw=2, label="history (train)")
ax.plot(x[36:], test.values, color="black", lw=2.5, label="actual (test)")
for k, (v, c) in fc.items(): ax.plot(x[36:], v, "--", color=c, lw=1.8, label=k)
ax.axvline(35.5, color="grey", lw=1)
ax.set_xlabel("month number (1 = Jan 2021)", fontsize=11); ax.set_ylabel("sales (Rs thousand)", fontsize=11)
ax.legend(fontsize=9, frameon=False, ncol=2, loc="upper left"); ax.tick_params(labelsize=10)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("forecast_backtest.png")
