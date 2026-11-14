import numpy as np
def metropolis(logp, start, step, N, seed):
    r = np.random.default_rng(seed); x = start; lp = logp(x); out = np.empty(N); acc = 0
    for i in range(N):
        p = x + step * r.normal(); lq = logp(p)
        if np.log(r.uniform()) < lq - lp: x, lp = p, lq; acc += 1
        out[i] = x
    return out, acc / N
def split_rhat(ch):                       # ch: (chains, draws); split each chain in two
    m, n = ch.shape; h = n // 2
    s = np.vstack([ch[:, :h], ch[:, h:2*h]])
    W = s.var(axis=1, ddof=1).mean(); B = h * s.mean(axis=1).var(ddof=1)
    return np.sqrt(((h - 1) / h * W + B / h) / W)
def ess(ch):                              # between-chain-aware ESS (Vehtari et al. style, simple truncation)
    m, n = ch.shape; x = ch - ch.mean(axis=1, keepdims=True)
    W = ch.var(axis=1, ddof=1).mean(); B = n * ch.mean(axis=1).var(ddof=1)
    var_plus = (n - 1) / n * W + B / n
    acov = lambda l: np.mean([np.dot(c[:n-l], c[l:]) / n for c in x])
    rho = [1 - (W - acov(l)) / var_plus for l in range(300)]
    tau = 1.0
    for l in range(1, 299, 2):
        pair = rho[l] + rho[l + 1]
        if pair < 0: break
        tau += 2 * pair
    return m * n / tau
mix = lambda x: np.logaddexp(-0.5 * (x - 4) ** 2, -0.5 * (x + 4) ** 2)     # two bumps at -4 and +4
starts = [-4.0, -4.0, 4.0, 4.0]
res = {}
for name, step in [("step 0.5 (stuck)", 0.5), ("step 6.0 (mixes)", 6.0)]:
    chains, accs = zip(*[metropolis(mix, s, step, 4000, i) for i, s in enumerate(starts)])
    res[name] = np.array(chains)
    print(f"{name:>18}: acceptance {np.mean(accs):.2f}, split R-hat {split_rhat(res[name]):.2f}, ESS {ess(res[name]):.0f} of {res[name].size}, share of draws above 0: {(res[name] > 0).mean():.2f}")
print("truth: the target is symmetric, so the share above 0 should be 0.50 and the mean 0")
