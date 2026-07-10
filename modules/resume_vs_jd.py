from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)
def compare_resume_with_jd(resume_text, jd_text):

    prompt = f"""
Compare this Resume with the Job Description.

Resume:

{resume_text}

Job Description:

{jd_text}

Return:

1 Strengths

2 Weaknesses

3 Missing Skills

4 Improvement Tips

5 Final Recommendation

"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content