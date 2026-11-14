import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
sc=[5,4,None,5,3,None,4,5]
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2))
labs=["COUNT(*)","COUNT(score)","COUNT(DISTINCT\nscore)"]; v=[8,6,3]
a.bar(labs,v,color=[B,O,T]); 
for i,x in enumerate(v): a.text(i,x+.15,str(x),ha="center",fontsize=11)
a.set_title("Same column, three counts",fontsize=10); a.tick_params(axis="x",labelsize=8); a.set_ylim(0,9.5)
vals=[s for s in sc if s is not None]
av1=sum(vals)/len(vals); av2=sum(vals)/len(sc)
b.bar(["AVG(score)\nNULL skipped","AVG(COALESCE\n(score,0))"],[av1,av2],color=[T,R])
for i,x in enumerate([av1,av2]): b.text(i,x+.06,f"{x:.2f}",ha="center",fontsize=11)
b.set_ylim(0,5.2); b.set_title("Same column, two averages",fontsize=10); b.tick_params(axis="x",labelsize=8)
for ax in (a,b):
    for s in("top","right"): ax.spines[s].set_visible(False)
fig.suptitle("scores: 5, 4, NULL, 5, 3, NULL, 4, 5",fontsize=9,color="#555")
plt.tight_layout(); plt.savefig("ch03d_nulls.png",dpi=110)
