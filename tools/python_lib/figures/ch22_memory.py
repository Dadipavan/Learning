import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd, os, tempfile, tracemalloc
BL, OR, TE, RE, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 13, "axes.titlesize": 15})

rng = np.random.default_rng(42); n = 1_000_000
df = pd.DataFrame({"order_id": np.arange(n), "customer_id": rng.integers(0, 50_000, n),
    "region": rng.choice(["EU", "US", "APAC", "LATAM", "MEA"], n), "qty": rng.integers(1, 20, n), "price": rng.normal(50, 15, n).round(2)})
small = df.assign(order_id=pd.to_numeric(df.order_id, downcast="unsigned"), customer_id=pd.to_numeric(df.customer_id, downcast="unsigned"),
    region=df.region.astype("category"), qty=pd.to_numeric(df.qty, downcast="unsigned"), price=df.price.astype("float32"))
mb = lambda d: [d[c].memory_usage(deep=True, index=False) / 1e6 for c in df]
a, b = mb(df), mb(small); x = np.arange(len(df.columns)); w = 0.38
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(x - w / 2, a, w, color=OR, label="default dtypes (%.0f MB)" % sum(a))
ax.bar(x + w / 2, b, w, color=TE, label="downcast + category (%.0f MB)" % sum(b))
ax.set_xticks(x); ax.set_xticklabels(list(df), rotation=15); ax.set_ylabel("MB (1M rows)")
ax.legend(); ax.set_title("Memory per column, measured")
fig.tight_layout(); fig.savefig("lib22_memory.png", dpi=110)
