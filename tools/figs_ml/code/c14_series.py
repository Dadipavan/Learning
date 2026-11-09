import numpy as np
rng = np.random.default_rng(3)
days = 140; dow = np.arange(days) % 7
season = np.array([100, 104, 108, 110, 112, 80, 70.0])          # weekly pattern of a daily metric
y = season[dow] + rng.normal(0, 2.0, days)
y[60] += 25                                                      # one-day spike
y[100:] += 9                                                     # level shift from day 100
# 1) remove seasonality with the median of each weekday over the first 56 days (all normal)
profile = np.array([np.median(y[:56][dow[:56] == d]) for d in range(7)])
resid = y - profile[dow]
mad = np.median(np.abs(resid[:56] - np.median(resid[:56])))
sigma = 1.4826 * mad
print("robust sigma of residual: %.2f" % sigma)
z = resid / sigma
flag = np.where(np.abs(z) > 4)[0]
print("days flagged before the shift (|robust z| > 4 on the residual):", flag[flag < 100], "z of day 60: %.1f, z of day 9: %.1f" % (z[60], z[9]))
raw = (y - y.mean()) / y.std()
print("plain z of the raw series on day 60: %.2f, largest plain |z| on any day before 100: %.2f" % (raw[60], np.abs(raw[:100]).max()))
# 2) CUSUM on the residual (clipped at 3 sigma so one spike cannot trigger it): detects the level shift
k, h = 0.5 * sigma, 5 * sigma
r = np.clip(resid, -3 * sigma, 3 * sigma)
s = 0.0; alarm = None
for t in range(56, days):
    s = max(0.0, s + r[t] - k)
    if s > h and alarm is None: alarm = t
print("CUSUM alarm at day", alarm, "(true shift starts at day 100)")
