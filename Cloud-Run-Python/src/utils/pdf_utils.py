# src/utils/pdf_utils.py
from fpdf import FPDF
import textwrap

def generate_story_pdf(story_name: str, story_content: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, story_name, ln=True, align='C')
    
    # Add content
    pdf.set_font('Arial', '', 12)
    # Split text into manageable chunks
    wrapped_text = textwrap.fill(story_content, width=85)
    for line in wrapped_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    return pdf.output(dest='S').encode('latin-1')

def generate_narrative_pdf(narrative_name: str, narrative_content: str, source_stories: list) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, narrative_name, ln=True, align='C')
    
    # Add source stories section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Source Stories:', ln=True)
    pdf.set_font('Arial', '', 12)
    for story in source_stories:
        pdf.cell(0, 10, f"• {story['name']}", ln=True)
    
    # Add narrative content
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    wrapped_text = textwrap.fill(narrative_content, width=85)
    for line in wrapped_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    return pdf.output(dest='S').encode('latin-1')