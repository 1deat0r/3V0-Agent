# tests/ + tests-js/ + evals/ — the test suites — `tests/website/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `tests/website/__init__.py` | test | Python module `__init__.py` | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/website/test_extract_skills.py; tests/website/test_generate_skill_docs.py |
| `tests/website/test_extract_skills.py` | test | Tests for website/scripts/extract-skills.py helpers. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/website/__init__.py; tests/website/test_generate_skill_docs.py |
| `tests/website/test_generate_skill_docs.py` | test | Tests for website/scripts/generate-skill-docs.py. | Test module — asserts the repo contract; run via scripts/run_tests.sh | tests/website/__init__.py; tests/website/test_extract_skills.py |
