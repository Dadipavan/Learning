import numpy as np
rng = np.random.default_rng(5)
n = 4000                                     # users in one arm
sessions = rng.poisson(3, n) + 1             # x_i: sessions per user
taste = rng.normal(0, 1, n)                  # users differ, so one user's sessions are alike
per_session = [rng.normal(2 + 0.8 * u, 1.5, s).clip(0) for s, u in zip(sessions, taste)]
revenue = np.array([p.sum() for p in per_session])
R = revenue.sum() / sessions.sum()           # revenue per session
# delta method: Var(R) ~ (var_y + R^2 var_x - 2 R cov_xy) / (n * mean_x^2)
mx = sessions.mean()
vy, vx = revenue.var(ddof=1), sessions.var(ddof=1)
cxy = np.cov(revenue, sessions)[0, 1]
se_delta = np.sqrt((vy + R**2 * vx - 2 * R * cxy) / (n * mx**2))
# bootstrap users: resample users, keep each user's (revenue, sessions) pair together
boots = []
for _ in range(2000):
    i = rng.integers(0, n, n)
    boots.append(revenue[i].sum() / sessions[i].sum())
se_boot = np.std(boots, ddof=1)
# WRONG: treat every session as an independent row
all_sessions = np.concatenate(per_session)
se_wrong = all_sessions.std(ddof=1) / np.sqrt(len(all_sessions))
print("revenue per session   :", round(R, 4))
print("SE delta method       :", round(se_delta, 4))
print("SE bootstrap (users)  :", round(se_boot, 4))
print("SE wrong (sessions iid):", round(se_wrong, 4))
