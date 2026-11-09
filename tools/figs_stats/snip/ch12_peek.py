import numpy as np
from scipy.optimize import brentq
rng = np.random.default_rng(7)
K, reps = 5, 200000
# A/A test: standardized z statistic at K equally spaced looks.
# Partial sums of N(0,1) blocks: z_k = S_k / sqrt(k)
S = np.cumsum(rng.standard_normal((reps, K)), axis=1)
z = S / np.sqrt(np.arange(1, K + 1))
naive = (np.abs(z) > 1.96).any(axis=1).mean()
pocock_c = brentq(lambda c: (np.abs(z) > c).any(axis=1).mean() - 0.05, 2.0, 3.0)
obf_c = brentq(lambda c: (np.abs(z) > c * np.sqrt(K / np.arange(1, K + 1))).any(axis=1).mean() - 0.05, 1.5, 3.0)
print("peek 5 times at z>1.96  : false positive rate", round(naive, 3))
print("Pocock constant boundary:", round(pocock_c, 3))
print("O'Brien-Fleming c       :", round(obf_c, 3))
print("OBF boundaries per look :", np.round(obf_c * np.sqrt(K / np.arange(1, K + 1)), 2))
print("false positive, Pocock  :", round((np.abs(z) > pocock_c).any(axis=1).mean(), 3))
print("false positive, OBF     :", round((np.abs(z) > obf_c*np.sqrt(K/np.arange(1,K+1))).any(axis=1).mean(), 3))
