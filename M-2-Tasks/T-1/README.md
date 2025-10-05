Text Preprocessing Streamlit Application
An interactive web application for text preprocessing tasks including cleaning, tokenization, stop words removal, and lemmatization.
Features

Basic Text Cleaning: Remove emails, phone numbers, URLs, and special characters
Tokenization: Split text into individual tokens using spaCy
Stop Words Removal: Remove common stop words while preserving programming language names
Lemmatization: Convert words to their base forms
Interactive UI: Easy-to-use Streamlit interface with tabbed navigation

File Structure
text_preprocessing/
│
├── app.py                    # Streamlit application
├── requirements.txt          # Python dependencies
└── README.md                # This file
Installation
Step 1: Install Dependencies
bashpip install -r requirements.txt
Step 2: Download spaCy Language Model
bashpython -m spacy download en_core_web_sm
Running the Application
bashstreamlit run app.py
The application will open in your default web browser at http://localhost:8501
Usage
1. Basic Text Cleaning

Removes email addresses, phone numbers, and URLs
Removes special characters except +, #, -, .
Converts text to lowercase

Example:
Input: Contact: john@email.com | Phone: +1-555-0123
Output: contact phone visit skills python c++ c .net
2. Tokenization

Splits text into individual tokens
Handles contractions properly (I'm → I, am)

Example:
Input: I'm a Python developer. I've worked on ML projects.
Output: ['I', 'am', 'a', 'Python', 'developer', '.', 'I', 'have', 'worked', 'on', 'ML', 'projects', '.']
3. Stop Words Removal

Removes common stop words
Preserves programming language names: C, R, Go, D

Example:
Input: I have experience in Python and R programming with excellent skills in C and Go
Output: experience Python R programming excellent skills C Go
4. Lemmatization

Converts words to their base forms
Useful for text normalization

Example:
Input: I am working on developing multiple applications using programming languages
Output: I be work on develop multiple application use programming language
Requirements

Python 3.7+
Streamlit 1.28+
spaCy 3.0+
en_core_web_sm language model

Features
✅ Interactive web interface
✅ Real-time text processing
✅ Pre-filled examples for each function
✅ Clean and intuitive UI with tabs
✅ Code output display
Notes

The application uses spaCy's en_core_web_sm model for NLP tasks
Programming language names (C, R, Go, D) are preserved during stop word removal
All processing happens in real-time when you click the respective buttons

Author
Text Processing System
License
MIT License