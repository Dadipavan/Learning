import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
mu=100.0; u=np.linspace(0.05,0.97,200); rate=mu-u*mu
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(u*100,1000/rate,color="#2b4fd6",lw=2,label="mean latency")
ax.plot(u*100,1000*np.log(100)/rate,color="#b84a22",lw=2,label="p99 latency")
ax.axhline(200,color="#aa2d26",ls="--",lw=1.2); ax.text(6,215,"SLO: p99 under 200 ms",color="#aa2d26",fontsize=10)
ax.axvline(70,color="#357a70",ls=":",lw=1.5); ax.text(71,1150,"70% target",color="#357a70",fontsize=10)
ax.set_ylim(0,1500); ax.set_xlabel("Utilisation (% of replica capacity)"); ax.set_ylabel("Latency (ms)")
ax.set_title("One replica, 100 requests/s capacity: latency explodes near full load"); ax.legend(loc="upper left"); ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig("ch07_util_latency.png",dpi=110)
