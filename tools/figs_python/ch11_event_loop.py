from common import *
fig, ax = plt.subplots(figsize=(8.5, 3.8))
tasks = {"fetch A": [(0, 0.2, "run"), (0.2, 1.0, "wait"), (1.2, 0.2, "run")],
         "fetch B": [(0.2, 0.2, "run"), (0.4, 1.0, "wait"), (1.4, 0.2, "run")],
         "fetch C": [(0.4, 0.2, "run"), (0.6, 1.0, "wait"), (1.6, 0.2, "run")]}
for i, (name, segs) in enumerate(tasks.items()):
    y = 2 - i
    for st, d, k in segs:
        ax.barh(y, d, left=st, height=0.55, color=BLUE if k == "run" else "#d9d9d9", edgecolor=BLUE if k == "run" else "#999")
    ax.text(-0.05, y, name, ha="right", va="center")
ax.set_yticks([]); ax.set_xlim(-0.05, 1.9); ax.set_xlabel("time (seconds, one thread)")
ax.set_title("asyncio: three 1-second waits overlap, total about 1.8 s instead of 3.6 s")
ax.barh(-1, 0, color=BLUE, label="running Python code"); ax.barh(-1, 0, color="#d9d9d9", label="waiting on the network")
ax.legend(loc="lower right"); ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, "ch11_event_loop.png")
