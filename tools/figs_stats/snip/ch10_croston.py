import numpy as np
rng = np.random.default_rng(106)
T = 400; p_occ = 0.25
demand = np.where(rng.random(T) < p_occ, rng.poisson(4, T) + 1, 0)       # mean per period = 0.25 * 5 = 1.25
print("share of zero periods:", round((demand == 0).mean(), 2), " true mean per period: 1.25  sample mean:", round(demand.mean(), 2))
def ses(d, a=0.1):
    f = np.empty(len(d)); l = d[:10].mean()
    for t, x in enumerate(d): f[t] = l; l = l + a * (x - l)
    return f                                                               # f[t] = forecast made before seeing d[t]
def croston(d, a=0.1, sba=False):
    f = np.empty(len(d)); nz = np.flatnonzero(d)
    z = d[nz[0]]; q = nz[0] + 1.0; last = nz[0]
    for t, x in enumerate(d):
        f[t] = (1 - a / 2 if sba else 1) * z / q if t > nz[0] else d[:10].mean()
        if x > 0:
            z = z + a * (x - z); q = q + a * ((t - last) - q); last = t
    return f
s, c, b = ses(demand), croston(demand), croston(demand, sba=True)
sl = slice(100, None)
print(f"{'method':<14}{'mean forecast':>14}{'MAE':>7}{'RMSE':>7}")
for name, f in [("SES a=0.1", s), ("Croston", c), ("Croston SBA", b), ("always zero", np.zeros(T))]:
    e = demand[sl] - f[sl]; print(f"{name:<14}{f[sl].mean():>14.2f}{np.abs(e).mean():>7.2f}{np.sqrt((e**2).mean()):>7.2f}")
print("SD of the forecast over time: SES", round(s[sl].std(), 2), " Croston", round(c[sl].std(), 2))
