# Audit: study/de (Data Engineering)

Method: regex measurement of all ch01-ch16 and appendix HTML, plus sampled reading of intros, practice sets and targeted claim greps. Counts come from tag and class matches: "worked" = class problem, "steps" = steps tables. No bs4 was available, so words exclude script, style and svg.

## Verdict
The document is strong for a beginner. It uses one running example (ShopKart), an analogy for each concept, and a labelled "not run here" policy for tools that were not installed. Every chapter 1-14 has recap, practice, prompt pack and an answers block. Practice answers are numerically correct in the samples checked (ch03, ch07, ch10). It is thinnest in three places. First, expert depth: there are no Spark Structured Streaming internals, no table-format internals (Z-order, liquid clustering, deletion vectors), and little on cloud-specific tuning. Second, the whole "I. Python for Data Engineering" section of the site skill map has no chapter. Third, ch15-16 are project labs with zero worked problems, practice items or figures. Figures are scarce: 12 inline SVG or img in total, and ch05, ch07, ch08, ch10, ch12 and ch14 have none. Roughly 3 or more varied worked examples per concept is met in ch01-06 and ch11-14, but not in ch07-ch10. Those four have only 4-6 problems for 3 sections, and the dbt, Spark and warehouse chapters rely on "not run here" snippets.

## Per-chapter table
Beginner = beginner-clarity, Expert = expert-depth, both rated 1-5. "Prac" = practice items I could not count exactly; every ch01-14 has a practice set with answers (about 10-15 each).

| Ch | Topic | Words | h2 | Worked | Code | Callouts | Figures | Beginner | Expert |
|---|---|---|---|---|---|---|---|---|---|
| 01 | Lifecycle, architectures | 5063 | 7 | 7 | 10 | 9 | 2 | 5 | 3 |
| 02 | Data modeling | 4496 | 6 | 6 | 17 | 6 | 1 | 5 | 3 |
| 03 | File formats, table formats | 5831 | 7 | 8 | 18 | 9 | 1 | 5 | 4 |
| 04 | Ingestion, CDC | 4827 | 6 | 6 | 16 | 6 | 1 | 5 | 3 |
| 05 | Quality and testing | 4336 | 6 | 6 | 14 | 7 | 0 | 5 | 3 |
| 06 | Orchestration (Airflow) | 4783 | 6 | 6 | 12 | 6 | 1 | 5 | 3 |
| 07 | dbt | 4928 | 6 | 4 | 22 | 7 | 0 | 4 | 3 |
| 08 | Warehouses, cloud map | 4823 | 6 | 5 | 9 | 7 | 0 | 4 | 2 |
| 09 | Spark I | 5278 | 6 | 4 | 17 | 7 | 1 | 4 | 3 |
| 10 | Spark II performance | 5563 | 6 | 6 | 10 | 8 | 0 | 4 | 4 |
| 11 | Streaming, Kafka | 6894 | 6 | 9 | 20 | 9 | 3 | 4 | 4 |
| 12 | Infra, DataOps, governance | 6037 | 7 | 9 | 17 | 12 | 0 | 4 | 3 |
| 13 | System design | 5606 | 6 | 9 | 14 | 7 | 1 | 4 | 4 |
| 14 | Performance, capacity, interview | 6437 | 7 | 10 | 13 | 7 | 0 | 4 | 4 |
| 15 | Project lab 1 | 6322 | 9 | 0 | 28 | 2 | 0 | 4 | 3 |
| 16 | Project lab 2 | 4753 | 7 | 0 | 19 | 0 | 0 | 4 | 3 |
| App | Appendix (per-chapter notes) | 1824 | 15 | 0 | 0 | 0 | 0 | 3 | 2 |

Total about 82k words and 12 figures. That is about 1 figure per 7k words, very low for a visual topic (pipelines, DAGs, shuffles and Kafka partitions all draw well).

## Skill-map comparison (index.html const D, domain "de")
Sections A-H and J, M and N are covered by ch01-14.
- Section I, "Python for Data Engineering", has 0 items and no chapter. Greps found no asyncio, no type hints, and pandas only in passing. Pydantic appears once in ch04.
- Section K, "Cloud data services", has 0 items. ch08.3 gives only a concept-level map.
- Section E, Orchestration, has only 3 items, so there is little to compare with.
- Not covered at all: Dask, bloom filters, Photon, SQLMesh, a metric layer, Spark `foreachBatch`, and Z-order or liquid clustering.

## TOP 12 gaps (ranked by learner value)
1. **New chapter: Python for Data Engineering** (new ch, about 3,500 words). Cover:
   - generators and iterators for chunked file reads;
   - type hints, dataclasses and pydantic for contracts;
   - `requests` retries with backoff, and `asyncio` and thread pools for API pulls;
   - pandas memory (dtypes, chunksize), then Polars and DuckDB as single-node engines;
   - pytest fixtures for pipelines, logging, config, and packaging a pipeline as a module.
   Give 3 examples each: a 10 GB CSV in 100 MB chunks, async pagination of 500 pages, and an idempotent loader function.
2. **ch07 dbt: more worked examples** (about 1,500 words). Add:
   - three incremental strategies compared on one dataset (append, merge, delete+insert, with microbatch noted);
   - a snapshot walked through SCD2 step by step;
   - a Jinja macro with loop and conditional, a custom generic test, and `dbt build` selectors with state (`state:modified+`);
   - a diagram of the DAG with `ref` resolution.
3. **ch09/10 Spark: Structured Streaming and AQE in depth** (about 2,000 words).
   - Cover `foreachBatch` idempotent upserts, checkpoint contents, state store size, and `applyInPandas`/`mapInPandas`.
   - Walk AQE through its three features on one query: coalesce partitions, skew-join splitting, and dynamic join switching.
   - Add a worked "read the Spark UI" exercise using screenshots or SVGs of stage and task timelines.
4. **ch08 Warehouses: concrete engine tuning, three worked examples each for BigQuery, Snowflake and Redshift** (about 2,000 words).
   - Cover clustering vs partitioning, micro-partition pruning, slot or credit cost arithmetic, result caching, materialized views, and workload isolation.
   - Add a "cost of this query before and after" example for each warehouse, and a common-pitfalls list (SELECT *, cross joins, bad join order).
5. **ch03 Table-format internals for experts** (about 1,500 words).
   - Cover Iceberg metadata trees (manifest list, manifest, data file), Delta transaction log JSON and checkpoints, and Hudi copy-on-write vs merge-on-read.
   - Add Z-order, liquid clustering and deletion vectors, and schema and partition evolution (Iceberg hidden partitioning).
   - Add a small simulation of snapshot isolation with two writers conflicting.
6. **Figures sweep** (8-12 SVGs, about 800 words of captions). Needed in ch05 (check pipeline with quarantine), ch07 (DAG lineage), ch08 (compute and storage separation), ch10 (shuffle and skew with salting), ch12 (CI/CD flow), ch14 (Little's Law queue), and ch09 (stage DAG).
7. **ch11 Streaming: end-to-end exactly-once recipe** (about 1,200 words).
   - Walk one transactional pipeline: Kafka producer idempotence + transactions, consume-transform-produce, and a sink with idempotent upsert.
   - Add a failure-injection table (crash before commit, after commit, rebalance).
   - Add stream-stream and stream-table joins with state TTL, and late-data handling with side outputs.
8. **ch15-16: add practice sets with answers and stretch tasks** (about 1,200 words). These labs have zero worked problems or practice items. Add 10 checks per lab, plus a "break it on purpose and diagnose" exercise and expected output hashes.
9. **ch06 Orchestration: Airflow production patterns** (about 1,500 words).
   - Cover sensors vs deferrable operators, dynamic task mapping, datasets and assets, pools, SLAs, retries with idempotent tasks, and a backfill exercise with `logical_date`.
   - Walk through 3 failure diagnoses.
   - Add a short Dagster or Prefect comparison with the same pipeline in each.
10. **ch12 Governance and security depth** (about 1,500 words).
   - Cover RBAC and ABAC, column masking and row-level policies, secrets management, encryption at rest and in transit, and tokenization for PII.
   - Cover GDPR deletion in lakehouse formats (rewrite files, then vacuum), retention policies and lineage with OpenLineage. Give 3 worked cases, e.g. a right-to-erasure request in an Iceberg table.
11. **ch02 Modeling for experts** (about 1,200 words).
   - Add worked examples for bridge tables and many-to-many, junk, degenerate and role-playing dimensions, factless and accumulating snapshot facts, and late-arriving dimensions.
   - Add Data Vault loads with hash keys, and a semantic or metric layer (measure definitions, additivity).
12. **ch04/05 CDC and observability** (about 1,500 words).
   - CDC: Debezium log-based capture end to end, including the outbox pattern, tombstones, schema evolution, an initial snapshot and ordering guarantees; and a backfill plan that keeps idempotent merges correct.
   - Observability: data SLOs, anomaly detection on volume and freshness using z-score or seasonality, and incident write-up templates.

Total recommended additions: 12 items (about 19,000-21,000 words plus 8-12 figures).

## Errors and outdated claims found (verified in text)
- ch01: "Raft, Paxos ... Kafka's KRaft, etcd and ZooKeeper use them to elect a leader". ZooKeeper uses the Zab protocol, not Raft or Paxos. Reword it as "consensus protocols (Raft, Paxos, Zab)".
- ch11: KRaft is described as "newer" with ZooKeeper "the older design". As of Kafka 4.0 (2025) ZooKeeper support is removed. Update to "KRaft is the only mode in Kafka 4.x".
- ch06: the Airflow 3 notes are thin. They mention the `airflow.sdk` import change, but not that `execution_date` and `schedule_interval` are gone. I did not find a hit for `logical_date`, so verify how backfill and "data interval" are explained for Airflow 3.
- ch09, ch11, ch15 and others: the "not run here" labelling is honest, but it means all Spark, Kafka, Airflow and dbt code is untested. Recommend running it once on a real install and replacing the label with outputs.
- Spot-checked arithmetic with no errors found: ch03 practice 2, 4, 6 and 7; ch10 practice 3, 4, 5 and 7 (the unified memory figure (32,768-300) x 0.6 = 19,480.8 is correct); ch10 `autoBroadcastJoinThreshold` default 10 MB and `shuffle.partitions` default 200 are correct for current Spark.
- Not exhaustively verified: warehouse pricing and product behaviour in ch08, and Delta, Iceberg and Hudi feature claims in ch03. The prices the text quotes are marked illustrative. Recheck the feature claims against current docs.
- Appendix is only 1,824 words (a short per-chapter closing note), so it is no real reference. Consider a glossary, a cheat sheet and a config-defaults table there.
