import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, warnings; warnings.simplefilter("ignore")
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,(a1,a2)=plt.subplots(1,2,figsize=(8,4.2),gridspec_kw=dict(width_ratios=[1.1,1]))
s=np.arange(0,1000,5.0)
true=2*s+np.log1p(np.exp(-2*s)*0+0)  # logits [s,0,-s], true class is last: loss = logsumexp - (-s)
true=s+np.log(1+np.exp(-s)+np.exp(-2*s))+s
naive=[]
for v in s:
    z=np.array([v,0,-v]); p=np.exp(z)/np.exp(z).sum(); naive.append(-np.log(p[2]))
naive=np.array(naive)
a1.plot(s,true,color=B,lw=3,label="stable (logsumexp)")
fin=np.isfinite(naive); a1.plot(s[fin],naive[fin],color=O,lw=2,ls="--",label="naive exp / sum / log")
bad=s[~fin][0]; a1.axvline(bad,color=R,ls=":",lw=1.5); a1.text(bad+15,200,"naive breaks\n(inf or nan)",color=R,fontsize=9)
a1.set_xlabel("logit size s, logits = [s, 0, -s]",fontsize=10); a1.set_ylabel("cross-entropy of last class",fontsize=10)
a1.set_title("Same maths, different code",fontsize=11); a1.legend(fontsize=9,loc="upper left"); a1.grid(alpha=.3)
names=["float16","bfloat16","float32"]; mx=[np.log10(65504),38.53,38.53]; mn=[np.log10(6.1e-5),np.log10(1.18e-38),np.log10(1.18e-38)]
for i,(n,c) in enumerate(zip(names,[R,T,B])):
    a2.barh(i,mx[i]-mn[i],left=mn[i],color=c,height=.5)
    lab=["6.1e-5 to 65504","1.2e-38 to 3.4e38","1.2e-38 to 3.4e38"][i]
    a2.text(mx[i]+1.5,i,lab,va="center",ha="left",fontsize=9)
a2.set_xlim(-45,75)
a2.set_yticks(range(3)); a2.set_yticklabels(names,fontsize=10); a2.set_xlabel("log10 of value (smallest normal to largest)",fontsize=10)
a2.set_title("Range of normal numbers",fontsize=11); a2.grid(alpha=.3,axis="x")
fig.tight_layout(); fig.savefig("ch04d_stability.png",dpi=110)
