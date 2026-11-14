import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

import tracemalloc, io
import pandas as pd
rng = np.random.default_rng(0)
n = 200_000
df = pd.DataFrame({"id": np.arange(n), "x": rng.normal(size=n), "y": rng.integers(0, 100, n), "tag": rng.choice(["a", "b", "c"], n)})
import tempfile, os
path = os.path.join(tempfile.mkdtemp(), "big.csv"); df.to_csv(path, index=False); del df
def peak(chunk):
    tracemalloc.start()
    total = 0.0
    if chunk is None:
        total = pd.read_csv(path)["x"].sum()
    else:
        for part in pd.read_csv(path, chunksize=chunk):
            total += part["x"].sum()
    _, p = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return p / 1e6
labels = ["whole file", "100k rows", "20k rows", "5k rows", "1k rows"]
vals = [peak(None), peak(100_000), peak(20_000), peak(5_000), peak(1_000)]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
bars = ax.bar(labels, vals, color=[R, O, B, T, T])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.1f}", ha="center", va="bottom")
ax.set_ylabel("peak Python memory (MB, tracemalloc)")
ax.set_title("Chunked reading keeps memory low (200k-row CSV)")
fig.tight_layout(); fig.savefig("lib20_chunking.png")
