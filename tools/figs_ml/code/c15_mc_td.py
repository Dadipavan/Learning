import numpy as np
# 5-state random walk: states 1..5, start at 3, step left/right with prob 0.5.
# Left end (0) pays 0, right end (6) pays 1. True value of state i is i/6.
true = np.arange(1, 6) / 6
def episode(rng):
    s, path = 3, []
    while 0 < s < 6:
        path.append(s); s += rng.choice([-1, 1])
    return path, float(s == 6)

def mc(rng, n_ep, alpha):
    V = np.full(7, 0.5); V[0] = V[6] = 0
    for _ in range(n_ep):
        path, G = episode(rng)
        for s in path: V[s] += alpha * (G - V[s])
    return V[1:6]

def td(rng, n_ep, alpha):
    V = np.full(7, 0.5); V[0] = V[6] = 0
    for _ in range(n_ep):
        s = 3
        while 0 < s < 6:
            ns = s + rng.choice([-1, 1]); r = float(ns == 6)
            V[s] += alpha * (r + V[ns] - V[s]); s = ns
    return V[1:6]

for alpha in (0.02, 0.05, 0.1):
    e_mc, e_td = [], []
    for seed in range(200):
        e_mc.append(np.sqrt(np.mean((mc(np.random.default_rng(seed), 50, alpha) - true) ** 2)))
        e_td.append(np.sqrt(np.mean((td(np.random.default_rng(seed), 50, alpha) - true) ** 2)))
    print("alpha %.2f  RMS error after 50 episodes: MC %.3f  TD(0) %.3f" % (alpha, np.mean(e_mc), np.mean(e_td)))
