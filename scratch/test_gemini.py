import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY or GOOGLE_API_KEY is not set in your .env file!")
        return

    print("Checking Gemini API connectivity...")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.2
        )
        response = llm.invoke("Hello, say 'Gemini API is connected successfully!'")
        print("\n[SUCCESS] Response from Gemini:")
        print(response.content.strip())
    except Exception as e:
        print(f"\n[API ERROR] {e}")

if __name__ == "__main__":
    test_gemini()
