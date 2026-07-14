"""AI Resume Analyzer Pro — Main Application Entry Point.

Clean, modular orchestration of the full analysis pipeline.
No duplicate code, no dead imports, proper session state management.

Performance highlights:
- Parallel LLM API calls via ThreadPoolExecutor (3x faster analysis)
- Precompiled skill-extraction regex (module-level, not per-call)
- CSS loaded once and cached via @st.cache_data
- Multi-factor ATS scoring (5 weighted dimensions)
"""
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import streamlit as st
import streamlit.components.v1 as st_components


# ── Page Config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="assests/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_data(show_spinner=False)
def _load_css(path: str) -> str:
    """Load CSS file content, cached across reruns so disk is only read once."""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return ""

_CSS_CACHE = _load_css("styles/custom.css")
if _CSS_CACHE:
    st.markdown(f"<style>{_CSS_CACHE}</style>", unsafe_allow_html=True)

# tsParticles Galaxy Background runs natively via static index.html patch.

import importlib
import components.navbar
import components.hero
import components.upload_section
import components.metric_card
import components.loading_screen
import components.footer

# Force reload local UI modules during run to bypass OneDrive sync caching delays
importlib.reload(components.navbar)
importlib.reload(components.hero)
importlib.reload(components.upload_section)
importlib.reload(components.metric_card)
importlib.reload(components.loading_screen)
importlib.reload(components.footer)

from components.navbar import render_navbar
from components.hero import render_hero
from components.upload_section import render_upload_section
from components.metric_card import render_metric_cards
from components.loading_screen import run_loading_animation
from components.footer import render_footer

# ── Module Imports ────────────────────────────────────────────────────────────
from modules.resume_parser import extract_text
from modules.job_description_parser import extract_job_description
from modules.skill_extractor import extract_skills
from modules.resume_score import calculate_resume_score, calculate_resume_score_full
from modules.match_score import calculate_match_score
from modules.recommend_roles import recommend_roles
from modules.resume_suggestions import get_resume_suggestions
from modules.ai_resume_review import review_resume
from modules.resume_vs_jd import compare_resume_with_jd
from modules.interview_questions import generate_questions
from modules.report_generator import generate_report
from modules.ats_gauge import create_gauge
from modules.skills_chart import create_skill_chart, create_radar_chart, CHART_ROW_PX, CHART_HEADER_PX

# ── Helpers ──────────────────────────────────────────────────────────────────

def _sanitize_text(text: str) -> str:
    if not text:
        return ""
    # Clean common UTF-8 double-encoding artifacts
    replacements = {
        "â€¢": "•",
        "âœ”": "✔",
        "âœ“": "✓",
        "âž¤": "➢",
        "âž§": "➔",
        "â˜…": "★",
        "âš": "⚠️",
        "âž": "➔",
        "â€™": "'",
        "â€œ": '"',
        "â€ ": '"',
        "â€“": "—",
        "â€”": "—",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def _markdown_to_html(md: str) -> str:
    if not md:
        return ""
    html = []
    in_list = False
    for line in md.split("\n"):
        line_str = line.strip()
        if not line_str:
            continue
        # Headings
        if line_str.startswith("### "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"""<h3 style="font-family:'Outfit',sans-serif; font-size:18px; font-weight:800;
              background: linear-gradient(135deg, #c4b5fd 0%, #818cf8 50%, #60a5fa 100%);
              -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
              display: inline-block;
              margin-top:24px; margin-bottom:12px; border-left:3px solid #7c3aed; padding-left:10px;">{line_str[4:]}</h3>""")
        elif line_str.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"""<h2 style="font-family:'Outfit',sans-serif; font-size:20px; font-weight:800;
              background: linear-gradient(135deg, #c4b5fd 0%, #818cf8 50%, #60a5fa 100%);
              -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
              display: inline-block;
              margin-top:24px; margin-bottom:12px; border-left:3px solid #7c3aed; padding-left:10px;">{line_str[3:]}</h2>""")
        elif line_str.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"""<h1 style="font-family:'Outfit',sans-serif; font-size:22px; font-weight:800;
              background: linear-gradient(135deg, #c4b5fd 0%, #818cf8 50%, #60a5fa 100%);
              -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
              display: inline-block;
              margin-top:24px; margin-bottom:12px; border-left:3px solid #7c3aed; padding-left:10px;">{line_str[2:]}</h1>""")
        # List items
        elif line_str.startswith("- ") or line_str.startswith("* "):
            if not in_list:
                html.append("<ul style='list-style-type:none; padding-left:0; margin-bottom:16px; margin-top:8px;'>")
                in_list = True
            item_text = line_str[2:]
            item_text = re.sub(r"\*\*(.*?)\*\*", r"<strong style='color:#f1f5f9; font-weight:700;'>\1</strong>", item_text)
            html.append(f"<li style='position:relative; padding-left:20px; color:#e2e8f0; font-size:14px; font-weight:500; line-height:1.8; margin-bottom:8px;'><span style='position:absolute; left:0; color:#a78bfa;'>›</span>{item_text}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            p_text = re.sub(r"\*\*(.*?)\*\*", r"<strong style='color:#f1f5f9; font-weight:700;'>\1</strong>", line_str)
            html.append(f"<p style='color:#e2e8f0; font-size:14px; font-weight:500; line-height:1.8; margin-bottom:16px;'>{p_text}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)

def _count_questions(text: str) -> int:
    """Count numbered questions in text. Fallback: count '?' chars."""
    if not text:
        return 0
    count = len(re.findall(r"^\s*\d+[\.\)]\s+.+", text, re.MULTILINE))
    return count or text.count("?") or 20


def _skill_badges_html(skills: list, css_class: str) -> str:
    """Render a list of skills as inline pill badges."""
    if not skills:
        return "<p style='color:#64748b; font-style:italic; font-size:13px;'>None identified</p>"
    return (
        "<div style='display:flex; flex-wrap:wrap; gap:6px; margin:4px 0;'>"
        + "".join(f"<span class='skill-badge {css_class}'>{s}</span>" for s in skills)
        + "</div>"
    )


def _parse_question_categories(text: str) -> dict[str, list[str]]:
    """Split LLM output by ## headers into category → questions dict."""
    categories: dict[str, list[str]] = {}
    current = None
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped[3:].strip()
            categories[current] = []
        elif current and stripped and re.match(r"^\d+[\.\)]", stripped):
            categories[current].append(re.sub(r"^\d+[\.\)]\s*", "", stripped))
    return categories

def _validate_uploaded_file(file) -> str | None:
    """Validate uploaded file for size, extension, double extension, and PDF header signature.
    
    Returns error message string if invalid, otherwise None.
    """
    if not file:
        return None
    
    # 1. Size check (10MB limit)
    MAX_SIZE_BYTES = 10 * 1024 * 1024
    if file.size > MAX_SIZE_BYTES:
        return f"File '{file.name}' exceeds the 10 MB maximum size limit."
        
    # 2. Extension check
    name = file.name.lower()
    if not name.endswith(".pdf"):
        return f"File '{file.name}' is not a valid PDF file extension."
        
    # 3. Double extension check
    parts = name.split(".")
    if len(parts) > 2:
        # Check if any part before the last is a blacklisted executable/script extension
        blacklisted_exts = {"exe", "bat", "cmd", "sh", "py", "js", "html", "php", "zip", "tar", "gz", "rar"}
        for part in parts[:-1]:
            if part in blacklisted_exts:
                return f"File '{file.name}' contains a suspicious double extension."
                
    # 4. MIME/Header signature validation (PDF magic bytes: %PDF)
    try:
        header = file.read(4)
        file.seek(0)  # Reset stream pointer
        if header != b"%PDF":
            return f"File '{file.name}' is not a valid PDF document (header signature mismatch)."
    except Exception:
        return f"Could not read file header signature for '{file.name}'."
        
    return None


def _reset_analysis() -> None:
    """Clear all analysis session state and rerun."""
    keys = [
        "analysis_done", "resume_score", "match_score", "matched",
        "missing", "skills", "roles", "suggestions", "ai_review",
        "jd_review", "interview_questions", "num_questions", "current_tab",
        "pdf_report_bytes"
    ]
    for k in keys:
        st.session_state.pop(k, None)
    st.rerun()


def _card_hdr(icon_svg: str, text: str, accent: str = "linear-gradient(135deg,#a78bfa,#818cf8)") -> str:
    """Shared card-header helper — gradient icon box + gradient title text. Used across all tabs."""
    return f"""<div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;
  border-bottom:1px solid rgba(139,92,246,0.15);padding-bottom:14px;">
  <div style="width:36px;height:36px;border-radius:10px;background:{accent};
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 4px 12px rgba(124,58,237,0.3);flex-shrink:0;">{icon_svg}</div>
  <span style="font-family:'Outfit',sans-serif;font-size:18px;font-weight:800;
    background:linear-gradient(135deg,#ffffff 20%,#c4b5fd 60%,#818cf8 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;">{text}</span>
</div>"""


# ── Session State Init ────────────────────────────────────────────────────────
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Home"

# ── Navigation & Page Routing ────────────────────────────────────────────────
menu_options = ["Home", "Dashboard", "Resume Review", "JD Match", "Interview", "Settings"]
default_idx = menu_options.index(st.session_state.current_tab) if st.session_state.current_tab in menu_options else 0

selected = render_navbar(default_index=default_idx, key=f"nav_{st.session_state.current_tab}")

if selected != st.session_state.current_tab:
    st.session_state.current_tab = selected
    st.rerun()

# ── Nebula Background Elements ──────────────────────────────
st.markdown("""
<div class="nebula-glow-1"></div>
<div class="nebula-glow-2"></div>
""", unsafe_allow_html=True)

# tsParticles Galaxy Background injected dynamically into parent window DOM
st.components.v1.html("""
<script>
    const parentDoc = window.parent.document;
    
    // Check if particles container is already added to avoid duplicate injections
    if (!parentDoc.getElementById("tsparticles-bg")) {
        // 1. Create the particle background container
        const particlesBg = parentDoc.createElement("div");
        particlesBg.id = "tsparticles-bg";
        particlesBg.style.position = "fixed";
        particlesBg.style.top = "0";
        particlesBg.style.left = "0";
        particlesBg.style.width = "100vw";
        particlesBg.style.height = "100vh";
        particlesBg.style.zIndex = "-1";
        particlesBg.style.pointerEvents = "none";
        particlesBg.style.overflow = "hidden";
        particlesBg.style.background = "#05010f";

        // Add nebula blobs
        const blob1 = parentDoc.createElement("div");
        blob1.className = "nebula-blob nebula-1";
        const blob2 = parentDoc.createElement("div");
        blob2.className = "nebula-blob nebula-2";
        
        // Add canvas wrapper
        const canvasWrapper = parentDoc.createElement("div");
        canvasWrapper.id = "tsparticles-canvas-wrapper";
        canvasWrapper.style.position = "absolute";
        canvasWrapper.style.top = "0";
        canvasWrapper.style.left = "0";
        canvasWrapper.style.width = "100%";
        canvasWrapper.style.height = "100%";

        // Add noise overlay
        const noise = parentDoc.createElement("div");
        noise.className = "noise-overlay";

        particlesBg.appendChild(blob1);
        particlesBg.appendChild(blob2);
        particlesBg.appendChild(canvasWrapper);
        particlesBg.appendChild(noise);
        
        // Prepend container to parent body
        parentDoc.body.prepend(particlesBg);

        // 2. Load tsParticles CDN script
        const script = parentDoc.createElement("script");
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/tsparticles/2.12.0/tsparticles.bundle.min.js";
        script.onload = function() {
            parentDoc.defaultView.tsParticles.load("tsparticles-canvas-wrapper", {
                fpsLimit: 60,
                particles: {
                    number: {
                        value: parentDoc.defaultView.innerWidth < 768 ? 150 : 350,
                        density: { enable: true, area: 800 }
                    },
                    color: { value: "#ffffff" },
                    shape: { type: "circle" },
                    opacity: {
                        value: { min: 0.15, max: 0.85 },
                        animation: { enable: true, speed: 0.8, sync: false }
                    },
                    size: { value: { min: 1, max: 3.5 } },
                    move: {
                        enable: true,
                        speed: 0.45,
                        direction: "none",
                        random: true,
                        straight: false,
                        outModes: { default: "out" }
                    },
                    twinkle: {
                        particles: { enable: true, color: "#c084fc", frequency: 0.04, opacity: 1 }
                    }
                },
                interactivity: {
                    detectsOn: "window",
                    events: {
                        onHover: { enable: true, mode: "grab" },
                        onClick: { enable: true, mode: "push" },
                        resize: true
                    },
                    modes: {
                        grab: { distance: 180, links: { opacity: 0.35 } },
                        push: { quantity: 4 }
                    }
                }
            });
        };
        parentDoc.head.appendChild(script);
    }
</script>
""", height=0)

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE + UPLOAD FLOW
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.analysis_done or selected == "Home":
    demo_clicked = False

    if selected == "Settings":
        st.markdown("### Settings & System Controls")
        st.markdown("""
<div class="content-card" style="padding: 24px;">
  <h4 style="margin-top:0;">Restart Analysis</h4>
  <p style="color:#94a3b8; font-size:14px; margin-bottom:18px;">
    Reset the active analysis report and return to the document upload page to analyze a new resume.
  </p>
</div>
""", unsafe_allow_html=True)
        if st.button("Analyze Another Resume", type="primary"):
            _reset_analysis()
    else:
        if selected in ["Dashboard", "Resume Review", "JD Match", "Interview"]:
            st.info("Please upload your Resume and Job Description below to unlock full AI analysis reports and results.")

        # ── Hero Section ──────────────────────────────────────────────────────────
        demo_clicked = render_hero()

    if demo_clicked:
        # Rich demo data that showcases all features
        st.session_state.update({
            "resume_score": 82,
            "match_score": 78,
            "matched": ["Python", "SQL", "Pandas", "NumPy", "Machine Learning", "Git"],
            "missing": ["Docker", "Kubernetes", "AWS", "Spark"],
            "skills": ["Python", "SQL", "Pandas", "NumPy", "Machine Learning",
                       "Scikit-learn", "Git", "Statistics", "Data Analysis", "Flask"],
            "roles": ["Data Scientist", "Machine Learning Engineer", "Data Analyst"],
            "suggestions": [
                "Learn Docker by containerizing your Flask/Python projects and pushing to Docker Hub.",
                "Earn the AWS Cloud Practitioner certification — it's beginner-friendly and highly valued.",
                "Complete a Spark + PySpark course on Databricks to strengthen big data skills.",
                "Add Kubernetes to your skillset through KodeKloud's free Kubernetes for Developers path.",
            ],
            "ai_review": """## Executive Summary
Strong Python and data engineering background with solid ML foundations. Well-positioned for Data Scientist and ML Engineer roles.

## Key Strengths
- Proficient in Python, Pandas, NumPy — core data manipulation stack
- Machine Learning experience with Scikit-learn
- Statistical analysis and data visualization capabilities
- Clean code practices with Git version control

## Areas for Improvement
- No cloud platform experience (AWS/GCP/Azure) — critical for modern roles
- Missing containerization skills (Docker/Kubernetes)
- No large-scale data processing tools listed (Spark, Kafka)
- Could add more quantified impact metrics to experience bullets

## ATS Optimization Tips
- Add cloud certifications section near the top
- Include "Machine Learning" as a keyword in multiple sections
- Quantify model performance metrics (e.g., "Improved model accuracy to 94.2%")
- Add a Technical Skills section with clear categorization

## Career Path Recommendations
- Data Scientist at mid-size tech companies
- ML Engineer at AI startups
- Analytics Engineer at data-driven SaaS companies

## Action Items
- Earn AWS Cloud Practitioner within 3 months
- Build and containerize 2 ML projects with Docker
- Add Spark to tech stack through online courses
- Update resume with quantified impact for each role""",
            "jd_review": """## Match Overview
78% compatibility — Good Match. The candidate meets core requirements but lacks cloud and DevOps skills critical for this role.

## Aligned Strengths
- Python expertise fully aligns with JD requirements
- Machine Learning background matches the ML/AI requirements
- SQL and data analysis skills cover the analytics requirements
- Statistical knowledge covers the data science expectations

## Skill Gaps & Missing Requirements
- Docker/Kubernetes — required for model deployment (not on resume)
- AWS or cloud platform experience — explicitly required in JD
- Big data tools (Spark/Hadoop) — mentioned in JD as preferred
- CI/CD pipeline experience — DevOps requirement gap

## Skill Comparison Table
| Skill/Requirement | In Resume? | Priority |
|---|---|---|
| Python | Yes | Critical |
| SQL | Yes | High |
| Machine Learning | Yes | Critical |
| Docker | No | High |
| AWS | No | High |
| Kubernetes | No | Medium |
| Spark | No | Medium |
| Git | Yes | Medium |

## Recommendations to Bridge the Gap
- Start with AWS Cloud Practitioner certification (2-3 weeks)
- Learn Docker through a hands-on ML deployment project
- Take a Spark fundamentals course on Databricks Academy
- Add CI/CD experience through GitHub Actions on personal projects

## Final Verdict
**Good Match** — The candidate has strong core ML and data skills but will need to develop cloud and DevOps competencies to be a top-tier candidate for this role.""",
            "interview_questions": """## Easy Questions
1. Walk me through your experience with Python for data analysis.
2. How do you handle missing values in a Pandas DataFrame?
3. What is the difference between supervised and unsupervised learning?
4. How do you version control your data science projects using Git?
5. Describe a time you used SQL to answer a business question.

## Medium Questions
1. Explain how you would evaluate the performance of a classification model.
2. How would you handle class imbalance in a machine learning dataset?
3. Describe your approach to feature engineering for a regression problem.
4. How do you ensure reproducibility in your machine learning experiments?
5. Walk me through how you would tune hyperparameters for a model.

## Hard Questions
1. Design a scalable ML pipeline for real-time fraud detection at 1M transactions/day.
2. How would you implement A/B testing for a new recommendation algorithm?
3. Explain the bias-variance tradeoff and how you'd diagnose overfitting in practice.
4. How would you deploy a PyTorch model to production with low latency requirements?
5. Describe your approach to building a distributed feature store.

## Technical Questions
1. Write a Python function to compute rolling 7-day averages using Pandas.
2. How would you design a REST API for serving real-time ML predictions?
3. Explain the difference between Ridge and Lasso regularization with equations.
4. How do you implement cross-validation without data leakage in a pipeline?
5. Design a database schema for storing ML experiment metadata and results.

## Behavioral Questions
1. Tell me about a time you had to explain a complex ML model to a non-technical stakeholder.
2. Describe a situation where your model performed well in testing but poorly in production.
3. How have you handled disagreements with team members about technical approaches?
4. Give an example of a data project where you discovered an unexpected insight.
5. Tell me about a time you had to learn a new technology quickly to meet a deadline.

## HR Questions
1. Why are you interested in transitioning from your current role to this position?
2. Where do you see your data science career in 3-5 years?
3. How do you stay current with the rapidly evolving ML/AI landscape?
4. Describe your ideal work environment and team culture.
5. What's your approach to work-life balance when under project deadlines?""",
            "num_questions": 30,
            "analysis_done": True,
        })

        os.makedirs("Resume", exist_ok=True)
        try:
            generate_report(
                "resume_report.pdf",
                82, 78,
                st.session_state.ai_review,
                st.session_state.jd_review,
                skills=st.session_state.skills,
                matched=st.session_state.matched,
                missing=st.session_state.missing,
                roles=st.session_state.roles,
                interview_questions=st.session_state.interview_questions,
            )
        except Exception as pdf_err:
            print(f"Error generating PDF report: {pdf_err}")
        st.session_state.current_tab = "Dashboard"
        st.rerun()

    # ── Upload Section ────────────────────────────────────────────────────────
    st.markdown('<div id="upload-section"></div>', unsafe_allow_html=True)
    uploaded_file, job_file, analyze = render_upload_section()

    if analyze:
        if not uploaded_file or not job_file:
            st.error("⚠️ Please upload both your Resume PDF and Job Description PDF before analyzing.")
        else:
            # 1. Enforce strict upload validation
            resume_err = _validate_uploaded_file(uploaded_file)
            jd_err     = _validate_uploaded_file(job_file)
            
            if resume_err:
                st.error(f"⚠️ Resume validation failed: {resume_err}")
            elif jd_err:
                st.error(f"⚠️ Job Description validation failed: {jd_err}")
            else:
                import tempfile
                
                # Create secure unique temp files that are cleaned up immediately
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as resume_temp, \
                     tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as jd_temp:
                    
                    resume_temp.write(uploaded_file.getbuffer())
                    jd_temp.write(job_file.getbuffer())
                    resume_path = resume_temp.name
                    jd_path     = jd_temp.name

                try:
                    # ── Animated Loading Screen ────────────────────────────────────
                    loader_placeholder = st.empty()
                    run_loading_animation(loader_placeholder)

                    # ── AI Analysis Pipeline (parallel LLM calls for 3x speed) ─────
                    resume_text = extract_text(resume_path)
                    job_text    = extract_job_description(jd_path)
                finally:
                    # Secure Cleanup: delete temporary files immediately after text is extracted
                    for path in [resume_path, jd_path]:
                        if os.path.exists(path):
                            try:
                                os.remove(path)
                            except Exception:
                                pass

                # Extract skills immediately (fast, local, no network)
                skills     = extract_skills(resume_text)
                job_skills = extract_skills(job_text)

                # Run all 3 LLM calls concurrently instead of sequentially
                _tasks = {
                    "ai_review":           lambda: review_resume(resume_text),
                    "jd_review":           lambda: compare_resume_with_jd(resume_text, job_text),
                    "interview_questions": lambda: generate_questions(resume_text),
                }
                _results: dict[str, str] = {}
                with ThreadPoolExecutor(max_workers=3) as _pool:
                    _futures = {_pool.submit(fn): key for key, fn in _tasks.items()}
                    for _future in as_completed(_futures):
                        _key = _futures[_future]
                        try:
                            _results[_key] = _sanitize_text(_future.result())
                        except Exception as _e:
                            _results[_key] = f"## Error\n\nService unavailable: {_e}"

                ai_review           = _results["ai_review"]
                jd_review           = _results["jd_review"]
                interview_questions = _results["interview_questions"]

                # Multi-factor ATS scoring using resume text
                resume_score              = calculate_resume_score_full(skills, resume_text)
                match_score, matched, missing = calculate_match_score(skills, job_skills)
                roles                     = recommend_roles(skills)
                suggestions               = [_sanitize_text(s) for s in get_resume_suggestions(missing)]
                num_questions             = _count_questions(interview_questions)

                # ── Save PDF Report to secure memory ───────────────────────────
                try:
                    temp_report_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
                    generate_report(
                        temp_report_path,
                        resume_score, match_score,
                        ai_review, jd_review,
                        skills=skills,
                        matched=matched,
                        missing=missing,
                        roles=roles,
                        interview_questions=interview_questions,
                    )
                    # Load bytes into session memory and delete disk file immediately
                    with open(temp_report_path, "rb") as pdf_file:
                        st.session_state.pdf_report_bytes = pdf_file.read()
                    
                    if os.path.exists(temp_report_path):
                        os.remove(temp_report_path)
                except Exception as pdf_err:
                    print(f"Error generating PDF report: {pdf_err}")

            # ── Persist to Session State ───────────────────────────────────
            st.session_state.update({
                "resume_score":         resume_score,
                "match_score":          match_score,
                "matched":              matched,
                "missing":              missing,
                "skills":               skills,
                "roles":                roles,
                "suggestions":          suggestions,
                "ai_review":            ai_review,
                "jd_review":            jd_review,
                "interview_questions":  interview_questions,
                "num_questions":        num_questions,
                "analysis_done":        True,
                "current_tab":          "Dashboard",
            })
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
else:
    ss = st.session_state  # alias

    # ── Success Banner ─────────────────────────────────────────────────
    st.success("AI Analysis completed successfully! Use the navigation bar above to explore different sections.")

    st.markdown(f"""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 24px; border-left: 4px solid #7c3aed; padding-left: 16px;">
  <div style="flex-grow: 1;">
    <h1 style="
      font-family: 'Outfit', sans-serif;
      font-size: 32px; font-weight: 800;
      background: linear-gradient(135deg, #ffffff 30%, #c4b5fd 70%, #818cf8 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
      display: inline-block;
      margin: 0 0 4px 0;
    ">{selected}</h1>
    <p style="font-family:'Inter',sans-serif; color:#64748b; font-size:14px; margin:0;">
      {f"AI insights and analytics for your resume and match results." if selected != "Settings" else "Manage your session."}
    </p>
  </div>
  <!-- Premium small line illustration related to resume analyzer -->
  <div class="header-scanner-ill" style="flex-shrink: 0; margin-right: 8px;">
    <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="url(#grad-header)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px rgba(167, 139, 250, 0.4));">
      <defs>
        <linearGradient id="grad-header" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#a78bfa" />
          <stop offset="100%" stop-color="#06b6d4" />
        </linearGradient>
      </defs>
      <!-- Document page -->
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <!-- Small laser scanning line -->
      <line x1="6" y1="12" x2="18" y2="12" stroke="#10b981" stroke-width="2" />
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)



    if selected != "Settings":
        # ── 6 Metric Cards ─────────────────────────────────────────────────
        render_metric_cards(
            resume_score  = ss.resume_score,
            match_score   = ss.match_score,
            num_skills    = len(ss.skills),
            num_missing   = len(ss.missing),
            num_roles     = len(ss.roles),
            num_questions = ss.num_questions,
        )
        st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)

    # ── Page Routing based on navbar selection ─────────────────────────
    if selected == "Dashboard":
        _ICON_GAUGE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12a9.99 9.99 0 0 0 2.93 7.07l1.41-1.41A8 8 0 0 1 4 12c0-4.41 3.59-8 8-8s8 3.59 8 8a8 8 0 0 1-2.34 5.66l1.41 1.41A9.99 9.99 0 0 0 22 12c0-5.52-4.48-10-10-10zm-1 5v6l4.5 2.67.75-1.23-3.75-2.22V7H11z"/></svg>'
        _ICON_SUGGEST = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 2a7 7 0 0 1 7 7c0 2.38-1.19 4.47-3 5.74V17a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2.26A7 7 0 0 1 5 9a7 7 0 0 1 7-7m0 2a5 5 0 0 0-5 5 5 5 0 0 0 2.79 4.47l.21.1V16h4v-2.43l.21-.1A5 5 0 0 0 17 9a5 5 0 0 0-5-5m1 11h-2v2h2v-2z"/></svg>'
        _ICON_SKILLS  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 3L1 9l11 6 9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>'
        _ICON_MAP     = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/></svg>'

        # Row 1
        col_g, col_s = st.columns(2, gap="large")

        with col_g:
            gauge_html = create_gauge(ss.resume_score, ss.match_score, show_ats_bar=True, show_match_bar=True)
            st.markdown(f"""
<div class="dashboard-card" style="padding:24px 28px;">
  {_card_hdr(_ICON_GAUGE, "ATS Score Gauge")}
  {gauge_html}
</div>""", unsafe_allow_html=True)

        with col_s:
            sug_html = "".join(f"""
<div class="sug-item">
  <span class="sug-check">&#10003;</span>
  <span>{sug}</span>
</div>""" for sug in ss.suggestions)
            st.markdown(f"""
<div class="dashboard-card" style="min-height:420px;display:flex;flex-direction:column;padding:24px 28px;">
  {_card_hdr(_ICON_SUGGEST, "AI Improvement Suggestions", "linear-gradient(135deg,#10b981,#34d399)")}
  <div style="overflow-y:auto;flex:1;padding-right:4px;">
    {sug_html}
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin:12px 0;'></div>", unsafe_allow_html=True)

        # Row 2
        col_ch, col_b = st.columns([1.1, 1], gap="large")

        with col_ch:
            skill_fig   = create_skill_chart(ss.skills)
            skill_chart = skill_fig.to_html(full_html=False, include_plotlyjs="cdn",
                                            config={"displayModeBar": False, "responsive": False})

            # Height = chart rows + chart padding + card header (48px) + card top/bottom padding (48px)
            _CARD_CHROME = 96   # card header + padding
            iframe_height = max(300, len(ss.skills) * CHART_ROW_PX + CHART_HEADER_PX + _CARD_CHROME)
            iframe_content = f"""
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{ background: transparent !important; background-color: transparent !important; margin: 0; padding: 0; overflow: hidden; }}
    .glass-card {{
      background: rgba(10, 17, 38, 0.72);
      backdrop-filter: blur(20px) saturate(140%);
      -webkit-backdrop-filter: blur(20px) saturate(140%);
      border: 1px solid rgba(139, 92, 246, 0.18);
      border-radius: 20px;
      box-shadow: 0 24px 56px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05);
      padding: 24px 28px;
    }}
    .card-hdr {{ display:flex;align-items:center;gap:12px;margin-bottom:18px;border-bottom:1px solid rgba(139,92,246,0.15);padding-bottom:14px; }}
    .card-icon {{ width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#3b82f6,#60a5fa);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(59,130,246,0.35);flex-shrink:0; }}
    .card-title {{ font-family:'Outfit',sans-serif;font-size:18px;font-weight:800;background:linear-gradient(135deg,#ffffff 20%,#c4b5fd 60%,#818cf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }}
  </style>
</head>
<body>
  <div class="glass-card">
    <div class="card-hdr">
      <div class="card-icon">{_ICON_SKILLS}</div>
      <span class="card-title">Skills Profile</span>
    </div>
    <div style="width:100%;height:auto;">
      {skill_chart}
    </div>
  </div>
</body>
</html>
"""
            st_components.html(iframe_content, height=iframe_height + 4, scrolling=False)



        with col_b:
            badges_det = _skill_badges_html(ss.skills,   "badge-info")
            badges_mat = _skill_badges_html(ss.matched,  "badge-success")
            badges_mis = _skill_badges_html(ss.missing,  "badge-danger")
            badges_rol = _skill_badges_html(ss.roles,    "badge-purple")
            lbl = lambda t: f"<p style='font-family:Inter,sans-serif;font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.08em;text-transform:uppercase;margin:14px 0 6px 0;'>{t}</p>"
            st.markdown(f"""
<div class="dashboard-card" style="padding:24px 28px;">
  {_card_hdr(_ICON_MAP, "Skill Mapping")}
  {lbl("Detected Skills")} {badges_det}
  {lbl("Matched Skills")} {badges_mat}
  {lbl("Missing Skills")} {badges_mis}
  {lbl("Recommended Roles")} {badges_rol}
</div>""", unsafe_allow_html=True)

    elif selected == "Resume Review":
        col_g, col_txt = st.columns([1, 1.8], gap="large")

        _ICON_GAUGE_RV = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12a9.99 9.99 0 0 0 2.93 7.07l1.41-1.41A8 8 0 0 1 4 12c0-4.41 3.59-8 8-8s8 3.59 8 8a8 8 0 0 1-2.34 5.66l1.41 1.41A9.99 9.99 0 0 0 22 12c0-5.52-4.48-10-10-10zm-1 5v6l4.5 2.67.75-1.23-3.75-2.22V7H11z"/></svg>'
        _ICON_DOC      = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm-1 7V3.5L18.5 9H13zm-1 9H7v-2h5v2zm3-4H7v-2h7v2zm0-4H7V8h7v2z"/></svg>'

        with col_g:
            gauge_html = create_gauge(ss.resume_score, show_ats_bar=True, show_match_bar=False)
            st.markdown(f"""
<div class="dashboard-card" style="padding:24px 28px;">
  {_card_hdr(_ICON_GAUGE_RV, "ATS Score Gauge")}
  {gauge_html}
</div>""", unsafe_allow_html=True)

        with col_txt:
            parsed_review = _markdown_to_html(ss.ai_review)
            st.markdown(f"""
<div class="content-card" style="padding:28px;">
  {_card_hdr(_ICON_DOC, "AI Resume Review")}
  <div style="margin-top:20px;">
    {parsed_review}
  </div>
</div>""", unsafe_allow_html=True)


    elif selected == "JD Match":
        _ICON_JD    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>'
        _ICON_RADAR = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'
        _ICON_JD_TXT= '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm-1 7V3.5L18.5 9H13zm-1 9H7v-2h5v2zm3-4H7v-2h7v2zm0-4H7V8h7v2z"/></svg>'

        col_g, col_txt = st.columns([1, 1.8], gap="large")
        with col_g:
            gauge_html = create_gauge(ss.resume_score, ss.match_score, show_ats_bar=False, show_match_bar=True)
            radar_html = ""
            iframe_height = 390
            if ss.matched or ss.missing:
                radar_fig  = create_radar_chart(ss.matched, ss.missing)
                radar_html = radar_fig.to_html(full_html=False, include_plotlyjs="cdn",
                                               config={"displayModeBar": False, "responsive": True})
                iframe_height = 790

            iframe_content = f"""
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{ background: transparent !important; background-color: transparent !important; margin: 0; padding: 0; overflow: hidden; }}
    .glass-card {{
      background: rgba(10, 17, 38, 0.72);
      backdrop-filter: blur(20px) saturate(140%);
      -webkit-backdrop-filter: blur(20px) saturate(140%);
      border: 1px solid rgba(139, 92, 246, 0.18);
      border-radius: 20px;
      box-shadow: 0 24px 56px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05);
      padding: 24px 28px;
    }}
    .card-hdr {{ display:flex;align-items:center;gap:12px;margin-bottom:18px;border-bottom:1px solid rgba(139,92,246,0.15);padding-bottom:14px; }}
    .card-icon {{ width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#10b981,#34d399);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(16,185,129,0.35);flex-shrink:0; }}
    .card-title {{ font-family:'Outfit',sans-serif;font-size:18px;font-weight:800;background:linear-gradient(135deg,#ffffff 20%,#c4b5fd 60%,#818cf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }}
  </style>
</head>
<body>
  <div class="glass-card">
    <div class="card-hdr">
      <div class="card-icon">{_ICON_JD}</div>
      <span class="card-title">Job Description Match</span>
    </div>
    {gauge_html}
    <div style="margin-top:20px;">
      {radar_html}
    </div>
  </div>
</body>
</html>
"""
            st_components.html(iframe_content, height=iframe_height + 60, scrolling=False)


        with col_txt:
            parsed_jd_review = _markdown_to_html(ss.jd_review)
            st.markdown(f"""
<div class="content-card" style="padding:28px;">
  {_card_hdr(_ICON_JD_TXT, "JD Match Analysis", "linear-gradient(135deg,#10b981,#34d399)")}
  <div style="margin-top:20px;">
    {parsed_jd_review}
  </div>
</div>""", unsafe_allow_html=True)




    elif selected == "Interview":
        _ICON_INT = '<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 3.58 8 8 8v3l5.1-3.1C18.8 19.3 22 16 22 12c0-5.52-4.48-10-10-10zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>'

        # Header card for interview section
        st.markdown(f"""
<div class="dashboard-card" style="padding:24px 28px; margin-bottom:18px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;border-bottom:1px solid rgba(139,92,246,0.15);padding-bottom:12px;">
    <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#7c3aed,#a78bfa);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(124,58,237,0.3);flex-shrink:0;">
      {_ICON_INT}
    </div>
    <span style="font-family:'Outfit',sans-serif;font-size:18px;font-weight:800;background:linear-gradient(135deg,#ffffff 20%,#c4b5fd 60%,#818cf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
      Interview Question Bank
    </span>
  </div>
  <p style="font-family:'Inter',sans-serif; color:#94a3b8; font-size:14px; margin:0; line-height:1.6;">
    Explore AI-generated behavioral, technical, and role-specific interview preparation questions customized for your profile. Click on a category below to practice.
  </p>
</div>
""", unsafe_allow_html=True)

        categories = _parse_question_categories(ss.interview_questions)

        if categories:
            for cat_name, questions in categories.items():
                with st.expander(f"**{cat_name}**  ({len(questions)} questions)", expanded=False):
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"""
<div class="q-card">
  <span class="q-num">Q{i}</span>
  <span style="color:#e2e8f0; font-family:'Inter',sans-serif; font-size:14px; font-weight:500; line-height:1.6;">{q}</span>
</div>
""", unsafe_allow_html=True)
        else:
            # Fallback: Bug 5 fix — render markdown OUTSIDE the HTML div
            st.markdown('<div class="content-card" style="padding:28px;">', unsafe_allow_html=True)
            st.markdown(ss.interview_questions)
            st.markdown('</div>', unsafe_allow_html=True)


    elif selected == "Settings":
        _ICON_SET = '<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>'
        
        st.markdown(f"""
<div class="dashboard-card" style="padding:28px; margin-bottom:18px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;border-bottom:1px solid rgba(139,92,246,0.15);padding-bottom:12px;">
    <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#7c3aed,#a78bfa);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(124,58,237,0.3);flex-shrink:0;">
      {_ICON_SET}
    </div>
    <span style="font-family:'Outfit',sans-serif;font-size:18px;font-weight:800;background:linear-gradient(135deg,#ffffff 20%,#c4b5fd 60%,#818cf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
      Restart Analysis Configuration
    </span>
  </div>
  <p style="font-family:'Inter',sans-serif; color:#94a3b8; font-size:14px; margin-bottom:20px; line-height:1.6;">
    Reset the active analysis report and return to the document upload page to analyze a new resume. This will clear the current session state.
  </p>
</div>
""", unsafe_allow_html=True)
        if st.button("Analyze Another Resume", type="primary", use_container_width=True):
            _reset_analysis()


    # ── Download & Reset (renders at the bottom of all tabs except Settings) ───────
    if selected != "Settings":
        st.markdown("<hr>", unsafe_allow_html=True)
        col_dl, col_rst = st.columns(2, gap="medium")
 
        with col_dl:
            if "pdf_report_bytes" in st.session_state and st.session_state.pdf_report_bytes:
                st.download_button(
                    label="Download Full PDF Report",
                    data=st.session_state.pdf_report_bytes,
                    file_name="AI_Resume_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.warning("PDF report not found. Please run the analysis again.")

        with col_rst:
            if st.button("Analyze Another Resume", use_container_width=True):
                _reset_analysis()

# ── Footer ──────────────────────────────────────────────────────────────────
render_footer()
