import sys, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
DATA = "/Users/c2487352/Personal/Career/final/study/ways/data/"
sys.path.insert(0, DATA); import prep, mlprep
o, c, p = prep.load_clean(DATA); d = mlprep.late_frame(o)
tr = d[d.order_date < "2024-10-01"]; F = mlprep.CAT + mlprep.NUM
pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore", sparse_output=False), mlprep.CAT), ("n", StandardScaler(), mlprep.NUM)])
X = pre.fit_transform(tr[F]); y = tr.late.values
rng = np.random.default_rng(0); H = 16
W1 = rng.normal(0, .3, (X.shape[1], H)); b1 = np.zeros(H); W2 = rng.normal(0, .3, H); b2 = -1.8
sig = lambda z: 1 / (1 + np.exp(-z)); losses = []
for ep in range(400):
    A = np.tanh(X @ W1 + b1); P = sig(A @ W2 + b2)
    losses.append(-np.mean(y * np.log(P + 1e-9) + (1 - y) * np.log(1 - P + 1e-9)))
    dz = (P - y) / len(y); gW2 = A.T @ dz; gb2 = dz.sum(); dA = np.outer(dz, W2) * (1 - A ** 2)
    W1 -= .5 * (X.T @ dA); b1 -= .5 * dA.sum(0); W2 -= .5 * gW2; b2 -= .5 * gb2
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(losses, color="#2b4fd6"); ax[0].set_xlabel("epoch"); ax[0].set_ylabel("log loss"); ax[0].set_title("Numpy network: training loss")
V = TfidfVectorizer(); T = V.fit_transform(p.description)
Z = TruncatedSVD(2, random_state=0).fit_transform(T)
cols = {"Grocery": "#357a70", "Electronics": "#2b4fd6", "Fashion": "#b84a22", "Home": "#6a2fd0", "Beauty": "#aa2d26"}
for k, cc in cols.items():
    m = (p.category == k).values; ax[1].scatter(Z[m, 0], Z[m, 1], color=cc, label=k, s=36)
ax[1].legend(fontsize=7, frameon=False); ax[1].set_title("Product descriptions: TF-IDF + SVD, 2 dimensions")
for a in ax: a.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch07_nn_embed.png", dpi=110)
