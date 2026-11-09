import streamlit as st
import re

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# 1. Page Configuration
# -------------------------------

st.set_page_config(
    page_title="SmartHire",
    page_icon="📄",
    layout="wide"
)

st.title("📄 SmartHire")
st.subheader("AI-Powered Resume and Job Matching System")

st.write(
    "Upload your resume and enter an internship job description "
    "to analyse your skills and resume similarity."
)


# -------------------------------
# 2. Skill Dictionary
# -------------------------------

skills = [
    "python", "java", "c", "sql",
    "machine learning", "deep learning",
    "pandas", "numpy", "html", "css",
    "javascript", "data analysis",
    "tensorflow", "scikit-learn"
]


# -------------------------------
# 3. Text Cleaning
# -------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# -------------------------------
# 4. Automatic Skill Extraction
# -------------------------------

def extract_skills(text):
    found_skills = []

    for skill in skills:
        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# -------------------------------
# 5. Resume Upload
# -------------------------------

resume_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)


# -------------------------------
# 6. Job Description
# -------------------------------

job_description = st.text_area(
    "Enter Internship Job Description",
    height=200,
    placeholder="Paste the job description here..."
)


# -------------------------------
# 7. Analyse Resume
# -------------------------------

if st.button("Analyse Resume", type="primary"):

    if resume_file is None:
        st.warning("Please upload your resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        # Extract resume text
        reader = PdfReader(resume_file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            st.error("Could not extract text. Please upload a text-based PDF.")

        else:

            # Clean both texts
            cleaned_resume = clean_text(resume_text)
            cleaned_job = clean_text(job_description)

            # Calculate similarity
            documents = [cleaned_resume, cleaned_job]

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(documents)

            similarity = cosine_similarity(
                tfidf_matrix[0:1],
                tfidf_matrix[1:2]
            )

            score = similarity[0][0] * 100

            # Extract skills
            resume_skills = extract_skills(cleaned_resume)
            job_skills = extract_skills(cleaned_job)

            # Compare skills
            matching_skills = set(resume_skills) & set(job_skills)

            missing_skills = set(job_skills) - set(resume_skills)

            extra_skills = set(resume_skills) - set(job_skills)

            # Display results
            st.divider()

            st.header("Resume Analysis Results")

            st.metric(
                "Resume Matching Score",
                f"{score:.2f}%"
            )

            st.caption(
                "This score represents textual similarity, "
                "not the probability of getting selected."
            )

            st.subheader("Skill Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.success("Matching Skills")

                if matching_skills:
                    for skill in sorted(matching_skills):
                        st.write(f"✅ {skill}")
                else:
                    st.write("No matching skills found.")

            with col2:
                st.error("Missing Skills")

                if missing_skills:
                    for skill in sorted(missing_skills):
                        st.write(f"❌ {skill}")
                else:
                    st.write("No required skills are missing!")

            st.subheader("Extra Skills")

            if extra_skills:
                for skill in sorted(extra_skills):
                    st.write(f"➕ {skill}")
            else:
                st.write("No extra skills found.")

            # Improvement suggestions
            st.subheader("Skill Improvement Suggestions")

            if not missing_skills:
                st.success(
                    "Great! Your resume contains all the "
                    "required skills in our skill dictionary."
                )

            else:
                for skill in sorted(missing_skills):
                    st.write(f"📚 Consider learning {skill}.")

            st.divider()

            st.info("Analysis completed successfully!")
