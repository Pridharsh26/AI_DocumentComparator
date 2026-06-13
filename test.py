from tools.document_loader import load_document
from tools.chunking import create_chunks
from tools.semantic_search import SemanticComparator

from agents.document_analyzer import DocumentAnalyzerAgent
from utils.parser import save_json

import json


def main():

    old_file_path = input("Enter old document path: ").strip()
    new_file_path = input("Enter new document path: ").strip()

    print("\nLoading documents...")

    old_text = load_document(old_file_path)
    new_text = load_document(new_file_path)

    print("Creating chunks...")

    old_chunks = create_chunks(old_text)
    new_chunks = create_chunks(new_text)

    print("Performing semantic comparison...")

    comparator = SemanticComparator()
    changes = comparator.compare(old_chunks, new_chunks)
    print("Semantic changes:")
    print(changes)
    print("Running Analyzer Agent...")

    agent = DocumentAnalyzerAgent()

    result = agent.analyze(changes)

    save_json(result)

    print("\nAnalysis Completed\n")

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()