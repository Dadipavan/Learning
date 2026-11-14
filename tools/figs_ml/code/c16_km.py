import numpy as np
# Kaplan-Meier by hand: times, event=1 observed, 0 censored
t = np.array([2, 3, 3, 5, 6, 8, 8, 9, 12, 12]); e = np.array([1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
S = 1.0; print("time at_risk deaths  S(t)")
for u in np.unique(t[e == 1]):
    n = (t >= u).sum(); d = ((t == u) & (e == 1)).sum(); S *= 1 - d / n; print(f"{u:4d} {n:7d} {d:6d}  {S:.4f}")
# naive: drop censored vs treating censored as events
print("naive share of ALL 10 rows with an event by t=8:", ((t <= 8) & (e == 1)).sum() / len(t))
print("KM estimate of P(event by t=8):", round(1 - 0.4114, 4))
