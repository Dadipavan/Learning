import numpy as np
# 1-D Kalman filter for a slowly drifting level. x_t = x_(t-1) + process noise (variance Q); z_t = x_t + noise (variance R)
Q, R = 0.1, 1.0
x, P = 0.0, 1.0
for z in (1.2, 0.8):
    P_pred = P + Q; K = P_pred / (P_pred + R)
    x = x + K * (z - x); P = (1 - K) * P_pred
    print("z=%.1f  predicted var %.4f  gain %.4f  estimate %.4f  new var %.4f" % (z, P_pred, K, x, P))
# simulation: filter versus raw measurements
rng = np.random.default_rng(1)
n = 200; truth = np.cumsum(rng.normal(0, np.sqrt(Q), n)); z = truth + rng.normal(0, np.sqrt(R), n)
x, P, est = 0.0, 1.0, []
for zt in z:
    Pp = P + Q; K = Pp / (Pp + R); x = x + K * (zt - x); P = (1 - K) * Pp; est.append(x)
est = np.array(est)
print("RMSE raw measurement: %.3f   RMSE Kalman: %.3f   steady-state gain: %.3f" % (np.sqrt(np.mean((z - truth) ** 2)), np.sqrt(np.mean((est - truth) ** 2)), K))
