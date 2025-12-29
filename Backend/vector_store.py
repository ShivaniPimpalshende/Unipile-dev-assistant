# vector_store.py
from langchain_community.vectorstores import FAISS
from embeddings import TfidfEmbeddings

FAISS_PATH = "faiss_index"

def load_vector_store():
    embeddings = TfidfEmbeddings()
    return FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

# Load vector store once
vector_store = load_vector_store()

def retrieve_docs(query: str, k: int = 4):
    """
    Return top k similar documents from the FAISS vector store.
    """
    return vector_store.similarity_search(query, k=k)
