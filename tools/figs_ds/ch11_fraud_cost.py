import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
rng = np.random.default_rng(5)
n = 60000
fraud = (rng.random(n) < 0.01).astype(int)
amount = np.where(fraud == 1, rng.lognormal(5.0, 0.8, n), rng.lognormal(4.2, 0.8, n)).round(2)
night = np.where(fraud == 1, rng.random(n) < 0.45, rng.random(n) < 0.2).astype(int)
ring = (fraud == 1) & (rng.random(n) < 0.6)
device = np.where(ring, rng.integers(0, 60, n), 1000 + np.arange(n))
family = rng.random(n) < 0.15
device = np.where((fraud == 0) & family, 1000 + rng.integers(0, 20000, n), device)
df = pd.DataFrame(dict(amount=amount, night=night, device=device, fraud=fraud))
df["acc_on_device"] = df.groupby("device").device.transform("size")
train = np.arange(n) < 40000; test = ~train
y = df.fraud[test].values; amt = df.amount[test].values
ths = np.linspace(0.005, 0.6, 120)
fig, ax = plt.subplots(figsize=(8, 4.2))
for name, cols, c in [("amount + night", ["amount", "night"], ORANGE), ("with device graph feature", ["amount", "night", "acc_on_device"], BLUE)]:
    m = HistGradientBoostingClassifier(random_state=0).fit(df.loc[train, cols], df.fraud[train])
    s = m.predict_proba(df.loc[test, cols])[:, 1]
    cost = [5 * (s >= t).sum() + amt[(s < t) & (y == 1)].sum() for t in ths]
    ax.plot(ths, cost, color=c, lw=2, label=name)
    i = int(np.argmin(cost)); ax.plot(ths[i], cost[i], "o", color=c)
ax.axhline(amt[y == 1].sum(), color=GREY, ls="--", label="flag nothing")
ax.set_xlabel("flag a transaction if score is at least this"); ax.set_ylabel("total cost (rupees)")
ax.set_title("Cost against threshold on 20,000 test transactions"); ax.legend()
save("ds_ch11_fraud_cost.png")
