"""Match score calculator — compares resume skills against JD skills.

Returns:
    score (int): 0-100 percentage match
    matched (list[str]): skills present in both resume and JD
    missing (list[str]): skills required by JD but absent from resume
"""


def calculate_match_score(
    resume_skills: list, job_skills: list
) -> tuple[int, list, list]:
    """Return (score%, matched_skills, missing_skills).

    Guards against empty job_skills list to prevent ZeroDivisionError.
    """
    if not job_skills:
        return 0, [], []

    resume_lower = {s.lower() for s in resume_skills}
    matched = [s for s in job_skills if s.lower() in resume_lower]
    missing = [s for s in job_skills if s.lower() not in resume_lower]
    score = round((len(matched) / len(job_skills)) * 100)
    return score, matched, missing