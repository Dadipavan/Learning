import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
N=17
cap=1;size=0;cost=[]
for i in range(N):
    c=1
    if size==cap:
        c+=size;cap*=2
    size+=1;cost.append(c)
fig,(a,b)=plt.subplots(1,2,figsize=(9.5,4.2))
x=np.arange(1,N+1)
a.bar(x,cost,color=[R if c>1 else B for c in cost])
a.set_xlabel("append number");a.set_ylabel("work for this append")
a.set_title("Rare expensive appends (red)")
run=np.cumsum(cost)/x
b.plot(x,run,"o-",color=T,lw=2.5)
b.axhline(3,color=O,ls="--",lw=2);b.text(9.5,3.08,"never above 3",color=O,fontsize=12)
b.set_ylim(0,3.6);b.set_xlabel("number of appends so far");b.set_ylabel("average work per append")
b.set_title("The average stays small")
fig.tight_layout();fig.savefig("dsa1_amortised.png",dpi=110)
