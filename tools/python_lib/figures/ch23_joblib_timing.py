import time, tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from joblib import Memory, Parallel, delayed
B, O, T = "#2b4fd6", "#b84a22", "#357a70"
def tiny(i):
    return i * i
def heavy(n):
    s = 0
    for k in range(n):
        s += k % 7
    return s
def timeit(f):
    t = time.perf_counter(); f(); return time.perf_counter() - t
with tempfile.TemporaryDirectory() as d:
    cached = Memory(d, verbose=0).cache(heavy)
    t_first = timeit(lambda: cached(3_000_000)); t_second = timeit(lambda: cached(3_000_000))
Parallel(n_jobs=4)(delayed(tiny)(i) for i in range(4))  # warm up workers
res = {}
for name, fn, arg in (("tiny tasks", tiny, 5), ("heavy tasks", heavy, 3_000_000)):
    res[name] = (timeit(lambda: [fn(arg) for _ in range(16)]),
                 timeit(lambda: Parallel(n_jobs=4)(delayed(fn)(arg) for _ in range(16))))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
a1.bar(["first call", "cached call"], [t_first, t_second], color=[O, T])
a1.set_ylabel("seconds", fontsize=13); a1.set_title("joblib.Memory", fontsize=14)
x = np.arange(2)
a2.bar(x - 0.2, [res[k][0] for k in res], 0.4, color=B, label="serial")
a2.bar(x + 0.2, [res[k][1] for k in res], 0.4, color=T, label="n_jobs=4")
a2.set_xticks(x, list(res)); a2.set_yscale("log"); a2.set_title("16 tasks, log scale", fontsize=14)
a2.legend(fontsize=11)
for a in (a1, a2): a.tick_params(labelsize=11)
fig.suptitle("Measured on one machine; your numbers will vary", fontsize=11)
fig.tight_layout(); fig.savefig("lib23_joblib_timing.png")
