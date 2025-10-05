import docx
import os

def read_docx(file_path):
    """
    Returns:
        str: Extracted text content from DOCX file
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        print("Successfully read DOCX file")
        return text

    except FileNotFoundError:
        print("❌ DOCX file not found")
        return ""

    except Exception as e:
        print(f"❌ Error reading DOCX file: {e}")
        return ""

if __name__ == "__main__":
    print("Looking for file at:", os.path.abspath("sample_resume_doc.docx"))
    print("File exists:", os.path.exists("sample_resume_doc.docx"))
    
    docx_content = read_docx("sample_resume_doc.docx")
    print("\nDOCX Content Preview:")
    print(docx_content[:200] + "..." if len(docx_content) > 200 else docx_content)