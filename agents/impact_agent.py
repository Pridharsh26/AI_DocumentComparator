import json
import re
from langchain_core.prompts import PromptTemplate
from models.llm import get_llm
from prompts.impact_prompt import IMPACT_PROMPT


class ImpactAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = PromptTemplate(
            template=IMPACT_PROMPT,
            input_variables=["change_json"]
        )

    def _safe_parse(self, text):
        if not isinstance(text, str):
            return text

        text = text.strip()
        text = text.replace("```json", "").replace("```", "")
        text = re.sub(r"[\x00-\x1F\x7F]", "", text)

        try:
            return json.loads(text)
        except Exception as e:
            print("IMPACT PARSE ERROR:", e)
            print("RAW OUTPUT:", text)
            return {}

    def analyze(self, change_dict):

        chain = self.prompt | self.llm

        response = chain.invoke({
            "change_json": json.dumps(change_dict, indent=2)
        })

        parsed = self._safe_parse(response.content)

        # ✅ enforce structure (prevents N/A)
        return {
            "what_changed": parsed.get("what_changed"),
            "business_impact": parsed.get("business_impact"),
            "compliance_impact": parsed.get("compliance_impact"),
            "stakeholders_affected": parsed.get("stakeholders_affected"),
            "risk_level": parsed.get("risk_level"),
            "recommended_actions": parsed.get("recommended_actions"),
            "executive_summary": parsed.get("executive_summary"),
        }