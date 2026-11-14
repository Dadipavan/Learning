import numpy as np

def moons(n=100, noise=0.1, seed=0):
    rng = np.random.default_rng(seed)
    t = rng.uniform(0, np.pi, n)
    a = np.c_[np.cos(t), np.sin(t)]; b = np.c_[1-np.cos(t), 0.5-np.sin(t)]
    X = np.vstack([a, b]) + rng.normal(0, noise, (2*n, 2))
    y = np.r_[np.zeros(n), np.ones(n)].astype(int)
    return X, y

class MLP:
    def __init__(s, sizes, seed=0, scale=None):
        r = np.random.default_rng(seed)
        s.W = [r.normal(0, np.sqrt(2/i) if scale is None else scale, (i, o)) for i, o in zip(sizes[:-1], sizes[1:])]
        s.b = [np.zeros(o) for o in sizes[1:]]
    def forward(s, X):
        s.a = [X]
        for k, (W, b) in enumerate(zip(s.W, s.b)):
            z = s.a[-1] @ W + b
            if k < len(s.W) - 1:
                s.a.append(np.maximum(0, z))
            else:
                e = np.exp(z - z.max(1, keepdims=True))
                s.a.append(e / e.sum(1, keepdims=True))
        return s.a[-1]
    def loss(s, X, y):
        P = s.forward(X)
        return -np.log(P[np.arange(len(y)), y]).mean()
    def acc(s, X, y):
        return (s.forward(X).argmax(1) == y).mean()
    def backward(s, y):
        N = len(y); P = s.a[-1].copy(); P[np.arange(N), y] -= 1; d = P / N
        gW = [None]*len(s.W); gb = [None]*len(s.W)
        for k in reversed(range(len(s.W))):
            gW[k] = s.a[k].T @ d; gb[k] = d.sum(0)
            if k > 0:
                d = (d @ s.W[k].T) * (s.a[k] > 0)
        return gW, gb

def gnorm(gW, gb):
    return float(np.sqrt(sum((g**2).sum() for g in gW) + sum((g**2).sum() for g in gb)))
