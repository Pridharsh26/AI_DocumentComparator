from tools.document_loader import load_document
from tools.chunking import create_chunks
from services.chat_service import ChatService


# Load PDFs
old_text = load_document(open("/workspace/shared/Project/old.pdf", "rb"))
new_text = load_document(open("/workspace/shared/Project/new.pdf", "rb"))

print("Documents loaded")


# Create chunks
old_chunks = create_chunks(old_text)
new_chunks = create_chunks(new_text)

print("Chunks created")
print("Old chunks:", len(old_chunks))
print("New chunks:", len(new_chunks))


# Initialize RAG chatbot
chat = ChatService()


# Store old + new policies into FAISS
chat.load_documents(
    old_chunks,
    new_chunks
)

print("Policy chatbot ready!")
print("Type 'exit' to quit")


# Chat loop
while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break


    answer = chat.ask(question)


    print("\nAssistant:")
    print(answer)