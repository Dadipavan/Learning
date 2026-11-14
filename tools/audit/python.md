# Audit: study/python (Python & Software Engineering)

## Verdict
A strong, unusually practical course: about 100k words across 15 chapters plus an appendix. Every chapter has the same shape (intuition, worked problems, steps tables, callouts, recap, practice set with answers, prompt pack). It states that code was really run on Python 3.14, and it covers modern features (match, walrus, ExceptionGroup, PEP 695 generics, tomllib, batched, uv, free-threaded build). Beginner clarity is very good (jargon is defined, running examples are consistent). The weak spots are (a) expert depth in the language internals (descriptors, metaclasses, `__init_subclass__`, contextvars, weakref, GC, data model details, `functools.cached_property`, `TaskGroup`), (b) databases from Python (only sqlite3 appears in passing, no SQLAlchemy or migrations), (c) visuals (only 6 figures in 15 chapters, zero in ch03-ch09 and ch11-ch15), (d) practice sets of only about 8-10 short items per chapter, mostly one-liners with no tiered or project-sized exercises, (e) third-party tools (pytest, mypy, pydantic, FastAPI, httpx, numpy) are "not run here", so their code and outputs are unverified, and (f) ch15 (projects) is thin on worked examples.

Method: regex counts over the HTML (bs4 not installed), grep for topics, and reading the intro and practice set of ch01, ch05, ch07 and ch11 plus targeted passages. ch02-ch04, ch06, ch08-ch10 and ch12-ch14 were judged from counts, headings and grep only. Ratings are therefore partly inferred. "Prob" is the count of class-problem blocks, which includes practice problems.

## Per-chapter table
(B = beginner-clarity, E = expert-depth, 1-5)

| Ch | Topic | Words | h2 | Prob | Tables | Code | Callouts | Figs | B | E |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Setup, types, mutability | 5776 | 7 | 12 | 6 | 37 | 10 | 2 | 5 | 3 |
| 02 | Control flow, functions, scope, recursion | 5749 | 7 | 13 | 8 | 43 | 9 | 2 | 5 | 3 |
| 03 | Text, encoding, regex | 5814 | 7 | 13 | 11 | 35 | 9 | 0 | 5 | 3 |
| 04 | Collections, comprehensions, itertools, stdlib tour | 7395 | 10 | 15 | 17 | 39 | 14 | 0 | 4 | 3 |
| 05 | Files, JSON, CSV, time, config | 7275 | 8 | 23 | 22 | 44 | 20 | 0 | 5 | 3 |
| 06 | Errors, logging, pdb | 7225 | 8 | 24 | 18 | 44 | 20 | 0 | 5 | 4 |
| 07 | Iterators, generators, decorators, context managers | 7187 | 7 | 25 | 21 | 48 | 16 | 0 | 5 | 3 |
| 08 | OOP, SOLID, patterns | 7169 | 11 | 25 | 10 | 57 | 16 | 0 | 4 | 3 |
| 09 | Modules, envs, typing, validation | 5867 | 10 | 19 | 10 | 41 | 14 | 0 | 4 | 3 |
| 10 | Testing and quality | 7239 | 8 | 22 | 19 | 45 | 16 | 2 | 4 | 3 |
| 11 | Concurrency and performance | 7839 | 8 | 22 | 15 | 42 | 15 | 0 | 4 | 3 |
| 12 | APIs, web, CLI | 9151 | 10 | 25 | 24 | 42 | 14 | 0 | 3 | 3 |
| 13 | Professional practice, security | 8793 | 10 | 25 | 13 | 35 | 14 | 0 | 4 | 3 |
| 14 | Capstones, interview bank | 9043 | 9 | 17 | 11 | 22 | 12 | 0 | 4 | 4 |
| 15 | Project lab | 8346 | 8 | 8 | 8 | 50 | 2 | 0 | 4 | 3 |
| App | Glossary/index/closing | 1089 | 15 | 0 | 14 | 0 | 0 | 0 | - | - |

Notes: ch12 and ch13 are the densest per h2 (about 900 words per section), so sections are too long. ch15 has 8 problems and only 2 callouts. Each "Practice set" has about 8-10 items. The 5.P and 11.P items I read are short, correct and have answers. Many are "what is the output" or "find the bug" items. There are almost no multi-step or from-scratch coding exercises.

## Top 12 gaps (ranked by learner value)
1. **ch04/ch08/ch12, a Python and SQL database chapter section** (about 1800 words). The site skill map has "SQL & Database Management" and the Python items point at the sqlite3 docs. Add `sqlite3` end to end (connect, parameters, transactions, row_factory), then SQLAlchemy Core/ORM basics, sessions, a migrations intro (Alembic), the N+1 problem, and connection pooling. Examples: a CRUD repository class, a transaction rollback demo, N+1 versus a join with a query count.
2. **ch08, data model internals** (about 1500 words). Add descriptors (`__get__/__set__`, how property works), `__init_subclass__`, a metaclass primer and when not to use one, `__getattr__` versus `__getattribute__`, `__call__`, `__hash__`/`__eq__` contracts, and `functools.cached_property`. Examples: a validated-field descriptor, a plugin registry via `__init_subclass__`, a singleton via metaclass versus module.
3. **ch11, modern asyncio and concurrency depth** (about 1500 words). Add `asyncio.TaskGroup`, `timeout`, cancellation, `Semaphore`, `to_thread`, producer/consumer with `asyncio.Queue`, `contextvars`, race conditions, and `threading.Lock` demos. Also add `multiprocessing` start methods and pickling limits. Compare the 3.13/3.14 free-threaded build and subinterpreters with the GIL text. Examples: a rate-limited crawler, a deadlock reproduced and fixed, a lost-update counter fixed with a lock.
4. **Visuals across ch03-ch09 and ch11-ch15** (about 12 SVGs, roughly 600 words of captions). Add a memory/reference diagram (ch01 has some), a call-stack and frame diagram for recursion (ch02), an LEGB scope diagram, an MRO diagram, a generator state diagram, a decorator wrapping onion, an import resolution flow, an event-loop timeline, a test pyramid (ch10 has this), and a layered architecture diagram.
5. **ch09/ch10, typing in depth** (about 1200 words). Add `TypedDict`, `Literal`, `Protocol` with generics, `ParamSpec`/`Concatenate` for typed decorators, `Self`, `overload`, `Final`, `TypeGuard`, strict mypy/pyright configuration, and gradual typing strategy. Examples: typing the retry decorator from ch07, typing a JSON payload with `TypedDict` versus pydantic, a mypy error walkthrough.
6. **ch10, property-based and advanced testing** (about 1200 words). Add Hypothesis (shrinking example), snapshot or golden-file tests, mutation testing awareness, async tests (`pytest-asyncio`), testing time and randomness (freezegun, seeds), contract tests, flaky-test triage, and `conftest` layering. Examples: a Hypothesis test that finds an off-by-one in a chunk function, testing a retry with a fake clock.
7. **Practice sets, all chapters** (about 15 items x 15 chapters, about 4000 words in total). Raise each set to 15-20 items in three tiers (warm-up, build, stretch). Include 2-3 write-the-function exercises per chapter with hidden-test style checks, plus spaced-review mixed items. Add a short rubric or self-check for the project-sized items.
8. **ch11/ch01, memory and performance internals** (about 1200 words). Add reference counting versus the cyclic GC (`gc` module, `weakref`), the small-int and string interning caveats, `__slots__` memory measurement, `sys.getsizeof` pitfalls, `bisect`/`heapq`/`deque` complexity, a Big-O table with real measurements, `memoryview` and `array`, and the CPython bytecode and specialising interpreter. Examples: a memory leak via a cycle, a cache that grows without bound (use a `WeakValueDictionary`), list versus deque `pop(0)` timings.
9. **ch12, API-building depth** (about 1500 words). Add FastAPI dependency injection, pydantic v2 models (`model_validate`, validators), async endpoints, background tasks, middleware, testing with `TestClient`, structured error responses (RFC 9457 problem details), rate limiting, and a retry/backoff client with `httpx`. Include the auth flow (OAuth2 authorisation code, JWT pitfalls: `alg=none`, expiry, refresh). Examples: a full CRUD service with tests, an idempotency-key endpoint.
10. **ch09/ch13, packaging and delivery** (about 1200 words). Add building and publishing a wheel (build, twine, trusted publishing), src layout, entry points, lockfiles with uv and `uv run`, Dockerising a Python app (multi-stage, non-root, slim base, healthcheck), CI matrix across Python versions, and a pre-commit plus GitHub Actions example. The site has a Docker domain, so cross-link it. Examples: a CLI package installed by pipx, a multi-stage Dockerfile with image size comparison.
11. **ch03/ch04, more worked examples for core concepts** (about 1500 words). Regex (lookarounds, named groups, catastrophic backtracking/ReDoS, `re.VERBOSE`), Unicode normalisation (`unicodedata`), `textwrap`/`string.Template`, `decimal` and `fractions` versus float, sorting stability and `key=` with `functools.cmp_to_key`, shallow versus deep copy with 3 varied cases, and the `dict`/`set` hashing internals. Give at least 3 varied examples per concept (the audit found about 1-2 for several of these).
12. **ch06/ch13/ch14, debugging and observability in production** (about 1200 words). Add structured logging (JSON, `extra`, correlation IDs through `contextvars`), `logging.config.dictConfig`, `warnings` and deprecations, `faulthandler`, post-mortem with `pdb.post_mortem`, `py-spy` and a flame graph reading, a basic metrics and tracing intro (OpenTelemetry), and a postmortem write-up template. Examples: tracing one request across logs, finding a hot spot with a flame graph.

Also missing and worth a short box each (about 150 words each): the `argparse` subcommand pattern in more depth (CLI testing), `dataclasses` advanced (`field`, `__post_init__`, `frozen`, `slots=True`), `enum.StrEnum/Flag`, `pickle` security, `secrets` module, `subprocess` safety (`shell=True`), `shutil`/`tempfile`, `random` seeding, and `zipfile`/`gzip`. About half of these were not found by grep.

**Estimated total for the 12 gaps:** about 19,000 words plus about 12 figures.

## Errors, outdated or risky claims found
I verified the items below against the text. I found no outright code error in the sampled passages.
1. **Unverified third-party code.** ch09, ch10, ch11 and ch12 say pytest, mypy, pydantic, FastAPI, requests, httpx, numpy, pandas, uv and poetry were "not run here". The snippets are labelled, but the outputs may drift. Run them once with network access and replace the labels with real output.
2. **Version claim.** Every chapter says "All code run with Python 3.14" while the text says "works on 3.10+". Several features need newer versions: the `def f[T]` syntax (3.12+, noted in ch09), `itertools.batched` (3.12+, noted in ch04), and `ExceptionGroup` (3.11+, noted in ch06). They are noted individually, but the ch01 note should list these minimum versions in one table. Python 3.9 and 3.10 are end-of-life by 2026-11.
3. **Free-threaded build.** ch11 mentions the free-threaded build in one sentence. Check that it states that the build is optional, that some C extensions are not yet compatible, and that single-thread speed may drop. I did not read that passage in full, so I could not confirm whether it does.
4. **Missing deprecation notice.** `datetime.utcnow()` is not mentioned anywhere (deprecated in 3.12). Add a callout in ch05.
5. **Coverage mismatch with the skill map.** The site's "Python Programming" skill items include traceback reading (covered in ch06) and sqlite3 plus SQL injection (partly covered in ch12/ch13), but there is no SQL-from-Python chapter section (see gap 1).
6. **Structural.** `appendix.html` has 15 h2 sections but no problems, and its 1089 words are a recap/closing note, so there is no glossary or index of terms.
7. **Section length.** ch12 (9151 words, 10 h2) and ch13 (8793 words) have sections that are long. Split the sections or add mid-section checkpoints.
