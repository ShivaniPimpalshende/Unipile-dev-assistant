# llm.py
# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# MODEL_NAME = "models/gemini-flash-latest"

# SYSTEM_PROMPT = """
# You are Unipile Dev Assistant.

# LANGUAGE RULES (STRICT):
# - If the user does NOT specify a programming language, respond using Node.js.
# - If the user specifies a language, respond using ONLY that language.
# - Never show code in multiple languages.

# RESPONSE FORMAT (MANDATORY):
# 1. Give a SHORT explanation (2–4 lines max).
# 2. Then provide a COMPLETE code example.
# 3. Use ONE code block only.

# CODE RULES:
# - Code must be complete and runnable.
# - For Node.js, use fetch or axios.
# - Include URL, method, headers, and body when required.
# - Do not include unrelated boilerplate.

# DOCUMENTATION RULES:
# - Answer ONLY using the provided documentation.
# - If documentation is insufficient, reply EXACTLY:
#   "Not found in documentation."

# Do not include extra commentary after the code block.
# """




# def generate_answer(context: str, question: str, ) -> str:
#     print("🤖 Gemini LLM CALLED")   # 🔥 PROOF LINE

#     prompt = f"""
# {SYSTEM_PROMPT}

# DOCUMENTATION:
# {context}

# QUESTION:
# {question}
# """
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt
#     )
#     return response.text.strip()



import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = """
You are Unipile Dev Assistant.

LANGUAGE RULES:
- Default: Node.js
- If user specifies language, respond ONLY in that language.

RESPONSE FORMAT:
1. Short explanation (2–4 lines)
2. Complete, runnable code block
"""

def generate_answer(context: str, question: str) -> str:
    print("🤖 Gemini LLM CALLED")  # proof
    prompt = f"""
{SYSTEM_PROMPT}

DOCUMENTATION & MEMORY:
{context}

QUESTION:
{question}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()
