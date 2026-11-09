import numpy as np
rng = np.random.default_rng(103)
phi, sigma, mu = 0.8, 2.0, 50.0
hs = [1, 2, 5, 10, 20]
print("Forecast error SD at horizon h")
print(" h   AR(1) formula   simulated   random-walk formula")
reps = 200000
x0 = mu                                                 # last observation sits at the mean
e = rng.normal(0, sigma, (reps, max(hs)))
paths = np.zeros((reps, max(hs))); prev = np.full(reps, x0)
for j in range(max(hs)):
    prev = mu + phi * (prev - mu) + e[:, j]; paths[:, j] = prev
for h in hs:
    f = sigma * np.sqrt(sum(phi ** (2 * j) for j in range(h)))
    print(f"{h:>2}   {f:>12.3f}   {paths[:, h-1].std():>9.3f}   {sigma*np.sqrt(h):>14.3f}")
print("long-run SD of a stationary AR(1):", round(sigma / np.sqrt(1 - phi ** 2), 3))
print("95% interval for h=10 from AR(1): 50 +/-", round(1.96 * sigma * np.sqrt(sum(phi ** (2 * j) for j in range(10))), 2),
      "  vs random walk: +/-", round(1.96 * sigma * np.sqrt(10), 2))
