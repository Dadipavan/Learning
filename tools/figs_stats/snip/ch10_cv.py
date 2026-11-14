import numpy as np
rng = np.random.default_rng(102)
T, m = 144, 12
t = np.arange(T)
season = 10 * np.sin(2 * np.pi * t / m) + 4 * np.cos(2 * np.pi * t / m * 2)
y = 100 + 0.5 * t + season + rng.normal(0, 3, T)             # trend + seasonality + noise
H = 12
def f_naive(tr, h):  return np.repeat(tr[-1], h)
def f_snaive(tr, h): return np.array([tr[len(tr) - m + (i % m)] for i in range(h)])
def f_drift(tr, h):  return tr[-1] + (tr[-1] - tr[0]) / (len(tr) - 1) * np.arange(1, h + 1)
def f_reg(tr, h):                                              # linear trend + 11 month dummies, fit by least squares
    def X(idx): return np.column_stack([np.ones(len(idx)), idx] + [(idx % m == j).astype(float) for j in range(1, m)])
    idx = np.arange(len(tr)); b = np.linalg.lstsq(X(idx), tr, rcond=None)[0]
    return X(np.arange(len(tr), len(tr) + h)) @ b
models = {"naive": f_naive, "seasonal naive": f_snaive, "drift": f_drift, "trend + seasonal dummies": f_reg}
origins = range(72, T - H + 1, 6)                              # rolling origin, expanding window, 12 origins
print("origins:", len(list(origins)), " horizon:", H)
mae = {k: [] for k in models}
for o in origins:
    tr, te = y[:o], y[o:o + H]
    for k, f in models.items(): mae[k].append(np.mean(np.abs(te - f(tr, H))))
scale = np.mean(np.abs(y[m:72] - y[:72 - m]))                  # MASE scale: in-sample seasonal naive MAE on the first 72 points
print(f"{'model':<26}{'mean MAE':>9}{'worst origin':>14}{'MASE':>7}")
for k in models: print(f"{k:<26}{np.mean(mae[k]):>9.2f}{np.max(mae[k]):>14.2f}{np.mean(mae[k])/scale:>7.2f}")
