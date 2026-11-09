import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
rng=np.random.default_rng(4)
P=rng.uniform(0,10,size=(250,2)); q=np.array([8.2,7.6])
D=np.linalg.norm(P[:,None]-P[None],axis=2); np.fill_diagonal(D,99)
nb=[set(np.argsort(D[i])[:5].tolist()) for i in range(len(P))]
for i in range(len(P)):
    for j in list(nb[i]): nb[j].add(i)
cur=int(np.argmin(np.linalg.norm(P-[0.5,0.5],axis=1))); path=[cur]; calls=1
while True:
    best=cur
    for v in nb[cur]:
        calls+=1
        if np.linalg.norm(P[v]-q)<np.linalg.norm(P[best]-q): best=v
    if best==cur: break
    cur=best; path.append(cur)
fig,ax=plt.subplots(figsize=(8,4.2))
for i in range(len(P)):
    for j in nb[i]:
        if i<j: ax.plot(*zip(P[i],P[j]),color="#d0d0d0",lw=0.6,zorder=1)
ax.scatter(*P.T,s=14,color="#999",zorder=2)
ax.plot(*P[path].T,color="#2b4fd6",lw=2.5,marker="o",ms=6,zorder=3,label=f"greedy walk ({len(path)-1} hops)")
ax.scatter(*P[path[0]],s=120,color="#357a70",zorder=4,label="entry point"); 
ax.scatter(*q,marker="*",s=260,color="#aa2d26",zorder=5,label="query")
ax.scatter(*P[path[-1]],s=120,facecolors="none",edgecolors="#6a2fd0",lw=2.5,zorder=5,label="where the walk stopped")
ax.set_title(f"Graph search: {calls} distance checks instead of {len(P)} (toy 2-D example)")
ax.legend(frameon=False,fontsize=8.5,loc="lower left"); ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("ch06d_hnsw_walk.png",dpi=110)
print(len(path)-1,calls)
