# Audit: study/ds (Data Science in Practice)

## Verdict
Strong, applied and unusually honest course (16 chapters plus appendix, about 5.2k to 8.1k words each, ~97k total). Every chapter uses a running example, a plain-words intro, "Words you need" tables, runnable verified code, "Connection to the real job" and "Applications" blocks, and a practice set with inline answers. Beginner clarity is high. Weaknesses: (a) worked-problem density falls sharply after ch07 (ch08 to ch13 have 4 to 12 worked problems for 5 to 7 major concepts, so many concepts get one example, not three); (b) almost no figures (only 6 visuals in the whole document: ch01 x2, ch03 x2, ch09 x2); (c) several expert topics are only named, not taught (CATE/causal forests, ratio metrics and delta method, interference and switchback, hierarchical forecasting, survival for churn, conformal intervals, mixed models, CausalImpact/BSTS); (d) ch15 and ch16 are project scaffolds (0 worked problems, 0 steps tables, 0 to 2 callouts) rather than teaching chapters. No hard technical errors found in the sections I checked.

## Per chapter (words, worked problems = class problem, code blocks = pre, figures = svg/img; ratings 1-5: B = beginner clarity, E = expert depth)
| Ch | Topic | Words | h2 | Worked | Steps tbl | Code | Callouts | Figs | Practice | B | E |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Role, lifecycle, framing, baselines | 5927 | 7 | 18 | 8 | 16 | 10 | 2 | yes | 5 | 3 |
| 2 | Data collection, point-in-time, quality, labels, privacy | 5897 | 7 | 19 | 5 | 19 | 8 | 0 | yes | 5 | 4 |
| 3 | EDA for modelling | 5203 | 7 | 18 | 8 | 26 | 8 | 2 | yes | 5 | 4 |
| 4 | Statistical thinking, pitfalls | 5375 | 7 | 19 | 8 | 23 | 8 | 0 | yes | 5 | 3 |
| 5 | Feature engineering I | 6168 | 7 | 17 | 4 | 32 | 8 | 0 | yes | 5 | 4 |
| 6 | Feature engineering II, leakage-safe pipelines | 6574 | 7 | 18 | 12 | 27 | 8 | 0 | yes | 4 | 4 |
| 7 | A/B testing | 5615 | 7 | 10 | 7 | 14 | 9 | 0 | yes (answers) | 5 | 3 |
| 8 | Causal inference | 6268 | 10 | 8 | 4 | 21 | 14 | 0 | yes | 4 | 3 |
| 9 | Forecasting | 5723 | 7 | 8 | 6 | 12 | 8 | 2 | yes | 4 | 3 |
| 10 | Recommendation, ranking, search | 5381 | 7 | 8 | 6 | 12 | 8 | 0 | yes | 4 | 3 |
| 11 | Applied domains (7 domains in one chapter) | 8098 | 9 | 12 | 11 | 30 | 12 | 0 | yes | 4 | 3 |
| 12 | Decisions, optimisation, simulation | 6290 | 7 | 4 | 3 | 24 | 8 | 0 | yes | 4 | 3 |
| 13 | Communication, ethics, repro, production | 6251 | 8 | 5 | 6 | 24 | 10 | 0 | yes (10) | 4 | 3 |
| 14 | Capstones and interview bank | 7197 | 8 | 12 | 12 | 7 | 10 | 0 | yes | 4 | 4 |
| 15 | Project Lab 1 | 5420 | 7 | 0 | 0 | 17 | 2 | 0 | yes | 3 | 2 |
| 16 | Project Lab 2 | 5338 | 6 | 0 | 0 | 14 | 0 | 0 | yes | 3 | 2 |
| App | Cheat sheet | 2239 | 15 | 0 | 1 | 1 | 0 | 0 | n/a | 4 | 3 |

Practice sets have answers inline (checked ch07, ch08, ch12, ch15), graded easy/medium/hard. Good.

## Top 12 gaps (ranked by learner value)
1. Ch11 (split into ch11a/b): seven domains in 8k words, one worked example each. Add survival analysis for churn (Kaplan-Meier, Cox, discrete-time hazard on a non-contractual retailer), CLV with BG/NBD plus Gamma-Gamma, fraud with rare-event cost curves and graph features, scorecard reject inference. 3 worked examples per domain. ~3,500 words.
2. Ch07: advanced experimentation. Ratio metrics and the delta method (CTR, revenue per session with user-level clustering), interference and network effects (switchback, cluster randomisation, geo experiments), variance reduction beyond CUPED (stratification, regression adjustment), multiple metrics (guardrails, Benjamini-Hochberg), power for non-binary metrics, long-term holdouts, novelty/primacy. Worked: 3 sample-size calculations (binary, continuous, ratio), mSPRT/alpha-spending. ~2,200 words.
3. Ch08: heterogeneous effects and modern causal ML. Meta-learners (S/T/X) coded on one dataset, causal forest, double ML, Qini curve evaluation, CausalImpact/BSTS, staggered DiD pitfalls (TWFE bias), sensitivity analysis (E-value), IV/RD each with 3 examples. Currently 8 worked problems for 7 methods. ~2,500 words.
4. Ch09: forecasting depth. Hierarchical reconciliation (bottom-up, MinT), intermittent demand (Croston, TSB), conformal and quantile intervals, probabilistic metrics (pinball, CRPS), Prophet/ETS/ARIMA comparison on same series, rolling-origin backtests with 3 datasets (trend, seasonal, intermittent). ~2,000 words.
5. Figures across the document (only 6 total): add about 25 SVGs. Priority: DAG patterns (confounder, mediator, collider), power curve, SRM and peeking simulation, DiD parallel trends, RD discontinuity plot, ACF plots, lift/gain and calibration curves, ROC with cost line, MF latent factors, two-stage funnel. ~1,500 words captions plus SVG code.
6. Ch15 and ch16: add worked solutions. Include a full reference solution skeleton with expected metric ranges, checkpoints, and a rubric per project; at least 3 worked debugging problems each (leaky split, SRM bug, wrong NDCG). Convert the generic "How to run a project" boilerplate (same text in both) into project-specific content. ~2,500 words.
7. Ch10: ranking depth. Implicit ALS vs BPR, two-tower retrieval with in-batch negatives and ANN (FAISS/HNSW), LambdaMART, counterfactual evaluation (IPS, doubly robust, off-policy), bandits for recsys, diversity/novelty metrics. Worked: NDCG, MAP, MRR by hand on three lists. ~2,200 words.
8. Ch04: statistical foundations beyond the pitfalls. Hypothesis-test choice map (t, Mann-Whitney, permutation), bootstrap CIs on a median and on a ratio, Bayesian updating with Beta-Binomial and hierarchical shrinkage, multiple testing corrections (FDR), power. Add 3 examples for each. Cross-link stats/ch10 and stats/ch11 (mixed models). ~1,800 words.
9. Ch12: decisions. Integer programming (knapsack, assignment, MIP with PuLP/OR-Tools), robust and stochastic optimisation, newsvendor with quantile forecasts, contextual bandits and off-policy, Markov decision basics. Only 4 worked problems today. ~2,200 words.
10. Ch13: production depth. Data and concept drift (PSI, KS, CUSUM) with a worked monitor, shadow and canary deploys, model cards, fairness metrics (demographic parity, equalised odds, calibration across groups) worked on one dataset with the impossibility result, feature store, testing data pipelines. Only 5 worked problems. ~2,000 words.
11. Ch05 and ch06: modelling bridge. Chapters teach features but there is no chapter on model choice and tuning (GBM vs linear baselines, imbalance handling, calibration, SHAP) inside DS; add a short bridge chapter or explicit links to ml/ch08-ch10, with one end-to-end worked example. Also embeddings and text features beyond TF-IDF, time-based target encoding. ~2,000 words.
12. Ch01-ch03 and ch14: advanced scenario content. Add data-science case-study rehearsal (metric design, metric trees, north-star vs guardrails, define-the-ask exercises), SQL-for-DS cross-links, and a "senior DS" section (scoping, ROI estimation, build-vs-buy). Expand interview bank with 30 more questions with model answers (experimentation, causal, ML system design). ~2,500 words.

Total recommended additions: 12 (about 28,000 words plus about 25 figures).

## Errors and issues found
- No numeric errors found in checks: ch07 rule of thumb n = 16 p(1-p)/d^2 (6,400 and 3,600 correct), pooled z = 2.02, unpooled CI 0.06 to 3.94 points, ch12 M/M/1 times 0.8 h and 4.0 h, ch15 SRM chi-square 36, CUPED rho^2 = 0.49, 22.6% false alarm for 5 looks at 0.05: all verified.
- Minor: ch07 and ch15 repeat the 16 p(1-p)/d^2 rule without stating it assumes alpha 0.05 two-sided and 80% power (state it, plus a note for one-sided and other powers).
- Minor: ch15 practice 5 uses "independent looks" 1-0.95^5; real sequential looks are positively correlated so the true inflation is lower (about 14% for 5 equally spaced looks); the text should say the 22.6% is an upper bound.
- Structure: ch15 and ch16 repeat identical boilerplate subsections (repo layout, README template, LinkedIn post) and have no worked problems, so they inflate word counts without teaching.
- Site map: index.html has ds:* skill items on survival analysis for churn, conformal intervals, uplift meta-learners and causal forests, interference/network effects, and geospatial (geopandas, h3); the ds chapters touch these only in passing (not covered in depth: BSTS/CausalImpact 0 mentions, mixed models 0, geospatial minimal).
