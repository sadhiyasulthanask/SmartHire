# SmartHire – AI-Powered Resume Matcher

## About the Project
SmartHire is a resume analysis web application that helps students compare their resumes with internship job descriptions. It identifies matching skills, missing skills, and additional skills to help users understand where they can improve.

## Features
- Upload resumes in PDF format.
- Extract text from uploaded resumes.
- Calculate resume and job-description text similarity using TF-IDF and cosine similarity.
- Identify matching, missing, and extra skills.
- Calculate required skill coverage.
- Generate skill improvement suggestions.
- Download a resume analysis report.

## Technologies Used
- Python
- Streamlit
- Scikit-learn
- PyPDF
- Regular Expressions (re)
- GitHub

## How It Works
1. Upload your resume as a PDF.
2. Paste the internship job description.
3. SmartHire extracts and cleans the resume text.
4. TF-IDF and cosine similarity calculate textual similarity.
5. A predefined skill dictionary identifies and compares skills.
6. The application displays the results and improvement suggestions.

## Installation and Usage

Clone the repository:

```bash
git clone https://github.com/sadhiyasulthanask/SmartHire.git
cd SmartHire
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Important Note
The similarity score represents textual similarity, not the probability of being selected for an internship. Skill extraction currently uses a predefined dictionary.

## Future Improvements
- Expand the skill database.
- Improve skill extraction.
- Add multiple job-description comparisons.
- Introduce more advanced NLP techniques.

## Author
Developed as a beginner-friendly AI/ML portfolio project.
