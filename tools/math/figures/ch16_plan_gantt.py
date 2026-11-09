import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plan = [("Ch 1-2 Algebra, functions", 1, 1), ("Ch 3-4 Logs, counting", 2, 2), ("Ch 5 Vectors", 3, 3), ("Ch 6 Matrices", 4, 4),
        ("Ch 7-8 Systems, eigen", 5, 5), ("Ch 9 SVD, PCA", 6, 6), ("Ch 10-11 Calculus", 7, 7), ("Ch 12 Matrix calculus", 8, 8),
        ("Ch 13 Backprop", 9, 9), ("Ch 14 Optimization", 10, 10), ("Ch 15 Probability, info", 11, 11), ("Ch 16-17 Mocks, project", 12, 12)]
cols = ["#2b4fd6", "#2b4fd6", "#357a70", "#357a70", "#357a70", "#357a70", "#b84a22", "#b84a22", "#b84a22", "#6a2fd0", "#6a2fd0", "#aa2d26"]
fig, ax = plt.subplots(figsize=(8, 4.2))
for i, ((lab, a, b), c) in enumerate(zip(plan, cols)):
    ax.barh(i, 1, left=a-1, color=c)
    ax.text(a-1+1.1, i, lab, va="center", fontsize=8)
ax.set_yticks([]); ax.invert_yaxis(); ax.set_xlim(0, 20); ax.set_xticks(range(0, 13)); ax.set_xlabel("week")
ax.set_title("12-week plan: one block per week (blue algebra, teal linear algebra, orange calculus, purple ML)")
ax.title.set_fontsize(9); ax.grid(axis="x", alpha=0.3)
fig.tight_layout(); fig.savefig("ch16_plan_gantt.png", dpi=110)
