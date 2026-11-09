import numpy as np
states = ["Good", "Worn", "Failing"]; obs_names = ["Low", "Med", "High"]
pi = np.array([0.6, 0.3, 0.1])
A = np.array([[0.7, 0.2, 0.1], [0.1, 0.7, 0.2], [0.0, 0.2, 0.8]])
B = np.array([[0.7, 0.2, 0.1], [0.2, 0.6, 0.2], [0.1, 0.3, 0.6]])
obs = [0, 1, 2]                                                   # Low, Med, High
# forward algorithm
alpha = pi * B[:, obs[0]]
print("alpha1", np.round(alpha, 4))
for t in obs[1:]:
    alpha = (alpha @ A) * B[:, t]
    print("alpha%d" % (t + 1), np.round(alpha, 4))
print("P(Low, Med, High) = %.5f" % alpha.sum())
# Viterbi
delta = pi * B[:, obs[0]]; back = []
print("delta1", np.round(delta, 4))
for t in obs[1:]:
    cand = delta[:, None] * A                                     # cand[i, j] = delta_i * A_ij
    back.append(cand.argmax(0)); delta = cand.max(0) * B[:, t]
    print("delta%d" % (t + 1), np.round(delta, 4), "best previous", [states[i] for i in back[-1]])
path = [int(delta.argmax())]
for b in reversed(back): path.append(int(b[path[-1]]))
print("best path:", [states[i] for i in reversed(path)], "prob %.5f" % delta.max())
