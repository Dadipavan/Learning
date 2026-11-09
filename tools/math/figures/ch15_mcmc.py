import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(5)
def target(x): return 0.3*np.exp(-x**2/2)/np.sqrt(2*np.pi) + 0.7*np.exp(-(x-4)**2/(2*0.8**2))/(0.8*np.sqrt(2*np.pi))
x = 0.0; chain = []
for _ in range(20000):
    prop = x + rng.normal(0, 1.5)
    if rng.random() < target(prop)/target(x): x = prop
    chain.append(x)
chain = np.array(chain)
fig, axs = plt.subplots(1, 2, figsize=(9, 4.0))
axs[0].plot(chain[:600], color="#2b4fd6", lw=0.8); axs[0].set_title("Trace of first 600 steps"); axs[0].set_xlabel("step"); axs[0].set_ylabel("x"); axs[0].grid(alpha=0.3)
g = np.linspace(-4, 7, 400)
axs[1].hist(chain[1000:], bins=70, density=True, color="#2b4fd6", alpha=0.5, label="chain after burn-in")
axs[1].plot(g, target(g), color="#b84a22", lw=2, label="true target"); axs[1].legend(); axs[1].set_title("Histogram matches the target"); axs[1].set_xlabel("x"); axs[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch15_mcmc.png", dpi=110)
