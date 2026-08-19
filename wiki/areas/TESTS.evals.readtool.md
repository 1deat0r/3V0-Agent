# tests/ + tests-js/ + evals/ — the test suites — `evals/readtool/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `evals/readtool/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | evals/readtool/fixtures.py; evals/readtool/report.py; evals/readtool/results/.gitignore; evals/readtool/results/SUMMARY.md; evals/readtool/runner.py; evals/readtool/tasks.py |
| `evals/readtool/fixtures.py` | source | Hostile-workspace fixture generator for the read-tool eval. | Python module executed or imported by the runtime; check git intent before deleting | evals/readtool/README.md; evals/readtool/report.py; evals/readtool/results/.gitignore; evals/readtool/results/SUMMARY.md; evals/readtool/runner.py; evals/readtool/tasks.py |
| `evals/readtool/report.py` | source | Compare read-tool eval result sets (baseline vs feature labels). | Python module executed or imported by the runtime; check git intent before deleting | evals/readtool/README.md; evals/readtool/fixtures.py; evals/readtool/results/.gitignore; evals/readtool/results/SUMMARY.md; evals/readtool/runner.py; evals/readtool/tasks.py |
| `evals/readtool/results/.gitignore` | version-control | Git ignore rules | Defines untracked paths; wrong rules leak artifacts or drop source from the repo | evals/readtool/results/SUMMARY.md |
| `evals/readtool/results/SUMMARY.md` | doc | Read-Tool Eval — Results Log | Human/agent-readable documentation; the wiki keeps it pointer-capped | evals/readtool/results/.gitignore |
| `evals/readtool/runner.py` | source | Run the read-tool eval through the REAL Hermes AIAgent. | Python module executed or imported by the runtime; check git intent before deleting | evals/readtool/README.md; evals/readtool/fixtures.py; evals/readtool/report.py; evals/readtool/results/.gitignore; evals/readtool/results/SUMMARY.md; evals/readtool/tasks.py |
| `evals/readtool/tasks.py` | source | Task battery for the read-tool eval. | Python module executed or imported by the runtime; check git intent before deleting | evals/readtool/README.md; evals/readtool/fixtures.py; evals/readtool/report.py; evals/readtool/results/.gitignore; evals/readtool/results/SUMMARY.md; evals/readtool/runner.py |
