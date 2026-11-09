import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
m=["Jan","Feb","Mar","Apr"]
E=[2100,1500,1200,2700];H=[0,900,900,1800];S=[160,120,880,400]
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2),gridspec_kw={"width_ratios":[1,1.3]})
a.axis("off"); a.set_title("Long: one row per (month, category)",fontsize=9.5)
rows=[("2024-01","Electronics",2100),("2024-01","Stationery",160),("2024-02","Electronics",1500),("2024-02","Home",900),("2024-02","Stationery",120),("2024-03","Electronics",1200),("...","...","...")]
a.text(0,.95,"month        category        revenue",family="monospace",fontsize=8,weight="bold")
for i,r in enumerate(rows): a.text(0,.85-i*.1,f"{r[0]:<12} {r[1]:<14} {r[2]:>6}",family="monospace",fontsize=8)
a.text(0,.1,"Home has no row in 2024-01:\nthe wide table must show 0 there.",fontsize=8.5,color=O)
b.bar(m,E,color=B,label="Electronics FILTER")
b.bar(m,H,bottom=E,color=T,label="Home FILTER")
b.bar(m,S,bottom=[e+h for e,h in zip(E,H)],color=O,label="Stationery FILTER")
for i in range(4): b.text(i,E[i]+H[i]+S[i]+60,str(E[i]+H[i]+S[i]),ha="center",fontsize=9)
b.set_ylim(0,5600); b.legend(fontsize=8,frameon=False,loc="upper left"); b.set_title("Wide: one row per month, one column per category",fontsize=9.5)
for s in("top","right"): b.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("ch03d_pivot.png",dpi=110)
