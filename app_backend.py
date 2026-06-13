import json
from tools.document_loader import load_document
from services.comparison_service import ComparisonService
from services.impact_analysis_service import ImpactAnalysisService
from tools.impact_vector_store import ImpactVectorStore   
from services.notification_service import NotificationService

def run_backend_test(old_path, new_path):
    print("\n=== Loading Documents ===")
    old_text = load_document(old_path)
    new_text = load_document(new_path)

    print("\n=== Running Comparison Engine ===")
    comparison_service = ComparisonService()
    comparison_result = comparison_service.compare_documents(old_text, new_text)

    print(json.dumps(comparison_result, indent=2))

    print("\n=== Running Impact Analysis Engine ===")
    impact_service = ImpactAnalysisService()
    impact_result = impact_service.analyze(comparison_result)

    print(json.dumps(impact_result, indent=2))

    # Build Impact Vector Store
    print("\n=== Building Impact Vector Store ===")
    impact_texts = impact_service.to_vector_texts(impact_result)
    store = ImpactVectorStore()
    store.build(impact_texts)

    print("Impact vectors stored successfully.")

    print("\n=== Backend Test Completed ===")

    print("\n=== Running Notification Agent ===")
    notifier = NotificationService()
    notifier.process(impact_result)

if __name__ == "__main__":
    OLD_DOC = "old.pdf"
    NEW_DOC = "new.pdf"

    run_backend_test(OLD_DOC, NEW_DOC)
