import os
import spacy
from spacy.matcher import PhraseMatcher
import streamlit as st

# -----------------------
# File paths
# -----------------------
BASE_DIR = os.path.dirname(__file__)   # Task-2 folder
RESUME_FILE = os.path.join(BASE_DIR, "../Task-1/outputs/resume1_parsed.txt")
JD_FILE = os.path.join(BASE_DIR, "../Task-1/outputs/jd_parsed.txt")
SKILLS_FILE = os.path.join(BASE_DIR, "skills_dict.txt")

# -----------------------
# Load helper function
# -----------------------
def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"❌ File not found: {path}")
        st.info("👉 Run Task-1/parse_and_clean.py first to generate outputs.")
        return ""

# -----------------------
# Load skills dictionary
# -----------------------
def load_skills():
    try:
        with open(SKILLS_FILE, "r", encoding="utf-8") as f:
            skills = [line.strip() for line in f if line.strip()]
        return skills
    except FileNotFoundError:
        st.error(f"❌ Skills dictionary not found: {SKILLS_FILE}")
        return []

# -----------------------
# Skill extraction
# -----------------------
@st.cache_resource
def get_nlp():
    return spacy.load("en_core_web_sm")

def extract_skills(text, skills_list):
    nlp = get_nlp()
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    patterns = [nlp.make_doc(skill) for skill in skills_list]
    matcher.add("SKILLS", patterns)

    doc = nlp(text)
    matches = matcher(doc)

    found_skills = sorted(set([doc[start:end].text for match_id, start, end in matches]))
    return found_skills

# -----------------------
# Streamlit App
# -----------------------
st.title("🔎 Skill Extraction from Resume & JD")

st.write("This app extracts skills from a resume and job description using a custom skills dictionary.")

resume_text = st.text_area("Paste Resume Text", load_file(RESUME_FILE), height=200)
jd_text = st.text_area("Paste JD Text", load_file(JD_FILE), height=200)
skills_dict = load_skills()

if not skills_dict:
    st.stop()

if st.button("Extract Skills"):
    with st.spinner("Extracting skills..."):
        resume_skills = extract_skills(resume_text, skills_dict)
        jd_skills = extract_skills(jd_text, skills_dict)

    st.subheader("📄 Resume Skills Found")
    st.write(resume_skills if resume_skills else "No skills found.")

    st.subheader("📝 JD Skills Found")
    st.write(jd_skills if jd_skills else "No skills found.")
