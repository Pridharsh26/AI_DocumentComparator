import json
from models.llm import get_llm
import re

class TrainingAgent:
    def __init__(self):
        self.llm = get_llm()

    def generate_training(self, impact_result):
        """
        Creates a structured training lesson based ONLY on impact analysis.
        """

        prompt = f"""
You are a Training Content Generator.

Your job is to create a clear, simple, structured training lesson
based ONLY on the following impact analysis:

IMPACT ANALYSIS:
{json.dumps(impact_result, indent=2)}

TASK:
Create a training module with the following sections:

1. Overview of What Changed
2. Why This Change Matters
3. Real‑World Examples (2–3)
4. Key Takeaways (bullet points)
5. Mini Summary (short paragraph)

Return ONLY valid JSON with these keys:
- overview
- importance
- examples
- key_takeaways
- summary
"""

        response = self.llm.invoke(prompt).content
        
        cleaned = response.strip()
        
        # ✅ remove markdown
        cleaned = cleaned.replace("```json", "").replace("```", "")
        
        # ✅ ✅ FIX TRAILING COMMAS (MAIN FIX)
        cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
        
        try:
            return json.loads(cleaned)
        
        except Exception as e:
            return {
                "error": "Failed to parse training content",
                "raw": response,
                "cleaned": cleaned,
                "parse_error": str(e)
            }