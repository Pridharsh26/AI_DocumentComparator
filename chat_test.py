from services.chat_service import ChatService


chat = ChatService()


old_chunks = [
    """
    Employees are entitled to 12 annual leave days.
    Employees must work from office 9 AM to 6 PM.
    """
]


new_chunks = [
    """
    Employees are entitled to 20 annual leave days.
    Hybrid work is allowed three days a week.
    """
]


chat.load_documents(
    old_chunks,
    new_chunks
)


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break


    answer = chat.ask(question)


    print("\nAssistant:")
    print(answer)