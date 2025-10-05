# Task-1/parse_and_clean.py
import os
from parse_file import extract_text_auto

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "inputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

def parse_and_save(input_file, output_file):
    raw, cleaned = extract_text_auto(os.path.join(INPUT_DIR, input_file))
    out_path = os.path.join(OUTPUT_DIR, output_file)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"✅ Saved: {out_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    parse_and_save("resume-1.pdf", "resume1_parsed.txt")
    parse_and_save("resume-2.docx", "resume2_parsed.txt")
    parse_and_save("JD.txt", "JD_parsed.txt")

    print("\n🎉 Task 1 complete! Check outputs/ folder.")
