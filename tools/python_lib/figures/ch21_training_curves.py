import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=400, noise=0.35, random_state=0)
X = (X - X.mean(0)) / X.std(0)
Xtr, ytr, Xva, yva = X[:60], y[:60], X[60:], y[60:]

class MLP:
    def __init__(self, sizes, rng):
        self.W = [rng.normal(scale=np.sqrt(2 / a), size=(a, b)) for a, b in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros(b) for b in sizes[1:]]
    def params(self):
        return self.W + self.b
    def forward(self, x):
        self.acts = [x]
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            x = x @ W + b
            if i < len(self.W) - 1:
                x = np.maximum(x, 0)
            self.acts.append(x)
        return x
    def backward(self, g):
        gW, gb = [None] * len(self.W), [None] * len(self.W)
        for i in reversed(range(len(self.W))):
            gW[i] = self.acts[i].T @ g
            gb[i] = g.sum(0)
            if i > 0:
                g = (g @ self.W[i].T) * (self.acts[i] > 0)
        return gW + gb

class Adam:
    def __init__(self, params, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.p, self.lr, self.b1, self.b2, self.eps, self.t = params, lr, b1, b2, eps, 0
        self.m = [np.zeros_like(q) for q in params]
        self.v = [np.zeros_like(q) for q in params]
    def step(self, grads):
        self.t += 1
        for q, g, m, v in zip(self.p, grads, self.m, self.v):
            m *= self.b1; m += (1 - self.b1) * g
            v *= self.b2; v += (1 - self.b2) * g * g
            q -= self.lr * (m / (1 - self.b1 ** self.t)) / (np.sqrt(v / (1 - self.b2 ** self.t)) + self.eps)

def ce_loss_grad(logits, y):
    z = logits - logits.max(1, keepdims=True)
    p = np.exp(z); p /= p.sum(1, keepdims=True)
    loss = -np.log(p[np.arange(len(y)), y]).mean()
    p[np.arange(len(y)), y] -= 1
    return loss, p / len(y)

rng = np.random.default_rng(0)
model = MLP([2, 64, 2], rng)
opt = Adam(model.params(), lr=0.01)
tr, va = [], []
best_loss, best_epoch, bad = 1e9, -1, 0
for epoch in range(1, 301):
    order = rng.permutation(len(Xtr)); total = 0.0
    for i in range(0, len(order), 16):
        idx = order[i:i + 16]
        loss, g = ce_loss_grad(model.forward(Xtr[idx]), ytr[idx])
        opt.step(model.backward(g)); total += loss * len(idx)
    vl, _ = ce_loss_grad(model.forward(Xva), yva)
    tr.append(total / len(Xtr)); va.append(vl)
    if vl < best_loss - 1e-4:
        best_loss, best_epoch, bad = vl, epoch, 0
    else:
        bad += 1
    if bad >= 30:
        break
plt.rcParams.update({"font.size": 12})
fig, ax = plt.subplots(figsize=(8, 4.2))
ep = np.arange(1, len(tr) + 1)
ax.plot(ep, tr, color="#2b4fd6", lw=2.5, label="training loss")
ax.plot(ep, va, color="#b84a22", lw=2.5, label="validation loss")
ax.axvline(best_epoch, color="#357a70", ls="--", lw=2, label=f"best epoch {best_epoch}")
ax.set_xlabel("epoch"); ax.set_ylabel("cross-entropy loss"); ax.legend(fontsize=11); ax.grid(alpha=0.25)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("lib21_training_curves.png", dpi=110)
