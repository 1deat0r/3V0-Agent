"""Convert the portfolio markdown samples to simple, clean PDFs for the Fiverr gallery."""
import re
from fpdf import FPDF


def sanitize(line):
    for a, b in [("\u2014", "-"), ("\u2013", "-"), ("\u2192", "->"), ("\u2264", "<="),
                 ("\u201c", '"'), ("\u201d", '"'), ("\u2018", "'"), ("\u2019", "'"),
                 ("\u2026", "..."), ("\u00d7", "x")]:
        line = line.replace(a, b)
    return "".join(c for c in line if ord(c) < 256)


def md_to_pdf(md_path, pdf_path, title):
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 8, sanitize(title))
    pdf.ln(2)
    pdf.set_draw_color(46, 230, 168)
    pdf.set_line_width(0.6)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    in_code = False
    for raw in open(md_path, encoding="utf-8"):
        line = sanitize(raw.rstrip("\n"))
        pdf.set_x(pdf.l_margin)  # reset x before every render — prevents drift
        if line.strip().startswith("```"):
            in_code = not in_code
            pdf.ln(1)
            continue
        if in_code:
            pdf.set_font("Courier", "", 8.5)
            pdf.set_text_color(200, 210, 220)
            pdf.multi_cell(0, 4.2, line if line else " ")
            continue
        # strip emphasis markers
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        if text.startswith("# "):
            pdf.set_text_color(20, 20, 25)
            pdf.set_font("Helvetica", "B", 14)
            pdf.ln(3); pdf.multi_cell(0, 7, text[2:]); pdf.ln(2)
        elif text.startswith("## "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(46, 230, 168)
            pdf.ln(2); pdf.multi_cell(0, 6, text[3:]); pdf.ln(1)
        elif text.startswith("### "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(20, 20, 25)
            pdf.ln(2); pdf.multi_cell(0, 6, text[4:]); pdf.ln(1)
        elif text.strip() in ("---",):
            pdf.ln(2)
        elif text.startswith(("- ", "> ")):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 48)
            pdf.multi_cell(0, 5.5, "- " + text[2:])
        elif text.strip():
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 48)
            pdf.multi_cell(0, 5.5, text)
        else:
            pdf.ln(2)
    pdf.output(pdf_path)
    print("wrote", pdf_path)


md_to_pdf("portfolio/root-cause-report-sample.md",
          "assets/root-cause-report-sample.pdf",
          "Root-Cause Report - Sample Deliverable")
md_to_pdf("samples/debug-sample.md",
          "assets/debug-sample.pdf",
          "Bug Fix Report - Sample Deliverable")
