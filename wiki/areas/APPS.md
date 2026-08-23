# (pruned — desktop app removed; see commit 377b41e14b)

The desktop app surface was pruned from this single-agent body (commit
377b41e14b): `apps/` (desktop + bootstrap-installer) is gone. What remains in
this area is the dashboard-embedded TUI and its web workspace tooling.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `apps/shared/package.json` | build | Node package manifest | Declares JS workspace deps + scripts | apps/shared/src/billing.ts; apps/shared/src/charge-settlement.ts; apps/shared/src/index.ts; apps/shared/src/skin.ts |
| `apps/shared/src/billing.ts` | frontend-ts | TypeScript module `billing.ts` | Frontend/shared TS source consumed by the tsc/vite build | apps/shared/src/charge-settlement.ts; apps/shared/src/index.ts; apps/shared/src/skin.ts |
| `apps/shared/src/charge-settlement.ts` | frontend-ts | TypeScript module `charge-settlement.ts` | Frontend/shared TS source consumed by the tsc/vite build | apps/shared/src/billing.ts; apps/shared/src/index.ts; apps/shared/src/skin.ts |
| `apps/shared/src/index.ts` | frontend-ts | TypeScript module `index.ts` | Frontend/shared TS source consumed by the tsc/vite build | apps/shared/src/billing.ts; apps/shared/src/charge-settlement.ts; apps/shared/src/skin.ts |
| `apps/shared/src/skin.ts` | frontend-ts | TypeScript module `skin.ts` | Frontend/shared TS source consumed by the tsc/vite build | apps/shared/src/billing.ts; apps/shared/src/charge-settlement.ts; apps/shared/src/index.ts |
