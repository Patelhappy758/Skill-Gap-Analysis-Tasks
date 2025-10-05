import streamlit as st
import json
import pandas as pd
from io import BytesIO
import re
from collections import Counter

# Check for plotly availability
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not installed. Visualizations will use Streamlit native charts. Install with: pip install plotly")

# Initialize session state
if 'extracted_skills' not in st.session_state:
    st.session_state['extracted_skills'] = None
if 'original_text' not in st.session_state:
    st.session_state['original_text'] = None
if 'all_skills_list' not in st.session_state:
    st.session_state['all_skills_list'] = []

# Skill Database
SKILL_DATABASE = {
    'programming_languages': [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 
        'Ruby', 'Go', 'PHP', 'Swift', 'Kotlin',
        'TypeScript', 'Rust', 'Scala', 'R', 'MATLAB'
    ],
    'frameworks': [
        'TensorFlow', 'React', 'Django', 'Flask', 'Angular',
        'Vue.js', 'Spring Boot', 'Node.js', 'Express.js', 'PyTorch',
        'Keras', 'FastAPI', 'jQuery', 'Bootstrap', 'Next.js'
    ],
    'databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis',
        'SQLite', 'Cassandra', 'DynamoDB', 'MariaDB', 'Elasticsearch'
    ],
    'cloud': [
        'AWS', 'Azure', 'Google Cloud Platform', 'GCP', 'IBM Cloud',
        'Heroku', 'DigitalOcean', 'Oracle Cloud', 'Alibaba Cloud'
    ],
    'soft_skills': [
        'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
        'Critical Thinking', 'Time Management', 'Adaptability',
        'Collaboration', 'Creativity', 'Project Management'
    ],
    'tools': [
        'Git', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform',
        'Ansible', 'Jira', 'Slack', 'VS Code', 'IntelliJ'
    ]
}

# Abbreviation Mapping
ABBREVIATIONS = {
    'ML': 'Machine Learning',
    'DL': 'Deep Learning',
    'NLP': 'Natural Language Processing',
    'JS': 'JavaScript',
    'K8s': 'Kubernetes',
    'AWS': 'AWS',
    'GCP': 'Google Cloud Platform',
    'SQL': 'Structured Query Language',
    'API': 'Application Programming Interface',
    'CI/CD': 'Continuous Integration/Continuous Deployment',
    'OOP': 'Object Oriented Programming',
    'REST': 'Representational State Transfer',
    'AI': 'Artificial Intelligence',
    'UI': 'User Interface',
    'UX': 'User Experience',
    'DB': 'Database',
    'TS': 'TypeScript',
    'CV': 'Computer Vision',
    'DS': 'Data Science',
    'DevOps': 'Development Operations'
}

# Synonyms for better matching
SYNONYMS = {
    'Python': ['Python3', 'Python 3', 'py'],
    'JavaScript': ['JS', 'ECMAScript', 'ES6', 'ES2020'],
    'Machine Learning': ['ML', 'Statistical Learning'],
    'Kubernetes': ['K8s', 'k8s'],
    'PostgreSQL': ['Postgres', 'psql'],
    'MongoDB': ['Mongo'],
    'Node.js': ['NodeJS', 'Node'],
}

# Skill relationships for recommendations
SKILL_RELATIONSHIPS = {
    'Python': ['Django', 'Flask', 'FastAPI', 'TensorFlow', 'PyTorch'],
    'JavaScript': ['React', 'Angular', 'Vue.js', 'Node.js', 'Express.js'],
    'Java': ['Spring Boot'],
    'AWS': ['Docker', 'Kubernetes', 'Terraform'],
    'Machine Learning': ['Python', 'TensorFlow', 'PyTorch', 'Keras'],
    'React': ['JavaScript', 'Node.js', 'Redux'],
    'Docker': ['Kubernetes', 'AWS', 'Jenkins']
}


def fuzzy_match_skill(text_lower, skill, threshold=0.85):
    """Simple fuzzy matching based on substring and similarity"""
    skill_lower = skill.lower()
    
    # Exact match
    if skill_lower in text_lower:
        return True
    
    # Check synonyms
    if skill in SYNONYMS:
        for synonym in SYNONYMS[skill]:
            if synonym.lower() in text_lower:
                return True
    
    # Check if skill is mentioned with version numbers or variations
    pattern = re.escape(skill_lower) + r'[\d\.\s]*'
    if re.search(pattern, text_lower):
        return True
    
    return False


def extract_skills(text, skill_database):
    """Enhanced skill extraction with fuzzy matching and context"""
    text_lower = text.lower()
    found_skills = {}
    skill_contexts = {}
    all_skills = []
    
    for category, skills in skill_database.items():
        found_in_category = []
        contexts = {}
        
        for skill in skills:
            if fuzzy_match_skill(text_lower, skill):
                found_in_category.append(skill)
                all_skills.append(skill)
                
                # Extract context (surrounding words)
                skill_pattern = re.escape(skill.lower())
                matches = re.finditer(skill_pattern, text_lower)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    contexts[skill] = context
        
        if found_in_category:
            found_skills[category] = found_in_category
            skill_contexts[category] = contexts
    
    return found_skills, skill_contexts, all_skills


def normalize_skills(skill_list):
    """Converts skill abbreviations to their full names"""
    normalized = []
    
    for skill in skill_list:
        if skill in ABBREVIATIONS:
            normalized.append(ABBREVIATIONS[skill])
        else:
            normalized.append(skill)
    
    return normalized


def recommend_related_skills(found_skills):
    """Recommend related skills based on what was found"""
    recommendations = set()
    
    for category, skills in found_skills.items():
        for skill in skills:
            if skill in SKILL_RELATIONSHIPS:
                for related in SKILL_RELATIONSHIPS[skill]:
                    # Only recommend if not already found
                    already_found = False
                    for found_category, found_list in found_skills.items():
                        if related in found_list:
                            already_found = True
                            break
                    if not already_found:
                        recommendations.add(related)
    
    return list(recommendations)


def calculate_skill_match(candidate_skills, job_requirements):
    """Calculate match percentage between candidate and job requirements"""
    all_candidate_skills = []
    for skills in candidate_skills.values():
        all_candidate_skills.extend(skills)
    
    all_required_skills = []
    for skills in job_requirements.values():
        all_required_skills.extend(skills)
    
    if not all_required_skills:
        return 0, [], []
    
    matched = [skill for skill in all_required_skills if skill in all_candidate_skills]
    missing = [skill for skill in all_required_skills if skill not in all_candidate_skills]
    
    match_percentage = (len(matched) / len(all_required_skills)) * 100
    
    return match_percentage, matched, missing


def create_skill_visualization(found_skills):
    """Create visualizations for extracted skills"""
    # Prepare data
    categories = []
    counts = []
    
    for category, skills in found_skills.items():
        categories.append(category.replace('_', ' ').title())
        counts.append(len(skills))
    
    if PLOTLY_AVAILABLE:
        # Create bar chart
        fig_bar = px.bar(
            x=categories, 
            y=counts,
            labels={'x': 'Skill Category', 'y': 'Number of Skills'},
            title='Skills by Category',
            color=counts,
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(showlegend=False)
        
        # Create pie chart
        fig_pie = px.pie(
            values=counts,
            names=categories,
            title='Skill Distribution',
            hole=0.3
        )
        
        return fig_bar, fig_pie
    else:
        # Fallback to streamlit native charts
        df = pd.DataFrame({
            'Category': categories,
            'Count': counts
        })
        return df, df


def create_skill_radar(found_skills):
    """Create radar chart for skill profile"""
    categories = []
    values = []
    
    all_categories = list(SKILL_DATABASE.keys())
    
    for category in all_categories:
        cat_name = category.replace('_', ' ').title()
        categories.append(cat_name)
        
        if category in found_skills:
            values.append(len(found_skills[category]))
        else:
            values.append(0)
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Skills'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(values) + 2])),
            showlegend=False,
            title='Skill Profile Radar'
        )
        
        return fig
    else:
        # Fallback to dataframe
        df = pd.DataFrame({
            'Category': categories,
            'Count': values
        })
        return df


def export_to_excel(found_skills):
    """Export skills to Excel format"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Create summary sheet
        summary_data = []
        for category, skills in found_skills.items():
            for skill in skills:
                summary_data.append({
                    'Category': category.replace('_', ' ').title(),
                    'Skill': skill
                })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Skills Summary', index=False)
        
        # Create category breakdown sheets
        for category, skills in found_skills.items():
            df_category = pd.DataFrame({'Skill': skills})
            sheet_name = category.replace('_', ' ').title()[:31]  # Excel sheet name limit
            df_category.to_excel(writer, sheet_name=sheet_name, index=False)
    
    output.seek(0)
    return output


# Streamlit App Configuration
st.set_page_config(
    page_title="Advanced Skill Extraction System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    st.markdown("---")
    st.subheader("About")
    st.info(
        "Advanced Skill Extraction System with:\n\n"
        "✅ Fuzzy Matching\n"
        "✅ Skill Gap Analysis\n"
        "✅ Interactive Visualizations\n"
        "✅ Recommendations\n"
        "✅ Excel Export"
    )
    
    st.markdown("---")
    st.subheader("📊 Database Stats")
    total_skills = sum(len(skills) for skills in SKILL_DATABASE.values())
    st.metric("Total Skills", total_skills)
    st.metric("Categories", len(SKILL_DATABASE))
    st.metric("Abbreviations", len(ABBREVIATIONS))
    
    # Show extraction status
    st.markdown("---")
    st.subheader("📍 Status")
    if st.session_state['extracted_skills']:
        st.success("✅ Skills Extracted")
        total_extracted = sum(len(v) for v in st.session_state['extracted_skills'].values())
        st.info(f"Found: {total_extracted} skills")
    else:
        st.warning("⚠️ No skills extracted yet")
        st.write("Go to 'Extract Skills' tab")

# Main Title
st.markdown('<div class="main-header">🎯 Advanced Skill Extraction System</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Database", 
    "🔍 Extract Skills", 
    "🔄 Normalizer", 
    "📈 Gap Analysis",
    "💡 Recommendations"
])

# Tab 1: Skill Database
with tab1:
    st.header("Skill Database Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("💻 Technical Skills")
        with st.expander("Programming Languages", expanded=True):
            for lang in SKILL_DATABASE['programming_languages']:
                st.write(f"• {lang}")
        
        with st.expander("Frameworks/Libraries"):
            for framework in SKILL_DATABASE['frameworks']:
                st.write(f"• {framework}")
    
    with col2:
        st.subheader("🗄️ Data & Cloud")
        with st.expander("Databases", expanded=True):
            for db in SKILL_DATABASE['databases']:
                st.write(f"• {db}")
        
        with st.expander("Cloud Platforms"):
            for cloud in SKILL_DATABASE['cloud']:
                st.write(f"• {cloud}")
    
    with col3:
        st.subheader("🛠️ Tools & Soft Skills")
        with st.expander("Tools", expanded=True):
            for tool in SKILL_DATABASE['tools']:
                st.write(f"• {tool}")
        
        with st.expander("Soft Skills"):
            for skill in SKILL_DATABASE['soft_skills']:
                st.write(f"• {skill}")

# Tab 2: Extract Skills
with tab2:
    st.header("🔍 Intelligent Skill Extraction")
    st.write("Extract skills from job descriptions or resumes. These skills will be used across all other tabs.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_text = """Senior Software Engineer with 8+ years of experience.
        
Expert in Python, Java, and JavaScript development. Strong background in ML 
and DL using TensorFlow and PyTorch. Proficient in building scalable web 
applications with React, Django, and Node.js.

Cloud Infrastructure: Extensive experience with AWS, Docker, and K8s.
Database Management: PostgreSQL, MongoDB, Redis, and MySQL.

Soft Skills: Strong leadership, excellent communication, and problem-solving abilities.
Team player with proven project management experience."""
        
        text_input = st.text_area(
            "Enter Job Description or Resume:",
            value=default_text,
            height=250,
            help="Paste job description, resume, or any text containing skills. These extracted skills will be used in all other tabs."
        )
        
        extract_button = st.button("🔍 Extract Skills", type="primary", use_container_width=True)
    
    with col2:
        st.info(
            "**Features:**\n\n"
            "✓ Fuzzy matching\n"
            "✓ Synonym detection\n"
            "✓ Context extraction\n"
            "✓ Visual analytics\n"
            "✓ Excel export\n\n"
            "**Note:** Extracted skills will be automatically used in Normalizer, Gap Analysis, and Recommendations tabs."
        )
    
    if extract_button and text_input.strip():
        with st.spinner("🔄 Analyzing text and extracting skills..."):
            results, contexts, all_skills = extract_skills(text_input, SKILL_DATABASE)
            
            # Store in session state
            st.session_state['extracted_skills'] = results
            st.session_state['original_text'] = text_input
            st.session_state['all_skills_list'] = all_skills
            
            if results:
                total_found = sum(len(v) for v in results.values())
                st.success(f"✅ Found {total_found} skills across {len(results)} categories!")
                st.info("💡 These skills are now available in Normalizer, Gap Analysis, and Recommendations tabs.")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                metrics = [
                    ("Total Skills", total_found, "🎯"),
                    ("Categories", len(results), "📊"),
                    ("Technical", sum(len(results.get(k, [])) for k in ['programming_languages', 'frameworks', 'databases', 'cloud', 'tools']), "💻"),
                    ("Soft Skills", len(results.get('soft_skills', [])), "🤝")
                ]
                
                for col, (label, value, icon) in zip([col1, col2, col3, col4], metrics):
                    with col:
                        st.metric(f"{icon} {label}", value)
                
                st.markdown("---")
                
                # Skills by Category
                st.subheader("📋 Extracted Skills by Category")
                for category, skills in results.items():
                    category_display = category.replace('_', ' ').title()
                    
                    with st.expander(f"{category_display} ({len(skills)} found)", expanded=True):
                        cols = st.columns(3)
                        for idx, skill in enumerate(skills):
                            with cols[idx % 3]:
                                st.write(f"✓ **{skill}**")
                
                # Visualizations
                st.markdown("---")
                st.subheader("📊 Visual Analytics")
                
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    fig_bar, fig_pie = create_skill_visualization(results)
                    if PLOTLY_AVAILABLE:
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.subheader("Skills by Category")
                        st.bar_chart(fig_bar.set_index('Category'))
                
                with viz_col2:
                    if PLOTLY_AVAILABLE:
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.subheader("Skill Distribution")
                        st.bar_chart(fig_pie.set_index('Category'))
                
                # Radar Chart
                radar_fig = create_skill_radar(results)
                if PLOTLY_AVAILABLE:
                    st.plotly_chart(radar_fig, use_container_width=True)
                else:
                    st.subheader("Skill Profile")
                    st.bar_chart(radar_fig.set_index('Category'))
                
                # Export Options
                st.markdown("---")
                st.subheader("📥 Export Options")
                
                export_col1, export_col2 = st.columns(2)
                
                with export_col1:
                    # JSON Export
                    json_data = json.dumps(results, indent=2)
                    st.download_button(
                        label="📄 Download JSON",
                        data=json_data,
                        file_name="extracted_skills.json",
                        mime="application/json"
                    )
                
                with export_col2:
                    # Excel Export
                    excel_data = export_to_excel(results)
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_data,
                        file_name="extracted_skills.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("⚠️ No skills found. Try adding more technical terms or skills.")

# Tab 3: Skill Normalizer
with tab3:
    st.header("🔄 Skill Abbreviation Normalizer")
    
    if not st.session_state['extracted_skills']:
        st.warning("⚠️ Please extract skills first in the 'Extract Skills' tab!")
        st.info("👈 Go to 'Extract Skills' tab and analyze a job description or resume.")
    else:
        st.success("✅ Using extracted skills from previous step")
        
        # Show original text snippet
        with st.expander("📄 View Original Text", expanded=False):
            st.text_area("Original Text:", st.session_state['original_text'], height=150, disabled=True)
        
        with st.expander("📚 View All Abbreviation Mappings", expanded=False):
            abbrev_df = pd.DataFrame(
                list(ABBREVIATIONS.items()),
                columns=['Abbreviation', 'Full Name']
            )
            st.dataframe(abbrev_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Extracted Skills (Ready for Normalization)")
        
        # Get all skills from extracted results
        all_extracted_skills = st.session_state['all_skills_list']
        
        st.info(f"Found {len(all_extracted_skills)} skills to normalize")
        
        # Display extracted skills
        with st.expander("View All Extracted Skills", expanded=True):
            skill_cols = st.columns(4)
            for idx, skill in enumerate(all_extracted_skills):
                with skill_cols[idx % 4]:
                    st.write(f"• {skill}")
        
        if st.button("🔄 Normalize All Extracted Skills", type="primary", use_container_width=True):
            with st.spinner("Normalizing skills..."):
                normalized = normalize_skills(all_extracted_skills)
                
                st.success(f"✅ Normalized {len(all_extracted_skills)} skills!")
                
                # Check which ones changed
                changes = sum(1 for o, n in zip(all_extracted_skills, normalized) if o != n)
                st.info(f"🔄 {changes} abbreviations were expanded")
                
                # Comparison Table
                comparison_df = pd.DataFrame({
                    'Original': all_extracted_skills,
                    'Normalized': normalized,
                    'Changed': ['✓' if o != n else '−' for o, n in zip(all_extracted_skills, normalized)]
                })
                
                st.dataframe(comparison_df, use_container_width=True)
                
                # Side by side comparison
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Skills")
                    for skill in all_extracted_skills:
                        symbol = "🔤" if skill in ABBREVIATIONS else "•"
                        st.write(f"{symbol} {skill}")
                
                with col2:
                    st.subheader("Normalized Skills")
                    for i, skill in enumerate(normalized):
                        if all_extracted_skills[i] != skill:
                            st.write(f"✨ **{skill}**")
                        else:
                            st.write(f"• {skill}")

# Tab 4: Gap Analysis
with tab4:
    st.header("📈 Skill Gap Analysis")
    
    if not st.session_state['extracted_skills']:
        st.warning("⚠️ Please extract skills first in the 'Extract Skills' tab!")
        st.info("👈 Go to 'Extract Skills' tab and analyze a job description or resume.")
    else:
        st.success("✅ Using extracted skills from the job description")
        st.write("Compare candidate resume against the extracted job requirements to identify gaps and matches.")
        
        # Show job requirements
        with st.expander("📋 Job Requirements (Extracted)", expanded=False):
            job_skills = st.session_state['extracted_skills']
            for category, skills in job_skills.items():
                st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(skills)}")
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("👤 Candidate Resume")
            candidate_text = st.text_area(
                "Enter candidate resume/profile:",
                value="Proficient in Python, React, and MongoDB. Experience with AWS and Docker. Strong communication and teamwork skills.",
                height=200,
                key="candidate"
            )
        
        with col2:
            st.info(
                "**Job Requirements:**\n\n"
                f"Total Skills: {sum(len(v) for v in st.session_state['extracted_skills'].values())}\n\n"
                "The candidate will be compared against these requirements."
            )
        
        if st.button("🔍 Analyze Gap", type="primary", use_container_width=True):
            with st.spinner("Analyzing skill gap..."):
                candidate_skills, _, _ = extract_skills(candidate_text, SKILL_DATABASE)
                job_requirements = st.session_state['extracted_skills']
                
                match_percentage, matched, missing = calculate_skill_match(
                    candidate_skills, 
                    job_requirements
                )
                
                # Display match percentage
                st.markdown("---")
                st.subheader("📊 Match Analysis")
                
                # Progress bar with color
                if match_percentage >= 75:
                    color = "green"
                    status = "Excellent Match! 🎉"
                elif match_percentage >= 50:
                    color = "orange"
                    status = "Good Match 👍"
                else:
                    color = "red"
                    status = "Needs Improvement 📚"
                
                st.markdown(f"### {status}")
                st.progress(match_percentage / 100)
                st.markdown(f"<h2 style='text-align: center; color: {color};'>{match_percentage:.1f}% Match</h2>", unsafe_allow_html=True)
                
                # Detailed breakdown
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("✅ Matched Skills", len(matched))
                with col2:
                    st.metric("❌ Missing Skills", len(missing))
                with col3:
                    total_required = len(matched) + len(missing)
                    st.metric("📋 Total Required", total_required)
                
                # Matched Skills
                if matched:
                    st.markdown("---")
                    st.subheader("✅ Matched Skills")
                    matched_cols = st.columns(4)
                    for idx, skill in enumerate(matched):
                        with matched_cols[idx % 4]:
                            st.success(f"✓ {skill}")
                
                # Missing Skills
                if missing:
                    st.markdown("---")
                    st.subheader("❌ Missing Skills (Required in Job)")
                    missing_cols = st.columns(4)
                    for idx, skill in enumerate(missing):
                        with missing_cols[idx % 4]:
                            st.error(f"✗ {skill}")
                
                # Recommendations
                if missing:
                    st.markdown("---")
                    st.subheader("💡 Learning Recommendations")
                    st.info(
                        f"To improve your match score, consider learning: "
                        f"{', '.join(missing[:5])}{'...' if len(missing) > 5 else ''}"
                    )

# Tab 5: Recommendations
with tab5:
    st.header("💡 Skill Recommendations")
    
    if not st.session_state['extracted_skills']:
        st.warning("⚠️ Please extract skills first in the 'Extract Skills' tab!")
        st.info("👈 Go to 'Extract Skills' tab and analyze a job description or resume.")
    else:
        found_skills = st.session_state['extracted_skills']
        
        st.success("✅ Using extracted skills from the job description")
        st.write("Get personalized skill recommendations based on the extracted skillset and identify missing skills from the database.")
        
        # Show current skills
        with st.expander("📋 Current Skills from Job Description", expanded=False):
            for category, skills in found_skills.items():
                st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(skills)}")
        
        st.markdown("---")
        st.subheader("📊 Skills Overview")
        total = sum(len(skills) for skills in found_skills.values())
        
        # Calculate total possible skills
        total_possible = sum(len(skills) for skills in SKILL_DATABASE.values())
        coverage_percentage = (total / total_possible) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Skills", total)
        with col2:
            st.metric("Categories", len(found_skills))
        with col3:
            technical = sum(len(found_skills.get(k, [])) for k in ['programming_languages', 'frameworks', 'databases', 'cloud', 'tools'])
            st.metric("Technical Skills", technical)
        with col4:
            st.metric("Coverage", f"{coverage_percentage:.1f}%")
        
        # Calculate missing skills from database
        st.markdown("---")
        st.subheader("❌ Missing Skills from Database")
        st.write("Skills available in the database but not found in your extracted skillset:")
        
        missing_by_category = {}
        total_missing = 0
        
        for category, all_skills in SKILL_DATABASE.items():
            found_in_category = found_skills.get(category, [])
            missing_in_category = [skill for skill in all_skills if skill not in found_in_category]
            if missing_in_category:
                missing_by_category[category] = missing_in_category
                total_missing += len(missing_in_category)
        
        if missing_by_category:
            st.info(f"📊 Found {total_missing} skills in the database that are not in your current skillset")
            
            # Display missing skills by category
            for category, missing_skills in missing_by_category.items():
                category_display = category.replace('_', ' ').title()
                
                with st.expander(f"❌ {category_display} ({len(missing_skills)} missing)", expanded=False):
                    # Show in columns
                    cols = st.columns(4)
                    for idx, skill in enumerate(missing_skills):
                        with cols[idx % 4]:
                            st.write(f"• {skill}")
        else:
            st.success("🎉 Amazing! You have all skills from the database!")
        
        # Get complementary recommendations
        st.markdown("---")
        st.subheader("🎯 Recommended Complementary Skills")
        st.write("Based on your current skillset, consider learning these related skills:")
        
        recommendations = recommend_related_skills(found_skills)
        
        if recommendations:
            # Separate recommendations into found and not found
            recommended_missing = [skill for skill in recommendations if skill in [s for category_skills in missing_by_category.values() for s in category_skills]]
            recommended_present = [skill for skill in recommendations if skill not in recommended_missing]
            
            if recommended_missing:
                st.info(f"💡 {len(recommended_missing)} recommended skills are missing from your skillset")
                
                rec_cols = st.columns(3)
                for idx, skill in enumerate(recommended_missing):
                    with rec_cols[idx % 3]:
                        st.warning(f"⭐ {skill}")
            
            if recommended_present:
                st.success(f"✅ You already have {len(recommended_present)} recommended complementary skills!")
            
            # Show why these are recommended
            st.markdown("---")
            st.subheader("📚 Why These Skills?")
            st.write("Here's how recommended skills complement your current expertise:")
            
            for skill in recommendations[:8]:  # Show top 8
                related_to = []
                for current_skill in [s for skills in found_skills.values() for s in skills]:
                    if current_skill in SKILL_RELATIONSHIPS and skill in SKILL_RELATIONSHIPS[current_skill]:
                        related_to.append(current_skill)
                
                if related_to:
                    # Check if skill is missing
                    is_missing = skill in [s for category_skills in missing_by_category.values() for s in category_skills]
                    icon = "⭐" if is_missing else "💡"
                    
                    with st.expander(f"{icon} {skill}", expanded=False):
                        st.write(f"**Complements:** {', '.join(related_to)}")
                        if is_missing:
                            st.warning("🎯 Priority: This skill is missing from your skillset!")
                        else:
                            st.info("✅ You already have this skill!")
                        st.write("Learning this skill will enhance your expertise in these areas.")
        else:
            st.success("🌟 Great! You have a well-rounded skillset with all complementary skills covered!")
        
        # Show skill relationships
        st.markdown("---")
        st.subheader("🔗 Skill Relationships Map")
        st.write("Common skill pairings found in your skillset:")
        
        relationship_found = False
        for skill in [s for skills in found_skills.values() for s in skills]:
            if skill in SKILL_RELATIONSHIPS:
                relationship_found = True
                with st.expander(f"{skill} ➜ Related Skills"):
                    related = SKILL_RELATIONSHIPS[skill]
                    for rel_skill in related:
                        # Check if related skill is already in the skillset
                        is_present = any(rel_skill in skills_list for skills_list in found_skills.values())
                        if is_present:
                            st.write(f"✅ {rel_skill} (Already in your skillset)")
                        else:
                            st.write(f"📌 {rel_skill} (Recommended to learn)")
        
        if not relationship_found:
            st.info("No specific skill relationships found in the database for your current skills.")
        
        # Priority Learning Path
        st.markdown("---")
        st.subheader("🎓 Priority Learning Path")
        
        if recommendations and missing_by_category:
            priority_skills = [skill for skill in recommendations if skill in [s for category_skills in missing_by_category.values() for s in category_skills]]
            
            if priority_skills:
                st.write("Focus on learning these skills first (ordered by relevance):")
                
                for idx, skill in enumerate(priority_skills[:5], 1):
                    related_to = []
                    for current_skill in [s for skills in found_skills.values() for s in skills]:
                        if current_skill in SKILL_RELATIONSHIPS and skill in SKILL_RELATIONSHIPS[current_skill]:
                            related_to.append(current_skill)
                    
                    st.write(f"**{idx}. {skill}**")
                    if related_to:
                        st.write(f"   ↳ Builds on: {', '.join(related_to)}")
                    st.write("")
            else:
                st.success("✅ All priority skills are covered!")
        else:
            st.success("🎉 You have excellent skill coverage!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p><strong>Advanced Skill Extraction System</strong> | Built with ❤️ using Streamlit</p>
        <p>Features: Fuzzy Matching • Gap Analysis • Visualizations • Recommendations • Excel Export</p>
    </div>
    """,
    unsafe_allow_html=True
)