def calculate_resume_score(found_skills):

    required_skills = [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "Git",
        "GitHub"
    ]

    score = round((len(found_skills) / len(required_skills)) * 100)

    if score > 100:
        score = 100

    return score