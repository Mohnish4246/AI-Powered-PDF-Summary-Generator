import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    # Open the PDF in-memory
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Extract clean, stripped text from each page
    text = ""
    texts_by_page = []
    
    for page in doc:
        page_text = page.get_text().strip()
        texts_by_page.append(page_text)
        text += page_text + "\n"

    return text, len(doc), texts_by_page
