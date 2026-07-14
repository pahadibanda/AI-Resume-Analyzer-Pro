"""Premium AI loading screen component.

Renders a fixed, full-screen animated loading overlay that locks scrolling
and plays a continuous client-side animation while the main thread is blocked
by API calls. This prevents layout glitches and provides a smooth UX.
"""
import streamlit as st

_LOADING_CSS = """
<style>
/* Lock scrolling on the body while loader is active */
body { 
  overflow: hidden !important; 
}

.loader-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(5, 1, 15, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 999999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.scanner-box {
  width: 140px; height: 140px;
  position: relative;
  margin-bottom: 40px;
}

.scanner-box svg {
  width: 100%; height: 100%;
  fill: none; 
  stroke: rgba(167, 139, 250, 0.6); 
  stroke-width: 1.5;
  filter: drop-shadow(0 0 12px rgba(124,58,237,0.4));
}

.scanner-line {
  position: absolute;
  left: 5%; right: 5%; height: 3px;
  background: #a78bfa;
  border-radius: 4px;
  box-shadow: 0 0 16px #c4b5fd, 0 0 32px #7c3aed;
  animation: scan 1.8s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

@keyframes scan {
  0% { top: 5%; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 95%; opacity: 0; }
}

.loader-text {
  font-family: 'Outfit', sans-serif;
  font-size: 28px; font-weight: 800;
  color: #f1f5f9;
  letter-spacing: 0.02em;
  background: linear-gradient(135deg, #ffffff 20%, #c4b5fd 60%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: pulseText 2s ease-in-out infinite alternate;
}

@keyframes pulseText {
  0% { transform: scale(0.98); filter: brightness(0.8); }
  100% { transform: scale(1.02); filter: brightness(1.2); }
}

.loader-subtext {
  font-family: 'Inter', sans-serif;
  font-size: 15px; font-weight: 500;
  color: #94a3b8;
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.loader-subtext::after {
  content: '';
  animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
  0%, 20% { content: ''; }
  40% { content: '.'; }
  60% { content: '..'; }
  80%, 100% { content: '...'; }
}
</style>
"""


def run_loading_animation(placeholder) -> None:
    """Render the fixed loading overlay."""
    html = f"""
{_LOADING_CSS}
<div class="loader-overlay">
  <div class="scanner-box">
    <svg viewBox="0 0 24 24">
       <!-- Corner brackets -->
       <path d="M4 7V4h3m10 0h3v3M4 17v3h3m10 0h3v3" stroke-linecap="round" stroke-linejoin="round"/>
       <!-- Inner abstract document/chip shape -->
       <rect x="7" y="7" width="10" height="10" rx="2" stroke="rgba(124,58,237,0.3)" fill="rgba(124,58,237,0.05)"/>
       <line x1="10" y1="10" x2="14" y2="10" stroke="rgba(167,139,250,0.5)" stroke-linecap="round"/>
       <line x1="10" y1="14" x2="14" y2="14" stroke="rgba(167,139,250,0.5)" stroke-linecap="round"/>
    </svg>
    <div class="scanner-line"></div>
  </div>
  <div class="loader-text">AI is Analyzing Your Profile</div>
  <div class="loader-subtext">Extracting skills, computing ATS score, and generating insights</div>
</div>
"""
    placeholder.markdown(html, unsafe_allow_html=True)
    # We do NOT use time.sleep() here anymore. The CSS animation plays on the client
    # while the Python thread continues to fetch from the API in the background.
