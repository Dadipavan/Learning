import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

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
fig, ax = plt.subplots(figsize=(8, 4.2))
for lr, col in [(0.01, BLUE), (0.1, TEAL), (1.0, ORANGE), (10.0, PURPLE)]:
    m = MLP([2, 64, 3], act="relu", seed=0)
    h = m.train(X, y, lr=lr, epochs=600, every=0)
    ax.plot(h, color=col, lw=2, label=f"learning rate {lr}")
ax.set_yscale("log"); ax.set_xlabel("epoch"); ax.set_ylabel("loss (log scale)")
ax.set_title("Same network, four learning rates"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch13_lr.png", dpi=110)
