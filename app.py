
import streamlit as st
import re

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SmartHire | Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# 2. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: #f5f5f5;
}

.block-container {
    padding-top: 2rem;
    max-width: 1150px;
}

.hero {
    background: linear-gradient(120deg, #172554, #111827);
    padding: 35px;
    border-radius: 18px;
    border: 1px solid #334155;
    margin-bottom: 30px;
}

.hero h1 {
    color: #ffffff;
    font-size: 42px;
}

.hero h3 {
    color: #38bdf8;
    font-size: 25px;
}

.hero p {
    color: #cbd5e1;
    font-size: 16px;
}

.section-heading {
    color: #38bdf8;
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
}

.skill-card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
}

.success-card {
    background-color: #123524;
    border-left: 5px solid #22c55e;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.missing-card {
    background-color: #3b1d26;
    border-left: 5px solid #ef4444;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.info-card {
    background-color: #172554;
    border-left: 5px solid #38bdf8;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <h1>📄 SmartHire</h1>
    <h3>Find Your Career Match.</h3>
    <p>
        An AI-powered resume analysis platform that helps
        students identify skill gaps and understand how
        their resumes compare with internship requirements.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. SKILL DICTIONARY
# ==========================================

skills = [
    "python",
    "java",
    "c++",
    "c#",
    "c",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "django",
    "streamlit",
    "git",
    "github",
    "excel",
    "power bi"
]


# ==========================================
# 5. TEXT CLEANING
# ==========================================

def clean_text(text):

    text = text.lower()

    # Preserve characters useful in technical skills
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 6. SKILL EXTRACTION
# ==========================================

def extract_skills(text):

    found_skills = []

    for skill in skills:

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills


# ==========================================
# 7. INPUT SECTION
# ==========================================

st.markdown(
    '<div class="section-heading">📂 Analyse Your Resume</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Upload Your Resume")

    resume_file = st.file_uploader(
        "Upload PDF file",
        type=["pdf"]
    )

with col2:

    st.markdown("### Internship Job Description")

    job_description = st.text_area(
        "Paste the job requirements",
        height=180,
        placeholder=(
            "Example: Python, SQL, Machine Learning, "
            "Pandas, NumPy..."
        )
    )


# ==========================================
# 8. ANALYSIS BUTTON
# ==========================================

analyse_button = st.button(
    "🚀 Analyse My Resume",
    type="primary",
    use_container_width=True
)


if analyse_button:

    if resume_file is None:

        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        try:

            # ==================================
            # 9. EXTRACT PDF TEXT
            # ==================================

            reader = PdfReader(resume_file)

            resume_text = ""

            for page in reader.pages:

                resume_text += page.extract_text() or ""

            if not resume_text.strip():

                st.error(
                    "Could not extract text from this PDF. "
                    "Please upload a text-based PDF."
                )

            else:

                # ==================================
                # 10. CLEAN TEXT
                # ==================================

                cleaned_resume = clean_text(resume_text)

                cleaned_job = clean_text(job_description)


                # ==================================
                # 11. CALCULATE TEXT SIMILARITY
                # ==================================

                documents = [
                    cleaned_resume,
                    cleaned_job
                ]

                vectorizer = TfidfVectorizer()

                tfidf_matrix = vectorizer.fit_transform(
                    documents
                )

                similarity = cosine_similarity(
                    tfidf_matrix[0:1],
                    tfidf_matrix[1:2]
                )

                score = similarity[0][0] * 100


                # ==================================
                # 12. EXTRACT SKILLS
                # ==================================

                resume_skills = extract_skills(
                    cleaned_resume
                )

                job_skills = extract_skills(
                    cleaned_job
                )


                # ==================================
                # 13. COMPARE SKILLS
                # ==================================

                matching_skills = (
                    set(resume_skills)
                    & set(job_skills)
                )

                missing_skills = (
                    set(job_skills)
                    - set(resume_skills)
                )

                extra_skills = (
                    set(resume_skills)
                    - set(job_skills)
                )


                # ==================================
                # 14. CALCULATE SKILL COVERAGE
                # ==================================

                total_job_skills = len(job_skills)

                if total_job_skills > 0:

                    skill_coverage = (
                        len(matching_skills)
                        / total_job_skills
                    ) * 100

                else:

                    skill_coverage = 0


                # ==================================
                # 15. RESULTS DASHBOARD
                # ==================================

                st.divider()

                st.markdown(
                    '<div class="section-heading">'
                    '📊 Resume Analysis Dashboard'
                    '</div>',
                    unsafe_allow_html=True
                )

                metric1, metric2, metric3 = st.columns(3)

                with metric1:

                    st.metric(
                        "Text Similarity",
                        f"{score:.2f}%"
                    )

                with metric2:

                    st.metric(
                        "Matching Skills",
                        len(matching_skills)
                    )

                with metric3:

                    st.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )

                st.caption(
                    "Text similarity measures textual overlap. "
                    "It is not the probability of getting selected."
                )


                # ==================================
                # 16. SKILL COVERAGE
                # ==================================

                st.markdown("### 🎯 Required Skill Coverage")

                st.progress(
                    int(skill_coverage)
                )

                st.write(
                    f"You have **{skill_coverage:.1f}%** "
                    "of the detected required skills."
                )

                st.caption(
                    "Coverage is based on skills recognized "
                    "by the current skill dictionary."
                )


                # ==================================
                # 17. SKILL ANALYSIS
                # ==================================

                st.divider()

                st.markdown(
                    '<div class="section-heading">'
                    '🧠 Skill Analysis'
                    '</div>',
                    unsafe_allow_html=True
                )

                skill_col1, skill_col2 = st.columns(2)

                with skill_col1:

                    st.markdown("### ✅ Matching Skills")

                    if matching_skills:

                        for skill in sorted(matching_skills):

                            st.markdown(
                                f'<div class="success-card">'
                                f'✅ {skill.title()}'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                    else:

                        st.info("No matching skills detected.")


                with skill_col2:

                    st.markdown("### ❌ Missing Skills")

                    if missing_skills:

                        for skill in sorted(missing_skills):

                            st.markdown(
                                f'<div class="missing-card">'
                                f'❌ {skill.title()}'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                    else:

                        st.success(
                            "All detected required skills are present!"
                        )


                # ==================================
                # 18. EXTRA SKILLS
                # ==================================

                st.markdown("### ⭐ Extra Skills")

                if extra_skills:

                    for skill in sorted(extra_skills):

                        st.markdown(
                            f'<div class="info-card">'
                            f'⭐ {skill.title()}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "No additional skills detected."
                    )


                # ==================================
                # 19. IMPROVEMENT SUGGESTIONS
                # ==================================

                st.divider()

                st.markdown(
                    '<div class="section-heading">'
                    '📚 Your Skill Improvement Roadmap'
                    '</div>',
                    unsafe_allow_html=True
                )

                if missing_skills:

                    st.write(
                        "Consider developing these skills "
                        "to better match the job requirements:"
                    )

                    for skill in sorted(missing_skills):

                        st.markdown(
                            f'<div class="info-card">'
                            f'📖 Learn <b>{skill.title()}</b>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                else:

                    st.success(
                        "Great! Your resume contains all "
                        "the detected required skills."
                    )


                # ==================================
                # 20. FINAL MESSAGE
                # ==================================

                st.divider()

                st.success(
                    "🎉 Resume analysis completed successfully!"
                )

                st.caption(
                    "SmartHire currently uses TF-IDF, cosine "
                    "similarity and dictionary-based skill "
                    "extraction. Its results are preliminary "
                    "indicators, not hiring decisions."
                )

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )




