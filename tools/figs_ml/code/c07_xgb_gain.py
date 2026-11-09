import numpy as np
x = np.arange(1, 9); y = np.array([2, 3, 3, 2, 8, 9, 7, 9.0])
F0 = y.mean(); g = F0 - y; h = np.ones(8)       # squared error: g = F - y, h = 1
print("F0 = %.3f  g = %s" % (F0, np.round(g, 3)))
def gain(k, lam, gamma):
    GL, HL, GR, HR = g[:k].sum(), h[:k].sum(), g[k:].sum(), h[k:].sum()
    return 0.5 * (GL**2 / (HL + lam) + GR**2 / (HR + lam) - (GL + GR)**2 / (HL + HR + lam)) - gamma
print("split after row k:    " + "  ".join("%6d" % k for k in range(1, 8)))
for lam in (0, 1, 10):
    print("gain, lambda=%-2d g=0:  " % lam + "  ".join("%6.3f" % gain(k, lam, 0) for k in range(1, 8)))
lam = 1
k = 4
GL, HL, GR, HR = g[:k].sum(), h[:k].sum(), g[k:].sum(), h[k:].sum()
print("split after row 4: G_L %.3f H_L %d G_R %.3f H_R %d" % (GL, HL, GR, HR))
for lam in (0, 1, 10):
    print("lambda=%-2d leaf values: left %.4f right %.4f" % (lam, -GL / (HL + lam), -GR / (HR + lam)))
def best_inside(lo, hi, lam, gamma):
    # best split inside rows lo..hi-1 (python slice), same g and h as above
    best = (-1e9, None)
    for k in range(lo + 1, hi):
        GL, HL, GR, HR = g[lo:k].sum(), h[lo:k].sum(), g[k:hi].sum(), h[k:hi].sum()
        gn = 0.5 * (GL**2 / (HL + lam) + GR**2 / (HR + lam) - (GL + GR)**2 / (HL + HR + lam)) - gamma
        best = max(best, (gn, k))
    return best
for lam in (0, 1):
    for gamma in (0, 1, 3):
        bl, br = best_inside(0, 4, lam, gamma), best_inside(4, 8, lam, gamma)
        print("lambda=%d gamma=%d  left child net gain %7.3f (after row %d), right child %7.3f (after row %d)" % (lam, gamma, bl[0], bl[1], br[0], br[1]))
