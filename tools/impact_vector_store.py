from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

class ImpactVectorStore:
    def __init__(self, path="vectorstore/impact_index"):
        self.path = path
        self.embedder = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = None

    def build(self, impact_texts):
        os.makedirs("vectorstore", exist_ok=True)
        self.db = FAISS.from_texts(impact_texts, self.embedder)
        self.db.save_local(self.path)

    def load(self):
        self.db = FAISS.load_local(self.path, self.embedder)

    def search(self, query, k=3):
        return self.db.similarity_search(query, k=k)
