import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, math
from functools import reduce
from operator import add
rng = np.random.default_rng(0)
values = (rng.normal(size=100_000) * 10.0 ** rng.integers(-3, 8, size=100_000)).tolist()
ref = math.fsum(values)
errs = []
for t in range(300):
    o = values[:]; np.random.default_rng(t).shuffle(o); errs.append(reduce(add, o) - ref)
errs = np.array(errs)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.hist(errs * 1e6, bins=30, color="#2b4fd6", alpha=.85)
ax.axvline(0, color="#aa2d26", lw=2, label="exact sum (math.fsum)")
ax.set_xlabel("error of left-to-right sum (x 1e-6)"); ax.set_ylabel("number of shuffles (of 300)")
ax.set_title("Same 100,000 numbers, 300 different orders: the sum wanders")
ax.legend(); ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig("ch02d_float_order.png", dpi=110)
print("std of error:", errs.std(), "distinct sums:", len(set(errs.tolist())))
