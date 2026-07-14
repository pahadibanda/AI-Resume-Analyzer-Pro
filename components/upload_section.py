"""Premium glassmorphic upload section component.

Two side-by-side drag-and-drop upload cards (Resume + JD) with
visual state feedback and a gradient CTA Analyze button.
"""
import streamlit as st

_CARD_CSS = """
<style>
.upload-success {
  margin-top: 8px; padding: 6px 14px;
  background: rgba(16,185,129,0.10);
  border: 1px solid rgba(16,185,129,0.25);
  border-radius: 10px;
  font-size: 12px; color: #6ee7b7;
  font-family: 'Inter', sans-serif;
}
.section-divider {
  height: 2px;
  background: linear-gradient(to right, rgba(139,92,246,0), rgba(139,92,246,0.4), rgba(139,92,246,0));
  margin: 24px 0 20px;
  border: none;
}
</style>
"""


def render_upload_section():
    """Render two glassmorphic upload cards and a CTA analyze button."""
    st.markdown(_CARD_CSS, unsafe_allow_html=True)

    # Section header
    st.markdown("""
<div style="text-align:center; margin-bottom: 28px;">
  <h2 style="font-family:'Outfit',sans-serif; font-size:28px; font-weight:800;
             color:#c4b5fd;
             margin-bottom:8px;">
    Upload Your Documents
  </h2>
  <p style="font-family:'Inter',sans-serif; color:#94a3b8; font-size:15px;">
    Upload your Resume and Job Description to get started with AI analysis
  </p>
  <div style="margin-top: 10px; font-size: 12.5px; color: #c4b5fd; font-family:'Inter',sans-serif; opacity: 0.85;">
    🔒 Your resume is analyzed securely and automatically deleted after processing. We never sell or share your data.
  </div>
</div>
""", unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
  <div style="width:32px; height:32px; border-radius:8px; background:rgba(167,139,250,0.12); border:1px solid rgba(167,139,250,0.3); display:flex; align-items:center; justify-content:center; color:#c4b5fd; flex-shrink:0;">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
  </div>
  <h4 style="font-family:'Outfit',sans-serif; color:#f1f5f9; font-size:16px; font-weight:700; margin:0;">Resume (PDF)</h4>
</div>
""", unsafe_allow_html=True)
        resume = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"],
            key="resume_upload",
            label_visibility="collapsed",
        )
        if resume:
            st.markdown(f'<div class="upload-success">Loaded: <b>{resume.name}</b></div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
  <div style="width:32px; height:32px; border-radius:8px; background:rgba(6,182,212,0.12); border:1px solid rgba(6,182,212,0.3); display:flex; align-items:center; justify-content:center; color:#06b6d4; flex-shrink:0;">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
  </div>
  <h4 style="font-family:'Outfit',sans-serif; color:#f1f5f9; font-size:16px; font-weight:700; margin:0;">Job Description (PDF)</h4>
</div>
""", unsafe_allow_html=True)
        jd = st.file_uploader(
            "Upload Job Description PDF",
            type=["pdf"],
            key="jd_upload",
            label_visibility="collapsed",
        )
        if jd:
            st.markdown(f'<div class="upload-success">Loaded: <b>{jd.name}</b></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # CTA button
    analyze = st.button(
        "Analyze with AI",
        use_container_width=True,
        type="primary",
        key="analyze_btn",
    )
    return resume, jd, analyze