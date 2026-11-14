import numpy as np
# DQN target arithmetic for one stored transition (s, a, r, s').
gamma = 0.9
q_online_s = np.array([1.0, 2.5])          # online network Q(s, .) for 2 actions
a, r = 1, -1.0
q_target_next = np.array([3.0, 5.0])       # frozen target network Q_target(s', .)
q_online_next = np.array([4.0, 2.0])       # online network Q(s', .)
y_dqn = r + gamma * q_target_next.max()
print("DQN target y:", y_dqn)
a_star = q_online_next.argmax()            # Double DQN: online net picks, target net scores
y_ddqn = r + gamma * q_target_next[a_star]
print("Double DQN target y:", round(y_ddqn, 2))
loss = (y_dqn - q_online_s[a]) ** 2
print("squared TD error for DQN:", loss)
# terminal transition: no bootstrap
print("terminal transition, reward 10, target:", 10.0)
