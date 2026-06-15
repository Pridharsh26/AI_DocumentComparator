import json
import re

def save_json(result):

    with open(
        "output/comparison_result.json",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(result)

# ==================================================
# SAFE JSON PARSER
# ==================================================
def safe_json_loads(text):
    """
    Safely parse JSON from LLM output.
    Handles markdown, bad characters, and invalid JSON.
    """

    if not isinstance(text, str):
        return text

    text = text.strip()

    # ✅ Remove markdown wrappers
    text = text.replace("```json", "").replace("```", "")

    # ✅ Remove bad control characters
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)

    # ✅ Fix trailing commas (VERY IMPORTANT for LLM output)
    text = re.sub(r",(\s*[}\]])", r"\1", text)

    try:
        return json.loads(text)
    except Exception:
        return text  # fallback


# ==================================================
# QUIZ FALLBACK PARSER (TEXT → JSON)
# ==================================================
def convert_text_quiz_to_json(text):
    """
    Convert LLM text response into structured quiz JSON.
    Supports inline + multiline options.
    """

    questions = []

    # ✅ Split by question numbers
    blocks = re.split(r"\n?\d+\.\s+", text)

    for block in blocks:
        if not block.strip():
            continue

        try:
            # ✅ Extract question
            q_match = re.search(
                r"(?:Question:\s*)?(.*?)(?=\n[A-D]\.|\bA\.)",
                block,
                re.DOTALL
            )
            question = q_match.group(1).strip() if q_match else ""

            # ✅ Extract options (inline + multiline)
            options = re.findall(
                r"([A-D])\.\s*([^A-D]+?)(?=\s*[A-D]\.|$)",
                block
            )

            # ✅ Limit to A–D
            options = options[:4]

            # ✅ Clean options
            options_text = [
    re.sub(r"^[A-D]\.\s*", "", opt[1].strip())
    for opt in options
]

            # ✅ Extract answer letter
            a_match = re.search(r"Answer:\s*([A-D])", block)
            answer_letter = a_match.group(1) if a_match else ""

            # ✅ Extract explanation
            e_match = re.search(r"Explanation:\s*(.*)", block)
            explanation = e_match.group(1).strip() if e_match else ""

            # ✅ Add valid question
            if question and options_text:
                questions.append({
                    "question": question,
                    "options": options_text,
                    "answer": answer_letter,   # ✅ letter-based
                    "explanation": explanation
                })

        except Exception:
            continue

    return questions
