# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# from mongo import ensure_indexes, search_documents, insert_chat, get_chat_history
# from llm import generate_answer

# app = FastAPI(title="Unipile Dev Assistant API")

# # ---------------- CORS ----------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------- Startup ----------------
# @app.on_event("startup")
# def startup_event():
#     ensure_indexes()

# # ---------------- Models ----------------
# class ChatRequest(BaseModel):
#     message: str

# # ---------------- FAQ for common questions ----------------
# FAQ = {
#     "what is unipile": "Unipile is a unified platform to manage emails, calendars, and messaging apps. It integrates multiple communication services into one interface.",
#     "webhooks": "Webhooks in Unipile are HTTP callbacks that allow external apps to receive real-time notifications of events such as new emails, calendar updates, or messages."
# }

# # ---------------- Health Check ----------------
# @app.get("/")
# def root():
#     return {"status": "Backend is running"}

# # ---------------- Chat API ----------------
# @app.post("/chat")
# def chat(req: ChatRequest):
#     question = req.message.strip()
#     if not question:
#         return {"answer": "Message cannot be empty."}

#     # 1️⃣ Greetings
#     greetings = {"hi", "hello", "hey", "hellow", "hii", "good morning"}
#     if question.lower() in greetings:
#         answer = "Hello! I’m the Unipile Dev Assistant. How can I help you?"
#         insert_chat(question, answer)
#         return {"question": question, "answer": answer}

#     # 2️⃣ FAQ check
#     for key, ans in FAQ.items():
#         if key in question.lower():
#             insert_chat(question, ans)
#             return {"question": question, "answer": ans}

#     # 3️⃣ Search MongoDB
#     results = search_documents(question)
#     if not results:
#         answer = "Not found in documentation."
#         insert_chat(question, answer)
#         return {"question": question, "answer": answer}

#     # 4️⃣ Combine content for LLM
#     context = "\n".join(r["content"].strip() for r in results if r.get("content"))

#     # 5️⃣ Call LLM
#     final_answer = generate_answer(context, question)

#     # 6️⃣ Save to chat history
#     insert_chat(question, final_answer)

#     return {"question": question, "answer": final_answer}

# # ---------------- Chat History API ----------------
# @app.get("/history")
# def history(limit: int = 20):
#     return {"history": get_chat_history(limit)}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mongo import ensure_indexes, search_documents, insert_chat, get_chat_history, get_user_memory, save_memory
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
    user_id: str = "anonymous"

# ---------------- FAQ ----------------
FAQ = {
    "what is unipile": "Unipile is a unified platform to manage emails, calendars, and messaging apps.",
    "webhooks": "Webhooks in Unipile allow external apps to receive real-time notifications."
}

# ---------------- Health Check ----------------
@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.get("/user_history/{user_id}")
def user_history(user_id: str, limit: int = 20):
    """
    Fetch last `limit` messages for a given user from chat_memory
    to render in sidebar.
    """
    from mongo import get_user_memory

    memory = get_user_memory(user_id, limit)
    # Convert to frontend-friendly format
    chats = [{
        "id": 1,  # single chat for simplicity
        "title": "Previous Chat",
        "messages": [
            {"text": m["message"], "sender": m["role"], "timestamp": m["timestamp"].isoformat()}
            for m in memory
        ]
    }]
    return {"chats": chats}

# ---------------- Chat API ----------------
@app.post("/chat")
def chat(req: ChatRequest):
    user_id = req.user_id.strip() or "anonymous"
    question = req.message.strip()
    if not question:
        return {"answer": "Message cannot be empty."}

    # 1️⃣ Greetings
    greetings = {"hi", "hello", "hey", "hii", "good morning"}
    if question.lower() in greetings:
        answer = "Hello! I’m the Unipile Dev Assistant. How can I help you?"
        insert_chat(question, answer)
        save_memory(user_id, "user", question)
        save_memory(user_id, "assistant", answer)
        return {"question": question, "answer": answer}

    # 2️⃣ FAQ
    for key, ans in FAQ.items():
        if key in question.lower():
            insert_chat(question, ans)
            save_memory(user_id, "user", question)
            save_memory(user_id, "assistant", ans)
            return {"question": question, "answer": ans}

    # 3️⃣ Search MongoDB
    results = search_documents(question)
    if not results:
        answer = "Not found in documentation."
        insert_chat(question, answer)
        save_memory(user_id, "user", question)
        save_memory(user_id, "assistant", answer)
        return {"question": question, "answer": answer}

    # 4️⃣ Combine context with memory
    context_docs = "\n".join(r["content"].strip() for r in results if r.get("content"))
    memory_messages = get_user_memory(user_id)
    memory_text = "\n".join(f"{m['role']}: {m['message']}" for m in memory_messages)
    combined_context = f"{memory_text}\n{context_docs}".strip()

    # 5️⃣ Call LLM
    final_answer = generate_answer(combined_context, question)

    # 6️⃣ Save history and memory
    insert_chat(question, final_answer)
    save_memory(user_id, "user", question)
    save_memory(user_id, "assistant", final_answer)

    return {"question": question, "answer": final_answer}

# ---------------- Chat History ----------------
@app.get("/history")
def history(limit: int = 20):
    return {"history": get_chat_history(limit)}
