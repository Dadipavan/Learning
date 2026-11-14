import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
BLUE, ORANGE, TEAL, RED = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"

def softmax(Z):
    E = np.exp(Z - Z.max(axis=1, keepdims=True))   # subtract max for stability
    return E / E.sum(axis=1, keepdims=True)

class MLP:
    def __init__(self, sizes, act="relu", seed=0):
        rng = np.random.default_rng(seed)
        self.act = act
        self.W, self.b = [], []
        for n_in, n_out in zip(sizes[:-1], sizes[1:]):
            gain = 2.0 if act == "relu" else 1.0          # He for relu, Xavier-like for tanh
            self.W.append(rng.normal(0, np.sqrt(gain / n_in), (n_out, n_in)))
            self.b.append(np.zeros(n_out))

    def f(self, Z):
        return np.maximum(Z, 0) if self.act == "relu" else np.tanh(Z)

    def df(self, Z, A):
        return (Z > 0).astype(float) if self.act == "relu" else 1 - A**2

    def forward(self, X):
        self.As, self.Zs = [X], []
        A = X
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            Z = A @ W.T + b                      # (N, n_out)
            self.Zs.append(Z)
            A = self.f(Z) if i < len(self.W) - 1 else Z
            self.As.append(A)
        return softmax(self.As[-1])              # class probabilities

    def loss(self, P, y):
        return -np.log(P[np.arange(len(y)), y]).mean()

    def backward(self, P, y):
        N = len(y)
        dZ = P.copy()
        dZ[np.arange(N), y] -= 1                 # p - y (one-hot)
        dZ /= N                                  # mean over the batch
        gW, gb = [None] * len(self.W), [None] * len(self.W)
        for i in reversed(range(len(self.W))):
            gW[i] = dZ.T @ self.As[i]            # (n_out, n_in)
            gb[i] = dZ.sum(axis=0)
            if i > 0:
                dA = dZ @ self.W[i]              # (N, n_in)
                dZ = dA * self.df(self.Zs[i-1], self.As[i])
        return gW, gb

    def train(self, X, y, lr=0.5, epochs=1000, every=250):
        hist = []
        for ep in range(epochs + 1):
            P = self.forward(X)
            L = self.loss(P, y)
            hist.append(L)
            if every and ep % every == 0:
                acc = (P.argmax(axis=1) == y).mean()
                print(f"epoch {ep:5d}  loss {L:.4f}  acc {acc:.3f}")
            gW, gb = self.backward(P, y)
            for i in range(len(self.W)):
                self.W[i] -= lr * gW[i]
                self.b[i] -= lr * gb[i]
        return hist

def spiral(n=100, k=3, seed=0):
    rng = np.random.default_rng(seed)
    X = np.zeros((n * k, 2)); y = np.zeros(n * k, dtype=int)
    for j in range(k):
        r = np.linspace(0.05, 1, n)
        t = np.linspace(j * 4, (j + 1) * 4, n) + rng.normal(0, 0.2, n)
        X[j*n:(j+1)*n] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[j*n:(j+1)*n] = j
    return X, y

X, y = spiral(seed=0)
m = MLP([2, 64, 3], act="relu", seed=0)
hist = m.train(X, y, lr=1.0, epochs=1500, every=0)
gx, gy = np.meshgrid(np.linspace(-1.3, 1.3, 300), np.linspace(-1.3, 1.3, 300))
G = np.c_[gx.ravel(), gy.ravel()]
pred = m.forward(G).argmax(axis=1).reshape(gx.shape)
cols = [BLUE, ORANGE, TEAL]
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].contourf(gx, gy, pred, levels=[-0.5, 0.5, 1.5, 2.5], colors=cols, alpha=0.25)
for c in range(3):
    ax[0].scatter(X[y == c, 0], X[y == c, 1], s=14, color=cols[c], edgecolor="k", lw=0.3, label=f"class {c}")
ax[0].set_title("Decision boundary of a 2-64-3 ReLU net"); ax[0].set_xlabel("x1"); ax[0].set_ylabel("x2"); ax[0].legend(fontsize=8)
ax[1].plot(hist, color=RED, lw=2)
ax[1].set_yscale("log"); ax[1].set_xlabel("epoch"); ax[1].set_ylabel("cross-entropy loss (log scale)")
ax[1].set_title("Training loss"); ax[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch13_spiral.png", dpi=110)
