"""Expanded skill extractor — 160+ skills across all domains.

Patterns are **precompiled at module load time** to avoid repeated regex
compilation overhead on every `extract_skills()` call.

Domains covered: Programming, Web, Backend, Databases, Data & Analytics,
AI/ML/LLM, Cloud & DevOps, Collaboration, Mobile, Security, Soft Skills.
"""
import re
from typing import NamedTuple


class _SkillPattern(NamedTuple):
    name: str
    pattern: re.Pattern


SKILLS_DATABASE: list[str] = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go",
    "Rust", "Swift", "Kotlin", "Ruby", "PHP", "Scala", "R", "MATLAB",
    "Bash", "Shell", "Perl", "Dart", "Groovy", "Elixir", "Haskell",

    # Web Frontend
    "HTML", "CSS", "React", "Vue", "Angular", "Next.js", "Nuxt.js",
    "Svelte", "jQuery", "Bootstrap", "Tailwind CSS", "SASS", "LESS",
    "Redux", "GraphQL", "REST API", "WebSockets", "Webpack", "Vite",

    # Web Backend
    "Node.js", "Express.js", "Django", "Flask", "FastAPI", "Spring Boot",
    "Laravel", "Rails", "ASP.NET", "NestJS", "Hono", "Fiber",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Cassandra",
    "DynamoDB", "Elasticsearch", "Firebase", "Supabase", "Oracle",
    "Microsoft SQL Server", "MariaDB", "CockroachDB", "Snowflake",

    # Data & Analytics
    "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly",
    "Excel", "Power BI", "Tableau", "Looker", "Google Analytics",
    "Data Analysis", "Data Visualization", "Statistics", "Hypothesis Testing",
    "A/B Testing", "ETL", "Data Warehousing", "Data Engineering",
    "Data Modeling", "Spark", "Hadoop", "Airflow", "dbt", "Kafka",
    "Flink", "Databricks", "Redshift", "BigQuery",

    # AI / ML / LLM (expanded)
    "Machine Learning", "Deep Learning", "Neural Networks", "NLP",
    "Computer Vision", "Scikit-learn", "TensorFlow", "Keras", "PyTorch",
    "Hugging Face", "OpenCV", "LangChain", "LangGraph", "LlamaIndex",
    "LLM", "Generative AI", "RAG", "Vector Database", "Pinecone",
    "Weaviate", "Chroma", "FAISS", "Reinforcement Learning",
    "XGBoost", "LightGBM", "CatBoost", "Random Forest",
    "Regression", "Classification", "Clustering", "Feature Engineering",
    "Model Deployment", "MLOps", "Prompt Engineering", "Fine-tuning",
    "Embeddings", "Transformers", "BERT", "GPT", "OpenAI API",
    "Vertex AI", "SageMaker", "MLflow", "Weights & Biases",

    # Cloud & DevOps
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform", "Ansible",
    "Jenkins", "GitHub Actions", "GitLab CI", "CI/CD", "Linux", "Nginx",
    "Apache", "Serverless", "Microservices", "Helm", "Prometheus", "Grafana",
    "CloudFormation", "Pulumi",

    # Version Control & Collaboration
    "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Notion",
    "Slack", "Agile", "Scrum", "Kanban",

    # Mobile
    "Android", "iOS", "React Native", "Flutter",

    # Security
    "Cybersecurity", "OWASP", "Penetration Testing", "Network Security",
    "OAuth", "JWT", "SSL/TLS",

    # App / Other Frameworks
    "Streamlit", "Gradio", "FastAPI", "Pydantic", "Celery", "RabbitMQ",

    # Soft Skills
    "Communication", "Leadership", "Problem Solving", "Teamwork",
    "Critical Thinking", "Time Management", "Project Management",
    "Mentoring", "Presentation",
]

# ── Precompile all patterns once at module load ──────────────────────────────
_COMPILED: list[_SkillPattern] = [
    _SkillPattern(
        name=skill,
        pattern=re.compile(r"\b" + re.escape(skill.lower()) + r"\b"),
    )
    for skill in SKILLS_DATABASE
]


def extract_skills(text: str) -> list[str]:
    """Return skills found in `text` using precompiled case-insensitive patterns.

    Uses word-boundary matching so short skills like 'R' or 'C' don't
    false-match inside longer words.
    """
    if not text:
        return []
    text_lower = text.lower()
    return [sp.name for sp in _COMPILED if sp.pattern.search(text_lower)]