# app/pdf_generator.py
from fpdf import FPDF
import pandas as pd
import tempfile
import os

def generate_pdf(question: str, sql: str, result: pd.DataFrame) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="AI BI Platform - Query Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Question:\n{question}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Generated SQL:\n{sql}")
    pdf.ln(10)
    pdf.cell(0, 10, "Result:", ln=True)

    # Render result DataFrame
    if not result.empty:
        col_width = pdf.w / (len(result.columns) + 1)
        row_height = 8
        for col in result.columns:
            pdf.cell(col_width, row_height, str(col), border=1)
        pdf.ln()
        for row in result.itertuples(index=False):
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1)
            pdf.ln()
    else:
        pdf.cell(0, 10, "No results found.", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name
