import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
import time,bisect,random
def best(f,reps=5):
    b=1e9
    for _ in range(reps):
        t=time.perf_counter();f();b=min(b,time.perf_counter()-t)
    return b
sizes=[10**3,10**4,10**5,10**6]
lst_t,set_t,bis_t=[],[],[]
for n in sizes:
    a=list(range(n));s=set(a);target=n-1;k=200
    lst_t.append(best(lambda:[target in a for _ in range(20)])/20*1e6)
    set_t.append(best(lambda:[target in s for _ in range(k)])/k*1e6)
    bis_t.append(best(lambda:[bisect.bisect_left(a,target) for _ in range(k)])/k*1e6)
def dup_nested(a):
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            if a[i]==a[j]:return True
    return False
def dup_set(a):
    return len(set(a))<len(a)
ns=[250,500,1000,2000,4000]
tn,ts=[],[]
for n in ns:
    a=list(range(n))
    tn.append(best(lambda:dup_nested(a),3));ts.append(best(lambda:dup_set(a),3))
fig,(a1,a2)=plt.subplots(1,2,figsize=(9.5,4.4))
a1.loglog(sizes,lst_t,"o-",color=O,lw=2.5,label="x in list  O(n)")
a1.loglog(sizes,bis_t,"s-",color=T,lw=2.5,label="bisect  O(log n)")
a1.loglog(sizes,set_t,"^-",color=B,lw=2.5,label="x in set  O(1)")
a1.set_xlabel("n (items stored)");a1.set_ylabel("time per lookup (microseconds)")
a1.set_title("Looking up one value");a1.legend(fontsize=11,frameon=False);a1.grid(alpha=.25,which="both")
a2.loglog(ns,tn,"o-",color=R,lw=2.5,label="nested loops  O(n²)")
a2.loglog(ns,ts,"^-",color=B,lw=2.5,label="set  O(n)")
a2.set_xlabel("n (list length)");a2.set_ylabel("time (seconds)")
a2.set_xticks(ns);a2.set_xticklabels([str(k) for k in ns],fontsize=10);a2.minorticks_off()
a2.set_title("Duplicate check, no duplicates");a2.legend(fontsize=11,frameon=False);a2.grid(alpha=.25,which="both")
fig.tight_layout();fig.savefig("dsa1_timing.png",dpi=110)
