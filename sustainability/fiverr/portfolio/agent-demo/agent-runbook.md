# AI Agent Demo — Lead-Qualification Agent (runbook + example run)

*Spec-work sample for the "AI agent that does real work" gig. This shows the
shape of every delivery: not a demo video, a runbook — how to run it, what it
needs, what it does when things go wrong, and a real example run against
sample data. Client data is redacted; structure is real.*

---

## 1. What the agent does

A **lead-qualification agent** for a small business: it reads new leads from a
Google Sheet, scores each one against the owner's rules, writes the score back
to the sheet, and emails a daily summary of only the leads that need a human.

- **Input:** a Google Sheet (`new_leads` tab) — columns: `name`, `email`,
  `company`, `budget`, `use_case`, `lead_source`.
- **Tools it calls:** Google Sheets API (read + write), Gmail API (send
  summary).
- **Memory:** a small JSON state file (`agent_state.json`) remembering which
  leads it has already scored, so re-runs are idempotent — no double emails,
  no re-scoring.
- **Failure behavior:** if a sheet read fails, it stops and writes
  `error.log` with the exact API error; it never silently skips a lead.

## 2. Qualification rules (from the owner, in plain English)

1. Budget ≥ $2,000 → score 3 ("hot"). Budget $500–$1,999 → 2 ("warm").
   Below $500 → 1 ("cold").
2. `use_case` mentions "automation" or "workflow" → +1.
3. `lead_source` is "referral" → +1.
4. Final: 4–5 = hot, 2–3 = warm, 0–1 = cold. Hot + warm go in the daily
   summary; cold leads are logged only.

## 3. How to run it

```bash
cp config.example.yaml config.yaml   # add your Sheets ID + Gmail credentials
python3 lead_agent.py --sheet-id 1AbC... --dry-run   # preview: no writes
python3 lead_agent.py --sheet-id 1AbC...             # real run
```

- `--dry-run` scores everything and prints the summary **without writing** —
  verify before running on real data.
- Needs: Python 3.10+, `google-api-python-client`, `google-auth`. **You bring
  the API keys** — the agent never sees your account password; it uses a
  service-account key you create and can revoke.

## 4. Example run (redacted)

```text
$ python3 lead_agent.py --sheet-id 1AbC... --dry-run
[09:02] read 7 leads from sheet (2 already scored, skipped)
[09:02] scored 5 leads
[09:02] SUMMARY (dry-run — nothing written)
  HOT  (2):
    - Maya R.  acme.co       budget $4,000  "workflow automation"  referral   score 5
    - Tom K.   northwind.io  budget $2,500  "reporting"            inbound   score 3
  WARM (2):
    - Li W.    plumb.io      budget $800    "automation"           inbound   score 3
    - Sara P.  (no company)  budget $1,200  "crm sync"             inbound   score 2
  COLD (1): logged only
[09:02] done — no emails sent, sheet untouched
```

```text
$ python3 lead_agent.py --sheet-id 1AbC...
[09:15] read 7 leads (2 already scored, skipped)
[09:15] scored 5 leads, wrote scores to sheet (5 rows updated)
[09:15] emailed daily summary to owner@acme.co — 4 leads (2 hot, 2 warm)
[09:15] state saved: agent_state.json (7 leads processed total)
```

## 5. What happens when it breaks

- **Sheet read fails** → writes `error.log` with the API error, exits 1, sends
  nothing. It does not guess.
- **One lead has a missing email** → that lead is skipped and listed under
  "needs review" in the summary, never silently dropped.
- **Email send fails** → scores are still saved; the summary is retried on the
  next run from `agent_state.json`.

## 6. What you'd receive on a real order

The agent code + config template, this runbook, the example run above
re-executed against **your** data, and a 30-minute handoff call. LLM-agnostic:
OpenAI, Anthropic, DeepSeek, or local — you bring the key, I write the agent.

---

*Sample only: lead names/companies are fictional; the delivery structure
(runbook, dry-run, idempotent state, loud failure) is what every order ships
with.*
