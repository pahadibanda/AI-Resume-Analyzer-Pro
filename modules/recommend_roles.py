"""Career role recommender based on detected skills.

Maps skill combinations to realistic job title recommendations.
Returns a de-duplicated list (max 5).
"""

ROLE_RULES = [
    # Data & Analytics
    ({"Python", "SQL", "Pandas"}, "Data Analyst"),
    ({"Python", "SQL", "Data Analysis"}, "Data Analyst"),
    ({"Power BI", "Excel", "SQL"}, "Business Intelligence Analyst"),
    ({"Tableau", "SQL", "Data Visualization"}, "BI Developer"),
    ({"Python", "Statistics", "Machine Learning"}, "Data Scientist"),
    ({"Machine Learning", "TensorFlow", "PyTorch"}, "Machine Learning Engineer"),
    ({"Deep Learning", "Computer Vision", "PyTorch"}, "Computer Vision Engineer"),
    ({"NLP", "Hugging Face", "LangChain"}, "NLP / LLM Engineer"),
    ({"Spark", "Kafka", "Airflow"}, "Data Engineer"),
    ({"ETL", "Data Warehousing", "SQL"}, "Data Engineer"),
    ({"dbt", "SQL", "Python"}, "Analytics Engineer"),

    # Software Engineering
    ({"Python", "Django", "REST API"}, "Backend Developer"),
    ({"Python", "FastAPI", "Docker"}, "Backend Engineer"),
    ({"Java", "Spring Boot", "REST API"}, "Java Backend Developer"),
    ({"Node.js", "Express.js", "MongoDB"}, "Full Stack Developer (Node)"),
    ({"React", "TypeScript", "REST API"}, "Frontend Developer"),
    ({"React", "Node.js", "MongoDB"}, "MERN Stack Developer"),
    ({"Next.js", "React", "TypeScript"}, "Frontend / Full Stack Developer"),
    ({"Flutter", "Dart"}, "Mobile Developer (Flutter)"),
    ({"Android", "Kotlin"}, "Android Developer"),
    ({"iOS", "Swift"}, "iOS Developer"),

    # DevOps & Cloud
    ({"Docker", "Kubernetes", "CI/CD"}, "DevOps Engineer"),
    ({"AWS", "Terraform", "Docker"}, "Cloud Engineer (AWS)"),
    ({"Azure", "Docker", "Kubernetes"}, "Cloud Engineer (Azure)"),
    ({"GCP", "Terraform", "Kubernetes"}, "Cloud Engineer (GCP)"),
    ({"Linux", "Bash", "Ansible"}, "Site Reliability Engineer"),

    # General fallback
    ({"Python"}, "Python Developer"),
    ({"JavaScript"}, "JavaScript Developer"),
    ({"SQL"}, "Database Administrator"),
]


def recommend_roles(skills: list) -> list[str]:
    """Return up to 5 recommended job roles based on detected skills."""
    skill_set = set(skills)
    roles: list[str] = []

    for required, role in ROLE_RULES:
        if required.issubset(skill_set) and role not in roles:
            roles.append(role)
        if len(roles) >= 5:
            break

    if not roles:
        roles.append("Software Engineer / Generalist")

    return roles