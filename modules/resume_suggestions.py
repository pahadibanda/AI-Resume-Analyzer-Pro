"""AI-powered resume improvement suggestions using shared LLM.

Falls back to rule-based local logic on any API failure.
"""
import json
from langchain_core.messages import HumanMessage
from modules.llm_client import llm


def get_resume_suggestions(missing_skills: list) -> list[str]:
    """Return 3-5 actionable improvement suggestions based on missing skills."""
    if not missing_skills:
        return [
            "Great match! Your resume covers all required skills.",
            "Consider adding quantified achievements (e.g., 'Improved query speed by 40%').",
            "Ensure your resume has a clean ATS-friendly format with standard section headers.",
        ]

    prompt = f"""You are an expert Career Advisor and Technical Recruiter.

The candidate is missing these skills from their resume compared to the job description:
{", ".join(missing_skills)}

Generate exactly 4 highly specific, actionable suggestions to help them acquire or
demonstrate these skills. Each suggestion should:
- Reference a specific skill from the missing list
- Mention a concrete action (e.g., specific course, project, certification)
- Be 1-2 sentences maximum

Respond ONLY with a JSON array of strings. No markdown, no preamble.
Example: ["suggestion 1", "suggestion 2", "suggestion 3", "suggestion 4"]
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        # Strip markdown code fences if present
        for marker in ("```json", "```"):
            if content.startswith(marker):
                content = content[len(marker):]
            if content.endswith("```"):
                content = content[:-3]
        content = content.strip()
        suggestions = json.loads(content)
        if isinstance(suggestions, list) and suggestions:
            return [str(s) for s in suggestions[:5]]
    except Exception:
        pass

    # Rule-based fallback
    suggestions: list[str] = []
    skills_lower = [s.lower() for s in missing_skills]

    fallback_map = {
        "docker": "Learn Docker by containerizing a personal Python/Node project and pushing to Docker Hub.",
        "kubernetes": "Complete the Kubernetes for Developers course on KodeKloud or A Cloud Guru.",
        "aws": "Earn the AWS Cloud Practitioner certification — it's beginner-friendly and highly valued.",
        "azure": "Earn the AZ-900 Microsoft Azure Fundamentals certification.",
        "gcp": "Complete the Google Cloud Digital Leader certification as a starting point.",
        "tensorflow": "Build a deep learning project using TensorFlow and publish it to GitHub.",
        "pytorch": "Implement a neural network from scratch using PyTorch and document it.",
        "sql": "Practice 50+ SQL problems on LeetCode or HackerRank to sharpen query skills.",
        "power bi": "Build 3 interactive Power BI dashboards using public datasets and share them.",
        "tableau": "Complete Tableau Public's free training and publish 2 visualizations.",
        "react": "Build a React portfolio app to demonstrate frontend development skills.",
        "typescript": "Refactor an existing JavaScript project to TypeScript and document the process.",
        "machine learning": "Complete Andrew Ng's Machine Learning course on Coursera and build a project.",
        "statistics": "Study A/B testing, regression, and hypothesis testing using Khan Academy or Coursera.",
    }

    for skill_lower, suggestion in fallback_map.items():
        if skill_lower in skills_lower and len(suggestions) < 4:
            suggestions.append(suggestion)

    if not suggestions:
        for skill in missing_skills[:3]:
            suggestions.append(
                f"Build a hands-on project featuring '{skill}' and add it to your GitHub portfolio."
            )

    return suggestions