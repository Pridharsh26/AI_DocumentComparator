import json
from langchain_core.prompts import PromptTemplate
from models.llm import get_llm
from prompts.analyzer_prompt import ANALYZER_PROMPT


class DocumentAnalyzerAgent:

    def __init__(self):
        self.llm = get_llm()

        self.prompt = PromptTemplate(
            template=ANALYZER_PROMPT,
            input_variables=["old_text", "new_text"]
        )

    def analyze(self, changes):
        chain = self.prompt | self.llm

        results = []

        for change in changes:
            response = chain.invoke({
                "old_text": change["old_chunk"],
                "new_text": change["new_chunk"]
            })

            results.append({
                "old_text": change["old_chunk"],
                "new_text": change["new_chunk"],
                "analysis": response.content,
                "similarity": change.get("similarity", None)
            })

        return results