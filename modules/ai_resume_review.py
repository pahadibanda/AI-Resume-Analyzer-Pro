"""AI Resume Reviewer using shared LLM client.

Returns a rich markdown-formatted review with structured sections.
"""
from langchain_core.messages import HumanMessage
from modules.llm_client import llm


def review_resume(resume_text: str) -> str:
    """Analyze resume and return structured markdown review."""
    prompt = f"""You are a Senior ATS Resume Expert and Career Coach with 15 years of experience
 reviewing resumes for top tech companies.

Analyze the following resume and produce a **detailed, structured markdown report**.

Use EXACTLY this format with these section headers:

## Executive Summary
A 2-3 sentence overall assessment of the candidate.

## Key Strengths
- List 4-6 concrete strengths with specific evidence from the resume

## Areas for Improvement
- List 4-6 specific, actionable weaknesses

## ATS Optimization Tips
- List 4-5 specific tips to improve ATS compatibility (keywords, formatting, sections)

## Career Path Recommendations
- List 3-4 recommended job titles that match this profile

## Action Items
- List 3-5 immediate next steps the candidate should take

Resume:
{resume_text}

Be specific, professional, and actionable. Use markdown formatting throughout.
Do NOT add any preamble or conversational text. Start directly with ## Executive Summary.
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"## AI Review Unavailable\n\nCould not connect to AI service: {e}\n\nPlease check your GROQ_API_KEY and try again."