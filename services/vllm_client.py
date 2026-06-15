from openai import OpenAI


class VLLMClient:

    def __init__(self):

        self.client = OpenAI(
            api_key="abc-123",
            base_url="http://localhost:8000/v1"
        )

        self.model = "deepseek-7b"

    def generate(self, prompt):

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a policy assistant. "
                            "Answer only using the given policy documents."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=512
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"LLM ERROR: {str(e)}"