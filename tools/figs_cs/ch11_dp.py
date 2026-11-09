import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np
# LCS
a,b="AGGTAB","GXTXAYB"
dp=[[0]*(len(b)+1) for _ in range(len(a)+1)]
for i in range(1,len(a)+1):
    for j in range(1,len(b)+1):
        dp[i][j]=dp[i-1][j-1]+1 if a[i-1]==b[j-1] else max(dp[i-1][j],dp[i][j-1])
# traceback
i,j=len(a),len(b); path=[]
while i and j:
    if a[i-1]==b[j-1]: path.append((i,j)); i-=1; j-=1
    elif dp[i-1][j]>=dp[i][j-1]: i-=1
    else: j-=1
fig,ax=plt.subplots(figsize=(8,4.6))
M=np.array(dp)
ax.imshow(M,cmap="Blues",vmin=0,vmax=7)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        hit=(i,j) in path
        ax.text(j,i,str(M[i,j]),ha="center",va="center",fontsize=12,color=ORANGE if hit else "#111",fontweight="bold" if hit else "normal")
        if hit: ax.add_patch(plt.Rectangle((j-.5,i-.5),1,1,fill=False,ec=ORANGE,lw=2.5))
ax.set_xticks(range(len(b)+1)); ax.set_xticklabels(["-"]+list(b),fontsize=12)
ax.set_yticks(range(len(a)+1)); ax.set_yticklabels(["-"]+list(a),fontsize=12)
ax.xaxis.tick_top()
ax.set_title("LCS table for AGGTAB and GXTXAYB (orange = cells where letters matched)",pad=28,fontsize=11)
plt.tight_layout(); plt.savefig("ch11_lcs_table.png",dpi=110); plt.close()
print(dp[-1][-1],[ (a[i-1]) for i,j in path][::-1])
# knapsack
items=[(1,1),(3,4),(4,5),(5,7)]; W=7
K=[[0]*(W+1) for _ in range(len(items)+1)]
for i,(w,v) in enumerate(items,1):
    for c in range(W+1):
        K[i][c]=K[i-1][c]
        if c>=w: K[i][c]=max(K[i][c],K[i-1][c-w]+v)
# trace chosen
c=W; chosen=[]
for i in range(len(items),0,-1):
    if K[i][c]!=K[i-1][c]: chosen.append(i); c-=items[i-1][0]
fig,ax=plt.subplots(figsize=(8,3.9))
M=np.array(K)
ax.imshow(M,cmap="Blues",vmin=0,vmax=12)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j,i,str(M[i,j]),ha="center",va="center",fontsize=12)
ax.add_patch(plt.Rectangle((W-.5,len(items)-.5),1,1,fill=False,ec=ORANGE,lw=3))
ax.set_xticks(range(W+1)); ax.set_xlabel("capacity")
ax.set_yticks(range(len(items)+1)); ax.set_yticklabels(["no items"]+[f"item {i} (w={w}, v={v})" for i,(w,v) in enumerate(items,1)])
ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
plt.tight_layout(); plt.savefig("ch11_knapsack_table.png",dpi=110); plt.close()
print(K[-1][-1],chosen)
# fib call tree: naive vs memo
def tree(n,memo):
    seen=set(); edges=[]; cnt=[0]
    def f(n,parent_id,depth,xi):
        pass
    return None
# count calls
def calls(n): return 1 if n<2 else 1+calls(n-1)+calls(n-2)
ns=list(range(2,31)); naive=[calls(n) for n in ns]; memo=[2*n-1 for n in ns]
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(ns,naive,color=ORANGE,lw=2.5,label="naive recursion: calls to fib(n)")
ax.plot(ns,memo,color=BLUE,lw=2.5,label="with memoization: 2n - 1 calls")
ax.set_yscale("log"); ax.set_xlabel("n"); ax.set_ylabel("number of calls (log scale)")
ax.legend(); ax.grid(alpha=.3); ax.set_title("Memoization turns exponential work into linear work")
plt.tight_layout(); plt.savefig("ch11_fib_calls.png",dpi=110); plt.close()
print(calls(30), 2*30-1)
