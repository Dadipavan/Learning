# Audit: study/analyst (Data Analytics)

## Verdict
Strong, consistent, beginner-friendly book (17 chapters plus appendix, about 92k words). Each chapter has intuition boxes, 8-12 worked problems, a recap, a practice set with answers, and AI prompts. Excel, pandas, Power BI/DAX, KPIs/cohorts and A/B testing are good. The big hole is SQL: the site skill map has about 8 SQL-analyst items (window functions, running totals/YoY, sessionization, gaps and islands, top-N per group, median in SQL, date spines, DQ checks as queries, CTE style), but there is no SQL chapter. SELECT appears mainly as DAX SELECTCOLUMNS or in a few ch15/16 snippets, and "OVER (" appears about 10 times in total. Other gaps: forecasting, regression and inference depth (no bootstrap, FDR, or Bayesian), and figures (only ch05, ch07, ch08, ch09 have any, and ch08 has 10). The book is lighter on expert material in ch01, ch04 and ch11. Counts of "worked problems" are class=problem elements; no steps tables exist anywhere.

## Per-chapter table
Ratings: B = beginner clarity, E = expert depth (1-5). Words are text only. "Problems" = class problem count.

| Ch | Title | Words | h2 | Problems | Code | Figs | B | E |
|---|---|---|---|---|---|---|---|---|
| 01 | Analytics mindset and process | 4431 | 8 | 10 | 10 | 0 | 5 | 2 |
| 02 | Excel formulas | 5778 | 9 | 11 | 11 | 0 | 5 | 4 |
| 03 | Excel analysis, Power Query/Pivot | 6513 | 10 | 11 | 16 | 0 | 4 | 4 |
| 04 | pandas I | 4641 | 8 | 11 | 32 | 0 | 5 | 3 |
| 05 | pandas II | 5911 | 9 | 11 | 33 | 2 | 4 | 4 |
| 06 | NumPy and fast pandas | 4191 | 8 | 11 | 29 | 0 | 4 | 3 |
| 07 | EDA | 5940 | 9 | 11 | 28 | 2 | 4 | 4 |
| 08 | Visualization | 4613 | 8 | 9 | 14 | 10 | 5 | 3 |
| 09 | Power BI I (M, modeling) | 4938 | 8 | 9 | 12 | 2 | 4 | 4 |
| 10 | DAX | 4552 | 8 | 10 | 17 | 0 | 4 | 4 |
| 11 | Report design, security, BI tools | 4849 | 8 | 8 | 11 | 0 | 4 | 3 |
| 12 | Business analytics (KPIs, cohorts, RFM) | 6012 | 8 | 11 | 18 | 0 | 4 | 3 |
| 13 | A/B testing | 5040 | 7 | 12 | 20 | 0 | 4 | 4 |
| 14 | Storytelling and communication | 5275 | 8 | 11 | 13 | 0 | 5 | 3 |
| 15 | Capstone and interview bank | 6267 | 8 | 12 | 13 | 0 | 4 | 3 |
| 16 | Project Lab I | 6729 | 7 | 0 | 33 | 0 | 4 | 3 |
| 17 | Project Lab II | 5466 | 6 | 0 | 26 | 0 | 4 | 3 |
| App | Cheat sheet | 1771 | 15 | 0 | 0 | 0 | n/a | n/a |

Notes: ch16 and ch17 are project walkthroughs (no class=problem, practice sets are short). Steps tables: none in any chapter. Callouts: 8-15 per chapter, none in the appendix. Practice sets have answers (details/answer markup present in all chapters).

## Top 12 gaps (ranked by learner value)
1. New chapter "SQL for Analysts" (place after ch03 or ch06): SELECT/WHERE/GROUP BY/HAVING, all JOINs, CTEs, subqueries, CASE, NULL logic, then window functions (ROW_NUMBER/RANK/LAG/LEAD, running totals, moving average, YoY/MoM, top-N per group), median/percentile, date spines, dedupe, pivot/unpivot, DQ checks as queries. 3 examples per concept using the shop data via DuckDB/SQLite. About 6000 words. The skill map covers all of this, and the interview bank (ch15) already assumes it.
2. Sessionization and gaps-and-islands (the new SQL chapter, or ch12 as SQL plus pandas): 30-minute inactivity sessions, consecutive-day streaks, active-user streaks with LAG and a running SUM flag. About 1200 words.
3. Cohort retention, funnels and LTV in SQL (ch12): the same retention table in SQL and pandas, the Excel version, and a simple LTV (ARPU/churn) with a worked comparison. About 1000 words.
4. Regression and inference for analysts (ch07 or a new ch after ch13): simple and multiple regression, interpreting coefficients, R-squared, residual checks, multicollinearity, dummy variables, logistic regression for conversion. The Excel ToolPak, statsmodels and a business reading each get an example. About 2500 words.
5. Resampling and robust methods (ch13 or ch07): bootstrap CI for medians and revenue per user, permutation test, FDR/Benjamini-Hochberg (only Bonferroni exists), Bayesian A/B briefly, ratio-metric delta method, CUPED worked example (only mentioned). About 1800 words.
6. Forecasting basics (new section in ch12 or ch05): naive and seasonal-naive baselines, moving average, exponential smoothing and Holt-Winters, Excel FORECAST.ETS, error metrics (MAE/MAPE/WAPE), backtesting. 3 examples with Excel, pandas and DAX variants. About 1800 words.
7. Causal analysis without an experiment (ch13/15; difference-in-differences is only named in a prompt): DiD worked example, before/after pitfalls, matching idea, regression discontinuity awareness, choosing between observational methods. About 1500 words.
8. Data modeling depth (ch09 or new): SCDs (Type 1/2), snowflake vs star, many-to-many bridge tables, grain definition drills, dbt-style staging layers and testing, incremental refresh, Fabric/Direct Lake/DirectQuery vs Import tradeoffs. About 1800 words. "SCD" and "Fabric" have 0 hits in the book.
9. Figures and steps tables: add about 25-30 SVG diagrams (analysis process flow, metric tree, star schema, filter-context propagation, funnel, cohort heatmap, A/B power curve, CI plot, join Venn/row-count diagrams, pivot/melt reshape) and step-by-step tables for Power BI/Excel click paths. Only 16 figures in the entire book, 10 in ch08. About 5000 words equivalent in captions and steps.
10. DAX and Power BI performance (ch10/11): VertiPaq basics, DAX Studio and Performance Analyzer workflow, variables, avoiding FILTER over a whole table, calculation groups (2 hits), field parameters with an example, dynamic segmentation, semi-additive measures (closing balance), ranking ties, many-to-many. 3 examples per pattern. About 2000 words.
11. Advanced pandas (ch04-06): MultiIndex deep dive (1 hit in ch04), window and groupby transform recipes, method chaining and pipe, merge validation and merge_asof with timezones, nullable and pyarrow dtypes, Copy-on-Write behaviour in pandas 3, testing data with pandera or assert-style checks, and a profiling workflow on a 5M-row file. About 2200 words.
12. Analytical engineering and real-world workflow (ch01/ch14/appendix): data-quality contracts, metric definitions/semantic layers, git workflow for analysts, notebooks vs scripts, scheduling, and a worked "metric disagrees between two dashboards" investigation. About 1500 words. Also add an expert section in ch01 (root-cause trees, Simpson's paradox, survivorship bias, Shapley and mix/rate decomposition of 3+ factors; only the 2-factor split is shown).

Total estimated additions: about 30,000 words plus 25-30 figures.

## Other observations
- Varied-example rule (3 per concept): met in ch02, ch04, ch05, ch10 and ch12 for most concepts; weaker for ch11 (8 problems for 5 big sections), ch09 (9 problems, 5 sections including M language), ch08 (9 problems across 3 libraries), ch13 (sample size and power have fewer variants).
- ch16/ch17 have no practice problems with answers (only project steps and a short practice set); add extension tasks with expected outputs.
- Tableau/Looker Studio are only a section in ch11 (no worked example); consider a Tableau LOD (FIXED/INCLUDE/EXCLUDE) comparison to DAX CALCULATE.
- Skill map items not found at all in the book: gaps and islands, sessionization, LAG/LEAD, Altair (one mention only), Dash (not covered in depth), bootstrap, BH-FDR.

## Errors found
- No hard technical errors verified in the sampled sections. The pandas 3.0.6 notes (applymap renamed to map in 2.1, Copy-on-Write, string dtype) are consistent with current pandas.
- Wording to check: ch05 states `applymap` was "renamed" in 2.1; it was deprecated in 2.1 (alias still existed through 2.x), and is removed in pandas 3.0. Suggest "deprecated in 2.1, removed in 3.0".
- Claim style: ch10 says DAX is "not run here" and that numbers were computed with pandas. That is honest but unverifiable by the learner; add a small downloadable sample .pbix or CSV with expected values.
- Not checked in detail: every numeric output in the 17 chapters. Only intros, one middle section and the ends of ch01, ch10, ch13, ch16 were read; the others were assessed by structure and keyword counts.
