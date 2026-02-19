from pymongo import MongoClient
import glob
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()  # loads .env automatically
MONGO_URL = os.getenv("MONGO_URL")  # make sure your .env has MONGO_URL=your_url
DATA_FOLDER = "data"
LINES_PER_CHUNK = 5

if not MONGO_URL:
    raise ValueError("❌ MONGO_URL not found in .env!")

# ---------------- CONNECT ----------------
client = MongoClient(MONGO_URL)
db = client["rag_db"]
collection = db["documents"]
chat_collection = db["chat_history"]

# ---------------- DROP OLD COLLECTIONS ----------------
collection.drop()
chat_collection.drop()
print("✅ Old collections dropped.")

# ---------------- CHUNK FUNCTION ----------------
def chunk_text(text, lines=LINES_PER_CHUNK):
    parts = text.splitlines()
    for i in range(0, len(parts), lines):
        chunk = "\n".join(parts[i:i+lines]).strip()
        if chunk:
            yield chunk

# ---------------- INGEST FILES ----------------
total_chunks = 0
for file_path in glob.glob(os.path.join(DATA_FOLDER, "*.txt")):
    title = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    chunk_count = 0
    for chunk in chunk_text(content):
        collection.insert_one({
            "title": title,
            "content": chunk
        })
        chunk_count += 1
        total_chunks += 1

    print(f"✅ Ingested {chunk_count} chunks from: {title}")

print(f"🎉 All files ingested successfully! Total chunks: {total_chunks}")
