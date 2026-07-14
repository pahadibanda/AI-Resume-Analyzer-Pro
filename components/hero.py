"""Premium hero landing section with animated gradient title,
feature highlights, stats row, and CTA buttons.
"""
import os
import streamlit as st


_FEATURES = [
    (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>',
        "Instant AI Analysis",
        "Results in under 60 seconds"
    ),
    (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>',
        "ATS Score Calculator",
        "Industry-standard scoring"
    ),
    (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707.707M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"></path></svg>',
        "AI Resume Review",
        "Powered by Groq LLaMA 3.3"
    ),
    (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect><path d="M9 14h6"></path><path d="M9 18h6"></path><path d="M12 10h.01"></path></svg>',
        "JD Match Analysis",
        "Skill gap detection"
    ),
    (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>',
        "Interview Questions",
        "Categorized by difficulty"
    ),
    (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
        "PDF Report Generator",
        "Professional & downloadable"
    ),
]

_STATS = [
    ("10K+", "Resumes Analyzed"),
    ("95%",  "ATS Accuracy"),
    ("100+", "Skills Detected"),
    ("6",    "Report Sections"),
]


def render_hero() -> bool:
    """Render the full hero landing section. Returns True if Live Demo clicked."""
    left, right = st.columns([1.15, 1], gap="large")
    demo_clicked = False

    with left:
        st.markdown("""
<div style="margin-bottom: 12px;">
  <div class="hero-badge">AI-Powered Career Intelligence</div>
</div>

<div style="display: flex; align-items: center; gap: 40px; margin: 0 0 24px 0; flex-wrap: wrap;">
  <div class="hero-h1" style="margin: 0; line-height: 1.06;">
    AI Resume<br>Analyzer Pro
  </div>
  <div class="heading-illustration" style="flex-shrink: 0; margin-top: 12px; margin-left: 56px;">
    <svg class="pulse-scan-svg" width="165" height="165" viewBox="0 0 28 28" fill="none" stroke="url(#gradient-purple-cyan)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
      <defs>
        <linearGradient id="gradient-purple-cyan" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#a855f7" />
          <stop offset="100%" stop-color="#06b6d4" />
        </linearGradient>
      </defs>
      <rect x="4" y="2" width="20" height="13" rx="1.2" />
      <path d="M12 15v4" />
      <path d="M9 19h6" />
      <rect x="10" y="4" width="8" height="9" rx="0.8" fill="rgba(255, 255, 255, 0.05)" />
      <line x1="12" y1="6" x2="16" y2="6" stroke-width="0.8" opacity="0.8" />
      <line x1="12" y1="8" x2="16" y2="8" stroke-width="0.8" opacity="0.8" />
      <line x1="12" y1="10" x2="15" y2="10" stroke-width="0.8" opacity="0.8" />
      <rect x="5" y="21" width="12" height="3" rx="0.6" />
      <line x1="7" y1="22.2" x2="15" y2="22.2" stroke-width="0.8" stroke-dasharray="1 1" />
      <line x1="9" y1="23" x2="13" y2="23" stroke-width="0.8" />
      <rect x="19" y="21" width="3" height="4" rx="1.5" />
      <line x1="20.5" y1="21" x2="20.5" y2="23" stroke-width="0.8" />
      <line class="scan-line-motion" x1="5" y1="8.5" x2="23" y2="8.5" stroke="#10b981" stroke-width="1.8" />
      <circle cx="14" cy="8.5" r="3" stroke="#06b6d4" stroke-width="0.5" stroke-dasharray="1.5 1.5" />
    </svg>
  </div>
</div>

<p class="hero-sub">
  Analyze your resume with AI. Get your ATS score, compare with Job
  Descriptions, identify skill gaps, generate interview questions,
  and download a professional PDF report - all in one place.
</p>
""", unsafe_allow_html=True)

        # CTA buttons
        btn_col1, btn_col2 = st.columns(2, gap="small")
        with btn_col1:
            st.markdown("""
<a href="#upload-section" style="text-decoration:none; display:block;">
  <button class="cosmic-btn">
    Upload Resume
  </button>
</a>
""", unsafe_allow_html=True)
        with btn_col2:
            demo_clicked = st.button(
                "Live Demo",
                use_container_width=True,
                key="live_demo_btn",
            )

        # Feature chips row
        st.markdown("""
<div class="feature-pills-row">
  <div class="feature-pill">
    <svg class="pill-check-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
    <span>ATS Optimized</span>
  </div>
  <div class="feature-pill">
    <svg class="pill-check-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
    <span>AI Powered</span>
  </div>
  <div class="feature-pill">
    <svg class="pill-check-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
    <span>PDF Report</span>
  </div>
</div>
""", unsafe_allow_html=True)

        # Stats row
        st.markdown("""
<div style="display:flex; gap:14px; margin-top:28px; flex-wrap:wrap; width:100%;">
  <div class="stat-box">
    <div class="stat-icon-wrapper">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
    </div>
    <div class="stat-number stat-resumes">10K+</div>
    <div class="stat-label" style="font-family:'Inter',sans-serif; color:#94A3B8; font-size:12px; font-weight:500; margin-top:4px;">Resumes Analyzed</div>
  </div>
  <div class="stat-box">
    <div class="stat-icon-wrapper">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
    </div>
    <div class="stat-number stat-accuracy">95%</div>
    <div class="stat-label" style="font-family:'Inter',sans-serif; color:#94A3B8; font-size:12px; font-weight:500; margin-top:4px;">ATS Accuracy</div>
  </div>
  <div class="stat-box">
    <div class="stat-icon-wrapper">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
    </div>
    <div class="stat-number stat-skills">100+</div>
    <div class="stat-label" style="font-family:'Inter',sans-serif; color:#94A3B8; font-size:12px; font-weight:500; margin-top:4px;">Skills Detected</div>
  </div>
  <div class="stat-box">
    <div class="stat-icon-wrapper">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>
    </div>
    <div class="stat-number stat-sections">6</div>
    <div class="stat-label" style="font-family:'Inter',sans-serif; color:#94A3B8; font-size:12px; font-weight:500; margin-top:4px;">AI Review Sections</div>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        video_src = "static/robot_walk.mp4"

        robot_html = f"""
<style>
.hero-media-container {{
  position: relative;
  width: 100%;
  max-width: 440px;
  margin: 0 auto;
  padding: 40px 20px;
}}

.robot-card {{
  position: relative;
  width: 100%;
  border-radius: 24px;
  overflow: hidden;
  background: transparent;
  z-index: 5;
}}

.video-wrapper {{
  position: relative;
  width: 100%;
  padding-bottom: 75%; /* 4:3 Aspect Ratio */
  height: 0;
  border-radius: 16px;
  overflow: hidden;
  background: transparent;
}}

.video-wrapper video {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: url(#chromakey-filter);
}}

.workflow-card {{
  position: absolute;
  background: rgba(10, 17, 38, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 8px 12px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 10;
  font-family:'Outfit',sans-serif; 
  font-size:11px; 
  font-weight:700; 
  color:#cbd5e1;
}}

.connector-line-glow {{
  stroke-dasharray: 6, 6;
  animation: dash 20s linear infinite;
}}

@keyframes dash {{
  to {{ stroke-dashoffset: -1000; }}
}}
</style>

<svg width="0" height="0" style="position: absolute;">
  <defs>
    <filter id="chromakey-filter">
      <feColorMatrix type="matrix" values="1 0 0 0 0
                                           0 1 0 0 0
                                           0 0 1 0 0
                                           -1.9 -1.9 -1.9 5.3 0" />
    </filter>
  </defs>
</svg>

<div class="hero-media-container">

  <!-- Resume Uploaded -->
  <div class="workflow-card float-anim-1" style="top: 35px; left: -45px; border-left: 3px solid #10b981 !important;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
    <span>Resume Uploaded</span>
  </div>

  <!-- Main Transparent Robot Card -->
  <div class="robot-card">
    <div class="video-wrapper">
      <video autoplay loop muted playsinline>
        <source src="{video_src}" type="video/mp4">
      </video>
    </div>
  </div>

  <!-- AI Analysis -->
  <div class="workflow-card float-anim-2" style="top: 155px; left: -65px; border-left: 3px solid #a855f7 !important;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
    <span>Skill Analysis</span>
  </div>

  <!-- ATS Score 95% -->
  <div class="workflow-card float-anim-3" style="top: 285px; left: -45px; border-left: 3px solid #06b6d4 !important;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
    <span>ATS Score 95%</span>
  </div>

  <!-- JD Match -->
  <div class="workflow-card float-anim-1" style="top: 55px; right: -45px; border-left: 3px solid #ff5a1f !important;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>JD Match</span>
  </div>

  <!-- Interview Questions -->
  <div class="workflow-card float-anim-2" style="top: 175px; right: -65px; border-left: 3px solid #f59e0b !important;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
    <span>Interview Qs</span>
  </div>

  <!-- PDF Export -->
  <div class="workflow-card float-anim-3" style="top: 305px; right: -45px; border-left: 3px solid #ec4899 !important;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
    <span>PDF Export</span>
  </div>
</div>
"""
        st.markdown(robot_html, unsafe_allow_html=True)

    # Feature highlights row
    st.markdown("<div style='margin-top: 40px; margin-bottom: 8px;'><hr style='border-color: rgba(139,92,246,0.15); margin: 0;'/></div>", unsafe_allow_html=True)
    st.markdown("""
<p style="font-family:'Inter',sans-serif; font-size:12px; font-weight:600;
   color:#64748b; text-align:center; letter-spacing:0.08em;
   margin-bottom: 16px; text-transform: uppercase;">
  Everything you need to land your next role
</p>
""", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3, gap="medium")
    for col, (icon, title, sub) in zip([f1, f2, f3], _FEATURES[:3]):
        with col:
            st.markdown(f"""
<div class="feature-chip" style="gap: 16px; align-items: center;">
  <div class="feature-chip-icon">{icon}</div>
  <div>
    <div class="feature-chip-title">{title}</div>
    <div class="feature-chip-sub">{sub}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3, gap="medium")
    for col, (icon, title, sub) in zip([f4, f5, f6], _FEATURES[3:]):
        with col:
            st.markdown(f"""
<div class="feature-chip" style="gap: 16px; align-items: center;">
  <div class="feature-chip-icon">{icon}</div>
  <div>
    <div class="feature-chip-title">{title}</div>
    <div class="feature-chip-sub">{sub}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    return demo_clicked