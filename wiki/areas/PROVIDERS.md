# providers/ + native/ — inference provider profiles

Inference provider profiles: `providers/__init__.py` discovery + `base.py` ABC; `native/` has the FTS5 CJK tokenizer. Provider plugins override bundled profiles by last-writer-wins.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `native/fts5_cjk/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | native/fts5_cjk/build.sh; native/fts5_cjk/fts5_cjk.c; native/fts5_cjk/vendor/sqlite3.h; native/fts5_cjk/vendor/sqlite3ext.h |
| `native/fts5_cjk/build.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks | native/fts5_cjk/README.md; native/fts5_cjk/fts5_cjk.c; native/fts5_cjk/vendor/sqlite3.h; native/fts5_cjk/vendor/sqlite3ext.h |
| `native/fts5_cjk/fts5_cjk.c` | asset | File `fts5_cjk.c` | Repository content; see related files / area page for the enclosing subsystem | native/fts5_cjk/README.md; native/fts5_cjk/build.sh; native/fts5_cjk/vendor/sqlite3.h; native/fts5_cjk/vendor/sqlite3ext.h |
| `native/fts5_cjk/vendor/sqlite3.h` | asset | File `sqlite3.h` | Repository content; see related files / area page for the enclosing subsystem | native/fts5_cjk/vendor/sqlite3ext.h |
| `native/fts5_cjk/vendor/sqlite3ext.h` | asset | File `sqlite3ext.h` | Repository content; see related files / area page for the enclosing subsystem | native/fts5_cjk/vendor/sqlite3.h |
| `providers/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | providers/__init__.py; providers/base.py |
| `providers/__init__.py` | source | Provider registry + lazy discovery (bundled, user, legacy) | Lazy separate discovery; user plugins override bundled (last-writer-wins) | plugins/model-providers/ |
| `providers/base.py` | source | Provider ABC — base contract for model-provider plugins | The seam implemented by every provider plugin | plugins/model-providers/;providers/__init__.py |
