import numpy as np
rng = np.random.default_rng(3)
n = 50000
talent = rng.normal(0, 1, n)
looks = rng.normal(0, 1, n)                      # independent of talent by construction
famous = (talent + looks + rng.normal(0, 0.5, n)) > 1.5   # collider: caused by both
print("corr(talent, looks), everyone      :", round(np.corrcoef(talent, looks)[0, 1], 3))
print("corr(talent, looks), famous only   :", round(np.corrcoef(talent[famous], looks[famous])[0, 1], 3))
print("share famous                       :", round(famous.mean(), 3))
