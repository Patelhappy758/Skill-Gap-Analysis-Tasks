"""
POS Tagging Streamlit Application
"""

import spacy
import streamlit as st
from collections import Counter

# Load spaCy English model
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


def pos_tag_resume(text):
    """
    Tag each word with its Part of Speech.
    
    Args:
        text (str): Input text to tag
        
    Returns:
        list: List of tuples (word, POS_tag)
    """
    doc = nlp(text)
    
    # Extract word and POS tag, excluding punctuation and whitespace
    pos_tags = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            pos_tags.append((token.text, token.pos_))
    
    return pos_tags


def extract_nouns(text):
    """
    Extract all nouns and proper nouns from text.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of nouns (potential skills)
    """
    doc = nlp(text)
    
    # Extract NOUN and PROPN (proper nouns)
    nouns = []
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN']:
            nouns.append(token.text)
    
    return nouns


def find_adj_noun_patterns(text):
    """
    Find Adjective + Noun patterns (skill patterns).
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of adjective-noun patterns
    """
    doc = nlp(text)
    patterns = []
    
    # Iterate through tokens to find ADJ + NOUN patterns
    for i in range(len(doc) - 1):
        current_token = doc[i]
        next_token = doc[i + 1]
        
        # Check for Adjective followed by Noun or Proper Noun
        if current_token.pos_ == 'ADJ' and next_token.pos_ in ['NOUN', 'PROPN']:
            patterns.append(f"{current_token.text} {next_token.text}")
        
        # Check for Proper Noun followed by Noun/Proper Noun (e.g., "Machine Learning")
        elif current_token.pos_ == 'PROPN' and next_token.pos_ in ['NOUN', 'PROPN']:
            patterns.append(f"{current_token.text} {next_token.text}")
    
    return patterns


# Streamlit App
def main():
    st.set_page_config(
        page_title="POS Tagging Tool", 
        page_icon="🏷️", 
        layout="wide"
    )
    
    st.title("🏷️ Part-of-Speech (POS) Tagging Tool")
    st.markdown("### Advanced text analysis for resume screening and skill extraction")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("📖 About POS Tagging")
    st.sidebar.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            border-radius: 12px;
            padding: 18px 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            font-size: 16px;
            color: #222;
        ">
        <b>POS Tagging</b> identifies the grammatical role of each word:<br><br>
        <ul style="padding-left: 18px;">
            <li><b>NOUN</b>: Thing/concept (developer, programming)</li>
            <li><b>PROPN</b>: Proper noun (Python, John)</li>
            <li><b>ADJ</b>: Adjective (experienced, skilled)</li>
            <li><b>VERB</b>: Action (develop, create)</li>
            <li><b>AUX</b>: Auxiliary verb (is, has)</li>
            <li><b>DET</b>: Determiner (a, an, the)</li>
        </ul>
        <span style="color: #888;">Built with <b>Streamlit</b> & <b>spaCy</b></span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("💡 Use Cases")
    st.sidebar.markdown(
        "• Resume skill extraction\n"
        "• Job matching systems\n"
        "• Text classification\n"
        "• Information retrieval"
    )
    
    # Main content - Tabs
    tab1, tab2, tab3 = st.tabs([
        "🏷️ Basic POS Tagging",
        "📝 Extract Nouns",
        "🎯 Skill Patterns (ADJ+NOUN)"
    ])
    
    # Tab 1: Basic POS Tagging
    with tab1:
        st.header("Basic POS Tagging")
        st.markdown("Tags each word with its grammatical category")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            default_text1 = "John is an experienced Python developer"
            
            input_text1 = st.text_area(
                "Enter text to tag:",
                value=default_text1,
                height=100,
                key="pos_input"
            )
            
            if st.button("Tag POS", key="pos_btn"):
                if input_text1:
                    result = pos_tag_resume(input_text1)
                    
                    st.success("✅ POS Tags:")
                    st.code(str(result), language="python")
                    
                    # Display in table format
                    st.markdown("#### 📊 Detailed View:")
                    import pandas as pd
                    df = pd.DataFrame(result, columns=['Word', 'POS Tag'])
                    st.dataframe(df, use_container_width=True)
                    
                    # POS Distribution
                    pos_counts = Counter([pos for _, pos in result])
                    st.markdown("#### 📈 POS Distribution:")
                    st.bar_chart(pos_counts)
                    
                else:
                    st.warning("⚠️ Please enter some text to tag.")
        
        with col2:
            st.markdown("#### 🔍 Common POS Tags:")
            st.markdown("""
            - **PROPN**: Proper noun (names)
            - **NOUN**: Common noun
            - **VERB**: Verb
            - **ADJ**: Adjective
            - **AUX**: Auxiliary verb
            - **DET**: Determiner
            - **ADP**: Adposition
            - **PRON**: Pronoun
            - **ADV**: Adverb
            """)
    
    # Tab 2: Extract Nouns
    with tab2:
        st.header("Extract Nouns (Potential Skills)")
        st.markdown("Identifies nouns and proper nouns - often representing skills and technologies")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            default_text2 = "Experienced Data Scientist proficient in Machine Learning and Python programming"
            
            input_text2 = st.text_area(
                "Enter text:",
                value=default_text2,
                height=120,
                key="noun_input"
            )
            
            if st.button("Extract Nouns", key="noun_btn"):
                if input_text2:
                    nouns = extract_nouns(input_text2)
                    
                    st.success(f"✅ Found {len(nouns)} nouns:")
                    st.code(str(nouns), language="python")
                    
                    # Display as tags (styled cards)
                    st.markdown("#### 🏷️ Extracted Skills/Terms:")
                    noun_html = ""
                    for noun in nouns:
                        noun_html += (
                            f'<div style="'
                            f'background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);'
                            f'color: white; padding: 8px 18px; margin: 6px 4px; border-radius: 18px; '
                            f'display: inline-block; font-size: 15px; font-weight: 500; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'
                            f'letter-spacing: 0.5px;">'
                            f'🏷️ {noun}'
                            f'</div>'
                        )
                    st.markdown(noun_html, unsafe_allow_html=True)
                    
                    # Noun frequency
                    if nouns:
                        noun_counts = Counter(nouns)
                        st.markdown("#### 📊 Noun Frequency:")
                        import pandas as pd
                        freq_df = pd.DataFrame(noun_counts.most_common(), columns=['Noun', 'Count'])
                        st.dataframe(freq_df, use_container_width=True)
                    
                else:
                    st.warning("⚠️ Please enter some text.")
        
        with col2:
            st.markdown("#### 💡 Why Extract Nouns?")
            st.info(
                "Nouns often represent:\n\n"
                "• **Skills**: Python, JavaScript\n"
                "• **Technologies**: TensorFlow, React\n"
                "• **Roles**: Developer, Scientist\n"
                "• **Domains**: Machine, Learning\n\n"
                "Perfect for resume screening!"
            )
    
    # Tab 3: Skill Patterns
    with tab3:
        st.header("Identify Skill Patterns (Adjective + Noun)")
        st.markdown("Finds meaningful skill combinations like 'Machine Learning' and 'Deep Learning'")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            default_text3 = "Expert in Machine Learning, Deep Learning, and Natural Language Processing"
            
            input_text3 = st.text_area(
                "Enter text:",
                value=default_text3,
                height=120,
                key="pattern_input"
            )
            
            if st.button("Find Patterns", key="pattern_btn"):
                if input_text3:
                    patterns = find_adj_noun_patterns(input_text3)
                    
                    st.success(f"✅ Found {len(patterns)} skill patterns:")
                    st.code(str(patterns), language="python")
                    
                    # Display as highlighted cards
                    if patterns:
                        st.markdown("#### 🎯 Identified Skills:")
                        for pattern in patterns:
                            st.markdown(
                                f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                                f'color: white; padding: 15px; margin: 10px 0; border-radius: 10px; '
                                f'font-weight: bold; font-size: 16px;">'
                                f'🔹 {pattern}'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                        
                        # Pattern analysis
                        st.markdown("#### 📊 Pattern Analysis:")
                        doc = nlp(input_text3)
                        pattern_details = []
                        for pattern in patterns:
                            words = pattern.split()
                            pattern_details.append({
                                'Pattern': pattern,
                                'First Word': words[0],
                                'Second Word': words[1] if len(words) > 1 else '',
                                'Type': 'Skill/Technology'
                            })
                        
                        import pandas as pd
                        pattern_df = pd.DataFrame(pattern_details)
                        st.dataframe(pattern_df, use_container_width=True)
                    else:
                        st.info("No ADJ+NOUN patterns found. Try text with phrases like 'Machine Learning' or 'Artificial Intelligence'.")
                    
                else:
                    st.warning("⚠️ Please enter some text.")
        
        with col2:
            st.markdown("#### 🔍 Pattern Types:")
            st.info(
                "**ADJ + NOUN patterns:**\n\n"
                "• Machine Learning\n"
                "• Deep Learning\n"
                "• Artificial Intelligence\n"
                "• Natural Language\n\n"
                "**PROPN + NOUN patterns:**\n\n"
                "• Python programming\n"
                "• Data Science\n"
                "• Web Development"
            )
            
            st.markdown("#### ⚡ Pro Tip:")
            st.success(
                "These patterns are excellent for:\n"
                "• Skill extraction from resumes\n"
                "• Job requirement matching\n"
                "• Automated screening"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; padding: 20px;'>"
        "🏷️ POS Tagging Tool | Built with Streamlit & spaCy | "
        "Powered by Natural Language Processing"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
