import numpy as np
rng = np.random.default_rng(9)
n = 20000
lifetime = rng.exponential(10, n)                   # everyone: same hazard 0.1 per month, NO effect of upgrading
upgrade_at = rng.uniform(0, 24, n)                  # the month each customer WOULD upgrade if still around
upgraded = lifetime > upgrade_at                    # you can only upgrade while you are still subscribed
print("share who ever upgraded          :", round(upgraded.mean(), 3))
print("mean tenure, 'ever upgraded'      :", round(lifetime[upgraded].mean(), 2))
print("mean tenure, 'never upgraded'     :", round(lifetime[~upgraded].mean(), 2))
# correct: measure tenure AFTER the upgrade date (time at risk after joining the upgrade group)
after = (lifetime - upgrade_at)[upgraded]
print("mean time after upgrade point     :", round(after.mean(), 2), "(true mean 10)")
