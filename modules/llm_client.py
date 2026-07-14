"""Shared LLM client singleton.

All AI modules import `llm` from here to avoid creating multiple
ChatGroq instances at module load time.

Configuration:
    - model:      llama-3.3-70b-versatile (best quality/speed ratio on Groq)
    - temperature: 0.2 (lower → more consistent, structured outputs)
    - max_tokens: 4096 (cap to avoid runaway responses)
    - timeout:    45s  (prevent hanging on slow network)
"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

_api_key = os.getenv("GROQ_API_KEY")
if not _api_key:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. "
        "Add it to your .env file: GROQ_API_KEY=gsk_..."
    )

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=_api_key,
    temperature=0.2,
    max_tokens=4096,
    timeout=45,
)

