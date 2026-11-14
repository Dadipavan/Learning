import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np, math
C,M=3.0,360.0
T=np.linspace(5,400,300); w=C/T+T/(2*M)
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(T,w*100,color="#2b4fd6",lw=2,label="formula: C/T + T/(2M)")
st=[10,20,46,90,180,360]; sim=[25.5,17.0,13.5,16.4,25.7,43.7]
ax.plot(st,sim,"o",color="#b84a22",ms=7,label="simulation")
opt=math.sqrt(2*C*M); ax.axvline(opt,color="#357a70",ls=":",lw=1.6); ax.text(opt+6,45,f"Young-Daly: {opt:.0f} min",color="#357a70",fontsize=10)
ax.set_ylim(0,55); ax.set_xlabel("Checkpoint interval (minutes)"); ax.set_ylabel("Time wasted (%)")
ax.set_title("Checkpoint too often or too rarely: both waste time (C = 3 min, MTBF = 6 h)"); ax.legend(loc="upper center"); ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig("ch06_young_daly.png",dpi=110)
