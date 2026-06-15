import streamlit as st
import json
import re

from tools.document_loader import load_document
from tools.chunking import create_chunks  

from agents.document_analyzer import DocumentAnalyzerAgent
from agents.impact_agent import ImpactAgent
from agents.report_delivery_agent import ReportDeliveryAgent
from agents.training_agent import TrainingAgent
from agents.quiz_agent import QuizAgent
from utils.parser import safe_json_loads, convert_text_quiz_to_json

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Document Comparator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PROFESSIONAL UI STYLING
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.header-title {
    font-size: 32px;
    font-weight: 700;
}
.badge {
    background: #eef2ff;
    color: #4338ca;
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: 600;
}

/* Cards */
.card {
    padding: 22px;
    border-radius: 14px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.7em 1.5em;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #1d4ed8, #4338ca);
}

/* Section title */
.section {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("### Workflow")
    st.write("1. Upload Documents")
    st.write("2. Analyze")
    st.write("3. Review Results")
    st.write("4. Training")
    st.write("5. Quiz")
    st.write("6. Deliver Report")

    
    if st.button("🤖 Open Chatbot"):
            st.switch_page("pages/Chatbot.py")


    st.markdown("---")
    st.info("Supported: PDF, DOCX, TXT")

# ==================================================
# HEADER
# ==================================================
col1, col2 = st.columns([8, 2])

with col1:
    st.markdown('<div class="header-title">📄 AI Document Comparator</div>', unsafe_allow_html=True)
    st.caption("AI-powered document intelligence platform")



# ==================================================
# SESSION STATE
# ==================================================
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "doc_result" not in st.session_state:
    st.session_state.doc_result = None

if "impact_result" not in st.session_state:
    st.session_state.impact_result = None

if "show_email_popup" not in st.session_state:
    st.session_state.show_email_popup = False

# ==================================================
# UPLOAD SECTION
# ==================================================
st.markdown("## 📤 Upload Documents")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section">Old Document</div>', unsafe_allow_html=True)

    old_file = st.file_uploader(
        "Upload old document",
        type=["pdf", "docx", "txt"],
        key="old",
        label_visibility="collapsed"
    )

    if old_file:
        st.success(f"✅ {old_file.name}")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section">New Document</div>', unsafe_allow_html=True)

    new_file = st.file_uploader(
        "Upload new document",
        type=["pdf", "docx", "txt"],
        key="new",
        label_visibility="collapsed"
    )

    if new_file:
        st.success(f"✅ {new_file.name}")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# ANALYZE BUTTON
# ==================================================


center_col = st.columns([2, 3, 2])[1]

with center_col:
    analyze_clicked = st.button("🔍 Analyze Documents", use_container_width=True)

# ==================================================
# ANALYSIS LOGIC (KEEP YOUR AGENTS LOGIC)
# ==================================================


if analyze_clicked:
    if not old_file or not new_file:
        st.warning("⚠️ Please upload both documents")
    else:
        with st.spinner("Running AI analysis pipeline..."):

            # Load
            old_text = load_document(old_file)
            new_text = load_document(new_file)

            # Chunk
            old_chunks = create_chunks(old_text)
            new_chunks = create_chunks(new_text)

            # Analyze
            analyzer = DocumentAnalyzerAgent()
            doc_result = analyzer.analyze(old_chunks, new_chunks)

            # Impact
            impact_agent = ImpactAgent()
            impact_result = impact_agent.analyze(doc_result)

            # Store
            st.session_state.doc_result = doc_result
            st.session_state.impact_result = impact_result
            st.session_state.analysis_done = True

# ==================================================
# RESULTS UI (PROFESSIONAL DASHBOARD)
# ==================================================
if st.session_state.analysis_done:

    st.markdown("---")
    st.success("✅ Analysis Completed")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Changes",
        "⚡ Impact",
        "🎓 Training",
        "📝 Quiz",
        "📬 Send Report"
    ])

    # ===============================
    # CHANGES TAB
    # ===============================

    with tab1:
        st.subheader("Document Differences")
    
        doc_result = st.session_state.doc_result
        print(doc_result)
        
        if isinstance(doc_result, str):
                try:
                    doc_result = json.loads(doc_result)
                except:
                    doc_result = []

    
        if isinstance(doc_result, list) and len(doc_result) > 0:
    
            for i, item in enumerate(doc_result):
    
                change_type = item.get("change_type")
                summary = item.get("summary", "")
                old_text = item.get("old_text", "")
                new_text = item.get("new_text", "")
    
                st.write(f"Change {i+1}")
    
    
                if change_type == "ADDED":
                    st.success(f"**New Update – {summary}**")
                    st.write(f"**New Rule – {new_text}**")
                
    
                elif change_type == "REMOVED":
                    st.error(f"**Removed – {summary}**")
                    st.write(f"**Previous Rule – {old_text}**")
    
                else:
                    st.warning(f"**Updated – {summary}**")
                    st.write(f"**Previous:** {old_text}")
                    st.write(f"**Updated:** {new_text}")
    
                st.markdown("---")
    
        else:
            st.info("No changes detected")
     
        st.markdown('</div>', unsafe_allow_html=True)


    with tab2:
        st.subheader("Impact Analysis")
    
        impact = st.session_state.impact_result
    
        # ✅ Handle string JSON
        if isinstance(impact, str):
            try:
                impact = json.loads(impact)
            except:
                impact = {}
    
        if isinstance(impact, dict):
    
            st.markdown("### 🧾 Executive Summary")
            st.info(impact.get("executive_summary", "Not available"))
    
            st.markdown("### 🔍 Key Insights")
    
            st.markdown(f"""
            • **What Changed:**  
            {impact.get("what_changed", "")}
            """)
    
            st.markdown(f"""
            • **Business Impact:**  
            {impact.get("business_impact", "")}
            """)
    
            st.markdown(f"""
            • **Compliance Impact:**  
            {impact.get("compliance_impact", "")}
            """)
    
            st.markdown(f"""
            • **Stakeholders Affected:**  
            {impact.get("stakeholders_affected", "")}
            """)
    
            # ✅ Risk Highlight
            risk = impact.get("risk_level", "UNKNOWN")
    
            if risk.upper() == "LOW":
                st.success(f"✅ Risk Level: {risk}")
            elif risk.upper() == "MEDIUM":
                st.warning(f"⚠️ Risk Level: {risk}")
            else:
                st.error(f"❌ Risk Level: {risk}")
    
            st.markdown("### ✅ Recommended Actions")
            st.write(impact.get("recommended_actions", ""))
    
        else:
            st.warning("No impact data available")
    
        st.markdown('</div>', unsafe_allow_html=True)

    # ===============================
    # TRAINING TAB
    # ===============================
    with tab3:
    
        st.subheader("Training Insights")
    
        training_agent = TrainingAgent()
    
        # ✅ Show button ONLY if training not generated
        if "training_data" not in st.session_state:
    
            if st.button("Generate Training"):
    
                with st.spinner("📘 Generating training module..."):
                    training_output = training_agent.generate_training(
                        st.session_state.impact_result
                    )
    
                st.session_state.training_data = training_output
                st.rerun()
    
        # ✅ SHOW TRAINING IF AVAILABLE
        training_data = st.session_state.get("training_data")
    
        if training_data:
    
            st.markdown("## 🎓 Training Module")
    
            if isinstance(training_data, dict):
    
                overview = training_data.get("overview") or "⚠️ No overview generated"
                importance = training_data.get("importance") or "⚠️ No importance provided"
                examples = training_data.get("examples") or []
                takeaways = training_data.get("key_takeaways") or []
                summary = training_data.get("summary") or "⚠️ No summary available"
    
                st.markdown("### 🎯 Overview")
                st.info(overview)
    
                st.markdown("### ❗ Why This Matters")
                st.write(importance)
    
                st.markdown("### 📌 Real‑World Examples")
                if examples:
                    for ex in examples:
                        st.write(f"- {ex}")
                else:
                    st.write("⚠️ No examples generated")
    
                st.markdown("### 🧠 Key Takeaways")
                if takeaways:
                    for t in takeaways:
                        st.write(f"- {t}")
                else:
                    st.write("⚠️ No takeaways generated")
    
                st.markdown("### ✅ Summary")
                st.success(summary)
    
            else:
                st.write(training_data)

    # ===============================
    # QUIZ TAB
    # ===============================
    with tab4:
    
        st.subheader("Quiz")
    
        quiz_agent = QuizAgent()
    
        if "quiz" not in st.session_state:
    
            if st.button("Generate Quiz"):
    
                with st.spinner("📝 Generating quiz..."):
    
                    out = quiz_agent.generate_quiz(st.session_state.impact_result)
    
                quiz = safe_json_loads(out)
    
                if not isinstance(quiz, list):
                    quiz = convert_text_quiz_to_json(out)
    
                if not quiz:
                    st.error("❌ Quiz generation failed")
                    st.stop()
    
                st.session_state.quiz = quiz
                st.session_state.quiz_index = 0
                st.session_state.score = 0
                st.session_state.show_feedback = False

                st.rerun()
    
        quiz = st.session_state.get("quiz")
    
        if quiz:
    
            idx = st.session_state.quiz_index
            total = len(quiz)
    
            st.progress(idx / total)
    
            if idx < total:
    
                st.write(f"Question {idx+1} of {total}")
    
                q = quiz[idx]

                st.markdown(f"### ❓ {q['question']}")

                clean_options = [
                    re.sub(r"^[A-D]\.\s*", "", opt)  # remove existing label
                    for opt in q["options"][:4]
                ]
                
                options = [
                    f"{chr(65+i)}. {opt}"
                    for i, opt in enumerate(clean_options)
                ]
    
                ans = st.radio(
                    "Choose",
                    options,
                    index=None,
                    key=f"q_{idx}",
                    disabled=st.session_state.get("show_feedback", False)
                )
    
                if not st.session_state.get("show_feedback"):
    
                    if st.button("Submit", key=f"s_{idx}"):
    
                        if not ans:
                            st.warning("Select answer")
                            st.stop()
    
                        st.session_state.last_answer = ans
                        st.session_state.show_feedback = True
                        st.rerun()
    
                if st.session_state.get("show_feedback"):
    
                    match = re.match(r"([A-D])", st.session_state.get("last_answer",""))
                    user_letter = match.group(1) if match else ""
    
                    correct_letter = q["answer"]
    
                    if user_letter == correct_letter:
                        st.success("✅ Correct")
                        if not q.get("_scored"):
                            st.session_state.score += 1
                            q["_scored"] = True
                    else:
                        st.error(f"❌ Correct: {correct_letter}")
    
                    st.info(q["explanation"])
    
                    if st.button("Next", key=f"n_{idx}"):
                        st.session_state.quiz_index += 1
                        st.session_state.show_feedback = False
                        st.rerun()
    
            else:
                score = st.session_state.score
                st.success(f"🎉 Completed! Score: {score}/{total}")
    
                if st.button("Restart Quiz"):
                    for k in ["quiz","quiz_index","score","show_feedback","last_answer"]:
                        if k in st.session_state:
                            del st.session_state[k]
                    st.rerun()
                    
    # ===============================
    # REPORT TAB (DON'T CHANGE CORE FLOW)
    # ===============================
    with tab5:
        st.subheader("Report Delivery")

        email = st.text_input("Enter Email Address")

        if st.button("📤 Send Report"):
            report_agent = ReportDeliveryAgent()
            response = report_agent.run(
                st.session_state.doc_result,
                st.session_state.impact_result,
                email
            )

            st.success("✅ Report sent successfully")

        st.markdown('</div>', unsafe_allow_html=True)