# services/quiz_service.py
from agents.quiz_agent import QuizAgent

class QuizService:
    def __init__(self):
        self.agent = QuizAgent()

    def create_quiz(self, impact_result):
        quizzes = []
        for item in impact_result["impact_analysis"]:
            quizzes.append(self.agent.generate_quiz(item))
        return quizzes
