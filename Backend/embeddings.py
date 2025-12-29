# embeddings.py
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TfidfEmbeddings:
    """
    Simple TF-IDF based embeddings class compatible with FAISS.
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        """
        Generate embeddings for a list of documents.
        """
        return self.vectorizer.fit_transform(texts).toarray()

    def embed_query(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single query string.
        """
        return self.vectorizer.transform([text]).toarray()[0]
