def create_gauge(score, match_score=None, show_ats_bar=True, show_match_bar=True):
    """Generates HTML with an SVG semi-circular progress gauge styled like Ookla Speedtest,
    with an increased gauge size (w-72 h-36) and flexible progress bar options.
    Shows the ATS Score bar, JD Match bar, or both based on options.
    Fully responsive for light/dark theme transitions using translucent styling.
    """
    # Determine the status and glowing shadow color
    if score < 50:
        glow_color = "#ef4444"  # Red
        category = "Needs Work"
    elif score < 80:
        glow_color = "#fbbf24"  # Amber
        category = "Good Match"
    else:
        glow_color = "#10b981"  # Emerald
        category = "Excellent"

    # Semicircular arc path (Radius = 40, Center = (50, 50))
    total_length = 125.6
    offset = total_length - (total_length * (score / 100))

    # Calculate height and prepare bars html
    bars_html = []
    
    if show_ats_bar:
        bars_html.append(f"""
        <div style="width: 100%; margin-top: 12px; font-family: 'Inter', sans-serif;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--text-color, #94a3b8); margin-bottom: 5px;">
                <span style="font-weight: 600;">ATS Score Strength</span>
                <span style="font-weight: 700; color: #a78bfa;">{score}%</span>
            </div>
            <div style="width: 100%; background: rgba(124, 58, 237, 0.08); border-radius: 999px; height: 8px; overflow: hidden; border: 1px solid rgba(124, 58, 237, 0.15);">
                <div style="background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%); height: 100%; border-radius: 999px; width: {score}%;"></div>
            </div>
        </div>
        """)

    if show_match_bar and match_score is not None:
        bars_html.append(f"""
        <div style="width: 100%; margin-top: 12px; font-family: 'Inter', sans-serif;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--text-color, #94a3b8); margin-bottom: 5px;">
                <span style="font-weight: 600;">Job Description Match</span>
                <span style="font-weight: 700; color: #34d399;">{match_score}%</span>
            </div>
            <div style="width: 100%; background: rgba(16, 185, 129, 0.08); border-radius: 999px; height: 8px; overflow: hidden; border: 1px solid rgba(16, 185, 129, 0.15);">
                <div style="background: linear-gradient(90deg, #059669 0%, #34d399 100%); height: 100%; border-radius: 999px; width: {match_score}%;"></div>
            </div>
        </div>
        """)

    num_bars = len(bars_html)
    if num_bars == 2:
        card_height = "400px"
    elif num_bars == 1:
        card_height = "330px"
    else:
        card_height = "260px"

    bars_joined = "".join(bars_html)
    # Add top border separator if there are bars
    if num_bars > 0:
        bars_joined = f"""<div style="width: 100%; margin-top: 16px; border-top: 1px solid rgba(124, 58, 237, 0.15); padding-top: 10px;">{bars_joined}</div>"""

    # No outer card wrapper — caller's card div controls the background/border/padding
    html_code = f"""
<style>
@property --score-val-{score} {{
  syntax: '<integer>';
  inherits: false;
  initial-value: 0;
}}
@keyframes count-up-{score} {{
  from {{ --score-val-{score}: 0; }}
  to {{ --score-val-{score}: {score}; }}
}}
.gauge-num-{score} {{
  animation: count-up-{score} 1.8s cubic-bezier(0.1, 0.8, 0.25, 1) forwards;
  counter-reset: scoreVar var(--score-val-{score});
  font-size: 0px !important;
}}
.gauge-num-{score}::after {{
  content: counter(scoreVar) "%";
  font-size: 11px !important;
}}
@keyframes draw-gauge {{
from {{ stroke-dashoffset: {total_length}; }}
to {{ stroke-dashoffset: {offset}; }}
}}
.active-gauge-path {{
stroke-dasharray: {total_length};
stroke-dashoffset: {total_length};
animation: draw-gauge 1.8s cubic-bezier(0.1, 0.8, 0.25, 1) forwards;
}}
</style>
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 8px 0;">
<svg class="w-72 h-36" viewBox="0 0 100 55" style="width:100%; max-width:320px; height:auto; margin-top: 5px;">
<defs>
<linearGradient id="speedtest-grad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#ef4444" />
<stop offset="50%" stop-color="#f59e0b" />
<stop offset="100%" stop-color="#10b981" />
</linearGradient>
</defs>
<path d="M 10,50 A 40,40 0 0,1 90,50" fill="none" stroke="rgba(124,58,237,0.06)" stroke-width="7" stroke-linecap="round" />
<path class="active-gauge-path" d="M 10,50 A 40,40 0 0,1 90,50" fill="none" stroke="url(#speedtest-grad)" stroke-width="7" stroke-linecap="round" style="filter: drop-shadow(0px 3px 6px {glow_color});" />
<foreignObject x="30" y="30" width="40" height="15">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display:flex; align-items:center; justify-content:center; width:100%; height:100%; color:#ffffff; font-family:'Outfit', sans-serif; font-weight:bold; text-align:center;" class="gauge-num-{score}">{score}%</div>
</foreignObject>
<text x="50" y="48" text-anchor="middle" fill="#94a3b8" font-size="4" font-family="Inter, sans-serif" font-weight="600">{category.upper()}</text>
</svg>
{bars_joined}
</div>"""
    return html_code.replace("    ", " ")