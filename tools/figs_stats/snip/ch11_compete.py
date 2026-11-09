import numpy as np
rng = np.random.default_rng(14)
n = 20000
lam1, lam2 = 0.05, 0.05                             # cancel (cause 1) and payment failure (cause 2), per month
t1 = rng.exponential(1 / lam1, n); t2 = rng.exponential(1 / lam2, n)
time = np.minimum(t1, t2); cause = np.where(t1 <= t2, 1, 2)
horizon = 24
true_cif = lam1 / (lam1 + lam2) * (1 - np.exp(-(lam1 + lam2) * horizon))
# naive: treat payment failures as censored and use 1 - Kaplan-Meier
ts = np.sort(np.unique(time[(cause == 1) & (time <= horizon)]))
S = 1.0
for u in ts:
    at_risk = (time >= u).sum(); d = ((time == u) & (cause == 1)).sum()
    S *= 1 - d / at_risk
naive = 1 - S
# correct: Aalen-Johansen cumulative incidence = sum of S_overall(t-) * d1 / n_at_risk
S_all, cif = 1.0, 0.0
for u in np.sort(np.unique(time[time <= horizon])):
    at_risk = (time >= u).sum()
    d1 = ((time == u) & (cause == 1)).sum(); d_all = (time == u).sum()
    cif += S_all * d1 / at_risk
    S_all *= 1 - d_all / at_risk
print("true cumulative incidence of cancel by month 24:", round(true_cif, 4))
print("naive 1 - KM (other cause censored)           :", round(naive, 4))
print("Aalen-Johansen estimate                        :", round(cif, 4))
print("share of customers still active at month 24    :", round((time > horizon).mean(), 4))
