import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
   model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.3
)

def review_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the following resume.

Give your response in this format:

1. ATS Score (/100)
2. Strengths
3. Weaknesses
4. Missing Skills
5. Resume Improvement Tips
6. Best Suitable Job Roles

Resume:

{resume_text}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content