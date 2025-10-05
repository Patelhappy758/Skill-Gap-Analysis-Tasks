import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------
# 1. Load Sentence-BERT model
# ------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ------------------------------
# 2. Input Section
# ------------------------------
st.title("🔍 Resume vs JD Skill Similarity")
st.write("This app compares your **resume skills** with **job description (JD) skills** using Sentence-BERT.")

resume_input = st.text_area(
    "Enter Resume Skills (comma-separated):",
    "Python, Machine Learning, Data Analysis, SQL, Communication"
)

jd_input = st.text_area(
    "Enter JD Skills (comma-separated):",
    "Python, Deep Learning, Data Visualization, SQL, Problem Solving"
)

if st.button("Compute Similarity"):
    # Split into skill lists
    resume_skills = [s.strip() for s in resume_input.split(",") if s.strip()]
    jd_skills = [s.strip() for s in jd_input.split(",") if s.strip()]

    if not resume_skills or not jd_skills:
        st.warning("Please enter at least one skill in both fields.")
    else:
        # ------------------------------
        # 3. Embedding Generation
        # ------------------------------
        resume_embeddings = model.encode(resume_skills)
        jd_embeddings = model.encode(jd_skills)

        # ------------------------------
        # 4. Similarity Matrix
        # ------------------------------
        similarity_matrix = cosine_similarity(resume_embeddings, jd_embeddings)

        # ------------------------------
        # 5. Top-3 Matches for Each Resume Skill
        # ------------------------------
        results = []
        for i, res_skill in enumerate(resume_skills):
            sim_scores = list(enumerate(similarity_matrix[i]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:3]

            for idx, score in sim_scores:
                results.append({
                    "Resume Skill": res_skill,
                    "JD Match": jd_skills[idx],
                    "Similarity Score": round(float(score), 3)
                })

        df_results = pd.DataFrame(results)

        # ------------------------------
        # 6. Display Results
        # ------------------------------
        st.subheader("📊 Top Matches (Resume → JD Skills)")
        st.dataframe(df_results)
