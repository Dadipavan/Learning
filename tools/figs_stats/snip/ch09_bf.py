import numpy as np
from scipy.special import betaln
from scipy.stats import binomtest
def log_bf10(k, n, a=1.0, b=1.0):
    # H0: theta = 0.5.  H1: theta ~ Beta(a, b).  Binomial coefficient cancels.
    log_m1 = betaln(k + a, n - k + b) - betaln(a, b)
    log_m0 = n * np.log(0.5)
    return log_m1 - log_m0
print("data           p-value   BF10 (Beta(1,1))  BF10 (Beta(10,10))  P(H1|data) at 50/50 prior odds")
for k, n in [(62, 100), (55, 100), (530, 1000), (5100, 10000), (5250, 10000)]:
    p = binomtest(k, n, 0.5).pvalue
    b1, b2 = np.exp(log_bf10(k, n)), np.exp(log_bf10(k, n, 10, 10))
    print(f"{k:>5}/{n:<6}  {p:8.1e}   {b1:15.3f}   {b2:17.3f}   {b1/(1+b1):12.3f}")
