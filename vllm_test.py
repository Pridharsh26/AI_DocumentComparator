from services.vllm_client import VLLMClient


llm = VLLMClient()


answer = llm.generate(
    "What is the leave policy?"
)


print(answer)