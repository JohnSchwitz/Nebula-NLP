# src/utils/pdf_generator.py
from fpdf import FPDF
import textwrap

class StoryPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Nebula-NLP', 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 20)
        self.cell(0, 20, title, 0, 1, 'C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Times', '', 12)
        # Split text into manageable chunks
        wrapped_text = textwrap.fill(body, width=85)
        for line in wrapped_text.split('\n'):
            self.multi_cell(0, 10, line)
        self.ln()

def generate_story_pdf(story_name, story_content):
    pdf = StoryPDF()
    pdf.add_page()
    pdf.chapter_title(story_name)
    pdf.chapter_body(story_content)
    return pdf.output(dest='S').encode('latin-1')

def generate_narrative_pdf(narrative_name, narrative_content, source_stories):
    pdf = StoryPDF()
    pdf.add_page()
    
    # Add narrative title
    pdf.chapter_title(narrative_name)
    
    # Add source stories section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Source Stories:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    for story in source_stories:
        pdf.cell(0, 10, f"• {story[1]}", 0, 1, 'L')
    pdf.ln(10)
    
    # Add narrative content
    pdf.chapter_body(narrative_content)
    
    return pdf.output(dest='S').encode('latin-1')