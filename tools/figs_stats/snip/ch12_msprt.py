import numpy as np
rng = np.random.default_rng(11)
# mSPRT for a mean difference with known variance sigma^2 = 1, prior N(0, tau^2) on the effect.
tau2, sigma2, alpha = 0.25, 1.0, 0.05
def mix_lr(n, xbar):
    return np.sqrt(sigma2 / (sigma2 + n * tau2)) * np.exp(n**2 * tau2 * xbar**2 / (2 * sigma2 * (sigma2 + n * tau2)))
N, reps = 3000, 2000
def rejects(true_effect):
    x = rng.normal(true_effect, 1, (reps, N))
    n = np.arange(1, N + 1)
    xbar = np.cumsum(x, axis=1) / n
    lr = mix_lr(n, xbar)
    return (lr >= 1 / alpha).any(axis=1).mean(), (lr >= 1/alpha).argmax(axis=1)[(lr >= 1/alpha).any(axis=1)]
fp, _ = rejects(0.0)
pw, stop = rejects(0.1)
print("effect 0.0, monitored at every user: false positive rate", round(fp, 3))
print("effect 0.1: power by n=3000", round(pw, 3), " median stopping n", int(np.median(stop)) + 1)
