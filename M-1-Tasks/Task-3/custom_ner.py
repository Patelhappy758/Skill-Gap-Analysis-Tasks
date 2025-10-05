import spacy
from spacy.training.example import Example
import streamlit as st

# -----------------------
# Training data
# -----------------------
TRAIN_DATA = [
    ("I have experience with Python programming.", {"entities": [(21, 27, "SKILL")]}),
    ("Worked on SQL databases and data analysis.", {"entities": [(10, 13, "SKILL"), (29, 42, "SKILL")]}),
    ("Excellent communication and leadership qualities.", {"entities": [(10, 22, "SOFT_SKILL"), (27, 37, "SOFT_SKILL")]}),
    ("Proficient in Java and cloud computing.", {"entities": [(13, 17, "SKILL"), (22, 37, "SKILL")]}),
    ("Good problem solving and critical thinking.", {"entities": [(5, 20, "SOFT_SKILL"), (25, 42, "SOFT_SKILL")]}),
    ("Hands-on experience with Excel and Power BI.", {"entities": [(27, 32, "SKILL"), (37, 45, "SKILL")]}),
    ("Strong teamwork and collaboration skills.", {"entities": [(7, 15, "SOFT_SKILL"), (20, 33, "SOFT_SKILL")]}),
    ("Knowledge of machine learning and deep learning.", {"entities": [(13, 29, "SKILL"), (34, 46, "SKILL")]}),
    ("Skilled in time management and adaptability.", {"entities": [(11, 26, "SOFT_SKILL"), (31, 43, "SOFT_SKILL")]}),
    ("Experienced in project management and Python.", {"entities": [(16, 34, "SOFT_SKILL"), (39, 45, "SKILL")]}),
]

# -----------------------
# Training pipeline
# -----------------------
@st.cache_resource
def train_ner():
    nlp = spacy.blank("en")  # start with a blank English model
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    ner.add_label("SKILL")
    ner.add_label("SOFT_SKILL")

    # Initialize the model
    nlp.initialize()

    for itn in range(30):  # 30 training iterations
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses)
        # Optionally, show progress in Streamlit
        if itn % 10 == 0:
            st.write(f"Iteration {itn} - Losses: {losses}")

    return nlp

st.title("🧠 Custom NER for Resume Skill Extraction")
st.write("This app trains a simple spaCy NER model to extract technical and soft skills from resume text.")

if st.button("Train NER Model"):
    with st.spinner("Training model..."):
        model = train_ner()
    st.success("Model trained!")

    uploaded_file = st.file_uploader("Upload a resume text file", type=["txt"])
    if uploaded_file is not None:
        resume_text = uploaded_file.read().decode("utf-8")
        doc = model(resume_text)
        st.subheader("🎯 Extracted Entities")
        if doc.ents:
            for ent in doc.ents:
                st.write(f"{ent.text}  →  {ent.label_}")
        else:
            st.info("No entities found in the uploaded text.")
else:
    st.info("Click 'Train NER Model' to start.")
