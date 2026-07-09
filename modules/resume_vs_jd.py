from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
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