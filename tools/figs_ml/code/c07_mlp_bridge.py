import numpy as np, warnings; warnings.filterwarnings("ignore")
from sklearn.ensemble import HistGradientBoostingClassifier as H
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, QuantileTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0); n = 6000
X = np.c_[rng.lognormal(0, 1.5, (n, 3)), rng.normal(size=(n, 3)), rng.normal(size=(n, 14))]   # 3 skewed, 3 normal, 14 noise
z = (X[:, 0] > 1.5) * 1.5 + np.sin(3 * X[:, 3]) + (X[:, 1] > 1) * (X[:, 4] > 0) * 1.5 + 0.3 * X[:, 5]
y = (z + rng.normal(0, 0.5, n) > 1.2).astype(int)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
print("positive rate", y.mean().round(3))
mods = {"HistGB": H(random_state=0),
        "MLP raw": MLPClassifier((64, 64), max_iter=300, random_state=0),
        "MLP standardised": make_pipeline(StandardScaler(), MLPClassifier((64, 64), max_iter=300, random_state=0)),
        "MLP quantile": make_pipeline(QuantileTransformer(output_distribution="normal", random_state=0), MLPClassifier((64, 64), max_iter=300, random_state=0))}
for k, m in mods.items(): print(f"{k:18s} test accuracy {m.fit(Xtr, ytr).score(Xte, yte):.3f}")
