import numpy as np
from sklearn.datasets import make_friedman1
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
X, y = make_friedman1(n_samples=2000, noise=2.0, random_state=1)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, random_state=1)

def boost(X, y, k_under, rounds=150, eta=0.1):
    """Newton boosting for l = w (y-F)^2 with w = k_under if y > F else 1. Leaf = -G/H."""
    F = np.full(len(y), y.mean()); f0 = F[0]; trees = []
    for _ in range(rounds):
        w = np.where(y > F, k_under, 1.0)
        g = -2 * w * (y - F); h = 2 * w
        t = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, -g / h, sample_weight=h)  # leaf = sum(-g)/sum(h)
        F = F + eta * t.predict(X); trees.append(t)
    return lambda Z: f0 + eta * sum(t.predict(Z) for t in trees)

def cost(y, F, k): return np.mean(np.where(y > F, k, 1.0) * (y - F) ** 2)
for k in (1, 3):
    pred = boost(Xtr, ytr, k)(Xte)
    print("trained with weight %d: under-predicted %.1f%% of test rows, mean absolute error %.2f, asymmetric cost (weight 3) %.2f"
          % (k, 100 * np.mean(yte > pred), np.mean(np.abs(yte - pred)), cost(yte, pred, 3)))
