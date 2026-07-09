def calculate_match_score(resume_skills, job_skills):

    matched = []
    missing = []

    resume_skills_lower = [skill.lower() for skill in resume_skills]

    for skill in job_skills:
        if skill.lower() in resume_skills_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    score = round((len(matched) / len(job_skills)) * 100)

    return score, matched, missing