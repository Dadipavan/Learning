# Audit: study/sql (SQL & Databases Mastery)

## Verdict
A strong, consistent, runnable-example textbook (about 95k words, 16 chapters plus a cheat-sheet appendix, 350+ worked problems, 15 chapters with answer-bearing practice sets and prompt packs). It starts from zero (ch01 opens with an app analogy, then installs SQLite/PostgreSQL) and covers the standard analyst-to-intermediate-engineer syllabus well: joins, CTEs, windows, gaps and islands, indexes/EXPLAIN, normalization, star schema, SCD, analytics patterns, dialects. Weaknesses are (a) almost zero visuals (only 4 SVG/figures in the whole book, none for join Venn/fan-out, window frames, B-tree, isolation anomalies, plan trees); (b) expert/DBA/security material missing (SQL injection, GRANT/roles/RLS, stored procedures/triggers, partitioning, locking patterns such as SKIP LOCKED, plan-node internals); (c) ch15/ch16 projects and ch13 are lighter on varied worked examples per concept; (d) small cross-reference issues. Measurements are regex-based (bs4 not installed); "callouts" is a loose class match.

## Per-chapter table
Ratings 1-5: B = beginner clarity, E = expert depth.

| Ch | Topic | Words | h2 | Worked problems | Steps tables | Code blocks | Figures | B | E |
|---|---|---|---|---|---|---|---|---|---|
| 01 | Databases, relational model | 3928 | 7 | 18 | 7 | 31 | 0 | 5 | 2 |
| 02 | SELECT/WHERE/NULL | 4862 | 7 | 24 | 7 | 70 | 0 | 5 | 3 |
| 03 | Aggregation/GROUP BY/FILTER | 4183 | 7 | 22 | 5 | 50 | 0 | 5 | 3 |
| 04 | Joins | 6203 | 7 | 26 | 11 | 73 | 2 | 5 | 4 |
| 05 | Subqueries, CTEs, recursive | 5259 | 7 | 23 | 8 | 58 | 0 | 4 | 4 |
| 06 | CASE, strings, dates, JSON | 5745 | 7 | 27 | 4 | 63 | 0 | 4 | 3 |
| 07 | Sets, pivot, ROLLUP/CUBE | 4974 | 6 | 21 | 5 | 51 | 0 | 4 | 3 |
| 08 | Window functions | 7866 | 8 | 29 | 8 | 68 | 2 | 4 | 5 |
| 09 | DDL/DML/transactions | 5676 | 7 | 16 | 0 | 31 | 0 | 4 | 3 |
| 10 | Indexes, EXPLAIN, optimization | 5807 | 7 | 21 | 0 | 33 | 0 | 4 | 3 |
| 11 | Schema design, warehouse modeling | 5768 | 8 | 18 | 3 | 33 | 0 | 4 | 3 |
| 12 | Analytics patterns | 6551 | 9 | 28 | 2 | 50 | 0 | 4 | 4 |
| 13 | Beyond SQL (NoSQL, CAP) | 6271 | 10 | 26 | 3 | 40 | 0 | 4 | 3 |
| 14 | Dialects + 40-problem bank | 5797 | 8 | 59 | 1 | 25 | 0 | 4 | 3 |
| 15 | Project lab 1 | 6302 | 7 | 8 | 0 | 38 | 0 | 3 | 3 |
| 16 | Project lab 2 | 4656 | 5 | 8 | 0 | 25 | 0 | 3 | 3 |
| App | Cheat sheet | 1933 | 15 | 0 | 0 | 0 | 0 | 4 | 2 |

Observations: ch09, ch10 (the most conceptual non-query chapters) have 0 steps tables and only 31-33 code blocks and 16-21 problems; ch09 is the thinnest worked-example chapter. Visuals: ch04 (2), ch08 (2), rest none. Practice sets mix easy/computation/find-the-bug/what-is-output with inline answers (good); ch15/16 practice has only 2 mentions.

## Top 12 gaps (ranked by learner value)
1. ch04 + ch08 + ch10: visuals. Add SVG: join Venn/row-matching diagram plus fan-out picture (ch04), window frame ROWS vs RANGE vs GROUPS diagram on a 7-row table (ch08), B-tree lookup and covering index diagram, annotated EXPLAIN plan tree (ch10). About 8-10 figures, 600 words of captions.
2. ch09: transaction anomaly lab. Step-by-step two-session timelines for dirty read, non-repeatable read, phantom, lost update, write skew, with which isolation level prevents each (Postgres vs MySQL InnoDB), plus deadlock reproduction and retry loop, SELECT ... FOR UPDATE / SKIP LOCKED job-queue example. About 1200 words, 5 examples.
3. NEW (ch09 or ch11): Security and access control. SQL injection with a vulnerable vs parameterized query (Python psycopg/sqlite3 placeholders), GRANT/REVOKE and roles, least privilege, row-level security in Postgres, views as access filters. Skill map lists "SQL injection and parameterized queries" and nothing in the book covers it. About 1000 words.
4. ch10: advanced performance. Join algorithms (nested loop/hash/merge) each with an EXPLAIN example, statistics/ANALYZE and bad row estimates, sargability set (5 rewrites), index types (B-tree, hash, GIN, BRIN, GiST), table partitioning (RANGE by month) with partition pruning, N+1 and pagination (keyset vs OFFSET), pg_stat_statements. Currently BRIN, partitioned tables are absent. About 1500 words.
5. ch09: programmability. Views and materialized views refresh, stored functions/procedures, triggers (audit-log trigger example), sequences/identity, generated columns, MERGE (SQL standard) beyond ON CONFLICT. About 1200 words, 4 examples.
6. ch07: PIVOT/UNPIVOT native syntax (SQL Server/Snowflake/Oracle), crosstab/tablefunc in Postgres, dynamic pivot, plus 2 more ROLLUP/CUBE/GROUPING() reporting examples. About 700 words.
7. ch05/ch12: advanced patterns library. Top-N per group via LATERAL, graph shortest path/cycle detection in recursive CTE (with depth limit), bill-of-materials explosion, median/percentiles, interval overlap and merge, running distinct counts, temporal joins / as-of joins, relational division. 6 examples, about 1500 words.
8. ch15/ch16: more worked material. Only 8 problems each; add a fully worked end-to-end walkthrough (schema, load, 10 queries with outputs, findings write-up) per project and a rubric/solutions for the practice sets. About 1500 words.
9. ch02: NULL-safe comparison (IS DISTINCT FROM), NULLS FIRST/LAST, collation and case sensitivity, type coercion traps (text vs number in SQLite). `DISTINCT FROM` appears only in ch02 and NULLS FIRST nowhere. 3 examples, about 500 words.
10. ch13: depth on NoSQL beyond definitions. For each store, 3 realistic modeling examples (embed vs reference in Mongo with queries, Redis TTL/cache-aside/rate limiter, Cassandra partition-key design for a time-series, Cypher friends-of-friends), a SQL-vs-NoSQL decision table, transactions/consistency worked timeline. About 1500 words.
11. ch11: modeling extras. Worked BCNF/4NF decomposition with functional-dependency closure, many-to-many/self-referencing/polymorphic patterns, surrogate vs natural keys, soft delete, multi-tenant design, data vault awareness, dbt/ELT layering link (skill map links dbt chapter). About 1200 words.
12. ch14 + appendix: dialect breadth and cheat sheet. Add Oracle and a MySQL/Postgres/SQL Server/BigQuery/Snowflake side-by-side table for 15 common tasks (date trunc, string agg, upsert, top-N, QUALIFY, pivot), DuckDB/Spark SQL notes, and extend appendix with isolation-level, index and EXPLAIN cheat rows. About 900 words.

Total recommended additions: 12 (about 13,000-14,000 words, roughly 14% growth, plus 10+ figures).

## Skill-map comparison (index.html const D)
Covered: CTE/recursive, EXPLAIN, ACID/isolation/MVCC/deadlocks, ER/normalization, dialects (MySQL, SQL Server, BigQuery, Snowflake), NoSQL list, windows, sessionization, gaps/islands. Missing or thin: SQL injection/parameterized queries, Oracle differences, NewSQL/distributed SQL awareness (CockroachDB, Spanner), partitioning/clustering for warehouses, query engines (Trino, ClickHouse, DuckDB), point-in-time-correct training sets (add to ch12), percentile/median is only in ch08 (add a dedicated example), "readable reusable SQL" style/linting guidance (only partially).

## Errors / issues found (verified by reading or grep)
- No factual SQL errors found in sampled sections (ch01, ch04, ch09, ch10, ch14 practice answers checked; ch09 P.3 claim that SQLite evaluates 'refunded' as 0/false is correct; ch14 claim that MySQL gained CTEs/windows in 8.0 is correct; BigQuery 3 x 5% of 400 GB = 60 GB is correct). Full query outputs were not re-executed, so numeric outputs are unverified.
- Cross-reference inconsistency: the tracker (index.html) sends Projects #62-64 to "Chapter 15" and has "Build Project #63: 20-question case study", but that case study lives in ch16 (and the tracker has no reading task for ch16 in D). Fix link text or add a ch16 read task.
- ch15/ch16 practice-set headings are present, but the chapters have 0 callouts (ch16) and 1 (ch15), unlike the rest; pedagogy format is inconsistent.
- ch09 and ch10 have no steps tables, unlike ch01-08, so tracing of transaction and plan execution is prose only.
- Tracker also omits ch15/ch16 and appendix from the "Read" tasks (only ch01-ch14 appear); verify.
- Version-sensitive: windows/CTE note for MySQL is fine for 2026 but "older servers" phrasing is dated; mention MySQL 8.4 LTS, PostgreSQL 17/18 features (MERGE with RETURNING, SQL/JSON JSON_TABLE) if the owner wants current coverage. Not asserted as an error.

## Strongest / weakest
Strongest: ch08 (windows), ch04 (joins). Weakest: ch09 (thin, no steps, no security/programmability), ch16 and ch15 (few worked examples, no visuals), ch10 close behind (conceptual depth without figures or plan-node coverage).
