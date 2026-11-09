import numpy as np
from sklearn.linear_model import Ridge
from sklearn.datasets import make_regression
class MyRidge:
    def __init__(self, alpha=1.0): self.alpha = alpha
    def fit(self, X, y):
        self.mx, self.my = X.mean(0), y.mean(); Xc = X - self.mx
        self.coef_ = np.linalg.solve(Xc.T @ Xc + self.alpha * np.eye(X.shape[1]), Xc.T @ (y - self.my)); return self
    def predict(self, X): return (X - self.mx) @ self.coef_ + self.my
def check(name, ok): print(("PASS " if ok else "FAIL ") + name)
X, y = make_regression(200, 5, noise=3, random_state=0)
a, b = MyRidge(2.0).fit(X, y), Ridge(alpha=2.0).fit(X, y)
check("coef matches sklearn (atol 1e-8)", np.allclose(a.coef_, b.coef_, atol=1e-8))
check("predict matches sklearn", np.allclose(a.predict(X), b.predict(X), atol=1e-8))
check("alpha->inf shrinks to 0", np.abs(MyRidge(1e12).fit(X, y).coef_).max() < 1e-6)
check("row-permutation invariant", np.allclose(a.coef_, MyRidge(2.0).fit(X[::-1], y[::-1]).coef_))
bug = MyRidge(2.0); bug.fit = lambda X, y: (setattr(bug, "mx", np.zeros(5)) or setattr(bug, "my", 0.0) or setattr(bug, "coef_", np.linalg.solve(X.T @ X + 2 * np.eye(5), X.T @ y)) or bug)
check("buggy no-intercept version matches sklearn", np.allclose(bug.fit(X, y).coef_, b.coef_, atol=1e-8))
