import numpy as np
# One state, two actions, softmax policy with logits theta. REINFORCE gradient by hand and by code.
theta = np.array([0.0, 0.0])
pi = np.exp(theta) / np.exp(theta).sum()
print("pi:", pi)
# we took action 1 and got return G = 4
a, G = 1, 4.0
grad_logp = -pi.copy(); grad_logp[a] += 1       # d log pi(a) / d theta = onehot(a) - pi
print("grad log pi(a=1):", grad_logp)
alpha = 0.1
theta_new = theta + alpha * G * grad_logp
pi_new = np.exp(theta_new) / np.exp(theta_new).sum()
print("theta after update:", theta_new)
print("pi after update:", np.round(pi_new, 4))
# with a baseline b = 3 the push is smaller
b = 3.0
theta_b = theta + alpha * (G - b) * grad_logp
pi_b = np.exp(theta_b) / np.exp(theta_b).sum()
print("with baseline 3, pi:", np.round(pi_b, 4))
