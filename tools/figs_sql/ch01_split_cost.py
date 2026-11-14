import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2))
k=np.arange(1,501)
a.plot(k,k,color=O,lw=2.5,label="one flat table: rows to edit")
a.plot(k,np.ones_like(k),color=T,lw=2.5,label="split tables: rows to edit")
a.set_xlabel("orders this customer has placed"); a.set_ylabel("rows to change when she moves city")
a.set_title("Update cost",fontsize=10); a.legend(fontsize=8.5,frameon=False)
n=np.arange(0,5001,50); cust=100
flat=6*n; split=4*cust+4*n
b.plot(n,flat,color=O,lw=2.5,label="flat: 6 cells per order")
b.plot(n,split,color=T,lw=2.5,label="split: 100 customers + 4 cells per order")
b.set_xlabel("number of orders (100 customers)"); b.set_ylabel("cells stored"); b.set_title("Storage",fontsize=10)
b.legend(fontsize=8,frameon=False,loc="upper left")
for x in (a,b):
    for sp in("top","right"): x.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig("ch01d_split_cost.png",dpi=110)
