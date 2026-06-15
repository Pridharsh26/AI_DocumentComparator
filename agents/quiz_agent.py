from models.llm import get_llm
import json
import re

def clean_json(text):
    text = text.replace("```json", "").replace("```", "")
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)
    return text.strip()

class QuizAgent:
    def __init__(self):
        self.llm = get_llm()

    def generate_quiz(self, impact_item, num_questions=5):

        impact_json = json.dumps(impact_item, indent=2)

        prompt = f"""
You are a strict JSON generator.

Generate {num_questions} multiple‑choice quiz questions based ONLY on the following impact analysis:

IMPACT ANALYSIS (JSON):
{impact_json}

STRICT RULES:
- Output ONLY valid JSON
- Output MUST be a JSON array
- NO text before or after the JSON
- NO markdown
- NO numbering (1., 2., etc.)
- NO labels like "Question:" or "Answer:"
- NO explanations outside JSON

JSON FORMAT (DO NOT COPY LITERALLY, JUST FOLLOW STRUCTURE):
[
  {{
    "question": "string",
    "options": ["A", "B", "C", "D"],
    "answer": "A",
    "explanation": "string"
  }}
]
"""

        response = self.llm.invoke(prompt).content
        cleaned = clean_json(response)

        # Try to load JSON
        try:
            parsed = json.loads(cleaned)
            return parsed
        except:
            # Try to auto‑repair common issues
            try:
                fixed = cleaned.strip()
                if fixed.startswith("{"):
                    fixed = "[" + fixed + "]"
                return json.loads(fixed)
            except:
                return {
                    "error": "Invalid JSON returned by LLM",
                    "raw": cleaned
                }
