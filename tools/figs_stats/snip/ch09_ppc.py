import numpy as np
rng = np.random.default_rng(91)
# Observed: 120 days of support tickets. Truth is overdispersed (negative binomial), analyst assumes Poisson.
y = rng.negative_binomial(n=2, p=2/(2+5), size=120)          # mean 5, variance 17.5
print("observed: mean", round(y.mean(), 2), " variance", round(y.var(ddof=1), 2), " zeros", (y == 0).sum(), " max", y.max())
# Conjugate Poisson-Gamma: prior Gamma(2, 0.2) (mean 10), posterior Gamma(2 + sum y, 0.2 + n)
a, b = 2 + y.sum(), 0.2 + len(y)
lam = rng.gamma(a, 1 / b, 4000)
print(f"posterior mean rate {a/b:.2f}, 95% interval ({np.percentile(lam, 2.5):.2f}, {np.percentile(lam, 97.5):.2f})")
# Posterior predictive check: simulate a replicated dataset for each draw, compare statistics
rep = rng.poisson(lam[:, None], (4000, len(y)))
for name, f, obs in [("variance", lambda r: r.var(axis=1, ddof=1), y.var(ddof=1)),
                     ("max", lambda r: r.max(axis=1), y.max()),
                     ("zeros", lambda r: (r == 0).sum(axis=1), (y == 0).sum())]:
    t = f(rep)
    print(f"{name:>8}: observed {obs:6.2f}   replicated 95% range ({np.percentile(t, 2.5):.1f}, {np.percentile(t, 97.5):.1f})   P(T_rep >= T_obs) = {(t >= obs).mean():.3f}")
# Prior predictive check of a careless prior: log(rate) ~ Normal(0, 10^2)
lr = rng.normal(0, 10, 100000)
cnt = rng.poisson(np.exp(np.clip(lr, -30, 30)))
print("careless prior, share of prior predictive counts above 1,000,000:", round((cnt > 1e6).mean(), 3),
      "  share equal to 0:", round((cnt == 0).mean(), 3))
