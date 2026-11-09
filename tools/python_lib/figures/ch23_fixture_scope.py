import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T = "#2b4fd6", "#b84a22", "#357a70"
fig, axes = plt.subplots(2, 1, figsize=(8, 4.2), dpi=110, sharex=True)
for ax, title, scope in zip(axes, ["scope='function' (default)", "scope='session'"], ["f", "s"]):
    t = 0
    if scope == "s":
        ax.barh(0, 2, left=0, color=O, label="setup")
    for k in range(4):
        if scope == "f":
            ax.barh(0, 2, left=t, color=O, label="setup" if k == 0 else None)
            ax.barh(0, 1, left=t + 2, color=B, label="test body" if k == 0 else None)
            ax.barh(0, 0.8, left=t + 3, color=T, label="teardown" if k == 0 else None)
            t += 4
        else:
            start = 2 + k * 1.5
            ax.barh(0, 1, left=start, color=B, label="test body" if k == 0 else None)
    if scope == "s":
        ax.barh(0, 0.8, left=8, color=T, label="teardown")
    ax.set_yticks([]); ax.set_title(title, fontsize=13, loc="left")
    ax.legend(fontsize=11, loc="upper right", ncol=3, frameon=False)
    ax.set_xlim(0, 17); ax.set_ylim(-0.5, 1.2)
axes[1].set_xlabel("time (arbitrary units), four tests", fontsize=13)
for a in axes: a.tick_params(labelsize=12)
fig.tight_layout(); fig.savefig("lib23_fixture_scope.png")
