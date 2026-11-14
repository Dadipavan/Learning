import numpy as np
rng = np.random.default_rng(5)
users, m = 20, 50                                  # 20 users, 50 page loads each
icc_true = 0.3
sd_between, sd_within = np.sqrt(0.3), np.sqrt(0.7) # total variance 1
ybar_runs = []
for _ in range(2000):                              # how variable is the overall mean, really?
    u = rng.normal(0, sd_between, users)
    y = u[:, None] + rng.normal(0, sd_within, (users, m))
    ybar_runs.append(y.mean())
true_se = np.std(ybar_runs)
u = rng.normal(0, sd_between, users); y = u[:, None] + rng.normal(0, sd_within, (users, m))
naive_se = y.std(ddof=1) / np.sqrt(users * m)      # pretends 1000 independent rows
cluster_se = y.mean(axis=1).std(ddof=1) / np.sqrt(users)   # treats each user as one unit
deff = 1 + (m - 1) * icc_true
print("true SD of the overall mean (2000 repeats):", round(true_se, 4))
print("naive SE (1000 rows independent)          :", round(naive_se, 4))
print("cluster SE (20 user means)                :", round(cluster_se, 4))
print("design effect 1+(m-1)ICC                  :", round(deff, 2))
print("effective sample size 1000/deff           :", round(users * m / deff, 1))
print("naive SE x sqrt(deff)                     :", round(naive_se * np.sqrt(deff), 4))
