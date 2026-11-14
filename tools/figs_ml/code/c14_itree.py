import numpy as np
rng = np.random.default_rng(0)
x = np.r_[rng.normal(10, 1.0, 255), 18.0]          # 255 ordinary values and one outlier, n = 256

def path_length(v, data, depth=0, limit=8):
    """Depth at which value v is isolated by random cuts (stops when alone or at the depth limit)."""
    if len(data) <= 1 or depth >= limit: return depth + (c(len(data)) if len(data) > 1 else 0)
    lo, hi = data.min(), data.max()
    if lo == hi: return depth
    cut = rng.uniform(lo, hi)
    side = data[data < cut] if v < cut else data[data >= cut]
    return path_length(v, side, depth + 1, limit)

def c(n):                                           # average path length of an unsuccessful BST search
    return 0.0 if n <= 1 else 2 * (np.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n

n = len(x)
print("c(256) = %.3f" % c(n))
for name, v in [("outlier 18.0", 18.0), ("typical 10.0", x[0]), ("typical 10.5", x[1])]:
    E = np.mean([path_length(v, x) for _ in range(300)])
    print("%-13s mean path length %.2f  anomaly score 2^(-E/c) = %.3f" % (name, E, 2 ** (-E / c(n))))
