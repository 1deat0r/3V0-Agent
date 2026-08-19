# ui-tui/ — Ink terminal UI — `ui-tui//`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `ui-tui/.gitignore` | version-control | Git ignore rules | Defines untracked paths; wrong rules leak artifacts or drop source from the repo | ui-tui/README.md; ui-tui/eslint.config.mjs; ui-tui/package.json; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
| `ui-tui/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | ui-tui/.gitignore; ui-tui/eslint.config.mjs; ui-tui/package.json; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
| `ui-tui/eslint.config.mjs` | infra-checks | ESLint flat config | Lint rules for JS/TS; lint gates read it | ui-tui/.gitignore; ui-tui/README.md; ui-tui/package.json; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
| `ui-tui/package.json` | build | Node package manifest | Declares JS workspace deps + scripts | ui-tui/.gitignore; ui-tui/README.md; ui-tui/eslint.config.mjs; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
| `ui-tui/tsconfig.build.json` | build | TypeScript compiler config | tsc/editor compilation settings for the workspace | ui-tui/.gitignore; ui-tui/README.md; ui-tui/eslint.config.mjs; ui-tui/package.json; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
| `ui-tui/tsconfig.json` | build | TypeScript compiler config | tsc/editor compilation settings for the workspace | ui-tui/.gitignore; ui-tui/README.md; ui-tui/eslint.config.mjs; ui-tui/package.json; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
| `ui-tui/vitest.config.ts` | build | Vitest config | Unit test runner setup for JS/TS | ui-tui/.gitignore; ui-tui/README.md; ui-tui/eslint.config.mjs; ui-tui/package.json; ui-tui/packages/hermes-ink/ambient.d.ts; ui-tui/packages/hermes-ink/index.d.ts; ui-tui/packages/hermes-ink/index.js |
