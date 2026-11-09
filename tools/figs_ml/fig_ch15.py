import sys, os
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
plt.rcParams.update({"font.size": 11})
BLUE, ORANGE, TEAL, RED = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"

# Figure 1: regret curves
p = np.array([0.20, 0.25, 0.30]); T = 2000; R = 200
def run(policy, seed):
    rng = np.random.default_rng(seed); a_ = np.ones(3); b_ = np.ones(3)   # Beta counts (also used for means)
    n = np.zeros(3); w = np.zeros(3); reg = np.zeros(T)
    for t in range(T):
        if policy == "eps":
            arm = rng.integers(3) if (rng.random() < 0.1 or n.min() == 0) else int(np.argmax(w / np.maximum(n, 1)))
        elif policy == "ucb":
            arm = int(np.argmin(n)) if n.min() == 0 else int(np.argmax(w / n + np.sqrt(2 * np.log(t + 1) / n)))
        elif policy == "ts":
            arm = int(np.argmax(rng.beta(a_, b_)))
        else:
            arm = int(np.argmax(rng.random(3))) if False else rng.integers(3)
        x = rng.random() < p[arm]
        n[arm] += 1; w[arm] += x; a_[arm] += x; b_[arm] += 1 - x
        reg[t] = p.max() - p[arm]
    return np.cumsum(reg)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for pol, lab, c, ls in [("rand", "uniform (A/B style)", "#777777", ":"), ("eps", "epsilon-greedy (0.1)", ORANGE, "--"), ("ucb", "UCB", BLUE, "-"), ("ts", "Thompson", TEAL, "-")]:
    ax.plot(np.mean([run(pol, s) for s in range(R)], axis=0), color=c, ls=ls, lw=2, label=lab)
ax.set_xlabel("round"); ax.set_ylabel("cumulative expected regret"); ax.set_title("Regret, arms 0.20 / 0.25 / 0.30, mean of 200 runs")
ax.grid(alpha=.3); ax.legend(frameon=False); fig.tight_layout(); fig.savefig("ch15_regret.png"); plt.close(fig)

# Figure 2: REINFORCE with and without baseline
import importlib.util
spec = importlib.util.spec_from_file_location("c15r", os.path.join(os.path.dirname(os.path.abspath(__file__)), "code", "c15_reinforce.py"))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "code", "c15_reinforce.py")).read().split("for base in")[0]
ns = {}; exec(src, ns)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for base, c, lab in [(False, ORANGE, "no baseline"), (True, TEAL, "with baseline")]:
    curves = np.array([ns["reinforce"](s, episodes=1500, baseline=base)[1] for s in range(10)])
    sm = np.array([np.convolve(c_, np.ones(50) / 50, mode="valid") for c_ in curves])
    for row in sm: ax.plot(row, color=c, alpha=.25, lw=1)
    ax.plot(sm.mean(axis=0), color=c, lw=2.5, label=lab + " (thick = mean of 10 seeds)")
ax.set_ylim(-62, 8); ax.set_xlabel("episode"); ax.set_ylabel("return per episode (50-episode average)")
ax.set_title("REINFORCE on the 4 by 4 grid"); ax.grid(alpha=.3); ax.legend(frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig("ch15_reinforce.png"); plt.close(fig)
