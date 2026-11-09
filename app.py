
import streamlit as st
import re

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ----------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="SmartHire | AI Resume Matcher",
    page_icon="💼",
    layout="wide"
)


# ----------------------------------
# 2. CUSTOM DESIGN
# ----------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F4F7FB;
}

.block-container {
    padding-top: 2rem;
    max-width: 1150px;
}

.hero {
    background: linear-gradient(120deg, #101D35, #193C58);
    padding: 42px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
}

.hero h1 {
    color: white;
    font-size: 42px;
    font-weight: 800;
}

.hero p {
    color: #C8D8E8;
    font-size: 16px;
}

.section-title {
    color: #142B45;
    font-size: 23px;
    font-weight: 700;
    margin-top: 20px;
}

.info-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #E4EAF1;
    min-height: 120px;
}

.skill {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 20px;
    margin: 5px;
    font-size: 13px;
    font-weight: 600;
}

.match {
    background: #D9F5E9;
    color: #087443;
}

.missing {
    background: #FCE4E4;
    color: #B42318;
}

.extra {
    background: #E1EDFF;
    color: #2456A6;
}

.stButton > button {
    background: #13B8A6;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: 700;
    width: 100%;
}

.stButton > button:hover {
    background: #0E9488;
    color: white;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E4EAF1;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------
# 3. HEADER
# ----------------------------------

st.markdown("""
<div class="hero">
    <h1>💼 SmartHire</h1>
    <h2 style="color:#62D9C5;">Find your career match.</h2>
    <p>
        Analyse your resume, discover skill gaps and prepare
        yourself for better internship opportunities.
    </p>
</div>
""", unsafe_allow_html=True)


# ----------------------------------
# 4. SKILL DICTIONARY
# ----------------------------------

skills = [
    "python", "java", "c", "sql", "mysql",
    "machine learning", "deep learning",
    "pandas", "numpy", "html", "css",
    "javascript", "data analysis",
    "tensorflow", "scikit-learn"
]


# ----------------------------------
# 5. TEXT CLEANING
# ----------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ----------------------------------
# 6. SKILL EXTRACTION
# ----------------------------------

def extract_skills(text):
    found_skills = []

    for skill in skills:
        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# ----------------------------------
# 7. INPUT SECTION
# ----------------------------------

st.markdown(
    '<div class="section-title">📄 Upload Your Resume</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**Your Resume**")
    resume_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

with col2:
    st.markdown("**Internship Job Description**")
    job_description = st.text_area(
        "Paste job requirements",
        height=160,
        placeholder="Example: Python, SQL, Machine Learning, Pandas..."
    )


# ----------------------------------
# 8. ANALYSIS BUTTON
# ----------------------------------

st.write("")

analyse = st.button(
    "✨ Analyse My Resume",
    type="primary",
    use_container_width=True
)


# ----------------------------------
# 9. RESUME ANALYSIS
# ----------------------------------

if analyse:

    if resume_file is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        with st.spinner("Analysing your resume..."):

            reader = PdfReader(resume_file)

            resume_text = ""

            for page in reader.pages:
                resume_text += page.extract_text() or ""

            if not resume_text.strip():
                st.error(
                    "Could not extract text. "
                    "Please upload a text-based PDF."
                )

            else:

                cleaned_resume = clean_text(resume_text)
                cleaned_job = clean_text(job_description)

                # Text similarity

                documents = [cleaned_resume, cleaned_job]

                vectorizer = TfidfVectorizer()

                tfidf_matrix = vectorizer.fit_transform(documents)

                similarity = cosine_similarity(
                    tfidf_matrix[0:1],
                    tfidf_matrix[1:2]
                )

                score = similarity[0][0] * 100

                # Skill extraction

                resume_skills = extract_skills(cleaned_resume)
                job_skills = extract_skills(cleaned_job)

                # Skill comparison

                matching_skills = set(resume_skills) & set(job_skills)

                missing_skills = set(job_skills) - set(resume_skills)

                extra_skills = set(resume_skills) - set(job_skills)

        # ----------------------------------
        # 10. RESULTS
        # ----------------------------------

        st.divider()

        st.markdown(
            '<div class="section-title">📊 Resume Analysis Dashboard</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Text Similarity",
                f"{score:.2f}%"
            )

        with col2:
            st.metric(
                "Matching Skills",
                len(matching_skills)
            )

        with col3:
            st.metric(
                "Missing Skills",
                len(missing_skills)
            )

        st.caption(
            "Text similarity measures how closely the resume and "
            "job description match in wording. It is not a selection probability."
        )

        # ----------------------------------
        # 11. SKILL ANALYSIS
        # ----------------------------------

        st.markdown(
            '<div class="section-title">🎯 Skill Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success("✅ Matching Skills")

            if matching_skills:
                for skill in sorted(matching_skills):
                    st.markdown(
                        f'<span class="skill match">{skill.title()}</span>',
                        unsafe_allow_html=True
                    )
            else:
                st.write("No matching skills found.")

        with col2:

            st.error("❌ Missing Skills")

            if missing_skills:
                for skill in sorted(missing_skills):
                    st.markdown(
                        f'<span class="skill missing">{skill.title()}</span>',
                        unsafe_allow_html=True
                    )
            else:
                st.write("All detected required skills are present!")

        # ----------------------------------
        # 12. EXTRA SKILLS
        # ----------------------------------

        st.markdown(
            '<div class="section-title">🌟 Additional Skills</div>',
            unsafe_allow_html=True
        )

        if extra_skills:
            for skill in sorted(extra_skills):
                st.markdown(
                    f'<span class="skill extra">{skill.title()}</span>',
                    unsafe_allow_html=True
                )
        else:
            st.write("No additional skills detected.")

        # ----------------------------------
        # 13. IMPROVEMENT SUGGESTIONS
        # ----------------------------------

        st.markdown(
            '<div class="section-title">🚀 Your Improvement Roadmap</div>',
            unsafe_allow_html=True
        )

        if missing_skills:

            st.write(
                "Consider developing these skills to better align "
                "your resume with the job requirements:"
            )

            for skill in sorted(missing_skills):
                st.markdown(
                    f"📚 **{skill.title()}** — Consider learning "
                    f"and practising {skill.title()}."
                )

        else:
            st.success(
                "Excellent! All detected required skills "
                "are present in your resume."
            )

        st.divider()

        st.success("Analysis completed successfully!")

