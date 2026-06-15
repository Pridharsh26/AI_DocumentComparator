# services/training_service.py
from agents.training_agent import TrainingAgent

class TrainingService:
    def __init__(self):
        self.agent = TrainingAgent()

    def create_training(self, impact_result):
        modules = []
        for item in impact_result["impact_analysis"]:
            modules.append(self.agent.generate_training(item))
        return modules
