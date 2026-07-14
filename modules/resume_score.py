"""Professional multi-factor ATS resume score calculator.

Score (0–100) is computed across five weighted dimensions modeled after
real ATS systems used by companies like Workday, Greenhouse, and Lever:

  Factor                   Weight   Logic
  ─────────────────────────────────────────────────────────────────
  1. Skills Breadth          35 %   # detected skills vs. target (20)
  2. Contact Completeness    15 %   Email + Phone + LinkedIn/GitHub
  3. Section Coverage        20 %   Standard resume sections present
  4. Action Verbs            15 %   Power verbs indicating impact
  5. Quantified Achievements 15 %   Metrics: %, $, numbers, ratios

Minimum floor of 18 prevents zero scores on sparse resumes.
Maximum is capped at 100.
"""
import re

# ── Action verbs list (strong resume signal) ────────────────────────────────
_ACTION_VERBS: list[str] = [
    "led", "built", "developed", "designed", "implemented", "managed",
    "created", "launched", "improved", "optimized", "architected",
    "deployed", "automated", "delivered", "accelerated", "reduced",
    "increased", "achieved", "transformed", "spearheaded", "engineered",
    "coordinated", "mentored", "trained", "resolved", "analyzed",
    "streamlined", "scaled", "migrated", "integrated", "established",
]

# ── Standard ATS section headers ────────────────────────────────────────────
_SECTIONS: list[str] = [
    "experience", "education", "skills", "projects", "summary",
    "objective", "certifications", "awards", "publications",
    "volunteer", "languages", "interests",
]

# ── Contact patterns ─────────────────────────────────────────────────────────
_RE_EMAIL   = re.compile(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}")
_RE_PHONE   = re.compile(r"(\+?\d[\d\s\-().]{7,}\d)")
_RE_LINKS   = re.compile(r"(linkedin\.com|github\.com|portfolio|behance|dribbble)", re.I)

# ── Quantified achievement patterns ─────────────────────────────────────────
_RE_METRICS = re.compile(
    r"(\d+\s*%"           # percentages
    r"|\$\s*\d+"          # dollar amounts
    r"|\d+\s*x\b"         # multipliers (2x, 5x)
    r"|\d+\s*k\b"         # thousands (50k)
    r"|\d+\+\s*(users?|clients?|customers?|members?|engineers?)"  # user counts
    r"|\d+\s*(years?|months?)\s+of"  # experience mentions
    r")",
    re.I,
)


def calculate_resume_score(found_skills: list) -> int:
    """Return ATS score 0–100 using multi-factor weighted algorithm.

    Args:
        found_skills: List of skill strings detected in the resume.

    Returns:
        Integer score between 18 (floor) and 100 (cap).
    """
    return _compute_score(found_skills, resume_text="")


def calculate_resume_score_full(found_skills: list, resume_text: str) -> int:
    """Full multi-factor score that also analyses raw resume text.

    Preferred over `calculate_resume_score` when resume text is available.
    """
    return _compute_score(found_skills, resume_text)


def _compute_score(found_skills: list, resume_text: str) -> int:
    text_lower = resume_text.lower() if resume_text else ""

    # ── Factor 1: Skills Breadth (35%) ──────────────────────────────────────
    target_skills = 20
    skills_ratio  = min(len(found_skills) / target_skills, 1.0)
    f1 = skills_ratio * 35

    # ── Factor 2: Contact Completeness (15%) ────────────────────────────────
    if text_lower:
        has_email = 1 if _RE_EMAIL.search(resume_text) else 0
        has_phone = 1 if _RE_PHONE.search(resume_text) else 0
        has_link  = 1 if _RE_LINKS.search(resume_text) else 0
        f2 = (has_email * 6 + has_phone * 5 + has_link * 4)
    else:
        f2 = 7  # neutral when text unavailable

    # ── Factor 3: Section Coverage (20%) ────────────────────────────────────
    if text_lower:
        found_sections = sum(1 for s in _SECTIONS if s in text_lower)
        f3 = min(found_sections / 5, 1.0) * 20
    else:
        f3 = 10

    # ── Factor 4: Action Verbs (15%) ────────────────────────────────────────
    if text_lower:
        found_verbs = sum(
            1 for v in _ACTION_VERBS
            if re.search(r"\b" + v + r"\b", text_lower)
        )
        f4 = min(found_verbs / 8, 1.0) * 15
    else:
        f4 = 7

    # ── Factor 5: Quantified Achievements (15%) ──────────────────────────────
    if text_lower:
        metric_count = len(_RE_METRICS.findall(resume_text))
        f5 = min(metric_count / 5, 1.0) * 15
    else:
        f5 = 5

    raw = f1 + f2 + f3 + f4 + f5
    return max(18, min(100, round(raw)))