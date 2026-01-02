# from pymongo import MongoClient, ASCENDING
# import datetime

# # ---------------- MongoDB Connection ----------------
# MONGO_URL = "mongodb://127.0.0.1:27017"  # Replace with your Atlas URI if needed
# DB_NAME = "unipile"
# DOC_COLLECTION_NAME = "documents"
# CHAT_COLLECTION_NAME = "chat_history"

# client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
# db = client[DB_NAME]

# collection = db[DOC_COLLECTION_NAME]
# chat_collection = db[CHAT_COLLECTION_NAME]

# # ---------------- Indexes ----------------
# def ensure_indexes():
#     # Text index for relevance-ranked search
#     collection.create_index([("title", "text"), ("content", "text")])

# # ---------------- Document Functions ----------------
# def insert_document(doc: dict):
#     collection.insert_one(doc)

# def search_documents(question: str, limit: int = 5):
#     if not question.strip():
#         return []
#     return list(
#         collection.find(
#             {"$text": {"$search": question}},
#             {"score": {"$meta": "textScore"}, "_id": 0}
#         ).sort([("score", {"$meta": "textScore"})]).limit(limit)
#     )

# # ---------------- Chat History ----------------
# def insert_chat(question: str, answer: str):
#     chat_collection.insert_one({
#         "question": question,
#         "answer": answer,
#         "timestamp": datetime.datetime.utcnow()
#     })

# def get_chat_history(limit: int = 20):
#     return list(
#         chat_collection.find({}, {"_id": 0})
#         .sort("timestamp", -1)
#         .limit(limit)
#     )
from pymongo import MongoClient, ASCENDING
import datetime

# ---------------- MongoDB Connection ----------------
MONGO_URL = "mongodb://127.0.0.1:27017"  # Replace with Atlas URI if needed
DB_NAME = "unipile"
DOC_COLLECTION_NAME = "documents"
CHAT_COLLECTION_NAME = "chat_history"

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
db = client[DB_NAME]

collection = db[DOC_COLLECTION_NAME]
chat_collection = db[CHAT_COLLECTION_NAME]

# ---------------- Indexes ----------------
def ensure_indexes():
    # Text index for ranked search
    collection.create_index(
        [("title", "text"), ("content", "text")],
        name="doc_text_index"
    )

    # Chat history index
    chat_collection.create_index(
        [("timestamp", ASCENDING)],
        name="chat_time_index"
    )

# ---------------- Document Insert ----------------
def insert_document(doc: dict):
    collection.insert_one(doc)

# ---------------- Document Search (SMART) ----------------
def search_documents(question: str, limit: int = 5):
    if not question.strip():
        return []

    # 1️⃣ Try MongoDB text search (BEST)
    results = list(
        collection.find(
            {"$text": {"$search": question}},
            {"score": {"$meta": "textScore"}, "_id": 0}
        )
        .sort([("score", {"$meta": "textScore"})])
        .limit(limit)
    )

    # 2️⃣ Fallback to regex if text search finds nothing
    if results:
        return results

    words = question.lower().split()
    regex_query = {
        "$and": [
            {"content": {"$regex": w, "$options": "i"}}
            for w in words
        ]
    }

    return list(
        collection.find(regex_query, {"_id": 0}).limit(limit)
    )

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
