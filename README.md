# Career Journey

A personal learning site for becoming a data scientist / ML engineer: a 156-week roadmap with **1,092 daily lessons** (60 minutes a day), 15 study documents (web, PDF and Word, 270 chapters), spaced-repetition **flashcards**, graded **quizzes**, 9 realistic practice **datasets**, a notebook for every chapter, a 98-topic map, projects and ready-made AI prompts.

Open `index.html` (or the GitHub Pages address). Progress is saved only in your own browser: use Settings, Export progress to keep a backup.

## Daily routine
1. **Today**: one lesson a day (recap question, build, read, log).
2. **Review**: clear your due flashcards (about 10 minutes; new cards come from the documents you are studying).
3. **Quiz**: a 10-question quiz on the document you studied this week; missed questions return as flashcards.
4. **Data**: practise on the datasets (each lists planted problems to find, exercises and an answer key to check yourself).

## Rebuilding (maintainers)
| What | Command (from this folder) |
|---|---|
| Lessons into the site | `python3 tools/add_lessons.py` (sources: `tools/lessons/*.json`) |
| Flashcards and quizzes | `python3 tools/build_decks.py` (sources: `tools/decks/*.json`) |
| Dataset catalog | `python3 tools/build_data_catalog.py` (generators: `tools/datasets/make_*.py`, files in `data/`) |
| Chapter notebooks | `python3 tools/build_notebooks.py` |
| Search index | `python3 tools/build_search.py` |
| Check everything | `python3 tools/verify_site.py` |
