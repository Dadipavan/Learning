import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 7)
y = np.array([350, 330, 375, 405, 430, 455])

# Style 1: the pyplot "state machine" (acts on the current figure and axes)
plt.figure(figsize=(6, 3))
plt.plot(x, y, color="#2b4fd6")
plt.title("Sales")
plt.xlabel("Month")
line_a = plt.gca().lines[0].get_ydata()      # gca() = "get current axes"
plt.close()

# Style 2: object-oriented (you hold fig and ax and call methods on them)
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, y, color="#2b4fd6")
ax.set_title("Sales")
ax.set_xlabel("Month")
line_b = ax.lines[0].get_ydata()
plt.close(fig)

print("same data drawn:", bool((line_a == line_b).all()))
print("figures still open after closing both:", len(plt.get_fignums()))
