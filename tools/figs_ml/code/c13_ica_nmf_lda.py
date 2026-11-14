import numpy as np
from sklearn.decomposition import NMF, FastICA, PCA, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
rng = np.random.default_rng(0)
t = np.linspace(0, 8, 2000)
S = np.c_[np.sign(np.sin(3 * t)), np.sin(5 * t + 1)]
A = np.array([[1.0, 0.5], [0.4, 1.0]]); Xm = S @ A.T + 0.02 * rng.normal(size=S.shape)
ica = FastICA(n_components=2, random_state=0, whiten="unit-variance").fit(Xm)
est = ica.transform(Xm)
c = np.abs(np.corrcoef(S.T, est.T)[:2, 2:]).round(3)
p = PCA(2).fit_transform(Xm); cp = np.abs(np.corrcoef(S.T, p.T)[:2, 2:]).round(3)
print("ICA |corr| true vs recovered:\n", c, "\nPCA |corr|:\n", cp)
# NMF on parts
V = np.array([[5,4,0,0],[4,5,1,0],[0,1,5,4],[0,0,4,5],[3,3,3,3]], float)
m = NMF(2, init="nndsvda", random_state=0, max_iter=1000).fit(V)
print("W\n", m.transform(V).round(2), "\nH\n", m.components_.round(2), "\nerr", round(m.reconstruction_err_, 3))
docs = ["goal match team win league", "team coach win season goal", "match league season coach team",
        "stock market price trade bank", "bank price market loan trade", "loan stock bank market invest",
        "goal team bank market"] 
cv = CountVectorizer(); D = cv.fit_transform(docs)
lda = LatentDirichletAllocation(2, random_state=0, max_iter=200).fit(D)
w = np.array(cv.get_feature_names_out())
for k, row in enumerate(lda.components_): print("topic", k, w[row.argsort()[::-1][:4]])
print(lda.transform(D).round(2))
