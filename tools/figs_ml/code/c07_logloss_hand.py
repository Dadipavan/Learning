import numpy as np
x = np.arange(1, 7); y = np.array([0, 0, 1, 0, 1, 1.0])
lam, eta = 1.0, 0.5
F = np.zeros(6)
def logloss(F):
    p = 1 / (1 + np.exp(-F)); return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
print("round 0: log loss %.4f" % logloss(F))
for rnd in (1, 2):
    p = 1 / (1 + np.exp(-F)); g = p - y; h = p * (1 - p)
    print("round", rnd, "p =", np.round(p, 3), "g =", np.round(g, 3))
    best = None
    for k in range(1, 6):                      # split after row k
        GL, HL, GR, HR = g[:k].sum(), h[:k].sum(), g[k:].sum(), h[k:].sum()
        gain = 0.5 * (GL**2 / (HL + lam) + GR**2 / (HR + lam) - (GL + GR)**2 / (HL + HR + lam))
        if best is None or gain > best[0]: best = (gain, k, -GL / (HL + lam), -GR / (HR + lam))
    gain, k, wl, wr = best
    print("  best split after row %d, gain %.4f, leaf values %.4f and %.4f" % (k, gain, wl, wr))
    F = F + eta * np.where(x <= k, wl, wr)
    print("  new F =", np.round(F, 4))
    print("  log loss %.4f" % logloss(F))
