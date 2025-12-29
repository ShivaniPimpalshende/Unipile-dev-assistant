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
from mongo import ensure_indexes, search_documents

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

# ---------------- Health Check ----------------
@app.get("/")
def root():
    return {"status": "Backend is running"}

# ---------------- Request Model ----------------
class ChatRequest(BaseModel):
    message: str

# ---------------- Chat API ----------------
@app.post("/chat")
def chat(req: ChatRequest):
    question = req.message.strip()
    
    if not question:
        return {"error": "Message cannot be empty"}

    # Search MongoDB (returns 2–3 line chunks)
    results = search_documents(question)

    if not results:
        return {
            "question": question,
            "answer": "Sorry, I could not find any information on that."
        }

    # Combine and clean chunks
    combined_text = "\n".join([r["content"].strip() for r in results])
    combined_text = combined_text.replace("\n\n", "\n")  # remove extra blank lines

    # Optional: simple bullet formatting for readability
    bullets = []
    for line in combined_text.split("\n"):
        stripped = line.strip()
        if stripped:
            bullets.append(f"- {stripped}")
    clean_answer = "\n".join(bullets)

    return {
        "question": question,
        "answer": clean_answer
    }
