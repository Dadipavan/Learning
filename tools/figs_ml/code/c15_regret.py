import numpy as np
p = np.array([0.20, 0.25, 0.30]); T = 2000
def run(policy, seed):
    rng = np.random.default_rng(seed)
    a_ = np.ones(3); b_ = np.ones(3); n = np.zeros(3); w = np.zeros(3); regret = 0.0
    for t in range(T):
        if policy == "uniform":
            arm = rng.integers(3)
        elif policy == "eps-greedy":
            arm = rng.integers(3) if (rng.random() < 0.1 or n.min() == 0) else int(np.argmax(w / n))
        elif policy == "UCB":
            arm = int(np.argmin(n)) if n.min() == 0 else int(np.argmax(w / n + np.sqrt(2 * np.log(t + 1) / n)))
        else:
            arm = int(np.argmax(rng.beta(a_, b_)))
        x = rng.random() < p[arm]
        n[arm] += 1; w[arm] += x; a_[arm] += x; b_[arm] += 1 - x
        regret += p.max() - p[arm]
    return regret
for pol in ["uniform", "eps-greedy", "UCB", "Thompson"]:
    r = [run(pol, s) for s in range(200)]
    print("%-10s mean regret after %d rounds: %6.1f (std %.1f)" % (pol, T, np.mean(r), np.std(r)))
