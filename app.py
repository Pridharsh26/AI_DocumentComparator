# import streamlit as st

# from tools.document_loader import load_document
# from services.comparison_service import ComparisonService
# from services.impact_analysis_service import ImpactAnalysisService


# st.title("AI Intelligent Doc Comparator")

# old_doc = st.file_uploader(
#     "Old Document",
#     type=["pdf", "txt", "docx"]
# )

# new_doc = st.file_uploader(
#     "New Document",
#     type=["pdf", "txt", "docx"]
# )

# if st.button("Analyze"):

#     if old_doc and new_doc:

#         # 1. Load documents
#         old_text = load_document(old_doc)
#         new_text = load_document(new_doc)

#         # 2. Run comparison engine
#         comparison_service = ComparisonService()
#         comparison_result = comparison_service.compare_documents(
#             old_text,
#             new_text
#         )

#         # 3. Run impact analysis engine (NEW)
#         impact_service = ImpactAnalysisService()
#         impact_result = impact_service.analyze(comparison_result)

#         # 4. Combine results
#         final_output = {
#             "comparison": comparison_result,
#             "impact_analysis": impact_result
#         }

#         # 5. Display in Streamlit
#         st.json(final_output)


import streamlit as st

from tools.document_loader import load_document
from tools.chunking import create_chunks
from tools.semantic_search import compare_chunks

from agents.document_analyzer import (
    DocumentAnalyzerAgent
)

from utils.parser import save_json


st.title("Document Comparator")


old_file = st.file_uploader(
    "Upload Old Document",
    type=["pdf", "docx", "txt"]
)

new_file = st.file_uploader(
    "Upload New Document",
    type=["pdf", "docx", "txt"]
)


if st.button("Analyze"):

    if old_file and new_file:

        with st.spinner("Loading documents..."):

            old_text = load_document(old_file)
            new_text = load_document(new_file)

        with st.spinner("Creating chunks..."):

            old_chunks = create_chunks(old_text)
            new_chunks = create_chunks(new_text)

        with st.spinner("Performing semantic comparison..."):

            changes = compare_chunks(
                old_chunks,
                new_chunks
            )

        with st.spinner("Running Analyzer Agent..."):

            agent = DocumentAnalyzerAgent()

            result = agent.analyze(changes)

        save_json(result)

        st.success("Analysis Completed")

        st.json(result)
