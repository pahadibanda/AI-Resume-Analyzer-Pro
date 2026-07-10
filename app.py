import streamlit as st

from components.navbar import render_navbar
from components.hero import render_hero
from components.metric_card import render_metric_cards

from modules.resume_parser import extract_text
from modules.job_description_parser import extract_job_description
from modules.skill_extractor import extract_skills
from modules.resume_score import calculate_resume_score
from modules.match_score import calculate_match_score
from modules.recommend_roles import recommend_roles
from modules.resume_suggestions import get_resume_suggestions
from modules.ai_resume_review import review_resume
from modules.resume_vs_jd import compare_resume_with_jd
from modules.ats_gauge import create_gauge
from modules.skills_chart import create_skill_chart
from modules.interview_questions import generate_questions
from modules.report_generator import generate_report
# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide"
)
selected = render_navbar()
render_hero()
render_metric_cards()
st.markdown("""
<style>

.metric-card{
background:#1f2937;
padding:25px;
border-radius:18px;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 8px 30px rgba(0,0,0,.35);
transition:.3s;
text-align:center;
margin-bottom:20px;
}

.metric-card:hover{
transform:translateY(-6px);
border:1px solid #7C3AED;
box-shadow:0 12px 40px rgba(124,58,237,.35);
}

.metric-title{
color:#9CA3AF;
font-size:16px;
}

.metric-value{
font-size:42px;
font-weight:bold;
color:white;
margin-top:10px;
}

.metric-sub{
color:#22C55E;
margin-top:10px;
font-size:15px;
}

</style>
""", unsafe_allow_html=True)
# ---------------- FILE UPLOAD ---------------- #
left_col, right_col = st.columns([1,1])
with left_col:
    uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf"]
)
with right_col:

    st.markdown("### 📈 Analysis Summary")

    st.info("📄 Resume Uploaded")

    st.success("🤖 AI Ready")

    st.metric("🎯 ATS Score", "87%")

    st.metric("💼 JD Match", "82%")
job_file = st.file_uploader(
    "📑 Upload Job Description",
    type=["pdf"]
)

# ---------------- MAIN APP ---------------- #

if uploaded_file is not None and job_file is not None:

    with open("Resume/uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open("Resume/job_description.pdf", "wb") as f:
        f.write(job_file.getbuffer())

    st.success("✅ Files Uploaded Successfully!")

    resume_text = extract_text(
        "Resume/uploaded_resume.pdf"
    )

    job_text = extract_job_description(
        "Resume/job_description.pdf"
    )


    with st.spinner("🤖 Gemini AI is analyzing your resume..."):
        ai_review = review_resume(
            resume_text
        )

    with st.spinner("📄 Comparing Resume with Job Description..."):
        jd_review = compare_resume_with_jd(
            resume_text,
            job_text
        )
    with st.spinner("🎤 Generating AI Interview Questions..."):
        interview_questions = generate_questions(
            resume_text
        )

    skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_text
    )

    resume_score = calculate_resume_score(
        skills
    )

    match_score, matched, missing = calculate_match_score(
        skills,
        job_skills
    )

    roles = recommend_roles(
        skills
    )

    suggestions = get_resume_suggestions(
        missing
    )

    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
    "🤖 AI Review",
    "📄 Resume vs JD",
    "🎤 Interview"
    ])
    with tab1:

        col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Resume Score")

        st.metric(
            "Resume Score",
            f"{resume_score}/100"
        )

        st.progress(
            resume_score / 100
        )

        st.plotly_chart(
            create_gauge(resume_score),
            use_container_width=True
        )

    with col2:

        st.subheader("🎯 Job Match Score")

        st.metric(
            "Job Match",
            f"{match_score}%"
        )

        st.progress(
            match_score / 100
        )

    

    st.divider()
    # ================= Resume Skills =================

    st.subheader("📌 Resume Skills")

    for skill in skills:
        st.success(skill)

    st.plotly_chart(
    create_skill_chart(skills),
    use_container_width=True,
    key="skills_chart"
)
    st.divider()

    # ================= Matched Skills =================

    st.subheader("✅ Matched Skills")

    if matched:
        for skill in matched:
            st.success(skill)
    else:
        st.info("No matched skills found.")

    st.divider()

    # ================= Missing Skills =================

    st.subheader("❌ Missing Skills")

    if missing:
        for skill in missing:
            st.error(skill)
    else:
        st.success("No missing skills. Excellent!")

    st.divider()

    # ================= Recommended Roles =================

    st.subheader("💼 Recommended Roles")

    for role in roles:
        st.info(role)

    st.divider()

    # ================= AI Suggestions =================

    st.subheader("💡 AI Suggestions")

    if suggestions:
        for suggestion in suggestions:
            st.warning(suggestion)
    else:
        st.success("Your resume looks strong.")

    st.divider()

    # ================= Gemini AI Resume Review =================

    with tab2:

        st.subheader("🤖 Gemini AI Resume Review")

        st.markdown(ai_review)

    st.divider()

    # ================= Resume vs Job Description =================

    with tab3:

        st.subheader("📄 Resume vs Job Description Analysis")

        st.markdown(jd_review)

    st.markdown(jd_review)

    st.divider()

    # ================= AI Interview Questions =================

    with tab4:

        st.subheader("🎤 AI Interview Questions")

        st.markdown(interview_questions)

    st.markdown(interview_questions)

    st.divider()
    generate_report(
        "resume_report.pdf",
        resume_score,
        match_score,
        ai_review,
        jd_review
    )

    with open("resume_report.pdf", "rb") as pdf_file:

        st.download_button(
            label="📄 Download AI Report",
            data=pdf_file,
            file_name="AI_Resume_Report.pdf",
            mime="application/pdf"
        )
    st.success("🎉 AI Resume Analysis Completed Successfully!")

    st.balloons()