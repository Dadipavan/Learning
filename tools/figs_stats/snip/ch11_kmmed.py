import numpy as np
rng = np.random.default_rng(17)
n = 600
annual = (rng.random(n) < 0.4).astype(float); tickets = rng.poisson(1.5, n)
rate = 0.05 * np.exp(-0.7 * annual + 0.25 * tickets)
te = rng.exponential(1 / rate); tc = rng.uniform(6, 36, n)
time = np.minimum(te, tc); event = (te <= tc).astype(int)
def km_table(time, event):
    S = 1.0; rows = []
    for u in np.sort(np.unique(time[event == 1])):
        r = (time >= u).sum(); d = ((time == u) & (event == 1)).sum()
        S *= 1 - d / r; rows.append((u, S))
    return np.array(rows)
for g, name in ((0, "monthly"), (1, "annual")):
    m = annual == g
    k = km_table(time[m], event[m])
    median = k[np.argmax(k[:, 1] <= 0.5), 0]
    s12 = k[k[:, 0] <= 12][-1, 1]
    print(f"{name:8s} customers {m.sum()}  events {event[m].sum()}  median {median:.1f} months  S(12) {s12:.3f}")
