# Audit: study/stats (Statistics), ch01-ch15 + appendix

## Verdict
Strong, simulation-verified, problem-first course with a consistent template (intuition, worked problem, steps table, code, callouts, recap, practice set with answers, prompt pack). Ch01-06 are dense (22-24 worked problems each) and close to professional level. Ch07-14 thin out sharply (7-19 problems, 4-5k words) and ch11-14 have no figures. Missing vs a professional syllabus: A/B-testing practice (CUPED, sequential tests, SRM beyond one example), mixed models and Cox in depth, GLM extensions (ordinal/multinomial/zero-inflated), time-series beyond ARIMA (GARCH, state-space, hierarchical forecasting), Bayesian model checking/Bayes factors, causal inference (propensity, synthetic control, IV only mentioned). Several key tools are marked "not run here" (lifelines, statsmodels, PyMC), so those examples are unverified. Practice sets exist everywhere with answers (4-8 each, short numeric); they are a bit few for "perfect" mastery. Intro assumes the "Math PDF" (does not start fully from zero, by design).

## Per-chapter table (words, worked problems = class "problem", code = pre blocks, figures = svg/img)
| Ch | Topic | Words | Problems | Code | Figs | Practice Qs | Beginner 1-5 | Expert 1-5 |
|---|---|---|---|---|---|---|---|---|
| 01 | Probability, Bayes, descriptive | 7425 | 23 | 32 | 2 | ~6 | 4 | 3 |
| 02 | Distributions | 7638 | 24 | 38 | 2 | ~6 | 4 | 4 |
| 03 | Sampling, MLE, CI, bootstrap | 7497 | 22 | 34 | 4 | ~6 | 4 | 4 |
| 04 | Hypothesis testing | 8674 | 23 | 37 | 2 | 8 | 4 | 4 |
| 05 | Effect size, multiple testing, p-hacking | 6774 | 21 | 29 | 2 | ~6 | 4 | 4 |
| 06 | Linear regression | 9379 | 22 | 36 | 4 | 8 | 4 | 4 |
| 07 | Regularization, CV, AIC/BIC | 5022 | 9 | 12 | 2 | ~6 | 3 | 3 |
| 08 | GLMs | 4555 | 7 | 8 | 2 | 6 | 3 | 3 |
| 09 | Bayesian | 5418 | 10 | 10 | 2 | ~6 | 3 | 3 |
| 10 | Time series | 5936 | 14 | 8 | 2 | 7+ | 3 | 3 |
| 11 | Survival + mixed models | 4831 | 17 | 18 | 0 | ~6 | 3 | 2 |
| 12 | Causal inference/experiments | 3928 | 15 | 15 | 0 | 6 | 3 | 2 |
| 13 | Optimization + info theory | 5428 | 19 | 16 | 0 | 7 | 3 | 3 |
| 14 | Interview bank and pitfalls | 4234 | 19 | 13 | 0 | ~4 | 4 | 3 |
| 15 | Projects | 7520 | 0 | 27 | 0 | ~4 | 3 | 3 |
| App | Appendix (chapter notes) | 1554 | 0 | 0 | 0 | 0 | - | - |

Figures are PNGs in images/ (ch01-ch10 only). Callouts 8-18 per chapter (ch15: 1).

## Top 12 gaps (ranked by learner value)
1. Ch12 (+Ch05): Applied A/B testing toolkit: CUPED variance reduction, sequential testing / alpha spending (mSPRT), SRM diagnosis flow, novelty effects, ratio metrics with delta method, network interference. Examples: CUPED on simulated sessions (variance cut ~30%), peeking simulation vs O'Brien-Fleming, ratio-metric CI via delta method vs bootstrap. ~2000 words.
2. Ch12: Observational causal methods worked end to end: propensity scores (matching, IPW, balance table), synthetic control, regression discontinuity, IV (2SLS) with simulated truth; DAGs, colliders and backdoor criterion. ~2500 words.
3. Ch11: Mixed-effects models in depth: random intercept vs slope, ICC, shrinkage plot, GEE, and Cox PH assumption checks (Schoenfeld), time-varying covariates, competing risks. Needs figures (KM curve, shrinkage). Run the examples (lifelines/statsmodels currently "not run here"). ~2500 words.
4. Ch08: GLM extensions: multinomial and ordinal logistic, zero-inflated/hurdle, offsets/exposure for rates, quasi-Poisson, logistic diagnostics (ROC/AUC, calibration, Hosmer-Lemeshow, separation). Examples: ticket counts per day with exposure; 3-class churn reason. ~2000 words.
5. Ch10: Time series beyond ARIMA: ETS state-space taxonomy, ARIMAX/regression with ARMA errors, GARCH volatility (GARCH mentioned only in ch10), prediction intervals, rolling-origin CV with worked numbers, hierarchical forecasting and intermittent demand (Croston). Add residual diagnostics (Ljung-Box) figure. ~2200 words.
6. Ch09: Bayesian workflow: prior predictive and posterior predictive checks, Bayes factors (none in doc), hierarchical Bayesian model (partial pooling, ties to ch11), MCMC diagnostics (R-hat, ESS, divergences), runnable PyMC example. ~2000 words.
7. Ch07: Regularization depth: nested CV and data leakage, bias-variance simulation figure, elastic net path plot, one-standard-error rule, calibration of model selection with more than 3 worked examples (only 9 problems). ~1500 words.
8. All chapters 07-14: add 4-6 more graded practice problems each (medium/hard, multi-step, real-data style) plus a chapter quiz; current sets are 4-8 short numeric items. ~500 words per chapter.
9. Ch11, 12, 13, 14, 15: add figures (none). Priority: KM curves, shrinkage plot, DiD parallel trends, confounding scatter, gradient-descent contours, optimizer comparison. 6-8 figures.
10. Ch06 (+Ch08): Regression extensions: robust/HC standard errors, WLS, quantile regression, interactions and polynomial/splines (GAMs), heteroscedasticity fixes, prediction vs confidence interval comparison. ~2000 words.
11. Ch04/05: Equivalence and non-inferiority tests (TOST), exact tests (Fisher, binomial) worked, repeated-measures/two-way ANOVA and interaction, Kruskal-Wallis follow-up (Dunn), assumption tests (Levene appears only in ch04). ~1800 words.
12. Ch01-02: Multivariate and advanced probability: MGFs, transformations of RVs, multivariate normal/covariance geometry, Markov chains basics, extreme value, mixture models/EM. Also a clean from-zero "Notation and symbols" opener since ch01 defers to the Math PDF. ~2000 words.

Also noted: ch15 projects have no steps tables or problems and only 1 callout (add checkpoints and expected outputs, ~800 words); appendix is only notes (1554 words), no glossary or formula sheet (add one-page formula sheet and glossary, ~1200 words). Site skill map (index.html const D) lists stats items such as t-tests, chi-square, normality tests, Mann-Whitney, ANOVA, correlation, A/B testing, survival, time series; all are covered at some level, but power/A-B practice and Bayesian A/B are the weakest versus how often the map demands them.

## Errors / issues found (verified by hand recalculation)
Checked and correct: 4.7.1 (p=0.0099), 4.7.2 (t=1, p~0.32), 4.7.4 (F=6, p~0.007), 4.7.5 (chi2=3.333, p=0.189), 12.6.2 (chi2=18), 12.6.3 (~1,094 per group, within rounding of the standard 1,091 unpooled formula), 12.6.4 (DiD -7), 8 Q6 (OR 3 at 40% gives 66.7%), 10 Q6 (RMSE 4.30, MAPE 6.81).
Issues:
- Problem numbering inconsistent: ch04 practice labelled 4.7.x and ch12 12.6.x while sections end at 4.6/12.5 (counting recap as a section); ch08/ch10 use plain numbers. Harmonize.
- ch06, 08, 09, 10, 11, 13, 15 contain "not run here" code (28 occurrences, ch11 has 7): contradicts the "every number was computed" claim; install the libraries and run, or flag clearly.
- ch11 says lifelines/statsmodels were not installed when written; code for Cox and mixed models is unverified.
- Ch01 intro says "we do not repeat from zero" (relies on external Math PDF), so beginner-clarity is 4 not 5.
- "Mann-Whitney is about 95 percent as efficient as t" (ch04): true only asymptotically under normality (ARE 3/pi = 0.955); add that qualifier.
- No outdated claims spotted otherwise; I did not exhaustively verify all code outputs.

Recommended additions: 12 (listed above).
