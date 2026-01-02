# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from mongo import ensure_indexes, insert_document, search_documents
# from llm import generate_answer

# app = FastAPI(title="Unipile Dev Assistant API", version="1.0.0")

# # CORS for frontend
# origins = ["http://localhost:3000"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.on_event("startup")
# def startup_event():
#     ensure_indexes()

# # Chat request model
# class ChatRequest(BaseModel):
#     query: str

# @app.get("/")
# def health_check():
#     return {"status": "ok"}

# @app.post("/insert")
# def insert(doc: dict):
#     try:
#         insert_document(doc)
#         return {"message": "Document inserted"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.get("/search")
# def search(q: str):
#     results = search_documents({"title": {"$regex": q, "$options": "i"}})
#     return {"results": results}

# # @app.post("/chat")
# # def chat_endpoint(request: ChatRequest):
# #     try:
# #         docs = search_documents({})
# #         context = "\n\n".join([f"{d['title']}: {d.get('content','')}" for d in docs])
# #         answer = generate_answer(context, request.query)
# #         return {"answer": answer}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")
# @app.post("/chat")
# def chat_endpoint(request: ChatRequest):
#     try:
#         # Find docs that match keywords in the question
#         keyword = request.query
#         docs = search_documents({"content": {"$regex": keyword, "$options": "i"}})

#         if not docs:
#             return {"answer": "Not found in documentation."}

#         context = "\n\n".join([f"{d['title']}: {d.get('content','')}" for d in docs])
#         answer = generate_answer(context, request.query)
#         return {"answer": answer}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mongo import ensure_indexes, search_documents, insert_chat, get_chat_history
from llm import generate_answer

app = FastAPI(title="Unipile Dev Assistant API")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Startup ----------------
@app.on_event("startup")
def startup_event():
    ensure_indexes()

# ---------------- Models ----------------
class ChatRequest(BaseModel):
    message: str

# ---------------- FAQ for common questions ----------------
FAQ = {
    "what is unipile": "Unipile is a unified platform to manage emails, calendars, and messaging apps. It integrates multiple communication services into one interface.",
    "webhooks": "Webhooks in Unipile are HTTP callbacks that allow external apps to receive real-time notifications of events such as new emails, calendar updates, or messages."
}

# ---------------- Health Check ----------------
@app.get("/")
def root():
    return {"status": "Backend is running"}

# ---------------- Chat API ----------------
@app.post("/chat")
def chat(req: ChatRequest):
    question = req.message.strip()
    if not question:
        return {"answer": "Message cannot be empty."}

    # 1️⃣ Greetings
    greetings = {"hi", "hello", "hey", "hellow", "hii", "good morning"}
    if question.lower() in greetings:
        answer = "Hello! I’m the Unipile Dev Assistant. How can I help you?"
        insert_chat(question, answer)
        return {"question": question, "answer": answer}

    # 2️⃣ FAQ check
    for key, ans in FAQ.items():
        if key in question.lower():
            insert_chat(question, ans)
            return {"question": question, "answer": ans}

    # 3️⃣ Search MongoDB
    results = search_documents(question)
    if not results:
        answer = "Not found in documentation."
        insert_chat(question, answer)
        return {"question": question, "answer": answer}

    # 4️⃣ Combine content for LLM
    context = "\n".join(r["content"].strip() for r in results if r.get("content"))

    # 5️⃣ Call LLM
    final_answer = generate_answer(context, question)

    # 6️⃣ Save to chat history
    insert_chat(question, final_answer)

    return {"question": question, "answer": final_answer}

# ---------------- Chat History API ----------------
@app.get("/history")
def history(limit: int = 20):
    return {"history": get_chat_history(limit)}
