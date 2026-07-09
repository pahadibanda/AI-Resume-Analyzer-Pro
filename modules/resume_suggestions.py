def get_resume_suggestions(missing_skills):

    suggestions = []

    if "Python" in missing_skills:
        suggestions.append("Learn Python programming.")

    if "SQL" in missing_skills:
        suggestions.append("Improve SQL skills.")

    if "Power BI" in missing_skills:
        suggestions.append("Build Power BI Dashboard projects.")

    if "Excel" in missing_skills:
        suggestions.append("Practice Advanced Excel.")

    if "Tableau" in missing_skills:
        suggestions.append("Learn Tableau.")

    if "Statistics" in missing_skills:
        suggestions.append("Study Statistics.")

    if len(suggestions) == 0:
        suggestions.append("Great! Your resume matches the required skills well.")

    return suggestions