"""Skills visualization module.

Provides:
- create_skill_chart(): horizontal bar chart with ghost tracks and proficiency bars
- create_radar_chart(): radar/spider chart for matched vs missing skills

CHART_ROW_PX: exported constant — iframe height = CHART_HEADER_PX + n_skills * CHART_ROW_PX
"""
import hashlib
import plotly.graph_objects as go

# ── Per-row height used by the iframe to auto-scale the card ───────────────
CHART_ROW_PX    = 40   # height per skill row
CHART_HEADER_PX = 20   # top/bottom padding inside the chart

# Premium gradient palette  purple → indigo → blue → cyan → teal
_SKILL_COLORS = [
    "#8b5cf6", "#7c3aed", "#6d28d9", "#a78bfa",
    "#6366f1", "#4f46e5", "#818cf8", "#3b82f6",
    "#2563eb", "#0ea5e9", "#06b6d4", "#22d3ee",
    "#10b981", "#14b8a6", "#34d399", "#5eead4",
]


def _skill_strength(skill: str) -> float:
    """Return a deterministic proficiency value 0.72–1.0 based on skill name hash.

    This gives the chart visual variety (bars aren't all the same width)
    without needing real proficiency data.
    """
    h = int(hashlib.md5(skill.encode()).hexdigest(), 16)
    return 0.72 + (h % 1000) / 3571   # maps into [0.72, 1.0]


def create_skill_chart(skills: list) -> go.Figure:
    """Premium horizontal bar chart: ghost track + proficiency bar + % label.

    Design:
    - Ghost (track) bar at full width (opacity 0.10) — shows max extent
    - Colored proficiency bar — length varies per skill (hash-based 72–100%)
    - Percentage text annotation at bar end
    - Wider left margin so labels have clear breathing room from bars
    - Outfit lavender font for skill labels
    - Slim bars with generous gap (bargap=0.45) for an airy, modern feel
    """
    if not skills:
        skills = ["No Skills Detected"]

    # Sort A→Z then reverse so A is at the top
    sorted_skills = sorted(skills, reverse=True)
    n = len(sorted_skills)

    colours    = [_SKILL_COLORS[i % len(_SKILL_COLORS)] for i in range(n)]
    strengths  = [_skill_strength(s) for s in sorted_skills]

    fig = go.Figure()

    # ── Layer 1: Ghost / track bars (full width, very low opacity) ──────────
    fig.add_trace(go.Bar(
        x=[1.0] * n,
        y=sorted_skills,
        orientation="h",
        marker=dict(
            color=["rgba(139,92,246,0.10)"] * n,
            line=dict(width=0),
            cornerradius=8,
        ),
        hoverinfo="skip",
        showlegend=False,
    ))

    # ── Layer 2: Proficiency bars (varying length per skill) ─────────────────
    fig.add_trace(go.Bar(
        x=strengths,
        y=sorted_skills,
        orientation="h",
        marker=dict(
            color=colours,
            line=dict(width=0),
            cornerradius=8,
            opacity=0.92,
        ),
        text=[f"{int(s * 100)}%" for s in strengths],
        textposition="outside",
        textfont=dict(
            size=11,
            color="#a78bfa",
            family="Outfit, sans-serif",
        ),
        hovertemplate="<b>%{y}</b>  %{text}<extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        barmode="overlay",
        xaxis=dict(
            visible=False,
            showgrid=False,
            range=[0, 1.18],   # extra room for % label outside bar
        ),
        yaxis=dict(
            showgrid=False,
            title="",
            tickfont=dict(
                size=13,
                color="#c4b5fd",
                family="Outfit, Inter, sans-serif",
            ),
            autorange="reversed",
            categoryorder="array",
            categoryarray=sorted_skills,
            ticklabelstandoff=10,   # gap between label text and bar
        ),
        height=max(200, n * CHART_ROW_PX + CHART_HEADER_PX),
        bargap=0.42,    # generous gap between rows
        margin=dict(l=145, r=55, t=8, b=8),
    )
    return fig




def create_radar_chart(matched: list, missing: list) -> go.Figure:
    """Radar chart comparing matched vs missing JD skills coverage."""
    all_skills = list(dict.fromkeys(matched + missing))  # preserve order, dedupe
    if not all_skills:
        all_skills = ["No Data"]

    matched_set = {s.lower() for s in matched}
    match_vals  = [1 if s.lower() in matched_set else 0 for s in all_skills]
    miss_vals   = [0 if s.lower() in matched_set else 1 for s in all_skills]

    # Close the radar loop
    cats = all_skills + [all_skills[0]]
    mv   = match_vals + [match_vals[0]]
    msv  = miss_vals  + [miss_vals[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=mv, theta=cats, fill="toself",
        name="Matched",
        line=dict(color="#10B981", width=2.5),
        fillcolor="rgba(16,185,129,0.18)",
        marker=dict(color="#10B981", size=6),
    ))
    fig.add_trace(go.Scatterpolar(
        r=msv, theta=cats, fill="toself",
        name="Missing",
        line=dict(color="#f472b6", width=2.5),
        fillcolor="rgba(244,114,182,0.12)",
        marker=dict(color="#f472b6", size=6),
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f1f5f9", family="Outfit, Inter, sans-serif", size=13),
        margin=dict(l=15, r=15, t=10, b=10),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=False,
                gridcolor="rgba(139,92,246,0.15)",
                linecolor="rgba(139,92,246,0.1)",
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color="#e2e8f0", family="Inter, sans-serif"),
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(139,92,246,0.15)",
            ),
        ),
        legend=dict(
            font=dict(color="#e2e8f0", size=13),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(139,92,246,0.15)",
            borderwidth=1,
            orientation="h",
            x=0.5, xanchor="center", y=-0.08,
        ),
        height=330,
    )
    return fig