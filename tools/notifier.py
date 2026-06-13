import json

class Notifier:
    def send(self, decision_json):
        data = json.loads(decision_json)

        if not data["notify"]:
            return "No notification needed."

        print("\n=== Sending Notification ===")
        print("To:", ", ".join(data["stakeholders"]))
        print("Urgency:", data["urgency"])
        print("Message:", data["message"])
        print("Action:", data["action"])
        print("============================\n")

        return "Notification sent."
