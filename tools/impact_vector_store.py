from fastembed import TextEmbedding
from langchain_community.vectorstores import FAISS
import os


class ImpactVectorStore:

    def __init__(self, path="vectorstore/impact_index"):
        self.path = path
        self.embedder = TextEmbedding("BAAI/bge-small-en-v1.5")
        self.db = None

    def embed(self, texts):
        return list(self.embedder.embed(texts))

    def build(self, impact_texts):
        os.makedirs("vectorstore", exist_ok=True)

        embeddings = self.embed(impact_texts)

        self.db = FAISS.from_embeddings(
            text_embeddings=list(zip(impact_texts, embeddings)),
            embedding=self.embedder.embed
        )

        self.db.save_local(self.path)

    def load(self):
        self.db = FAISS.load_local(self.path, self.embedder.embed)

    def search(self, query, k=3):
        return self.db.similarity_search(query, k=k)