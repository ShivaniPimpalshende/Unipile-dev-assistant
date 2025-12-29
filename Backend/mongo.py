from pymongo import MongoClient, ASCENDING

MONGO_URL = "mongodb://127.0.0.1:27017"
DB_NAME = "unipile"
COLLECTION_NAME = "documents"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def ensure_indexes():
    collection.create_index([("title", ASCENDING)])

def insert_document(doc: dict):
    collection.insert_one(doc)

def clean_query(text: str):
    stop_words = {
        "what", "is", "the", "a", "an", "of", "to", "in",
        "about", "tell", "me", "please"
    }
    return [w for w in text.lower().split() if w not in stop_words]

def search_documents(question: str, limit: int = 3):
    keywords = clean_query(question)

    # 🔴 SAFETY: if no keywords, return empty
    if not keywords:
        return []

    query = {
        "$or": [
            {"content": {"$regex": kw, "$options": "i"}}
            for kw in keywords
        ]
    }

    return list(
        collection.find(query, {"_id": 0})
        .limit(limit)
    )
