import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BL, OR, TE, RD, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

import numpy as np

def make_moons(n, noise, rng):
    t = rng.uniform(0, np.pi, n // 2)
    upper = np.column_stack([np.cos(t), np.sin(t)])
    lower = np.column_stack([1 - np.cos(t), 0.5 - np.sin(t)])
    X = np.vstack([upper, lower]) + noise * rng.normal(size=(n, 2))
    return X, np.r_[np.zeros(n // 2), np.ones(n // 2)]

rng = np.random.default_rng(3)
X, y = make_moons(600, 0.25, rng)
idx = rng.permutation(600)
tr, te = idx[:400], idx[400:]
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Xtr, ytr, Xte, yte = (X[tr] - mu) / sd, y[tr], (X[te] - mu) / sd, y[te]
def init(sizes, rng):
    """Weights ~ N(0, 1/fan_in) (Xavier-style for tanh), biases 0."""
    return [[rng.normal(size=(a, b)) / np.sqrt(a), np.zeros(b)] for a, b in zip(sizes[:-1], sizes[1:])]

def forward(params, X):
    acts = [X]
    for W, b in params[:-1]:
        acts.append(np.tanh(acts[-1] @ W + b))           # hidden layers
    W, b = params[-1]
    logits = acts[-1] @ W + b                            # output layer: logit
    return acts, logits[:, 0]

def loss_and_grads(params, X, y):
    acts, z = forward(params, X)
    m = len(y)
    loss = np.mean(np.logaddexp(0, z) - y * z)           # stable binary cross-entropy
    dz = ((1 / (1 + np.exp(-z))) - y)[:, None] / m       # dLoss/dlogit = (p - y)/m
    grads = [None] * len(params)
    for i in range(len(params) - 1, -1, -1):
        W, b = params[i]
        grads[i] = [acts[i].T @ dz, dz.sum(axis=0)]      # dW, db
        if i > 0:
            dz = (dz @ W.T) * (1 - acts[i] ** 2)         # back through tanh: 1 - tanh^2
    return loss, grads
def train(opt, lr, epochs=150, batch=32, seed=1):
    rng = np.random.default_rng(seed)
    params = init([2, 16, 16, 1], rng)
    vel = [[np.zeros_like(a) for a in layer] for layer in params]     # momentum / Adam m
    sq = [[np.zeros_like(a) for a in layer] for layer in params]      # Adam v
    t, history = 0, []
    for epoch in range(1, epochs + 1):
        perm = rng.permutation(len(Xtr))
        for s in range(0, len(Xtr), batch):
            b = perm[s:s + batch]
            _, grads = loss_and_grads(params, Xtr[b], ytr[b])
            t += 1
            for i, layer in enumerate(params):
                for j, a in enumerate(layer):
                    g = grads[i][j]
                    if opt == "momentum":
                        vel[i][j] = 0.9 * vel[i][j] + g
                        a -= lr * vel[i][j]
                    else:  # adam
                        vel[i][j] = 0.9 * vel[i][j] + 0.1 * g
                        sq[i][j] = 0.999 * sq[i][j] + 0.001 * g**2
                        mh, vh = vel[i][j] / (1 - 0.9**t), sq[i][j] / (1 - 0.999**t)
                        a -= lr * mh / (np.sqrt(vh) + 1e-8)
        if epoch in (1, 10, 50, 150):
            history.append((epoch, loss_and_grads(params, Xtr, ytr)[0]))

    return params, history

params, _ = train("adam", 0.01, epochs=150)
# also record the loss curve per epoch for SGD with momentum and Adam
def curve(opt, lr, epochs=100):
    rng = np.random.default_rng(1); p = init([2, 16, 16, 1], rng)
    v = [[np.zeros_like(a) for a in l] for l in p]; q = [[np.zeros_like(a) for a in l] for l in p]; t = 0; out = []
    for e in range(epochs):
        perm = rng.permutation(len(Xtr))
        for s in range(0, len(Xtr), 32):
            b = perm[s:s+32]; _, g = loss_and_grads(p, Xtr[b], ytr[b]); t += 1
            for i, l in enumerate(p):
                for j, a in enumerate(l):
                    if opt == "m":
                        v[i][j] = 0.9 * v[i][j] + g[i][j]; a -= lr * v[i][j]
                    else:
                        v[i][j] = 0.9 * v[i][j] + 0.1 * g[i][j]; q[i][j] = 0.999 * q[i][j] + 0.001 * g[i][j]**2
                        a -= lr * (v[i][j] / (1 - 0.9**t)) / (np.sqrt(q[i][j] / (1 - 0.999**t)) + 1e-8)
        out.append(loss_and_grads(p, Xtr, ytr)[0])
    return out

fig, ax = plt.subplots(1, 2, figsize=(9.5, 4.2))
gx, gy = np.meshgrid(np.linspace(-2.6, 2.6, 250), np.linspace(-2.6, 2.6, 250))
prob = 1 / (1 + np.exp(-forward(params, np.column_stack([gx.ravel(), gy.ravel()]))[1])).reshape(gx.shape)
ax[0].contourf(gx, gy, prob, levels=[0, 0.5, 1], colors=["#d9e0f8", "#f3d9cc"])
ax[0].contour(gx, gy, prob, levels=[0.5], colors="k", linewidths=1.5)
ax[0].scatter(*Xtr[ytr == 0].T, c=BL, s=14, label="class 0 (train)")
ax[0].scatter(*Xtr[ytr == 1].T, c=OR, s=14, label="class 1 (train)")
ax[0].scatter(*Xte[yte == 0].T, c=BL, s=30, marker="x"); ax[0].scatter(*Xte[yte == 1].T, c=OR, s=30, marker="x")
ax[0].set_title("Decision boundary (Adam, 2x16 tanh); x = test"); ax[0].legend(fontsize=8, loc="lower left")
ax[1].plot(curve("m", 0.05), color=BL, label="SGD + momentum 0.05")
ax[1].plot(curve("a", 0.01), color=OR, label="Adam 0.01")
ax[1].set_xlabel("epoch"); ax[1].set_ylabel("training loss"); ax[1].set_title("Training loss"); ax[1].legend()
plt.tight_layout(); plt.savefig("ch17_nn.png", dpi=110)
