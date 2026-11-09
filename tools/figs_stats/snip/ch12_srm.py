import numpy as np
from scipy.stats import chisquare
# Overall split looks mildly off; is it the whole experiment, or one segment?
# rows: segment, users in control, users in treatment (planned 50/50)
data = {"desktop": (30210, 30190), "iOS": (14980, 15070), "Android": (9810, 8250)}
tot_c = sum(v[0] for v in data.values()); tot_t = sum(v[1] for v in data.values())
print("overall", tot_c, tot_t, "p =", round(chisquare([tot_c, tot_t]).pvalue, 6))
for k, (c, t) in data.items():
    stat, p = chisquare([c, t])
    print(f"{k:8s} {c:6d} {t:6d} ratio {t/c:.3f} chi2 {stat:7.2f} p {p:.6f}")
