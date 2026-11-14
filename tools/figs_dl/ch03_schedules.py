import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
peak, floor, total, warm = 1e-3, 1e-4, 100, 10
t = np.arange(total)
def cos(t):
    if t < warm: return peak*(t+1)/warm
    pr=(t-warm)/(total-warm); return floor+0.5*(peak-floor)*(1+np.cos(np.pi*pr))
def lin(t):
    if t < warm: return peak*(t+1)/warm
    pr=(t-warm)/(total-warm); return peak+(floor-peak)*pr
def stp(t): return peak*(0.1**(t//40))
fig, ax = plt.subplots(figsize=(8,4.2))
ax.plot(t,[cos(i) for i in t],color="#2b4fd6",lw=2.5,label="warmup + cosine")
ax.plot(t,[lin(i) for i in t],color="#b84a22",lw=2.5,ls="--",label="warmup + linear")
ax.plot(t,[stp(i) for i in t],color="#357a70",lw=2.5,ls=":",label="step decay (x0.1 every 40)")
ax.set_xlabel("training step",fontsize=12); ax.set_ylabel("learning rate",fontsize=12)
ax.set_title("Three learning-rate schedules, peak 1e-3, floor 1e-4",fontsize=13)
ax.tick_params(labelsize=11); ax.grid(alpha=.3); ax.legend(fontsize=11)
fig.tight_layout(); fig.savefig("schedule_shapes.png",dpi=110)
