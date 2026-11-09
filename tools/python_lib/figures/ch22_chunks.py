import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd, os, tempfile, tracemalloc
BL, OR, TE, RE, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 13, "axes.titlesize": 15})

rng = np.random.default_rng(42); n = 1_000_000
df = pd.DataFrame({"order_id": np.arange(n), "customer_id": rng.integers(0, 50_000, n),
    "region": rng.choice(["EU", "US", "APAC", "LATAM", "MEA"], n), "qty": rng.integers(1, 20, n), "price": rng.normal(50, 15, n).round(2)})
path = os.path.join(tempfile.mkdtemp(), "o.csv"); df.to_csv(path, index=False); del df
def peak(size):
    tracemalloc.start()
    if size is None: pd.read_csv(path)
    else:
        for ch in pd.read_csv(path, chunksize=size): pass
    p = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return p / 1e6
sizes = [1_000, 10_000, 100_000, 500_000]; ys = [peak(s) for s in sizes]; full = peak(None)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(sizes, ys, "o-", color=BL, lw=3, ms=9, label="chunked read")
ax.axhline(full, color=RE, lw=2.5, ls="--", label="read everything (%.0f MB)" % full)
ax.set_xscale("log"); ax.set_xlabel("rows per chunk"); ax.set_ylabel("peak Python memory (MB)")
ax.set_title("Peak memory grows with chunk size, not file size"); ax.legend()
fig.tight_layout(); fig.savefig("lib22_chunks.png", dpi=110)
