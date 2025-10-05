import streamlit as st
import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------
# 1. Load models
# ------------------------------
@st.cache_resource
def load_models():
    nlp = spacy.load("en_core_web_sm")
    sbert = SentenceTransformer("all-MiniLM-L6-v2")
    return nlp, sbert

nlp, sbert_model = load_models()

# ------------------------------
# 2. Extract skills (rule-based + NER)
# ------------------------------
def extract_skills(text):
    doc = nlp(text)
    tokens = [token.text for token in doc if token.pos_ in ["PROPN", "NOUN"]]
    entities = [ent.text for ent in doc.ents]
    skills = list(set(tokens + entities))
    return [s.strip() for s in skills if len(s.strip()) > 1]

# ------------------------------
# 3. Streamlit UI
# ------------------------------
st.title("📊 Mini Skill Gap Report")
st.write("Upload resume & job description text to generate a skill gap report.")

resume_text = st.text_area("✍️ Paste Resume Text")
jd_text = st.text_area("📄 Paste Job Description Text")

if st.button("Generate Report"):
    if not resume_text.strip() or not jd_text.strip():
        st.warning("⚠️ Please enter both Resume and JD text.")
    else:
        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        # Embeddings + similarity
        resume_emb = sbert_model.encode(resume_skills)
        jd_emb = sbert_model.encode(jd_skills)
        sim_matrix = cosine_similarity(jd_emb, resume_emb)

        results = []
        for i, jd_skill in enumerate(jd_skills):
            sims = list(enumerate(sim_matrix[i]))
            sims = sorted(sims, key=lambda x: x[1], reverse=True)
            best_idx, best_score = sims[0]
            resume_match = resume_skills[best_idx]

            if best_score >= 0.75:
                status = "Strong"
            elif best_score >= 0.5:
                status = "Partial"
            else:
                status = "Missing"
                resume_match = "-"

            results.append({
                "JD Skill": jd_skill,
                "Resume Match": resume_match,
                "Status": status
            })

        df = pd.DataFrame(results)

        st.subheader("📑 Skill Gap Report")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Report (CSV)",
            data=csv,
            file_name="skill_gap_report.csv",
            mime="text/csv"
        )
