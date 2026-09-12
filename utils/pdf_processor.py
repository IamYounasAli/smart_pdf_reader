import pypdf
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from an uploaded PDF file stream.
    """
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {str(e)}")
