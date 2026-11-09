import re, time
from common import *
ns = list(range(14, 25, 2))
bad, good = [], []
for n in ns:
    s = "a" * n + "c"
    t = time.perf_counter(); re.match(r"(a+)+b", s); bad.append(time.perf_counter() - t)
    t = time.perf_counter(); re.match(r"a+b", s); good.append(time.perf_counter() - t)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.semilogy(ns, bad, "o-", color=RED, lw=2, label=r"nested quantifier  (a+)+b")
ax.semilogy(ns, [max(g, 1e-7) for g in good], "s-", color=TEAL, lw=2, label=r"safe  a+b")
ax.set_xlabel("length n of the input  'a' * n + 'c'"); ax.set_ylabel("seconds (log scale)")
ax.set_title("Failing match time roughly doubles per extra character")
ax.grid(alpha=0.3); ax.legend()
save(fig, "ch03_backtracking.png")
