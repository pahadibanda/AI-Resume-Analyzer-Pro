"""Resume vs Job Description comparator using shared LLM.

Returns structured markdown analysis with skill overlap table and verdict.
"""
from langchain_core.messages import HumanMessage
from modules.llm_client import llm


def compare_resume_with_jd(resume_text: str, jd_text: str) -> str:
    """Compare resume against JD and return detailed markdown analysis."""
    prompt = f"""You are an expert Technical Recruiter and Career Advisor.

Compare the candidate's Resume with the Job Description below and produce a
**detailed, structured markdown report**.

Use EXACTLY this format:

## Match Overview
State the overall compatibility percentage and a brief summary (2-3 sentences).

## Aligned Strengths
- List 4-6 specific areas where the resume strongly matches the JD requirements

## Skill Gaps & Missing Requirements
- List specific skills, experiences, or qualifications required by the JD that are missing from the resume

## Skill Comparison Table
Create a markdown table with 3 columns: Skill/Requirement | In Resume? | Priority Level
Include the top 8-10 skills from the JD.

## Recommendations to Bridge the Gap
- List 4-5 specific, actionable steps the candidate can take to improve alignment

## Final Verdict
A clear recommendation: Strong Match / Good Match / Partial Match / Needs Work
Include 2-3 sentences explaining the verdict.

Resume:
{resume_text}

Job Description:
{jd_text}

Be specific, data-driven, and actionable. Start directly with ## Match Overview.
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"## JD Analysis Unavailable\n\nCould not connect to AI service: {e}"