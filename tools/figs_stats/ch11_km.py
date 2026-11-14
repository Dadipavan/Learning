import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, Rd, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
rng = np.random.default_rng(17)
n = 600
annual = (rng.random(n) < 0.4).astype(float); tickets = rng.poisson(1.5, n)
rate = 0.05 * np.exp(-0.7 * annual + 0.25 * tickets)
te = rng.exponential(1 / rate); tc = rng.uniform(6, 36, n)
time = np.minimum(te, tc); event = (te <= tc).astype(int)
def km(time, event):
    ts = np.sort(np.unique(time[event == 1])); S = 1.0; v = 0.0; out = [(0, 1.0, 0.0)]
    for u in ts:
        r = (time >= u).sum(); d = ((time == u) & (event == 1)).sum()
        S *= 1 - d / r; v += d / (r * (r - d)) if r > d else 0
        out.append((u, S, S * np.sqrt(v)))
    return np.array(out)
fig, ax = plt.subplots(figsize=(8.5, 4.6))
for g, c, lab in ((0, O, "monthly plan"), (1, B, "annual plan")):
    m = annual == g; k = km(time[m], event[m])
    ax.step(k[:, 0], k[:, 1], where="post", color=c, lw=2.2, label=lab)
    ax.fill_between(k[:, 0], k[:, 1] - 1.96 * k[:, 2], k[:, 1] + 1.96 * k[:, 2], step="post", color=c, alpha=.15)
    cens = m & (event == 0)
    kk = km(time[m], event[m]); idx = np.searchsorted(kk[:, 0], time[cens][::8], side="right") - 1
    ax.plot(time[cens][::8], kk[idx, 1], "|", color=c, ms=8)
ax.axhline(0.5, color="#888888", ls=":", lw=1); ax.text(33, 0.52, "median", fontsize=9, color="#555555")
ax.set_xlim(0, 36); ax.set_ylim(0, 1.02); ax.set_xlabel("months since sign-up"); ax.set_ylabel("share still subscribed, S(t)")
ax.set_title("Kaplan-Meier curves with 95% bands (600 simulated customers)")
ticks = [0, 6, 12, 18, 24, 30]
txt = "at risk   " + "   ".join(f"{t}m: {int(((time >= t) & (annual == 0)).sum())}/{int(((time >= t) & (annual == 1)).sum())}" for t in ticks)
ax.text(0.0, -0.27, txt + "   (monthly/annual)", transform=ax.transAxes, fontsize=8.5)
ax.legend(frameon=False)
plt.tight_layout(); plt.savefig("ch11_km.png", dpi=110)
