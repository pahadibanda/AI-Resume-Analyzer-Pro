import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def generate_questions(resume_text):
    prompt = f"""
You are an Interview Expert.

Based on this resume generate:

1. Python Questions

2. SQL Questions

3. Data Analytics Questions

4. HR Questions

Return 5 questions for each category.

Resume:

{resume_text}
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content