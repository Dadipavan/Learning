import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
T=1000
beta=np.linspace(1e-4,0.02,T); lin=np.cumprod(1-beta)
s=0.008; tt=np.arange(T+1)/T; f=np.cos((tt+s)/(1+s)*np.pi/2)**2; cos=(f/f[0])[1:]
t=np.arange(1,T+1)
fig,ax=plt.subplots(1,2,figsize=(9,4.2))
ax[0].plot(t,lin,color="#b84a22",lw=2.5,label="linear beta")
ax[0].plot(t,cos,color="#2b4fd6",lw=2.5,ls="--",label="cosine")
ax[0].set_xlabel("step t",fontsize=12); ax[0].set_ylabel("signal kept, abar_t",fontsize=12); ax[0].legend(fontsize=11); ax[0].grid(alpha=.3)
ax[1].semilogy(t,lin/(1-lin+1e-12),color="#b84a22",lw=2.5,label="linear beta")
ax[1].semilogy(t[:-1],cos[:-1]/(1-cos[:-1]),color="#2b4fd6",lw=2.5,ls="--",label="cosine")
ax[1].set_ylim(1e-4,1e3)
ax[1].set_xlabel("step t",fontsize=12); ax[1].set_ylabel("signal-to-noise abar/(1-abar)",fontsize=12); ax[1].grid(alpha=.3)
for a in ax: a.tick_params(labelsize=11)
fig.tight_layout(); fig.savefig("noise_schedules.png",dpi=110)
