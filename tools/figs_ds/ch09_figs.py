import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import numpy as np
from sklearn.linear_model import LinearRegression
rng = np.random.default_rng(4)
n, split = 400, 300
occur = rng.random(n) < 0.2; size = rng.poisson(4, n) + 1
d = np.where(occur, size, 0).astype(float)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.bar(np.arange(split, n), d[split:], color=GREY, alpha=0.7, label="actual demand (test days)")
for val, c, lab in [(0.0, RED, "forecast 0 (best MAE)"), (0.796, BLUE, "TSB 0.80 (best bias and RMSE)"), (d[split-1], ORANGE, "last value")]:
    ax.axhline(val, color=c, lw=2, label=lab)
ax.set_xlabel("day"); ax.set_ylabel("units"); ax.set_title("Intermittent demand: most days are zero"); ax.legend(fontsize=8.5)
save("ds_ch09_intermittent.png")
rng = np.random.default_rng(6)
n = 500; t = np.arange(n)
y = 200 + 0.2*t + 25*np.sin(2*np.pi*t/7) + rng.normal(0, 8, n) * (1 + 0.004*t)
X = np.c_[t, np.sin(2*np.pi*t/7), np.cos(2*np.pi*t/7)]
m = LinearRegression().fit(X[:300], y[:300])
res = np.abs(y[300:400] - m.predict(X[300:400])); k = int(np.ceil(101*0.9)); q = np.sort(res)[k-1]
sd = (y[:300] - m.predict(X[:300])).std()
pred = m.predict(X[400:]); tt = t[400:]
fig, ax = plt.subplots(figsize=(8, 4))
ax.fill_between(tt, pred - q, pred + q, color=BLUE, alpha=0.18, label="conformal 90% band")
ax.fill_between(tt, pred - 1.645*sd, pred + 1.645*sd, color=ORANGE, alpha=0.3, label="normal 90% band from training residuals")
ax.plot(tt, y[400:], color="#222", lw=1, label="actual")
ax.set_xlabel("day"); ax.set_ylabel("orders"); ax.set_title("Two 90% intervals on the last 100 days"); ax.legend(fontsize=8.5, loc="upper left")
save("ds_ch09_conformal.png")
