# pdf_utils.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def generate_pdf(text, filename="output.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    textobject = c.beginText()
    textobject.setTextOrigin(inch, inch)
    textobject.textLines(text)  # Add the text to the PDF
    c.drawText(textobject)
    c.save()
    print(f"PDF generated: {filename}")