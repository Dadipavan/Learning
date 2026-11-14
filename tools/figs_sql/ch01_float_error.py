import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
ns=list(range(1,2001)); fe=[]; s=0.0; ie=[]; si=0
for n in ns:
    s+=0.1; si+=10
    fe.append(abs(s-n/10)); ie.append(abs(si-n*10))
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(ns,fe,color=O,lw=1.4,label="REAL / float: add 0.1 n times")
ax.plot(ns,ie,color=T,lw=2.5,label="INTEGER paise: add 10 n times")
ax.set_xlabel("n (number of payments added up)"); ax.set_ylabel("absolute error of the total")
ax.set_title("Floating point drifts; integer paise never does",fontsize=11)
ax.legend(frameon=False)
for sp in("top","right"): ax.spines[sp].set_visible(False)
print(max(fe))
plt.tight_layout(); plt.savefig("ch01d_float_error.png",dpi=110)
