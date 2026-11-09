# Audit: study/cs (Linux, Git, Algorithms, CS Foundations)

## Verdict
Strong, consistent beginner-first course: 16 chapters + cheat sheet, ~100k words, 200+ worked problems, runnable code, callouts, practice sets with inline answers, prompt packs. Spot-checked answers (ch05 FCFS avg 11.67; ch10 topo orders=2, Dijkstra, grid edges=12; ch12 W+R>N, 3-node availability 0.999997, Little's law) were all correct. Weakness is advanced depth and visuals: several chapters (ch01, ch02, ch04, ch05, ch06, ch13) stop at "working engineer" level; interview chapters lack advanced structures (segment tree/Fenwick, KMP, Floyd/Bellman-Ford coverage as taught sections); OS/container internals (cgroups, namespaces), concurrency in code, and distributed-systems depth (clocks, 2PC/sagas, CRDTs) are thin; 7 chapters have zero figures (ch01, ch02, ch11, ch14, ch15, ch16, plus none in ch13 steps) so diagrams of trees, DP tables, packet flow are mostly text. Ch14-16 are bank/project style, weaker for concept teaching. Not verified: whether the ch-level numbers per concept reach 3 distinct examples each (most sections have 1-2 problems; ch01-ch06, ch15, ch16 average under 2 per section).

## Per-chapter table (words, worked problems, code blocks, figures; beginner / expert rating 1-5)
| Ch | Topic | Words | Problems | Code | Figs | Begin | Expert |
|---|---|---|---|---|---|---|---|
| 01 | Linux shell | 5172 | 10 | 25 | 0 | 5 | 3 |
| 02 | Shell scripting | 4526 | 8 | 23 | 0 | 5 | 3 |
| 03 | Git/GitHub | 5409 | 10 | 19 | 2 | 5 | 3 |
| 04 | Networks/HTTP | 6210 | 10 | 18 | 4 | 4 | 3 |
| 05 | OS debugging | 6200 | 10 | 21 | 2 | 4 | 3 |
| 06 | Security | 6923 | 14 | 23 | 2 | 4 | 3 |
| 07 | Complexity/arrays/hash/sort | 7206 | 14 | 48 | 2 | 5 | 4 |
| 08 | Two ptr/window/prefix/bsearch | 7440 | 13 | 41 | 2 | 5 | 4 |
| 09 | Lists/stacks/queues/heaps | 8217 | 19 | 55 | 2 | 5 | 4 |
| 10 | Trees and graphs | 7404 | 16 | 23 | 2 | 5 | 4 |
| 11 | Recursion/DP/greedy/bits | 7599 | 17 | 30 | 0 | 5 | 4 |
| 12 | Distributed systems | 6904 | 22 | 13 | 2 | 4 | 3 |
| 13 | Architecture/ML compute/Java | 6983 | 25 | 7 | 2 | 4 | 3 |
| 14 | Interview patterns bank | 10019 | 43 | 43 | 0 | 3 | 4 |
| 15 | Project lab 1 | 5966 | 8 | 17 | 0 | 4 | 3 |
| 16 | Project lab 2 | 4089 | 8 | 13 | 0 | 4 | 3 |
| App | Cheat sheet | 1224 | 0 | 0 | 0 | n/a | n/a |

## Top 12 gaps (ranked by learner value)
1. ch10/ch11/ch14 - Advanced data structures: Fenwick tree, segment tree (range sum/min, lazy), sparse table, KMP/Z/rolling hash (Rabin-Karp), Bellman-Ford, Floyd-Warshall, A*, SCC (Tarjan/Kosaraju), bipartite check. 3 examples each. ~3000 words.
2. ch10/ch11 - Figures: SVG of tree traversals, graph BFS layers, Dijkstra step states, DP table fills (LCS, knapsack), union-find forest. ~12 SVGs, ~600 words captions.
3. ch05 - Containers/OS internals: cgroups, namespaces, why exit 137, ulimits, page cache, strace/perf/iostat/vmstat walkthrough, a threads/asyncio/multiprocessing example in Python (GIL). ~1800 words.
4. ch12 - Time and transactions: Lamport/vector clocks, 2PC vs sagas, CRDTs, exactly-once myths, Raft log replication step table, quorum failure examples, Kafka-style log. ~2000 words.
5. ch04 - Deeper networking: TCP handshake/congestion (slow start, CUBIC/BBR), TLS 1.3 handshake step table, HTTP/2 vs HTTP/3 head-of-line, DNS TTL debugging with dig, tcpdump/Wireshark reading, Kubernetes/service-mesh basics. ~1800 words.
6. ch06 - Security depth: threat modeling (STRIDE) worked example, JWT/OAuth2/OIDC flows, CSRF/XSS/SSRF with fix examples, key rotation, prompt-injection and model-supply-chain case study. ~2000 words.
7. ch01/ch02 - Advanced shell: xargs/find -exec, process substitution, set -euo pipefail pitfalls, trap, getopts, shellcheck, jq, tmux, ssh config/tunnels, systemd units. ~1500 words.
8. ch03 - Advanced Git: interactive rebase workflow, merge conflict resolution multi-example, worktrees, submodules, monorepo/branching strategies (trunk-based), signed commits, CI caching, GitHub Actions matrix. ~1500 words.
9. ch07/ch09 - Complexity depth: master theorem, recurrence solving, space complexity, cache effects, hash collision handling/open addressing, quickselect, heap build O(n) proof. ~1500 words.
10. ch13 - Architecture depth: roofline worked numbers, tensor cores/precision (FP16/BF16/FP8), KV-cache memory math, NVLink/parallelism types (data/tensor/pipeline), FlashAttention intuition; only 7 code blocks, so add calculators. Java primer: records, streams, virtual threads (Java 21). ~1800 words.
11. ch14 - Add system-design and design-class interview section (LRU cache, rate limiter, URL shortener, distributed counter) and concurrency patterns; mixed-pattern drills with timing guidance. ~2500 words.
12. ch15/ch16 - Projects need graded rubrics, starter repos, tests, and extension tasks (WAL + compaction in KV store, benchmark statistics, CI pipeline). ~1500 words.

Total estimated: ~21,000 words, 12 recommended additions.

## Errors / risks found
No outright technical errors found in the spot-checked answers. Notes:
- ch12: practice problem 12.7.4 answer text contains "Quick check by computing" aside; stylistic, remove.
- Grep shows "MD5" mentioned in ch06 and ch12; verify each use is framed as non-secure for passwords/signatures (not checked in context).
- Version-sensitive claims (TLS, HTTP/3, Java version, GPU specs in ch13) should be re-dated; GPU spec tables age fastest (not verified line by line).
- Practice sets use short inline answers; most sets have ~10 items with a few interview items and no hints/walkthrough for hard ones.
