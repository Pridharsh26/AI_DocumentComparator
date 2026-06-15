# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings


# class PolicyVectorStore:

#     def __init__(self):
#         self.embedder = HuggingFaceEmbeddings(
#             model_name="sentence-transformers/all-MiniLM-L6-v2"
#         )
#         self.db = None


#     def build(self, texts):
#         if not texts:
#             raise ValueError("No policy texts provided")

#         self.db = FAISS.from_texts(
#             texts,
#             self.embedder
#         )


#     def search(self, query, k=5):
#         if self.db is None:
#             return []

#         docs = self.db.similarity_search(
#             query,
#             k=k
#         )

#         return [
#             doc.page_content
#             for doc in docs
#         ]

import faiss
import numpy as np

from tools.embedding_model import EmbeddingModel


class PolicyVectorStore:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.index = None

        self.documents = []


    def build(self, chunks):

        self.documents = chunks


        vectors = self.embedder.encode(
            chunks
        )


        dimension = vectors.shape[1]


        self.index = faiss.IndexFlatIP(
            dimension
        )


        self.index.add(
            np.array(vectors).astype(
                "float32"
            )
        )


    def search(
        self,
        question,
        k=5
    ):

        query_vector = self.embedder.encode(
            question
        )


        scores, indexes = self.index.search(
            query_vector.astype("float32"),
            k
        )


        results = []


        for i in indexes[0]:

            if i < len(self.documents):

                results.append(
                    self.documents[i]
                )


        return results