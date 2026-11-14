from ch12_common import *
segs = [("Clarify", 0, 5, B), ("Examples + brute force", 5, 10, T), ("Optimise", 10, 18, O),
        ("Code", 18, 33, P), ("Test", 33, 40, T), ("Complexity + Q&A", 40, 45, R)]
fig, ax = plt.subplots(figsize=(8, 3.6)); ax.set_xlim(0, 45); ax.set_ylim(-0.3, 3.0)
ax.spines[["top", "right", "left"]].set_visible(False); ax.set_yticks([])
for i, (n, s, e, c) in enumerate(segs):
    ax.add_patch(Rectangle((s, 0), e - s, 1, fc=c, ec="white", lw=3))
    ax.text((s + e) / 2, 1.15 + (0.8 if i % 2 else 0), n, ha="center", va="bottom", fontsize=13, color=c, fontweight="bold")
    ax.text((s + e) / 2, 0.5, "%d min" % (e - s), ha="center", va="center", fontsize=13, color="white", fontweight="bold")
ax.set_xticks(range(0, 46, 5)); ax.set_xlabel("minutes into a 45-minute round", fontsize=14)
ax.set_title("A time budget for one interview problem", fontsize=15)
plt.tight_layout(); plt.savefig("dsa12_timeline.png", dpi=110)
