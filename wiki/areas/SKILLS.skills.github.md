# skills/ + optional-skills/ — the skill libraries — `skills/github/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `skills/github/DESCRIPTION.md` | doc | GitHub workflow skills for managing repositories, pull requests, code reviews, issues, and CI/CD pipelines using the gh CLI and git via terminal. | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/codebase-inspection/SKILL.md; skills/github/github-auth/SKILL.md; skills/github/github-auth/scripts/gh-env.sh; skills/github/github-auth/scripts/git-credential-token.py |
| `skills/github/codebase-inspection/SKILL.md` | skill-doc | Skill definition for `codebase-inspection` | The instruction contract a model loads when the skill's trigger matches | skills/github/codebase-inspection/ |
| `skills/github/github-auth/SKILL.md` | skill-doc | Skill definition for `github-auth` | The instruction contract a model loads when the skill's trigger matches | skills/github/github-auth/scripts/gh-env.sh; skills/github/github-auth/scripts/git-credential-token.py |
| `skills/github/github-auth/scripts/gh-env.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks | skills/github/github-auth/scripts/git-credential-token.py |
| `skills/github/github-auth/scripts/git-credential-token.py` | source | Print the first unambiguous GitHub token in a git credential-store file. | Python module executed or imported by the runtime; check git intent before deleting | skills/github/github-auth/scripts/gh-env.sh |
| `skills/github/github-code-review/SKILL.md` | skill-doc | Skill definition for `github-code-review` | The instruction contract a model loads when the skill's trigger matches | skills/github/github-code-review/references/review-output-template.md |
| `skills/github/github-code-review/references/review-output-template.md` | doc | Review Output Template | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-code-review/references/ |
| `skills/github/github-issue-to-pr/SKILL.md` | skill-doc | Skill definition for `github-issue-to-pr` | The instruction contract a model loads when the skill's trigger matches | skills/github/github-issue-to-pr/ |
| `skills/github/github-issues/SKILL.md` | skill-doc | Skill definition for `github-issues` | The instruction contract a model loads when the skill's trigger matches | skills/github/github-issues/templates/bug-report.md; skills/github/github-issues/templates/feature-request.md |
| `skills/github/github-issues/templates/bug-report.md` | doc | Bug Description | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-issues/templates/feature-request.md |
| `skills/github/github-issues/templates/feature-request.md` | doc | Feature Description | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-issues/templates/bug-report.md |
| `skills/github/github-pr-workflow/SKILL.md` | skill-doc | Skill definition for `github-pr-workflow` | The instruction contract a model loads when the skill's trigger matches | skills/github/github-pr-workflow/references/ci-troubleshooting.md; skills/github/github-pr-workflow/references/conventional-commits.md; skills/github/github-pr-workflow/templates/pr-body-bugfix.md |
| `skills/github/github-pr-workflow/references/ci-troubleshooting.md` | doc | CI Troubleshooting Quick Reference | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-pr-workflow/references/conventional-commits.md |
| `skills/github/github-pr-workflow/references/conventional-commits.md` | doc | Conventional Commits Quick Reference | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-pr-workflow/references/ci-troubleshooting.md |
| `skills/github/github-pr-workflow/templates/pr-body-bugfix.md` | doc | Bug Description | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-pr-workflow/templates/pr-body-feature.md |
| `skills/github/github-pr-workflow/templates/pr-body-feature.md` | doc | Summary | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-pr-workflow/templates/pr-body-bugfix.md |
| `skills/github/github-repo-management/SKILL.md` | skill-doc | Skill definition for `github-repo-management` | The instruction contract a model loads when the skill's trigger matches | skills/github/github-repo-management/references/github-api-cheatsheet.md |
| `skills/github/github-repo-management/references/github-api-cheatsheet.md` | doc | GitHub REST API Cheatsheet | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/github/github-repo-management/references/ |
