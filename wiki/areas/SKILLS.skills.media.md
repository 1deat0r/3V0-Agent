# skills/ + optional-skills/ — the skill libraries — `skills/media/`

Auto-rendered from `wiki/manifest.tsv`.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `skills/media/DESCRIPTION.md` | doc | Skills for working with media content — YouTube transcripts, GIF search, music generation, and audio visualization. | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/media/gif-search/SKILL.md; skills/media/songsee/SKILL.md; skills/media/youtube-content/SKILL.md; skills/media/youtube-content/references/output-formats.md |
| `skills/media/gif-search/SKILL.md` | skill-doc | Skill definition for `gif-search` | The instruction contract a model loads when the skill's trigger matches | skills/media/gif-search/ |
| `skills/media/songsee/SKILL.md` | skill-doc | Skill definition for `songsee` | The instruction contract a model loads when the skill's trigger matches | skills/media/songsee/ |
| `skills/media/youtube-content/SKILL.md` | skill-doc | Skill definition for `youtube-content` | The instruction contract a model loads when the skill's trigger matches | skills/media/youtube-content/references/output-formats.md; skills/media/youtube-content/scripts/fetch_transcript.py |
| `skills/media/youtube-content/references/output-formats.md` | doc | Output Format Examples | Human/agent-readable documentation; the wiki keeps it pointer-capped | skills/media/youtube-content/references/ |
| `skills/media/youtube-content/scripts/fetch_transcript.py` | source | Fetch a YouTube video transcript and output it as structured JSON. | Python module executed or imported by the runtime; check git intent before deleting | skills/media/youtube-content/scripts/ |
