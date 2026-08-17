"""Render 4 gallery proof cards for the Fiverr gigs (1280x769, dark premium)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 769
BG = (13, 17, 23)          # dark
PANEL = (22, 27, 34)       # panel
ACCENT = (46, 230, 168)    # teal-green
GOLD = (212, 175, 55)      # brand gold
WHITE = (230, 237, 243)
GRAY = (139, 148, 158)
RED = (255, 123, 114)
GREEN = (63, 185, 80)

FONTS = {}
for size in (20, 24, 28, 34, 44):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                 "/usr/share/fonts/TTF/DejaVuSansMono.ttf"):
        try:
            FONTS[size] = ImageFont.truetype(path, size)
            break
        except OSError:
            continue
    if size not in FONTS:
        FONTS[size] = ImageFont.load_default()

def card(title, subtitle):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 96], fill=PANEL)
    d.rectangle([0, 96, W, 100], fill=ACCENT)
    d.text((48, 28), title, font=FONTS[34], fill=WHITE)
    d.text((48, 66), subtitle, font=FONTS[20], fill=GRAY)
    return img, d

def code_block(d, x, y, lines, color=WHITE, panel=PANEL):
    lh = 30
    d.rounded_rectangle([x, y, W - 48, y + lh * len(lines) + 24], radius=10, fill=panel)
    for i, ln in enumerate(lines):
        d.text((x + 24, y + 12 + i * lh), ln, font=FONTS[20], fill=color)
    return y + lh * len(lines) + 24

def kv(d, x, y, key, val, val_color=WHITE, maxw=1100):
    d.text((x, y), key, font=FONTS[24], fill=ACCENT)
    d.text((x, y + 34), val, font=FONTS[20], fill=val_color)
    return y + 78

# ---- 1. Root-cause report ----
img, d = card("ROOT-CAUSE REPORT", "sample deliverable · debug gig · every fix-tier order ships this shape")
y = 130
y = kv(d, 48, y, "SYMPTOM", '"Bot runs without errors but silently skips every item as wrong project."')
y = kv(d, 48, y, "REPRODUCED", "Deterministic — reproduced on first attempt against a database copy.")
y = kv(d, 48, y, "ROOT CAUSE", "Rows read by POSITIONAL column index; a new column was inserted mid-schema,", GOLD)
d.text((48, y), 'so index 4 held a timestamp, not the project directory — the "is mine?" check', font=FONTS[20], fill=GOLD)
d.text((48, y + 30), "silently rejected every session.", font=FONTS[20], fill=GOLD)
y += 78
y = code_block(d, 48, y, [
    "before:  cwd = row[4]                        # positional read — fragile",
    "after:   rec = dict(zip(select, row)); cwd = rec.get('cwd') or ''   # by name",
], GREEN)
y = kv(d, 48, y, "PROOF", "Regression test: shuffled schema must still read cwd correctly — fails loudly if not.")
y = kv(d, 48, y, "WARRANTY", "14 days: if this bug reappears, the fix is free.", ACCENT)
img.save("assets/gallery-root-cause-report.png")

# ---- 2. Before/after finding ----
img, d = card("CODE REVIEW FINDING — BEFORE / AFTER", "sample deliverable · code review gig · every finding ships this way")
y = 130
y = kv(d, 48, y, "FINDING #1 · HIGH", "Unsafe file write: a crash mid-write corrupts the whole file.", RED)
y = code_block(d, 48, y, [
    "f = open(path, 'w')",
    "f.write(json.dumps(ORDERS))      # half-written file on crash",
], RED)
y += 12
y = code_block(d, 48, y, [
    "tmp = f'{path}.tmp'",
    "with open(tmp, 'w') as f: json.dump(ORDERS, f)",
    "os.replace(tmp, path)           # atomic — never half-written",
], GREEN)
y += 16
y = kv(d, 48, y, "WHY IT MATTERS", "Data loss risk on any crash or kill during save. Severity-ranked, with the exact fix.")
y = kv(d, 48, y, "THE PROMISE", "Every finding = severity + exact lines + before/after fix. Never 'consider improving X'.", ACCENT)
img.save("assets/gallery-before-after-finding.png")

# ---- 3. Validation report ----
img, d = card("VALIDATION REPORT", "sample deliverable · scraping gig · loud failure, never silent wrong data")
y = 130
y = code_block(d, 48, y, [
    "validation report — products.html",
    "  cards found in html : 3",
    "  products extracted  : 3",
    "  empty fields:",
    "    name         : 0",
    "    price        : 1   <-- flagged, not skipped",
    "    link         : 0",
    "    availability : 0",
])
y += 16
y = kv(d, 48, y, "THE POINT", "You see exactly which fields came back empty and which pages failed —", ACCENT)
d.text((48, y), "before you trust the CSV. No silent wrong answers, ever.", font=FONTS[20], fill=ACCENT)
img.save("assets/gallery-validation-report.png")

# ---- 4. Agent run ----
img, d = card("AI AGENT — REAL RUN, NOT A DEMO", "sample deliverable · AI agent gig · dry-run first, then real")
y = 130
y = code_block(d, 48, y, [
    "$ python3 lead_agent.py --sheet-id 1AbC... --dry-run",
    "[09:02] read 7 leads from sheet (2 already scored, skipped)",
    "[09:02] scored 5 leads",
    "  HOT  (2):  Maya R.  acme.co       $4,000  referral   score 5",
    "  WARM (2):  Li W.    plumb.io      $800    inbound    score 3",
    "  COLD (1):  logged only",
    "[09:02] done — nothing written, no emails sent",
])
y += 16
y = kv(d, 48, y, "WHAT THIS PROVES", "Dry-run before real data, idempotent state (no double emails), and a runbook", ACCENT)
d.text((48, y), "covering what happens when the sheet read fails or an email is missing.", font=FONTS[20], fill=ACCENT)
img.save("assets/gallery-agent-run.png")

print("wrote 4 gallery images")
