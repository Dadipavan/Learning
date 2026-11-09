import numpy as np
rng = np.random.default_rng(0)
x = np.linspace(-3, 3, 8); y = 1.0 + 2.0 * x + rng.normal(0, 1.0, 8)
Phi = np.c_[np.ones_like(x), x]; sig2, alpha = 1.0, 1.0       # noise var, prior precision
S = np.linalg.inv(alpha * np.eye(2) + Phi.T @ Phi / sig2); m = S @ Phi.T @ y / sig2
ridge = np.linalg.solve(Phi.T @ Phi + alpha * sig2 * np.eye(2), Phi.T @ y)
print("posterior mean", m.round(3), "ridge (lambda=alpha*sigma2)", ridge.round(3))
print("posterior sd", np.sqrt(np.diag(S)).round(3))
for xs in (0.0, 2.0, 6.0):
    f = np.array([1, xs]); print(f"x={xs}: pred {f@m:.2f}  sd of mean {np.sqrt(f@S@f):.2f}  predictive sd {np.sqrt(f@S@f+sig2):.2f}")
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C
xt = np.sort(rng.uniform(-4, 4, 12)); yt = np.sin(xt) + rng.normal(0, 0.15, 12)
gp = GPR(C(1.0) * RBF(1.0) + WhiteKernel(0.1), normalize_y=True, n_restarts_optimizer=5, random_state=0).fit(xt[:, None], yt)
print(gp.kernel_)
mu, sd = gp.predict(np.array([[0.0], [2.0], [8.0]]), return_std=True)
print("mean", mu.round(2), "sd", sd.round(2))
