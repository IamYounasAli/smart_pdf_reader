import io
import re
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def format_markdown_to_reportlab(text: str) -> str:
    """Safely escapes XML characters and converts Markdown bolding to ReportLab XML tags."""
    # 1. Escape special characters (<, >, &) to prevent XML parsing crashes
    safe_text = escape(text)
    
    # 2. Safely convert **bold** markdown to ReportLab <b> tags
    safe_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
    
    return safe_text

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
    
    story = [
        Paragraph(format_markdown_to_reportlab(title), title_style),
        Spacer(1, 12)
    ]
    
    paragraphs = text.split("\n")
    for para in paragraphs:
        cleaned_para = para.strip()
        if cleaned_para:
            formatted_para = format_markdown_to_reportlab(cleaned_para)
            story.append(Paragraph(formatted_para, body_style))
            
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
