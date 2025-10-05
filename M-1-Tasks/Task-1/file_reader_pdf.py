import PyPDF2

def read_pdf(file_path):
    """
    Returns:
        str: Extracted text content from PDF
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            print("Successfully read PDF file")
            return text

    except FileNotFoundError:
        print("❌ PDF file not found")
        return ""

    except Exception as e:
        print(f"❌ Error reading PDF file: {e}")
        return ""

if __name__ == "__main__":
    pdf_content = read_pdf("sample_resume_pdf.pdf")
    print("\nPDF Content Preview:")
    print(pdf_content[:200] + "..." if len(pdf_content) > 200 else pdf_content)