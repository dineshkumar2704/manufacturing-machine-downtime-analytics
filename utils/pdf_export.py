from fpdf import FPDF
from datetime import datetime
import os


def get_windows_unicode_font():
    fonts = [
        r"C:\Windows\Fonts\seguisym.ttf",   # Emoji support
        r"C:\Windows\Fonts\arialuni.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for f in fonts:
        if os.path.exists(f):
            return f
    raise FileNotFoundError("Unicode font not found in Windows fonts.")


def safe_multicell(pdf, text, line_height=8):
    """
    Safe multicell that never crashes with Unicode width issues
    """
    page_width = pdf.w - 20  # left+right margin safe area
    pdf.multi_cell(page_width, line_height, text)


def generate_recommendation_pdf(
    machine,
    month,
    year,
    failure_prob,
    health_score,
    health_status,
    priority,
    reasons,
    maintenance_date,
):

    pdf = FPDF()
    pdf.add_page()

    font_path = get_windows_unicode_font()
    pdf.add_font("unicode", "", font_path, uni=True)
    pdf.set_font("unicode", size=12)

    # Title
    pdf.set_font("unicode", size=18)
    pdf.cell(0, 12, "AI Maintenance Recommendation Report", ln=True, align="C")
    pdf.ln(6)

    pdf.set_font("unicode", size=12)

    summary_text = f"""
Machine Type: {machine}
Month: {month}
Year: {year}

Failure Probability: {failure_prob*100:.2f}%
Health Score: {health_score:.2f}
Health Status: {health_status}
Priority Level: {priority}
Suggested Maintenance Date: {maintenance_date}

Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
"""

    safe_multicell(pdf, summary_text)
    pdf.ln(4)

    pdf.set_font("unicode", size=14)
    pdf.cell(0, 10, "Operational Insights & Reasons", ln=True)
    pdf.ln(2)

    pdf.set_font("unicode", size=12)

    for r in reasons:
        safe_multicell(pdf, f"• {r}")

    file_name = f"AI_Recommendation_{machine}_{month}_{year}.pdf"
    pdf.output(file_name)

    return file_name
