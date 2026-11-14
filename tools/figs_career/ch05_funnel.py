from common import *
st=["Visits","Add to cart","Start checkout","Paid"]; n=[10000,3200,900,270]
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
cols=[BLUE,BLUE,BLUE,ORANGE]
ax.barh(st[::-1],n[::-1],color=cols[::-1],height=0.55)
rates=["","32.0% of visits","28.1% of carts","30.0% of checkouts"]
for i,(s,v) in enumerate(zip(st,n)):
    y=3-i; ax.text(v+120,y,f"{v:,}   {rates[i]}",va="center",fontsize=9)
ax.set_xlim(0,13500); clean(ax); ax.set_xlabel("people")
ax.set_title("Only 2.7% of visits end in payment; every step loses about 70%",fontsize=10,fontweight="bold",loc="left")
fig.tight_layout(); fig.savefig("ch05d_funnel.png")
