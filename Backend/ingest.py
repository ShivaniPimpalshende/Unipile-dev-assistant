from mongo import insert_document
import glob
import os

DATA_FOLDER = "data"

def chunk_text(text, lines=5):
    parts = text.splitlines()
    for i in range(0, len(parts), lines):
        chunk = "\n".join(parts[i:i+lines]).strip()
        if chunk:
            yield chunk

for file_path in glob.glob(os.path.join(DATA_FOLDER, "*.txt")):
    title = os.path.basename(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    for chunk in chunk_text(content):
        insert_document({
            "title": title,
            "content": chunk
        })

    print(f"✅ Ingested chunks from: {title}")
