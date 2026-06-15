# from tools.policy_vector_store import (
#     PolicyVectorStore
# )

# from services.vllm_client import (
#     VLLMClient
# )


# class ChatService:


#     def __init__(self):

#         self.vector_store = PolicyVectorStore()

#         self.llm = VLLMClient()


#     def load_documents(
#         self,
#         old_chunks,
#         new_chunks
#     ):

#         all_chunks = []

#         for chunk in old_chunks:
#             all_chunks.append(
#                 "OLD POLICY:\n" + chunk
#             )


#         for chunk in new_chunks:
#             all_chunks.append(
#                 "NEW POLICY:\n" + chunk
#             )


#         self.vector_store.build(
#             all_chunks
#         )


#     def ask(self, question):

#         context = self.vector_store.search(
#             question,
#             k=5
#         )


#         prompt = f"""
# You are comparing old and new company policies.

# Context:
# {chr(10).join(context)}

# Question:
# {question}

# Rules:
# - Mention whether information came from old or new policy.
# - If the answer does not exist in the documents,
# say you don't know.
# - Explain changes clearly.
# """


#         return self.llm.generate(
#             prompt
#         )

from tools.policy_vector_store import PolicyVectorStore
from services.vllm_client import VLLMClient


class ChatService:

    def __init__(self):

        self.vector_store = PolicyVectorStore()
        self.llm = VLLMClient()

    def load_documents(self, old_chunks, new_chunks):

        print("🔵 LOADING DOCUMENTS...")

        all_chunks = []

        for chunk in old_chunks:
            all_chunks.append("OLD POLICY:\n" + chunk)

        for chunk in new_chunks:
            all_chunks.append("NEW POLICY:\n" + chunk)

        self.vector_store.build(all_chunks)

        print("🟢 VECTOR STORE READY")

    def ask(self, question):

        print("\n==============================")
        print("🔵 STEP 1: ENTERED ASK()")
        print("QUESTION:", question)

        # -------------------------
        # STEP 2: FAISS SEARCH
        # -------------------------
        try:
            context = self.vector_store.search(question, k=5)
            print("🟢 STEP 2: SEARCH DONE")
            print("CONTEXT SIZE:", len(context))
        except Exception as e:
            print("❌ STEP 2 FAILED (FAISS ERROR):", e)
            return f"FAISS ERROR: {str(e)}"

        # -------------------------
        # STEP 3: PROMPT BUILD
        # -------------------------
        try:
            prompt = f"""
You are comparing old and new company policies.

Context:
{chr(10).join(context)}

Question:
{question}

Rules:
- Mention OLD vs NEW clearly
- If not found, say you don't know
"""
            print("🟢 STEP 3: PROMPT READY")
        except Exception as e:
            print("❌ STEP 3 FAILED (PROMPT ERROR):", e)
            return f"PROMPT ERROR: {str(e)}"

        # -------------------------
        # STEP 4: LLM CALL
        # -------------------------
        try:
            print("🔵 STEP 4: CALLING LLM...")
            response = self.llm.generate(prompt)
            print("🟢 STEP 4: LLM RESPONSE RECEIVED")
        except Exception as e:
            print("❌ STEP 4 FAILED (LLM ERROR):", e)
            return f"LLM ERROR: {str(e)}"

        print("==============================\n")

        return response