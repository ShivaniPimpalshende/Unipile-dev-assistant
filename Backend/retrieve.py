from vector_store import load_vector_store

# Load FAISS index once
vector_store = load_vector_store()

def retrieve_docs(query: str, k: int = 4):
    return vector_store.similarity_search(query, k=k)


