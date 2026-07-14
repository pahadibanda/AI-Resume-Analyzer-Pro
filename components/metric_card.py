"""Premium animated metric cards component.

Renders a 6-card grid (2 rows × 3) with JS count-up animation,
gradient colored value text, SVG icons, and glassmorphic styling.
"""
import streamlit as st


_CARDS_CSS = """
<style>
@keyframes cardEntrance {
  from { opacity: 0; transform: translateY(22px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0)   scale(1);    }
}

.metric-card {
  position: relative; overflow: hidden;
  padding: 24px 20px 20px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(8px) saturate(145%);
  -webkit-backdrop-filter: blur(8px) saturate(145%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-top: 1px solid rgba(255, 255, 255, 0.18);
  border-left: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 0 rgba(255, 255, 255, 0.06);
  transition: all 0.38s cubic-bezier(0.4,0,0.2,1);
  animation: cardEntrance 0.6s cubic-bezier(0.16,1,0.3,1) both;
  cursor: default;
}
/* Stagger delays */
.metric-card:nth-child(1) { animation-delay: 0.04s; }
.metric-card:nth-child(2) { animation-delay: 0.08s; }
.metric-card:nth-child(3) { animation-delay: 0.12s; }
.metric-card:nth-child(4) { animation-delay: 0.16s; }
.metric-card:nth-child(5) { animation-delay: 0.20s; }
.metric-card:nth-child(6) { animation-delay: 0.24s; }

/* Accent left border */
.metric-card::before {
  content: '';
  position: absolute; left: 0; top: 16%; bottom: 16%;
  width: 3px; border-radius: 0 3px 3px 0;
}

/* Hover lift + glow */
.metric-card:hover {
  transform: translateY(-5px);
  border-color: rgba(255, 255, 255, 0.25);
  border-top-color: rgba(255, 255, 255, 0.4);
}

/* Shimmer on hover — same sweep as content-card */
.metric-card::after {
  content: '';
  position: absolute;
  top: -50%; left: -150%;
  width: 50%; height: 200%;
  background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.10) 50%, rgba(255,255,255,0) 100%);
  transform: rotate(25deg);
  pointer-events: none; z-index: 99;
}
.metric-card:hover::after {
  left: 150%;
  transition: left 0.85s cubic-bezier(0.16,1,0.3,1);
}

/* Top row: icon + badge */
.mc-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 14px; }
.mc-icon-wrap {
  width: 42px; height: 42px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
}
.mc-icon-wrap svg { width: 22px; height: 22px; fill: currentColor; }
.mc-badge {
  font-family: 'Inter', sans-serif;
  font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 3px 8px; border-radius: 999px;
}

/* Value — use solid color per theme (no webkit clip trick = always visible) */
.mc-value {
  font-family: 'Outfit', sans-serif;
  font-size: 38px; font-weight: 900; line-height: 1;
  margin-bottom: 5px;
  color: #f1f5f9;  /* base fallback */
}

/* Label */
.mc-label {
  font-family: 'Outfit', sans-serif;
  font-size: 14px; font-weight: 700; letter-spacing: 0.01em;
  color: #e2e8f0; margin-bottom: 3px;
}

/* Subtitle */
.mc-sub {
  font-family: 'Inter', sans-serif;
  font-size: 11px; font-weight: 500; color: #64748b;
}

/* ── Accent themes ─────────────────────── */
.mc-purple {
  background: linear-gradient(135deg, rgba(167, 139, 250, 0.07) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
  border-color: rgba(167, 139, 250, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(124, 58, 237, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
.mc-purple::before { background: linear-gradient(#7c3aed, #a78bfa); }
.mc-purple .mc-icon-wrap { background: rgba(124,58,237,0.15); color: #a78bfa; }
.mc-purple .mc-badge { background: rgba(124,58,237,0.15); color: #c4b5fd; border: 1px solid rgba(124,58,237,0.3); }
.mc-purple .mc-value { color: #a78bfa; }
.mc-purple:hover {
  background: linear-gradient(135deg, rgba(167, 139, 250, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
  box-shadow: 0 20px 50px rgba(124, 58, 237, 0.2), 0 0 30px rgba(124, 58, 237, 0.1) !important;
}

.mc-green {
  background: linear-gradient(135deg, rgba(110, 231, 183, 0.07) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
  border-color: rgba(110, 231, 183, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(16, 185, 129, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
.mc-green::before  { background: linear-gradient(#059669, #34d399); }
.mc-green .mc-icon-wrap  { background: rgba(16,185,129,0.15); color: #34d399; }
.mc-green .mc-badge  { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }
.mc-green .mc-value  { color: #34d399; }
.mc-green:hover {
  background: linear-gradient(135deg, rgba(110, 231, 183, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
  box-shadow: 0 20px 50px rgba(16, 185, 129, 0.25), 0 0 30px rgba(16, 185, 129, 0.1) !important;
}

.mc-blue {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.07) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
  border-color: rgba(147, 197, 253, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
.mc-blue::before   { background: linear-gradient(#1d4ed8, #60a5fa); }
.mc-blue .mc-icon-wrap   { background: rgba(59,130,246,0.15); color: #60a5fa; }
.mc-blue .mc-badge   { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
.mc-blue .mc-value   { color: #60a5fa; }
.mc-blue:hover {
  background: linear-gradient(135deg, rgba(147, 197, 253, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
  box-shadow: 0 20px 50px rgba(59, 130, 246, 0.25), 0 0 30px rgba(59, 130, 246, 0.1) !important;
}

.mc-red {
  background: linear-gradient(135deg, rgba(252, 165, 165, 0.07) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
  border-color: rgba(252, 165, 165, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(239, 68, 68, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
.mc-red::before    { background: linear-gradient(#b91c1c, #f87171); }
.mc-red .mc-icon-wrap    { background: rgba(239,68,68,0.15); color: #f87171; }
.mc-red .mc-badge    { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.mc-red .mc-value    { color: #f87171; }
.mc-red:hover {
  background: linear-gradient(135deg, rgba(252, 165, 165, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
  box-shadow: 0 20px 50px rgba(239, 68, 68, 0.25), 0 0 30px rgba(239, 68, 68, 0.1) !important;
}

.mc-amber {
  background: linear-gradient(135deg, rgba(253, 230, 138, 0.07) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
  border-color: rgba(253, 230, 138, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(245, 158, 11, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
.mc-amber::before  { background: linear-gradient(#b45309, #fbbf24); }
.mc-amber .mc-icon-wrap  { background: rgba(245,158,11,0.15); color: #fbbf24; }
.mc-amber .mc-badge  { background: rgba(245,158,11,0.15); color: #fde68a; border: 1px solid rgba(245,158,11,0.3); }
.mc-amber .mc-value  { color: #fbbf24; }
.mc-amber:hover {
  background: linear-gradient(135deg, rgba(253, 230, 138, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
  box-shadow: 0 20px 50px rgba(245, 158, 11, 0.25), 0 0 30px rgba(245, 158, 11, 0.1) !important;
}

.mc-indigo {
  background: linear-gradient(135deg, rgba(165, 180, 252, 0.07) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
  border-color: rgba(165, 180, 252, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
.mc-indigo::before { background: linear-gradient(#4338ca, #818cf8); }
.mc-indigo .mc-icon-wrap { background: rgba(99,102,241,0.15); color: #818cf8; }
.mc-indigo .mc-badge { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.3); }
.mc-indigo .mc-value { color: #818cf8; }
.mc-indigo:hover {
  background: linear-gradient(135deg, rgba(165, 180, 252, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
  box-shadow: 0 20px 50px rgba(99, 102, 241, 0.25), 0 0 30px rgba(99, 102, 241, 0.1) !important;
}


/* ── Count-up animation ─────────────────── */
@keyframes countUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.mc-animated { animation: countUp 0.6s ease forwards; }
</style>
"""

# SVG icon paths for each card
_ICONS = {
    "ats":       '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>',
    "match":     '<svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>',
    "skills":    '<svg viewBox="0 0 24 24"><path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3zM5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>',
    "missing":   '<svg viewBox="0 0 24 24"><path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/></svg>',
    "roles":     '<svg viewBox="0 0 24 24"><path d="M20 6h-2.18c.07-.44.18-.88.18-1.34C18 2.54 15.46 0 12.34 0c-1.62 0-3.06.66-4.12 1.72L12 5.5l3.78-3.78C16.42 2.56 17.26 3 18 3.33V6H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zM12 7c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm4 10H8v-1c0-1.33 2.67-2 4-2s4 .67 4 2v1z"/></svg>',
    "questions": '<svg viewBox="0 0 24 24"><path d="M11.07 12.85c.77-1.39 2.25-2.21 3.11-3.44.91-1.29.4-3.7-2.18-3.7-1.69 0-2.52 1.28-2.87 2.34L7.1 7.05C7.83 4.82 9.72 3 12.03 3c2.51 0 4.24 1.22 5.15 2.79.78 1.36.86 3.78-.4 5.31-.92 1.09-2.19 1.59-2.89 2.77-.28.47-.38.88-.38 1.3h-2.26c.01-.56.09-1.14.82-2.32zM14 20c0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2 2 .9 2 2z"/></svg>',
}

_CARDS_DATA = [
    ("ats",       "ATS Score",          "{ats}%",      "AI Evaluated",         "mc-purple"),
    ("match",     "JD Match",           "{match}%",    "Job Compatible",       "mc-green"),
    ("skills",    "Skills Found",       "{skills}",    "Detected in Resume",   "mc-blue"),
    ("missing",   "Missing Skills",     "{missing}",   "From Job Description", "mc-red"),
    ("roles",     "Recommended Roles",  "{roles}",     "Career Paths",         "mc-amber"),
    ("questions", "Questions",          "{questions}", "AI Generated",         "mc-indigo"),
]

_BADGE_LABELS = {
    "ats":       "Score",
    "match":     "Match",
    "skills":    "Found",
    "missing":   "Gaps",
    "roles":     "Roles",
    "questions": "Q&A",
}


def render_metric_cards(
    resume_score: int = 0,
    match_score: int = 0,
    num_skills: int = 0,
    num_missing: int = 0,
    num_roles: int = 0,
    num_questions: int = 0,
) -> None:
    """Render the 6 animated metric cards with count-up values."""
    st.markdown(_CARDS_CSS, unsafe_allow_html=True)

    values = {
        "ats":       resume_score,
        "match":     match_score,
        "skills":    num_skills,
        "missing":   num_missing,
        "roles":     num_roles,
        "questions": num_questions,
    }

    # JS count-up rendered inline per card
    count_up_script = """
<script>
(function() {
  var els = document.querySelectorAll('[data-countup]');
  els.forEach(function(el) {
    var target = parseFloat(el.getAttribute('data-countup'));
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 1200;
    var startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 4);
      el.textContent = Math.round(target * eased) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });
})();
</script>
"""

    row1 = st.columns(3, gap="medium")
    row2 = st.columns(3, gap="medium")
    all_cols = row1 + row2

    for col, (key, label, val_tpl, sub, accent) in zip(all_cols, _CARDS_DATA):
        raw_val = values.get(key, 0)
        suffix = "%" if "%" in val_tpl else ""
        icon_svg = _ICONS.get(key, "")
        badge = _BADGE_LABELS.get(key, "")

        with col:
            st.markdown(f"""
<div class="metric-card {accent}">
  <div class="mc-top">
    <div class="mc-icon-wrap">{icon_svg}</div>
    <span class="mc-badge">{badge}</span>
  </div>
  <div class="mc-value mc-animated" data-countup="{raw_val}" data-suffix="{suffix}">{raw_val}{suffix}</div>
  <div class="mc-label">{label}</div>
  <div class="mc-sub">{sub}</div>
</div>
""", unsafe_allow_html=True)

    # inject count-up script once
    st.markdown(count_up_script, unsafe_allow_html=True)