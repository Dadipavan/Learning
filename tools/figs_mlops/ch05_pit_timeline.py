import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import datetime as dt, matplotlib.dates as md
d=lambda s: dt.date.fromisoformat(s)
fts=[d("2026-01-05"),d("2026-01-25"),d("2026-02-10")]; fv=[1,4,9]
ev=[d("2026-01-20"),d("2026-02-03")]
fig,ax=plt.subplots(figsize=(8,3.6))
ax.hlines(0,d("2026-01-01"),d("2026-02-15"),color="#999",lw=2)
for t,v in zip(fts,fv):
    ax.plot([t],[0],"s",color="#2b4fd6",ms=11); ax.text(t,0.22,f"orders_30d = {v}",ha="center",color="#2b4fd6",fontsize=10)
for t,lab in zip(ev,["event A (Jan 20)","event B (Feb 3)"]):
    ax.axvline(t,color="#b84a22",ls="--",lw=1.6); ax.text(t,-0.55,lab,ha="center",color="#b84a22",fontsize=10)
ax.annotate("",xy=(d("2026-01-05"),-0.18),xytext=(d("2026-01-20"),-0.18),arrowprops=dict(arrowstyle="->",color="#357a70",lw=2))
ax.annotate("",xy=(d("2026-01-25"),-0.18),xytext=(d("2026-02-03"),-0.18),arrowprops=dict(arrowstyle="->",color="#357a70",lw=2))
ax.text(d("2026-02-10"),-0.35,"value of Feb 10 is the future\nfor both events: never use it",ha="center",color="#aa2d26",fontsize=9)
ax.set_ylim(-0.8,0.6); ax.set_yticks([]); ax.xaxis.set_major_formatter(md.DateFormatter("%b %d")); ax.set_title("Point-in-time join: each event takes the latest value on or before its date")
for s in ("left","right","top"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch05_pit_timeline.png",dpi=110)
