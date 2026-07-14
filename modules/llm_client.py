"""Shared LLM client singleton.

All AI modules import `llm` from here to avoid creating multiple
ChatGoogleGenerativeAI instances at module load time.

Configuration:
    - model:      gemini-1.5-flash (high speed, premium quality)
    - temperature: 0.2
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Accept both GEMINI_API_KEY and GOOGLE_API_KEY for seamless setup
_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not _api_key:
    raise EnvironmentError(
        "GEMINI_API_KEY or GOOGLE_API_KEY is not set. "
        "Add it to your .env file: GEMINI_API_KEY=AIzaSy..."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=_api_key,
    temperature=0.2,
    timeout=45,
)

