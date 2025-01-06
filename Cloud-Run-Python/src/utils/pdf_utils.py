# src/utils/pdf_utils.py
from fpdf import FPDF
import textwrap
from io import BytesIO

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
        wrapped_text = textwrap.fill(body, width=85)
        for line in wrapped_text.split('\n'):
            self.multi_cell(0, 10, line)
        self.ln()

def generate_story_pdf(story_name, story_content):
    pdf = StoryPDF()
    pdf.add_page()
    pdf.chapter_title(story_name)
    pdf.chapter_body(story_content)
    
    # Save to BytesIO object
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer