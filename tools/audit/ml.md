# Audit: study/ml (Machine Learning), 18 chapters + appendix

## Verdict
Strong, unusually honest text. Chapters 1-16 follow one pattern (intuition, derivation, from-scratch NumPy matched to scikit-learn, worked problems with step tables, recap, practice set with answers in tiers easy/medium/hard, prompt pack). Beginner clarity is high and numbers I spot-checked were correct (conformal k = ceil(1501*0.9) = 1351; undersampling prior correction; Q-learning update 3.3; Shapley setup). Weaknesses: (a) figures thin (ch06-ch18 have 0-2 SVGs; ch14-18 none), (b) several "expert" items from the site skill map are only a one-line mention (HMM, Kalman, NMF/ICA, LDA/BERTopic, HDBSCAN, Gower, MICE, multi-label, learning-to-rank, federated, metric learning, TabNet/FT-Transformer, survival/causal/uplift, Wilcoxon/Friedman), (c) ch15 RL is only 3 sections (no policy gradient/actor-critic derivation), (d) ch17/18 project labs have 0 formal worked problems/steps tables, (e) XGBoost/LightGBM/CatBoost code in ch07 is "not run here", (f) many concepts have 1-2 worked examples, not 3 varied ones (ch06-08, ch14, ch15). Counts below use regex and include code text in words, so words are inflated a little.

## Per chapter (words, h2 incl. recap/practice/prompt, problem, steps tables, code blocks, callouts, figures; ratings beginner / expert)
| Ch | Topic | Words | Prob | Steps | Code | Callouts | Fig | Beg | Exp |
|---|---|---|---|---|---|---|---|---|---|
| 01 | What learning means, ERM, bias-variance, MLE/MAP | 7023 | 12 | 12 | 24 | 13 | 6 | 5 | 4 |
| 02 | Linear regression | 6720 | 6 | 6 | 25 | 11 | 4 | 5 | 4 |
| 03 | Regularization | 5439 | 6 | 6 | 17 | 9 | 4 | 5 | 4 |
| 04 | Logistic, softmax, GLM, perceptron | 6795 | 9 | 9 | 20 | 12 | 4 | 5 | 4 |
| 05 | SVM, kNN, naive Bayes | 7263 | 7 | 7 | 16 | 11 | 4 | 5 | 3 |
| 06 | Trees, random forest | 5673 | 8 | 6 | 14 | 11 | 2 | 4 | 3 |
| 07 | Gradient boosting, XGB/LGBM/CatBoost | 5728 | 5 | 4 | 9 | 9 | 2 | 4 | 3 |
| 08 | Validation and leakage | 4981 | 6 | 4 | 13 | 10 | 2 | 4 | 4 |
| 09 | Metrics, calibration, conformal | 6273 | 10 | 8 | 7 | 14 | 2 | 4 | 5 |
| 10 | Debugging, comparing models | 6198 | 18 | 7 | 30 | 13 | 2 | 4 | 4 |
| 11 | Tuning, optimization, AutoML | 6683 | 19 | 9 | 27 | 17 | 2 | 4 | 3 |
| 12 | Hard data situations | 8033 | 19 | 7 | 44 | 15 | 2 | 4 | 4 |
| 13 | Unsupervised | 8419 | 17 | 4 | 42 | 18 | 4 | 4 | 3 |
| 14 | Anomaly, semi/self-supervised, active, transfer | 7185 | 10 | 10 | 15 | 12 | 0 | 4 | 3 |
| 15 | RL and bandits | 6384 | 9 | 9 | 13 | 7 | 0 | 4 | 2 |
| 16 | Explain, fairness, robustness, eng. hygiene, interview bank | 9170 | 14 | 14 | 24 | 12 | 0 | 4 | 3 |
| 17 | Project lab 1 | 7306 | 0 | 0 | 37 | 2 | 0 | 4 | 4 |
| 18 | Project lab 2 | 5874 | 0 | 0 | 16 | 0 | 0 | 4 | 4 |
| App | Cheat sheet | 2234 | 0 | 0 | 0 | 0 | 0 | 3 | n/a |

Practice sets: present in every chapter 1-18, tiered easy/medium/hard, include "find the bug" and "what is the output", all with answers. Appendix has no practice (fine).

## Weakest 3: ch15 (RL), ch07 (boosting; few examples, libs unrun), ch14 (breadth without depth, no figures). Close: ch05, ch06, ch13.
## Strongest 2: ch09 (metrics/calibration/conformal), ch01 (foundations, 12 worked problems). Also good: ch08, ch10.

## Top 12 gaps (ranked by learner value)
1. ch15: policy gradients (REINFORCE derivation, baseline, variance), actor-critic, DQN mechanics (replay, target net), Monte Carlo vs TD vs DP comparison; examples: CartPole REINFORCE in NumPy, value iteration on 4x4 grid with step table, UCB vs Thompson vs epsilon-greedy regret curves. ~2500 words, 2 figures.
2. ch07: three varied worked boosting examples (classification log-loss by hand with 6 rows, XGBoost gain/leaf-weight arithmetic with lambda and gamma, early-stopping curve), plus run and verify XGBoost/LightGBM/CatBoost output; add monotonic constraint and custom-loss example with figure. ~1800 words.
3. ch14/ch13: figures and code for Isolation Forest, LOF, autoencoder anomaly, CUSUM/ADWIN change-point; seasonal decomposition residual anomaly on a performance metric. Add worked changepoint example. ~1500 words, 4 figures.
4. ch13: expand HDBSCAN, Gower distance, NMF, ICA, factor analysis, LDA/BERTopic with topic coherence; silhouette/ARI/stability worked examples; PCA via SVD derivation with scree figure. ~2200 words.
5. New section (ch05 or ch04): Gaussian processes and kernel ridge, SVR, Bayesian linear regression; example: GP regression with uncertainty bands, Bayesian optimization link to ch11. ~1800 words.
6. New section (ch14 or new chapter): Hidden Markov Models (forward, Viterbi worked on 3 states) and Kalman filter (1-D worked update). ~1800 words.
7. ch06/ch08: tree visuals (split diagram, decision regions, OOB curve, permutation vs impurity importance bias), extra trees, categorical and missing handling in trees; 3rd worked example for pruning (cost-complexity alpha path). ~1200 words, 4 figures.
8. ch12: MICE/iterative imputation worked example, SMOTE/ADASYN with its pitfalls worked, missing indicator comparison; confident learning with cleanlab worked example. ~1500 words.
9. ch16/ch09: causal and uplift modelling basics, survival analysis (Cox, time-to-event, censoring) and multi-label/learning-to-rank (LambdaMART, NDCG worked). The site map lists learning-to-rank, multi-label, federated, metric learning; currently one-liners. ~2500 words.
10. ch10/ch11: statistical tests for comparing models across datasets (Wilcoxon, Friedman, Nemenyi; zero hits now), corrected resampled t-test worked example; Hyperband/ASHA and Optuna TPE worked trial table. ~1200 words.
11. ch17/ch18: add worked-problem and steps-table scaffolding (expected output, grading rubric, common failure per step) and a figure per project (cost curve, calibration plot, segment profile). ~1200 words, 4 figures.
12. New: tabular deep learning bridge (MLP with embeddings, TabNet, FT-Transformer, why GBM still wins), 2-layer NN backprop from scratch (listed in REBUILD list N), SVM via subgradient/SMO from scratch. ~2000 words.

Total recommended additions: 12 items, about 21,000 words and about 20 figures.

## Errors and risks found (verified by reading, none severe)
- No definite factual error found in sampled sections. Calculations checked: ch03 ridge/lasso toy answers, ch09 conformal k, undersampling correction (ch09, ch12: 0.1176), ch15 Q update, ch17 threshold 10/110 = 0.0909.
- ch07: library outputs for XGBoost/LightGBM/CatBoost are unexecuted ("not run here"); numbers about them cannot be trusted until run.
- ch09 conformal classification coverage 0.886 against 0.90 target is explained as sampling noise (SE about 0.007); this is 2 SE below, borderline; consider rerun with a different seed or more rows to avoid doubt.
- ch07 says scikit-learn 1.9.1 outputs; version string should be rechecked when the site is rebuilt. Ch16 "From-scratch list" and "Interview bank" live inside the ch16 file, so ch16 is overloaded (9170 words, 10 h2); split recommended.
- The ml index key lists section O (libraries), P (study path), S (interview), T (resources) with 0 items; ensure appendix/index covers them.
- No appendix practice and no figures from ch14 onward, reducing speed of learning for visual topics.
