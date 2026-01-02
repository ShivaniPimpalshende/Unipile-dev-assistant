# llm.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = """
You are Unipile Dev Assistant.

You may respond to greetings briefly.

For all technical questions:
- Answer ONLY using the provided documentation.
- If the documentation is insufficient or empty, reply exactly:
  "Not found in documentation."

Do not provide generic introductions when documentation is missing.
"""



def generate_answer(context: str, question: str) -> str:
    print("🤖 Gemini LLM CALLED")   # 🔥 PROOF LINE

    prompt = f"""
{SYSTEM_PROMPT}

DOCUMENTATION:
{context}

QUESTION:
{question}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()
