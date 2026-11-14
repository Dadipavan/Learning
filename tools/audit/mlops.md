# MLOps audit (study/mlops, ch01-16 + appendix)

## Verdict
Beginner-friendly, concrete (churn running example, bank-counter analogies, plain-word glossaries, numbers worked by hand) and broad: it covers lifecycle, reproducibility, tracking, versioning, feature stores, pipelines, serving, deployment, CI/CD, monitoring, K8s, cloud, LLMOps, performance, 2 project labs. Weaknesses: (a) worked-example density collapses in ch07-10 (5-9 problems for 5-6k words) vs 16-22 in ch01-06/11-14; practice sets are mostly one-liners with short answers; (b) expert depth is thin: tools are mostly named, not exercised (Triton, KServe, Feast, FSDP/DeepSpeed, Ray, Optuna appear in 1-3 chapters, few runnable examples); no real-GPU/LLM-serving internals; (c) figures nearly absent (0 in 10 of 16 chapters); (d) no ML security/governance/fairness chapter-level treatment and no streaming/online-learning depth. Skill-map items (MLflow, Feast, Optuna/Ray Tune, drift, canary/shadow, LLMOps) are all touched but at name-and-concept level for several.

## Per chapter (words, h2, worked problems, code blocks, figures, beginner 1-5 / expert 1-5)
Counts: "problem" = class-problem occurrences (regex, may double count wrappers; ch15/16 labs use other markup, 0 detected).
| Ch | Topic | Words | h2 | Worked | Code | Fig | Begin | Expert |
|---|---|---|---|---|---|---|---|---|
| 01 | Notebook to production | 4797 | 7 | 18 | 12 | 4 | 5 | 3 |
| 02 | Reproducibility/Docker | 4154 | 7 | 18 | 18 | 0 | 5 | 3 |
| 03 | Tracking and registry | 3580 | 6 | 16 | 16 | 0 | 5 | 3 |
| 04 | Data/model versioning | 3457 | 6 | 16 | 13 | 0 | 5 | 3 |
| 05 | Feature stores/validation | 3797 | 6 | 16 | 14 | 0 | 4 | 3 |
| 06 | Training pipelines/GPU | 4429 | 6 | 16 | 22 | 0 | 4 | 3 |
| 07 | Model serving | 5839 | 7 | 5 | 17 | 2 | 4 | 3 |
| 08 | Deployment strategies | 5392 | 7 | 6 | 15 | 2 | 4 | 3 |
| 09 | CI/CD for ML | 5731 | 7 | 7 | 15 | 0 | 4 | 3 |
| 10 | Monitoring/drift | 6500 | 7 | 9 | 16 | 2 | 5 | 4 |
| 11 | Kubernetes | 5552 | 7 | 18 | 14 | 0 | 4 | 3 |
| 12 | Cloud map AWS/Azure/GCP | 6035 | 9 | 19 | 12 | 0 | 4 | 3 |
| 13 | LLMOps | 6238 | 8 | 18 | 23 | 0 | 4 | 3 |
| 14 | Perf eng, capstones, interviews | 7312 | 9 | 22 | 18 | 4 | 4 | 4 |
| 15 | Project Lab 1 | 5974 | 7 | n/a | 24 | 0 | 4 | 4 |
| 16 | Project Lab 2 | 5148 | 6 | n/a | 26 | 0 | 4 | 4 |
| App | Cheat sheet | 2055 | 16 | 0 | 0 | 0 | 4 | 3 |

## Top 12 gaps (ranked by learner value)
1. ch07 + ch08: Add 8-10 worked problems each (only 5-6 now). Serving: latency budget p50/p99 math, Little's law sizing, batch-size/throughput curve, autoscaling replica calculation. Deployment: canary traffic-split with sample-size/significance, shadow comparison, rollback trigger math, A/B vs bandit. ~1800 words.
2. ch07: LLM-serving internals, currently concept only: KV-cache memory arithmetic (layers x heads x dim x tokens x bytes), continuous batching, PagedAttention, speculative decoding, quantization trade-offs (INT8/FP8/AWQ/GPTQ), TTFT vs tokens/s; worked: how many concurrent users fit on one 80 GB GPU. ~1500 words.
3. ch06: Distributed training depth: data vs tensor vs pipeline parallel, ZeRO/FSDP memory formula (params+grads+optimizer 16 B/param in mixed precision), gradient accumulation, mixed precision/bf16, checkpoint cadence optimum (Young-Daly). Worked: fit a 7B model on N GPUs. ~1500 words.
4. ch09: CI/CD for ML: runnable GitHub Actions pipeline end to end, model-validation gates (metric thresholds, slice tests, behavioral tests), data-contract tests, promotion workflow with registry aliases, GitOps (Argo CD). 3 varied examples. ~1200 words.
5. ch03: Hyperparameter search at scale (skill map item: Optuna, Ray Tune, SageMaker/Vertex tuning): Bayesian/TPE vs random vs Hyperband/ASHA, early stopping/pruning, budget math, worked Optuna study and multi-fidelity example. Only ch03 mentions it. ~1000 words.
6. ch05: Streaming features and online/offline consistency: Feast end-to-end (definitions, materialize, point-in-time join with leakage example), backfills, TTL, streaming aggregations (Flink/Spark), feature monitoring. ~1200 words.
7. ch10: Advanced monitoring: embedding/LLM drift, multivariate drift (domain classifier, MMD), label-delay estimators (CBPE/DLE), slice-based monitoring, fairness monitoring, SLO/error-budget alerting for models; trigger-retrain policy cost model. ~1200 words.
8. New or ch13/ch14: ML security and governance: pickle/model supply chain (safetensors, signing, SBOM), adversarial/data poisoning, prompt injection red-teaming, PII, EU AI Act risk tiers, model cards/audit trails, differential privacy basics. ~1500 words. (Fairness/AI Act touched in only few chapters, shallowly.)
9. ch13: LLMOps expert depth: RAG evaluation (recall@k, faithfulness, LLM-as-judge bias/calibration), fine-tuning ops (LoRA/QLoRA, DPO data pipelines), semantic caching, routing/cascades, agent tracing and eval, cost per task worked examples. ~1500 words.
10. ch11/ch12: Infra-as-code and K8s ML depth: Terraform module for a training stack, Helm chart for a model service, GPU scheduling (device plugin, MIG, node taints, Kueue/Volcano), HPA/KEDA on custom metrics, Kubeflow/Argo pipelines worked example; cloud cost model (spot, reserved, egress) with real arithmetic. ~1500 words.
11. Figures across ch02-06, 09, 11-13, 15-16 (0 each): add 1-2 SVG diagrams per chapter (lifecycle/DAG, Docker layers, registry stage flow, point-in-time join timeline, ZeRO memory bars, canary traffic split, CI gate flow, K8s object map, RAG pipeline, drift histograms). ~15 SVGs, ~0 prose words but high value.
12. Practice sets all chapters: expand beyond 4-8 short items; add graded tiers (basic/intermediate/expert), 2-3 multi-step design problems per chapter with full solutions (e.g. design a fraud-scoring platform with SLO, cost, rollback), plus a final cross-chapter ML system-design exam. ~3000 words total.

Recommended additions: 12 (about 17,000 words plus ~15 figures).

## Errors / outdated claims
No definite factual errors found in sampled arithmetic (retry failure 0.1^4 = 0.0001, fp32 1B params = 4 GB, speedup 100/4+8 = 33 ms, 3.03x, 75.8%: all correct; PSI 0.103 labelled "moderate" matches the usual 0.1/0.25 rule of thumb). Cautions to verify (not confirmed):
- Version-specific content (MLflow stages vs aliases, Feast, KServe, vLLM, cloud service names/prices, token prices in ch13/ch12) dates fast; add "as of" notes and date stamps. MLflow model-registry stages are deprecated in favor of aliases; check ch03 states this prominently.
- Cloud pricing examples ($652 vs $60 spot example in ch06) are illustrative simulations; label them as such.
- Chapters 15/16 labs and the appendix contain no problem markup, so they are not counted as worked/practice by the site's structure; consider consistent markup.
- Not exhaustively read: only intros, practice sets, and keyword scans were checked for ch02-05, 09, 11, 12, 14-16.
