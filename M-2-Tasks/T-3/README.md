# Advanced Skill Extraction System

A Streamlit app for intelligent skill extraction, gap analysis, and recommendations from resumes and job descriptions.

## Features

- 📊 Skill database with categories (programming, frameworks, cloud, tools, soft skills)
- 🔍 Fuzzy skill extraction with synonym and abbreviation support
- 🔄 Skill abbreviation normalization
- 📈 Skill gap analysis between candidate and job requirements
- 💡 Personalized skill recommendations
- 📥 Export results to JSON and Excel
- 🎯 Interactive visualizations (bar, pie, radar charts)

## Installation

1. Clone this repo and navigate to `M-2-Tasks/T-3/`
2. Install dependencies:
   ```sh
   pip install streamlit pandas xlsxwriter plotly
   ```
3. (Optional) For best experience, install all recommended packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the app:
```sh
streamlit run skill_extraction.py
```

## How It Works

- Paste a resume or job description in the "Extract Skills" tab.
- The app extracts skills using fuzzy matching, synonyms, and abbreviations.
- Visualize skills by category and export results.
- Normalize abbreviations in the "Normalizer" tab.
- Compare candidate skills vs job requirements in "Gap Analysis".
- Get personalized recommendations in the "Recommendations" tab.

## File Structure

- `skill_extraction.py` — Main Streamlit app
- `README.md` — This file

## Author

Skill Extraction System

## License

MIT License