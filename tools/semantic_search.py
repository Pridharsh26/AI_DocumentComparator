from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SemanticComparator:

    def __init__(self):
        # Lightweight open-source embedding model (NO torch, NO transformers)
        self.embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")

    def embed(self, texts):
        """
        Convert texts to embeddings
        fastembed returns generator → convert to list
        """
        return list(self.embedding_model.embed(texts))

    def compare(self, old_chunks, new_chunks):

        # Generate embeddings
        old_embeddings = self.embed(old_chunks)
        new_embeddings = self.embed(new_chunks)

        results = []

        for idx, new_chunk in enumerate(new_chunks):

            scores = cosine_similarity(
                [new_embeddings[idx]],
                old_embeddings
            )[0]

            best_index = np.argmax(scores)

            results.append({
                "new_chunk": new_chunk,
                "old_chunk": old_chunks[best_index],
                "similarity": float(scores[best_index])
            })
            print(results)

        return results


# wrapper function (same style as your original code)
def compare_chunks(old_chunks, new_chunks):
    comparator = SemanticComparator()
    return comparator.compare(old_chunks, new_chunks)