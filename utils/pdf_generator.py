import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_summary_pdf(text: str, title: str = "PDF Analysis Summary") -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        spaceAfter=15
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=10
    )
    
    story = []
    # Add Title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Process lines / paragraphs
    paragraphs = text.split("\n")
    for para in paragraphs:
        cleaned_para = para.strip()
        if cleaned_para:
            # Replace basic markdown bold text for ReportLab XML support
            cleaned_para = cleaned_para.replace("**", "<b>").replace("**", "</b>")
            story.append(Paragraph(cleaned_para, body_style))
            
    doc.build(story)
    
    # Retrieve bytes from buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
