import numpy as np
def dcg(r): return sum((2**v - 1) / np.log2(i + 2) for i, v in enumerate(r))
rel = [3, 2, 3, 0, 1, 2]
print("DCG@6", round(dcg(rel), 4), "ideal", round(dcg(sorted(rel, reverse=True)), 4), "NDCG", round(dcg(rel) / dcg(sorted(rel, reverse=True)), 4))
from sklearn.metrics import ndcg_score
print("sklearn", round(ndcg_score([rel], [[6,5,4,3,2,1]]), 4))
