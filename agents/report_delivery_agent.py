import json
import re
from langchain_core.prompts import ChatPromptTemplate
from models.llm import get_llm
from prompts.report_delivery_prompt import REPORT_DELIVERY_PROMPT
from tools.report_generator import ReportGenerator
from tools.email_sender import EmailSender


class ReportDeliveryAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            REPORT_DELIVERY_PROMPT
        )

    def _safe_parse(self, text):

        if not isinstance(text, str):
            return text if isinstance(text, dict) else {}

        text = text.strip()
        text = text.replace("```json", "").replace("```", "")
        text = re.sub(r"[\x00-\x1F\x7F]", "", text)

        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            text = text[start:end]

        try:
            parsed = json.loads(text)

            if not isinstance(parsed, dict):
                return {}

            return parsed

        except Exception as e:
            print("❌ JSON PARSE FAILED:", e)
            print("RAW OUTPUT:\n", text)
            return {}

    def run(self, doc_result, impact_result, recipient_email):

        chain = self.prompt | self.llm

        response = chain.invoke({
            "doc_analysis": json.dumps(doc_result, indent=2),
            "impact_analysis": json.dumps(impact_result, indent=2)
        })

        print("\n=== RAW REPORT OUTPUT ===\n", response.content)

        report_data = self._safe_parse(response.content)
        print(report_data)

        if not isinstance(report_data, dict) or not report_data:
            return {
                "status": "FAILED",
                "reason": "Invalid JSON from LLM"
            }

        if not report_data.get("send_email", True):
            return {
                "status": "SKIPPED",
                "reason": "No meaningful changes detected"
            }

        # ✅ Generate Word report using actual data
        report_path = ReportGenerator().generate_report(
            doc_result,
            impact_result
        )

        # ✅ Send email
        EmailSender().send_email(
            recipient_email,
            report_data.get("subject", "Document Report"),
            report_data.get("email_body", ""),
            report_path
        )

        return {
            "status": "SENT",
            "subject": report_data.get("subject")
        }