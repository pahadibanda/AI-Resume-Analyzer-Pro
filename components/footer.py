"""Premium footer and company marquee component.

Renders an infinite scrolling marquee of leading company logos,
followed by a 4-column glassmorphism footer with glowing details.
"""
import streamlit as st
import json
import os
import base64

_FOOTER_HTML = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Typography & Base Styles ──────────────────────────── */
.footer-section {
  background-color: #05010f;
  color: #f8fafc;
  font-family: 'Inter', sans-serif;
  margin-top: 50px;
  position: relative;
  z-index: 1;
}

.footer-section h3, .footer-section h4 {
  font-family: 'Space Grotesk', sans-serif;
  letter-spacing: 0.02em;
}

/* ── Marquee Section ───────────────────────────────────── */
.marquee-wrapper {
  padding: 60px 0 40px 0;
  text-align: center;
}

.marquee-heading {
  font-size: 24px;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #ffffff 40%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.marquee-subtitle {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 32px;
}

.marquee-container {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding: 16px 0;
  background: rgba(255, 255, 255, 0.01);
  border-top: 1px solid rgba(168, 85, 247, 0.1);
  border-bottom: 1px solid rgba(168, 85, 247, 0.1);
}

.marquee-container::before,
.marquee-container::after {
  content: "";
  position: absolute;
  top: 0; width: 150px; height: 100%;
  z-index: 2;
  pointer-events: none;
}

.marquee-container::before {
  left: 0;
  background: linear-gradient(to right, #05010f 20%, transparent 100%);
}

.marquee-container::after {
  right: 0;
  background: linear-gradient(to left, #05010f 20%, transparent 100%);
}

@keyframes marquee-scroll {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(-50%, 0, 0); }
}

.marquee-track {
  display: flex;
  width: max-content;
  animation: marquee-scroll 45s linear infinite;
  will-change: transform;
}

.marquee-track:hover {
  animation-play-state: paused;
}

.marquee-content {
  display: flex;
  align-items: center;
  gap: 48px;
  padding-right: 48px;
}

.company-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #94a3b8;
  filter: grayscale(100%) opacity(0.45);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: default;
  user-select: none;
  white-space: nowrap;
}

.company-logo svg:not(.multicolor) {
  fill: currentColor;
}

.company-logo svg {
  width: 20px;
  height: 20px;
  transition: transform 0.35s ease;
}

.company-logo:hover {
  filter: grayscale(0%) opacity(1);
  color: var(--brand-color, #a855f7);
  transform: scale(1.08);
  text-shadow: 0 0 15px var(--brand-glow, rgba(168, 85, 247, 0.3));
}

.company-logo:hover svg {
  transform: rotate(6deg);
}

/* ── Footer Main ───────────────────────────────────────── */
.main-footer {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(168, 85, 247, 0.25);
  box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.37);
  padding: 80px 0 30px 0;
  position: relative;
  overflow: hidden;
}

.footer-glow {
  position: absolute;
  top: -150px;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 300px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.15) 0%, transparent 70%);
  filter: blur(60px);
  pointer-events: none;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  gap: 48px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.footer-col {
  display: flex;
  flex-direction: column;
}

.footer-col-title {
  font-size: 15px;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 24px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  position: relative;
}

.footer-col-title::after {
  content: "";
  position: absolute;
  left: 0; bottom: -8px;
  width: 24px; height: 2px;
  background: #a855f7;
  border-radius: 999px;
  box-shadow: 0 0 8px #a855f7;
}

.footer-col p {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.7;
  margin: 0 0 20px 0;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  font-size: 14px;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.footer-links a:hover {
  color: #a855f7;
  transform: translateX(4px);
  text-shadow: 0 0 8px rgba(168, 85, 247, 0.4);
}

.footer-links svg {
  width: 14px;
  height: 14px;
  fill: currentColor;
}

/* ── Footer Bottom ─────────────────────────────────────── */
.footer-divider {
  border: 0;
  height: 1px;
  background: linear-gradient(to right,
    rgba(168, 85, 247, 0.02),
    rgba(168, 85, 247, 0.35),
    rgba(168, 85, 247, 0.02));
  margin: 48px auto 24px auto;
  max-width: 1200px;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.footer-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-copy span {
  font-size: 13px;
  color: #94a3b8;
}

.footer-copy .highlight {
  color: #f8fafc;
  font-weight: 500;
}

.social-links {
  display: flex;
  gap: 16px;
}

.social-icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(168, 85, 247, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.social-icon-btn svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.social-icon-btn:hover {
  color: #ffffff;
  background: rgba(168, 85, 247, 0.2);
  border-color: #a855f7;
  transform: translateY(-3px) scale(1.08);
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.45);
}

/* ── Responsive breakpoints ────────────────────────────── */
@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 36px;
  }
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 32px;
  }
  .footer-col {
    align-items: center;
  }
  .footer-col-title::after {
    left: 50%;
    transform: translateX(-50%);
  }
  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
  .marquee-container::before,
  .marquee-container::after {
    width: 60px;
  }
}
"""

def render_footer():
    """Renders the horizontal marquee and responsive glassmorphic footer."""
    st.markdown(f"<style>{_FOOTER_HTML}</style>", unsafe_allow_html=True)
    
    # Centralized Social & Contact Links (Edit here to change everywhere in the footer)
    EMAIL_LINK     = "rangrajat@gmail.com"
    LINKEDIN_LINK  = "https://www.linkedin.com/in/rajatrangra/"
    GITHUB_LINK    = "https://github.com/pahadibanda"
    PORTFOLIO_LINK = "https://rajat-portfolio-kappa.vercel.app/"

    # Load parsed SVG logo data
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_data_path = os.path.join(current_dir, "scratch", "logo_data.json")
    try:
        with open(logo_data_path, "r") as f:
            logo_data = json.load(f)
    except Exception:
        logo_data = {}

    # Load brand logo image as base64
    logo_base64 = ""
    logo_path = os.path.join(current_dir, "assests", "logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass

    # Target company keys in specified order
    tech_giants_keys = [
        "google", "microsoft", "amazon", "apple", "meta", "netflix", 
        "nvidia", "tesla", "ibm", "oracle", "adobe", "salesforce", 
        "intel", "cisco", "spotify", "uber", "airbnb", "linkedin", "openai"
    ]
    
    indian_firms_keys = [
        "tcs", "infosys", "wipro", "hcl", "techmahindra", "accenture", 
        "capgemini", "cognizant", "zoho", "flipkart", "phonepe", "paytm", 
        "razorpay", "freshworks", "swiggy", "zomato", "jio", "myntra"
    ]
    
    # Assemble all marquee elements using custom CSS properties for individual brand hover colors and glows
    logo_list_html = ""
    fallback_svg = '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 3.99L18.47 19H5.53L12 5.99z"/></svg>'
    
    for key in tech_giants_keys + indian_firms_keys:
        if key == "google":
            svg = """<svg class="multicolor" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
            </svg>"""
            name = '<span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span>'
            hex_color = "#4285F4"
        elif key == "microsoft":
            svg = """<svg class="multicolor" viewBox="0 0 23 23">
              <rect x="0" y="0" width="11" height="11" fill="#f25022"/>
              <rect x="12" y="0" width="11" height="11" fill="#7fba00"/>
              <rect x="0" y="12" width="11" height="11" fill="#00a4ef"/>
              <rect x="12" y="12" width="11" height="11" fill="#ffb900"/>
            </svg>"""
            name = "Microsoft"
            hex_color = "#ffffff"
        elif key == "tcs":
            info = logo_data.get(key, {})
            name = "TCS"
            hex_color = "#ffffff"
            path = info.get("path", "")
            svg = f'<svg viewBox="0 0 24 24"><path d="{path}"/></svg>'
        elif key == "ibm":
            info = logo_data.get(key, {})
            name = "IBM"
            hex_color = "#4589FF"
            path = info.get("path", "")
            svg = f'<svg viewBox="0 0 24 24"><path d="{path}"/></svg>'
        elif key == "myntra":
            info = logo_data.get(key, {})
            name = "Myntra"
            hex_color = "#FF3F6C"
            path = info.get("path", "")
            svg = f"""<svg class="multicolor" viewBox="0 0 24 24">
              <defs>
                <linearGradient id="myntra-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#FF3F6C"/>
                  <stop offset="100%" stop-color="#F26A1B"/>
                </linearGradient>
              </defs>
              <path d="{path}" fill="url(#myntra-grad)"/>
            </svg>"""
        elif key == "flipkart":
            info = logo_data.get(key, {})
            name = "Flipkart"
            hex_color = "#FFE11B"
            path = info.get("path", "")
            svg = f'<svg viewBox="0 0 24 24"><path d="{path}"/></svg>'
        elif key in logo_data:
            info = logo_data[key]
            name = info["title"]
            hex_color = info["hex"]
            path = info["path"]
            svg = f'<svg viewBox="0 0 24 24"><path d="{path}"/></svg>'
        else:
            name = key.upper()
            hex_color = "#a855f7"
            svg = fallback_svg
            
        glow_color = f"{hex_color}45" # Add alpha transparency for soft glow
        logo_list_html += f'<div class="company-logo" style="--brand-color: {hex_color}; --brand-glow: {glow_color};" loading="lazy">{svg}<span>{name}</span></div>'

    # Premium custom simple purple line glass illustrative SVG logo (minified to single line)
    logo_html = '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 2px 8px rgba(168,85,247,0.45)); display: block;"><path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2Z" fill="rgba(168, 85, 247, 0.06)" stroke="#a855f7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2V8H20" stroke="#a855f7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="rgba(168, 85, 247, 0.15)"/><line x1="8" y1="12" x2="16" y2="12" stroke="#a855f7" stroke-width="1.6" stroke-linecap="round" opacity="0.85"/><line x1="8" y1="16" x2="14" y2="16" stroke="#00f2fe" stroke-width="1.6" stroke-linecap="round" opacity="0.85"/><circle cx="16" cy="16" r="1.5" fill="#34d399" opacity="0.9"/></svg>'

    html_content = f"""<div class="footer-section">
<div class="marquee-wrapper">
<div class="marquee-heading">Trusted by Skills Used at Leading Companies</div>
<div class="marquee-subtitle">Prepare for opportunities at the world's leading technology and consulting companies.</div>
<div class="marquee-container">
<div class="marquee-track">
<div class="marquee-content">{logo_list_html}</div>
<div class="marquee-content">{logo_list_html}</div>
</div>
</div>
</div>
<footer class="main-footer">
<div class="footer-glow"></div>
<div class="footer-grid">
<div class="footer-col" style="align-items: flex-start;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
{logo_html}
<span style="font-family:'Space Grotesk',sans-serif; font-size:19px; font-weight:700; background: linear-gradient(135deg, #ffffff 30%, #c4b5fd 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">AI Resume Analyzer Pro</span>
</div>
<p>AI-powered resume analysis platform helping candidates improve ATS score, identify skill gaps, compare resumes with job descriptions, and prepare for interviews.</p>
</div>
<div class="footer-col">
<h4 class="footer-col-title">Quick Links</h4>
<ul class="footer-links">
<li><a href="#Home">Home</a></li>
<li><a href="#Dashboard">Dashboard</a></li>
<li><a href="#ResumeReview">Resume Review</a></li>
<li><a href="#JDMatch">JD Match</a></li>
<li><a href="#Interview">Interview</a></li>
<li><a href="#Settings">Settings</a></li>
</ul>
</div>
<div class="footer-col">
<h4 class="footer-col-title">Contact</h4>
<ul class="footer-links">
<li>
<a href="mailto:{EMAIL_LINK}">
<svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
Email
</a>
</li>
<li>
<a href="{LINKEDIN_LINK}" target="_blank">
<svg viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
LinkedIn
</a>
</li>
<li>
<a href="{GITHUB_LINK}" target="_blank">
<svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
GitHub
</a>
</li>
<li>
<a href="{PORTFOLIO_LINK}" target="_blank">
<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
Portfolio
</a>
</li>
<li>
<a href="#">
<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
India
</a>
</li>
</ul>
</div>
<div class="footer-col">
<h4 class="footer-col-title">Resources</h4>
<ul class="footer-links">
<li><a href="#">Privacy Policy</a></li>
<li><a href="#">Terms of Service</a></li>
<li><a href="#">FAQ</a></li>
<li><a href="#">Support</a></li>
<li><a href="#">Feedback</a></li>
</ul>
</div>
</div>
<hr class="footer-divider">
<div class="footer-bottom">
<div class="footer-copy">
<span>&copy; 2026 <span class="highlight">AI Resume Analyzer Pro</span></span>
<span>Designed & Developed by <span class="highlight">Rajat Rangra</span></span>
</div>
<div class="social-links">
<a class="social-icon-btn" href="{LINKEDIN_LINK}" target="_blank">
<svg viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
</a>
<a class="social-icon-btn" href="{GITHUB_LINK}" target="_blank">
<svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
</a>
<a class="social-icon-btn" href="{PORTFOLIO_LINK}" target="_blank">
<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
</a>
<a class="social-icon-btn" href="mailto:{EMAIL_LINK}">
<svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
</a>
</div>
</div>
</footer>
</div>"""
    st.markdown(html_content, unsafe_allow_html=True)

