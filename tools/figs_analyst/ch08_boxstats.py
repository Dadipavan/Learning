import matplotlib
matplotlib.use("Agg")
import numpy as np
x = np.array([12, 15, 18, 20, 22, 25, 60])
q1, med, q3 = np.percentile(x, [25, 50, 75])
iqr = q3 - q1
low_fence, high_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
inside = x[(x >= low_fence) & (x <= high_fence)]
print(f"Q1={q1}  median={med}  Q3={q3}  IQR={iqr}")
print(f"fences: {low_fence} to {high_fence}")
print(f"whiskers end at {inside.min()} and {inside.max()}; outliers: {x[(x < low_fence) | (x > high_fence)].tolist()}")
