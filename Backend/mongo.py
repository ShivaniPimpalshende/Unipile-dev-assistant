from pymongo import MongoClient, ASCENDING
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- MongoDB Connection ----------------
MONGO_URL_ATLAS = os.getenv("MONGO_URL_ATLAS")
DB_NAME = "unipile"

client = MongoClient(MONGO_URL_ATLAS, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

# Existing collections
doc_collection = db["documents"]
chat_collection = db["chat_history"]

# New memory collection
memory_collection = db["chat_memory"]

# ---------------- Indexes ----------------
def ensure_indexes():
    doc_collection.create_index(
        [("title", "text"), ("content", "text")],
        name="doc_text_index"
    )
    chat_collection.create_index(
        [("timestamp", ASCENDING)],
        name="chat_time_index"
    )
    memory_collection.create_index(
        [("user_id", ASCENDING)],
        name="memory_user_index",
        unique=True
    )

# ---------------- Document Functions ----------------
def insert_document(doc: dict):
    doc_collection.insert_one(doc)

def search_documents(question: str, limit: int = 5):
    if not question.strip():
        return []

    results = list(
        doc_collection.find(
            {"$text": {"$search": question}},
            {"score": {"$meta": "textScore"}, "_id": 0}
        )
        .sort([("score", {"$meta": "textScore"})])
        .limit(limit)
    )

    if results:
        return results

    # fallback regex search
    words = question.lower().split()
    regex_query = {"$and": [{"content": {"$regex": w, "$options": "i"}} for w in words]}
    return list(doc_collection.find(regex_query, {"_id": 0}).limit(limit))

# ---------------- Chat History ----------------
def insert_chat(question: str, answer: str):
    chat_collection.insert_one({
        "question": question,
        "answer": answer,
        "timestamp": datetime.datetime.utcnow()
    })

def get_chat_history(limit: int = 20):
    return list(
        chat_collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )

# ---------------- Memory Functions ----------------
def get_user_memory(user_id: str, limit: int = 10):
    """Retrieve last N messages for user conversation context"""
    doc = memory_collection.find_one({"user_id": user_id})
    if not doc:
        return []
    return doc.get("conversation", [])[-limit:]

def save_memory(user_id: str, role: str, message: str):
    """Save user or assistant message to memory"""
    entry = {"role": role, "message": message, "timestamp": datetime.datetime.utcnow()}
    memory_collection.update_one(
        {"user_id": user_id},
        {"$push": {"conversation": entry}, "$set": {"last_updated": datetime.datetime.utcnow()}},
        upsert=True
    )
