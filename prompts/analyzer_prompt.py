ANALYZER_PROMPT = """
You are an expert document comparison engine.

STRICTLY compare the OLD and NEW documents at the policy level.


IMPORTANT:
You MUST identify ALL changes.

Steps:
1. Extract ALL policy sections from OLD document
2. Extract ALL policy sections from NEW document
3. Compare EACH section


You MUST follow these rules EXACTLY:

1. If the SAME policy exists in both OLD and NEW but wording/value is changed → mark as "MODIFIED"
2. If a policy exists ONLY in NEW document → mark as "ADDED"
3. If a policy exists ONLY in OLD document → mark as "REMOVED"
4. NEVER classify everything as ADDED
5. You MUST detect similar meaning policies even if wording is different

IMPORTANT:
- Compare semantically, not exact text match
- If intent is same but wording changed → MODIFIED
- Only completely new ideas → ADDED

OUTPUT FORMAT:
Return ONLY a valid JSON array.

Each object must contain:
- change_type (ADDED / MODIFIED / REMOVED)
- old_text
- new_text
- summary (short title)

OLD DOCUMENT:
{old_text}

NEW DOCUMENT:
{new_text}
"""