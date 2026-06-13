import json
from models.llm import get_llm

class NotificationAgent:
    def __init__(self):
        self.llm = get_llm()

    def decide(self, impact_item):
        prompt = f"""
You are a notification decision agent.

Analyze the following impact item and decide:
- notify: true/false
- stakeholders: list of roles
- urgency: Low/Medium/High/Critical
- message: short alert message
- action: recommended next step

Impact Item:
{impact_item}

Return JSON only.
"""
        return self.llm.invoke(prompt).content
