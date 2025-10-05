import os

def read_txt(file_path):
    """
    Returns:
        str: Extracted text content from TXT file
    """
    try:
        print("Looking for file at:", os.path.abspath(file_path))
        print("File exists:", os.path.exists(file_path))
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        print("✅ Successfully read TXT file")
        return text

    except FileNotFoundError:
        print("❌ TXT file not found")
        return ""

    except Exception as e:
        print(f"❌ Error reading TXT file: {e}")
        return ""

if __name__ == "__main__":
    txt_content = read_txt("sample_description.txt")
    print("\nTXT Content Preview:")
    print(txt_content[:200] + "..." if len(txt_content) > 200 else txt_content)

