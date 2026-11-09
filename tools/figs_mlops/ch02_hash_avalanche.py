import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, hashlib, json, numpy as np
def bits(cfg):
    return int(hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest(), 16)
base = {"model": "rf", "n_estimators": 20, "max_depth": 4, "seed": 1, "data": "v3"}
b0 = bits(base)
diffs = []
for i in range(1000):
    c = dict(base); c["seed"] = 1000 + i          # a tiny change each time
    diffs.append(bin(b0 ^ bits(c)).count("1"))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.hist(diffs, bins=range(90, 170, 3), color="#357a70", alpha=.9)
ax.axvline(128, color="#aa2d26", lw=2, label="128 = half of 256 bits")
ax.set_xlabel("number of the 256 hash bits that flip"); ax.set_ylabel("count (of 1000 configs)")
ax.set_title("Change one setting a tiny bit: about half of the hash bits flip")
ax.legend(); ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig("ch02d_hash_avalanche.png", dpi=110)
print("mean flipped:", np.mean(diffs), "min", min(diffs), "max", max(diffs))
