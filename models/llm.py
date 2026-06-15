from langchain_openai import ChatOpenAI


def get_llm():
    return ChatOpenAI(
        model="deepseek-7b",
        base_url="http://localhost:8000/v1",
        api_key="abc-123",
        temperature=0
    )