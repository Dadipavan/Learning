# Audit: study/genai (Generative AI: NLP, LLMs, RAG and Agents)

## Verdict
Strong, consistent, beginner-friendly document: 16 chapters plus appendix, about 90k words. Each chapter has the same shape (intuition, key ideas, runnable code, "Problem x.y.z" with steps and Answer/Check/Why it matters, recap, practice set, AI prompt pack). Beginner clarity is high. Depth is professional-intermediate: it is excellent on cost, memory and eval arithmetic, and on RAG, agents and ops. It is thin on the modern expert layer. Missing or only name-checked: transformer and attention mechanics (deferred to the dl/ doc), long-context and KV-cache math, ColBERT/late interaction, Matryoshka embeddings, RAGAS-style frameworks, tool-use evals, agent benchmarks, inference serving internals, and the reasoning-model/RL pipeline. Worked-example density is uneven. Chapters 1-11 have 16-22 problems each (roughly 3 per section). Chapters 12 and 13 have only 9-10 problems across 5 big topics each. Chapters 15 and 16 (project labs) have none. Figures are scarce: 7 SVGs in 16 chapters, and chapters 1-5 and 12 have none. I did not run the code blocks. Technical claims I spot-checked were correct. The checks were the 16 bytes/param Adam memory rule, the Chinchilla 20 tokens/param and C=6ND rules, and the LoRA y=Wx+(a/r)BAx form with B initialised to 0.

## Per-chapter table
Words are from visible text. "Problems" counts class="problem". Figures are svg/img. Ratings are 1-5 (beginner clarity / expert depth).

| Ch | Title | Words | h2 | Problems | Code | Figs | Beginner | Expert |
|---|---|---|---|---|---|---|---|---|
| 01 | NLP Foundations | 5326 | 8 | 20 | 15 | 0 | 5 | 3 |
| 02 | Embeddings, Similarity, Semantic Search | 4007 | 6 | 17 | 12 | 0 | 5 | 2 |
| 03 | How LLMs Work | 5220 | 8 | 20 | 12 | 0 | 5 | 3 |
| 04 | Prompt and Context Engineering | 4287 | 7 | 18 | 13 | 0 | 5 | 3 |
| 05 | Using LLM APIs | 4370 | 7 | 18 | 17 | 0 | 5 | 3 |
| 06 | Vector DBs and Retrieval | 4081 | 6 | 16 | 14 | 2 | 4 | 3 |
| 07 | RAG End to End | 5919 | 8 | 20 | 13 | 4 | 4 | 4 |
| 08 | Evaluating LLM Systems | 7060 | 8 | 19 | 19 | 2 | 4 | 4 |
| 09 | Guardrails, Safety, Responsible AI | 5734 | 7 | 19 | 7 | 2 | 5 | 3 |
| 10 | Fine-Tuning LLMs | 7483 | 8 | 22 | 15 | 2 | 4 | 4 |
| 11 | AI Agents | 7396 | 8 | 22 | 12 | 2 | 4 | 4 |
| 12 | Multimodal, Document AI, Text-to-SQL | 6624 | 8 | 9 | 22 | 0 | 4 | 3 |
| 13 | LLMOps | 6426 | 8 | 10 | 24 | 2 | 4 | 3 |
| 14 | Capstones and Interview Bank | 7150 | 9 | 10 | 11 | 0 | 4 | 3 |
| 15 | Project Lab 1 | 6013 | 7 | 0 | 27 | 0 | 3 | 3 |
| 16 | Project Lab 2 | 5046 | 6 | 0 | 23 | 0 | 3 | 3 |
| App | Cheat Sheet | 1750 | 16 | 0 | 0 | 0 | 4 | 2 |

Practice sets exist in ch01-14 and ch15-16 (checked by the "Practice set" headings). Answers are inline ("Check yourself", "Answer"). Ch15 and ch16 have 12 or fewer answer/solution mentions each, so their practice sets are mostly open-ended.

## Skill-map coverage (index.html)
Phases p13 and p14 map to this doc: prompt engineering with an eval set, embeddings and vector DBs, RAG, retrieval metrics and faithfulness, tool/function calling, structured outputs, agent patterns, MCP, observability. All are covered. Items I found missing or weak:
- "Transformers from scratch (nanoGPT)" is only in dl/.
- GenAI-specific XAI/interpretability (p14 title mentions XAI) is not covered.
- Production serving (vLLM, batching) is mentioned but not worked.

## TOP 12 gaps (ranked by learner value)
1. **Ch12 and ch13: add worked problems (about 10 more each).** Targets: ch12 WER by hand with edit distance, SQL-guard bypass cases, invoice-field validation, token cost of an image/page; ch13 p50/p95/p99 from a latency list, queueing/capacity, cache hit-rate break-even, router savings vs quality loss. About 3,000 words.
2. **Ch15 and ch16: add checkpoints, expected outputs and practice problems.** Include grading rubrics, "your numbers should be near X", and 5 debugging problems per lab (for example, recall@k drops after a chunk-size change). About 2,500 words.
3. **Ch03: attention and KV-cache math (new 3.6).** Compute KV memory = 2 x layers x kv_heads x head_dim x seq x bytes for a 7B and a 70B model. Cover MQA/GQA, FlashAttention intuition, prefill vs decode (compute-bound vs memory-bound), speculative decoding and continuous batching. Examples: max concurrent users on one 80 GB GPU; context 8k vs 128k. About 1,500 words.
4. **Ch02/06: modern retrieval models.** Cover Matryoshka/truncated embeddings, binary and int8 quantisation, ColBERT late interaction, SPLADE/sparse-learned, bi-encoder vs cross-encoder, and domain adaptation of embeddings. Examples: MaxSim by hand; index-size and recall tradeoff table. About 1,800 words.
5. **Ch08: RAG evaluation frameworks and synthetic test sets.** Cover the RAGAS/TruLens/DeepEval metric families (context precision/recall, answer relevance), generating a golden set with an LLM plus human audit, judge calibration with Cohen's kappa, and pairwise judging with position-swap. Add a bootstrap CI example. About 1,800 words.
6. **Ch11: agent evaluation and reliability depth.** Cover trajectory evals, tool-call accuracy, pass^k vs pass@k, benchmarks (SWE-bench, tau-bench, GAIA), sandboxing for code execution, prompt-injection through tools, and a state-machine/LangGraph-style checkpoint example. About 1,800 words.
7. **Ch10: alignment and reasoning-model training worked example.** Compute the DPO loss on one pair by hand, a reward-model Bradley-Terry example, GRPO advantage from a group of 4 samples, catastrophic forgetting mitigation, and distillation. Also add a quantisation primer (GPTQ/AWQ/GGUF, with perplexity impact). About 2,000 words.
8. **Ch07: advanced RAG with measurements.** Cover query rewriting/HyDE/multi-query with RRF numbers, parent-child and late chunking, GraphRAG vs vector RAG decision, long-context vs RAG tradeoff cost calculation, multi-tenant ACL filtering and freshness/re-indexing. About 1,800 words.
9. **Figures (about 10 new SVGs).** Priority: ch03 (next-token loop, temperature curves, KV cache), ch02 (2-D embedding space, cosine geometry), ch04 (prompt anatomy), ch05 (retry/backoff timeline), ch09 (defence-in-depth layers), ch12 (VLM patch pipeline, text-to-SQL flow), ch14 (system-design diagram). About 300 words of captions plus SVG work.
10. **Ch04/05: structured output and tool-use depth.** Cover JSON-schema/constrained decoding, tool-call schemas across providers, prompt-caching layout (stable prefix first), batch APIs, and prompt-injection-safe templates. Examples: schema violation repair loop; cache-hit math. About 1,200 words.
11. **Ch13/05: serving and self-hosting.** Cover vLLM/TGI, GPU sizing (tokens/s per dollar), quantised vs hosted API break-even, and rate-limit/queue design. Example: break-even request volume for self-host vs API. About 1,200 words.
12. **Ch14: system-design interview worked answers and a modern topics bank.** Add 3 full design walkthroughs (enterprise RAG at 10M docs, customer-support agent, multilingual search), each with a capacity estimate and tradeoffs. Add 20 rapid-fire questions on MoE, long context, reasoning models, MCP and evals. About 2,000 words.

Total recommended additions: 12 items, roughly 22,000 words, plus about 10 SVGs.

## Errors and outdated claims found
No hard technical errors verified in the sampled sections. Items to double-check or soften:
- ch10: GRPO and ORPO get one paragraph and are labelled "read about later". For a doc aiming at expert level this is a gap, not an error.
- ch03: the Chinchilla rule is correctly caveated. Add a note that frontier models use 100+ tokens/param.
- ch13 mentions MoE only briefly. MoE affects the memory vs compute reasoning in ch03/ch10 (active vs total parameters), and the docs never explain that.
- Several chapters use "price" placeholders such as 1.00/4.00 per million tokens. These are fine as illustrations, but they should be labelled hypothetical, and a "check current pricing" note should be present everywhere.
- ch14 and ch15 duplicate projects (RAG, text-to-SQL, agent each appear in both). This is redundant. Merge them, or make ch14 a summary pointing to ch15/16.
- Provider and model names are mostly generic, so the doc ages well. Verify that any remaining library APIs (LangGraph, sentence-transformers) in code blocks run on current versions.
