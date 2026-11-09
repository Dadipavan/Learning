import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
ev = [(1,"09:00"),(1,"09:12"),(1,"09:30"),(1,"11:00"),(1,"11:05"),(2,"10:00"),(2,"10:45"),(2,"10:50")]
sess = {(1,"09:00"):1,(1,"09:12"):1,(1,"09:30"):1,(1,"11:00"):2,(1,"11:05"):2,(2,"10:00"):1,(2,"10:45"):2,(2,"10:50"):2}
cols = {1:"#2b4fd6", 2:"#b84a22"}
mins = lambda t: int(t[:2])*60 + int(t[3:])
fig, ax = plt.subplots(figsize=(8, 3.6), dpi=110)
for (u, t) in ev:
    s = sess[(u, t)]
    ax.scatter(mins(t), u, s=140, color=cols[s], zorder=3, edgecolor="white")
for u in (1, 2):
    xs = [mins(t) for (uu, t) in ev if uu == u]
    ax.plot(xs, [u]*len(xs), color="#bbbbbb", lw=1, zorder=1)
ax.annotate("gap 90 min\n(> 30: new session)", (mins("10:15"), 1.0), (mins("10:05"), 1.35), fontsize=9, ha="center")
ax.annotate("gap 45 min\n(> 30: new session)", (mins("10:22"), 2.0), (mins("10:22"), 2.35), fontsize=9, ha="center")
ax.set_yticks([1, 2]); ax.set_yticklabels(["user 1", "user 2"], fontsize=11); ax.set_ylim(0.5, 2.8)
ax.set_xticks([mins(f"{h:02d}:00") for h in range(9, 12)]); ax.set_xticklabels(["09:00", "10:00", "11:00"], fontsize=10)
ax.set_xlabel("time of day, 1 March 2025", fontsize=11)
ax.scatter([], [], color=cols[1], s=80, label="session 1"); ax.scatter([], [], color=cols[2], s=80, label="session 2")
ax.legend(frameon=False, fontsize=10, loc="lower right")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch12_sessions.png")
