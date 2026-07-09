def recommend_roles(skills):

    roles = []

    if "Python" in skills and "SQL" in skills:
        roles.append("Data Analyst")

    if "Power BI" in skills and "Excel" in skills:
        roles.append("Business Analyst")

    if "Machine Learning" in skills:
        roles.append("Machine Learning Engineer")

    if "Statistics" in skills and "Python" in skills:
        roles.append("Data Scientist")

    if len(roles) == 0:
        roles.append("Software Engineer")

    return roles