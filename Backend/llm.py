# llm.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = """
You are Unipile Dev Assistant.
Answer ONLY using the provided documentation.
If the answer is not present, say "Not found in documentation."
"""

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

DOCUMENTATION:
{context}

QUESTION:
{question}
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print("LLM error:", e)
        return "I don't know."
