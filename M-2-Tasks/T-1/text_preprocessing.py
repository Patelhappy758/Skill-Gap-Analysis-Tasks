"""
Text Preprocessing Streamlit Application
"""

import re
import spacy
import streamlit as st

# Load spaCy English model
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


def clean_resume_text(text):
    """Clean resume text by removing emails, phone numbers, URLs, and special characters."""
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    # Remove phone numbers (various formats)
    text = re.sub(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}', '', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Keep only alphanumeric characters and allowed special characters (+ # - .)
    text = re.sub(r'[^a-zA-Z0-9\s+#\-.]', ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def tokenize_text(text):
    """Tokenize text using spaCy."""
    doc = nlp(text)
    tokens = [token.text for token in doc]
    return tokens


def remove_stop_words(text):
    """Remove stop words while preserving programming language names."""
    # Programming languages to preserve
    preserve_words = {'c', 'r', 'go', 'd'}
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Filter tokens: keep non-stop words or preserved programming languages
    filtered_tokens = []
    for token in doc:
        # Check if token is a preserved word (case-insensitive check, but keep original case)
        if token.text.lower() in preserve_words:
            filtered_tokens.append(token.text)
        # Keep non-stop words that are not punctuation or whitespace
        elif not token.is_stop and not token.is_punct and not token.is_space:
            filtered_tokens.append(token.text)
    
    return ' '.join(filtered_tokens)


def lemmatize_text(text):
    """Lemmatize text to convert words to their base form."""
    doc = nlp(text)
    
    # Get lemma for each token, excluding punctuation and whitespace
    lemmas = []
    for token in doc:
        if not token.is_space:
            lemmas.append(token.lemma_)
    
    return ' '.join(lemmas)


# Streamlit App
def main():
    st.set_page_config(page_title="Text Preprocessing Tool", page_icon="📝", layout="wide")
    
    st.title("📝 Text Preprocessing Tool")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.markdown(
        """
        <div style="
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 18px 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            font-size: 16px;
            color: #333;
        ">
        <b>Text Preprocessing Tool</b> provides essential functions for NLP tasks:<br><br>
        <ul style="padding-left: 18px;">
            <li><b>Basic Text Cleaning</b></li>
            <li><b>Tokenization</b></li>
            <li><b>Stop Words Removal</b></li>
            <li><b>Lemmatization</b></li>
        </ul>
        <span style="color: #888;">Built with <b>Streamlit</b> & <b>spaCy</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Main content - Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧹 Basic Text Cleaning",
        "✂️ Tokenization",
        "🚫 Stop Words Removal",
        "🔤 Lemmatization"
    ])
    
    # Tab 1: Basic Text Cleaning
    with tab1:
        st.header("Basic Text Cleaning")
        st.markdown("Removes emails, phone numbers, URLs, and special characters (except + # - .)")
        
        default_text1 = """Contact: john@email.com | Phone: +1-555-0123
Visit: www.johndoe.com
Skills: Python, C++, C#, .NET"""
        
        input_text1 = st.text_area(
            "Enter text to clean:",
            value=default_text1,
            height=150,
            key="clean_input"
        )
        
        if st.button("Clean Text", key="clean_btn"):
            if input_text1:
                result = clean_resume_text(input_text1)
                st.success("Cleaned Text:")
                st.code(result, language=None)
            else:
                st.warning("Please enter some text to clean.")
    
    # Tab 2: Tokenization
    with tab2:
        st.header("Tokenization")
        st.markdown("Splits text into individual tokens using spaCy")
        
        default_text2 = "I'm a Python developer. I've worked on ML projects."
        
        input_text2 = st.text_area(
            "Enter text to tokenize:",
            value=default_text2,
            height=100,
            key="token_input"
        )
        
        if st.button("Tokenize", key="token_btn"):
            if input_text2:
                tokens = tokenize_text(input_text2)
                st.success(f"Tokens ({len(tokens)} total):")
                st.code(str(tokens), language="python")
            else:
                st.warning("Please enter some text to tokenize.")
    
    # Tab 3: Stop Words Removal
    with tab3:
        st.header("Stop Words Removal")
        st.markdown("Removes common stop words while preserving programming languages (C, R, Go, D)")
        
        default_text3 = "I have experience in Python and R programming with excellent skills in C and Go"
        
        input_text3 = st.text_area(
            "Enter text:",
            value=default_text3,
            height=100,
            key="stopword_input"
        )
        
        if st.button("Remove Stop Words", key="stopword_btn"):
            if input_text3:
                result = remove_stop_words(input_text3)
                st.success("Text after removing stop words:")
                st.code(result, language=None)
            else:
                st.warning("Please enter some text.")
    
    # Tab 4: Lemmatization
    with tab4:
        st.header("Lemmatization")
        st.markdown("Converts words to their base form")
        
        default_text4 = "I am working on developing multiple applications using programming languages"
        
        input_text4 = st.text_area(
            "Enter text to lemmatize:",
            value=default_text4,
            height=100,
            key="lemma_input"
        )
        
        if st.button("Lemmatize", key="lemma_btn"):
            if input_text4:
                result = lemmatize_text(input_text4)
                st.success("Lemmatized Text:")
                st.code(result, language=None)
            else:
                st.warning("Please enter some text to lemmatize.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Text Preprocessing Tool | Built with Streamlit & spaCy"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()