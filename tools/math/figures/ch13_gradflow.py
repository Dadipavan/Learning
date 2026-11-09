import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

def delta_norms(act, std, L=20, n=100, N=64, seed=0):
    rng = np.random.default_rng(seed)
    Ws = [rng.normal(0, std, (n, n)) for _ in range(L)]
    a = rng.normal(size=(N, n)); As = [a]; Zs = []
    for W in Ws:
        z = a @ W.T; Zs.append(z)
        a = 1/(1+np.exp(-z)) if act == "sigmoid" else np.maximum(z, 0) if act == "relu" else np.tanh(z)
        As.append(a)
    d = np.ones((N, n)); out = []
    for i in reversed(range(L)):
        if act == "sigmoid": d = d * As[i+1] * (1 - As[i+1])
        elif act == "relu": d = d * (Zs[i] > 0)
        else: d = d * (1 - As[i+1]**2)
        out.append(np.linalg.norm(d)); d = d @ Ws[i]
    return out[::-1]

n = 100
cases = [("sigmoid, Xavier", "sigmoid", np.sqrt(1/n), BLUE), ("ReLU, std 0.05 (too small)", "relu", 0.05, ORANGE),
         ("ReLU, std 0.3 (too big)", "relu", 0.3, RED), ("ReLU, He init", "relu", np.sqrt(2/n), TEAL),
         ("tanh, Xavier", "tanh", np.sqrt(1/n), PURPLE)]
fig, ax = plt.subplots(figsize=(8, 4.4))
for name, act, std, col in cases:
    ax.plot(range(1, 21), delta_norms(act, std), marker="o", ms=4, lw=2, color=col, label=name)
ax.set_xticks(range(1, 21, 2)); ax.set_yscale("log"); ax.set_xlabel("layer (1 = closest to the input, 20 = closest to the loss)")
ax.set_ylabel("norm of the backpropagated delta")
ax.set_title("Gradient signal at each layer of a 20-layer network"); ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch13_gradflow.png", dpi=110)
