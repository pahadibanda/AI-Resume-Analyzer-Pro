def extract_skills(text):

    skills = [
        "Python",
        "SQL",
        "Power BI",
        "Excel",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Scikit-learn",
        "Git",
        "GitHub",
        "Statistics",
        "Data Analysis"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills