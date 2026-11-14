import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
a=[5,3,7,9,6,4,1,2]
n=8
fig,ax=plt.subplots(figsize=(8,4.2))
for i in range(1,n+1):
    lo=i&-i
    left=i-lo
    col=[BLUE,TEAL,ORANGE,PURPLE][ (lo.bit_length()-1) ]
    ax.barh(n-i,lo,left=left+0.5,height=0.7,color=col,edgecolor="#222")
    ax.text(left+0.5+lo/2,n-i,f"t[{i}] = {sum(a[left:i])}",ha="center",va="center",color="white",fontsize=10)
ax.set_xticks(range(1,n+1)); ax.set_xticklabels([f"{a[i]}\n(pos {i+1})" for i in range(n)])
ax.set_yticks([]); ax.set_xlim(0.5,n+0.5)
ax.set_title("Fenwick tree: t[i] stores the sum of the last lowbit(i) values ending at i")
for s in ("top","right","left"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("ch10_fenwick.png",dpi=110); plt.close()
