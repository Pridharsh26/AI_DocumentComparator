# import streamlit as st
# import os
# from pypdf import PdfReader

# from services.chat_service import ChatService

# st.set_page_config(page_title="Policy Chatbot", layout="wide")


# # -------------------------
# # INIT BACKEND
# # -------------------------
# if "chat_service" not in st.session_state:
#     st.session_state.chat_service = ChatService()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "documents_loaded" not in st.session_state:
#     st.session_state.documents_loaded = False


# # -------------------------
# # PDF LOADER
# # -------------------------
# def extract_pdf_text(path):
#     reader = PdfReader(path)
#     text = ""
#     for page in reader.pages:
#         text += (page.extract_text() or "") + "\n"
#     return text


# def chunk_text(text, chunk_size=400):
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size):
#         chunks.append(" ".join(words[i:i + chunk_size]))
#     return chunks


# # -------------------------
# # PATHS
# # -------------------------
# base_dir = os.path.dirname(__file__)
# old_path = os.path.join(base_dir, "old.pdf")
# new_path = os.path.join(base_dir, "new.pdf")


# # -------------------------
# # TITLE
# # -------------------------
# st.title("🧠 AI Policy Comparison Chatbot")


# # -------------------------
# # LOAD POLICIES
# # -------------------------
# if st.button("📄 Load Policies"):

#     try:
#         with st.spinner("Reading PDFs..."):

#             old_text = extract_pdf_text(old_path)
#             new_text = extract_pdf_text(new_path)

#             old_chunks = chunk_text(old_text)
#             new_chunks = chunk_text(new_text)

#             st.session_state.chat_service.load_documents(old_chunks, new_chunks)

#             st.session_state.documents_loaded = True

#         st.success("Policies loaded successfully!")

#     except Exception as e:
#         st.error(f"Error loading PDFs: {str(e)}")


# # -------------------------
# # CHAT SECTION
# # -------------------------
# st.markdown("## 💬 Chat")

# if not st.session_state.documents_loaded:
#     st.warning("Please load policies first before chatting.")


# # -------------------------
# # CHAT HISTORY
# # -------------------------
# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.markdown(f"🧑 **You:** {msg['content']}")
#     else:
#         st.markdown(f"🤖 **Bot:** {msg['content']}")


# # -------------------------
# # INPUT BOX
# # -------------------------
# if "last_processed_input" not in st.session_state:
#     st.session_state.last_processed_input = None


# user_input = st.text_input("Ask about policy changes:")


# # -------------------------
# # PROCESS ONLY NEW INPUT
# # -------------------------
# if (
#     user_input
#     and st.session_state.documents_loaded
#     and user_input != st.session_state.last_processed_input
# ):

#     st.session_state.last_processed_input = user_input

#     # store user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     # call LLM
#     with st.spinner("Thinking..."):
#         response = st.session_state.chat_service.ask(user_input)

#     # store bot message
#     st.session_state.messages.append({
#         "role": "bot",
#         "content": response
#     })

#     # refresh UI once
#     st.rerun()

# import streamlit as st
# import os
# from pypdf import PdfReader
# from services.chat_service import ChatService

# st.set_page_config(page_title="Policy Chatbot", layout="wide")


# # =========================================================
# # 🎨 MODERN UI THEME (ONLY VISUAL LAYER)
# # =========================================================
# st.markdown("""
# <style>

# /* -------------------------
#    GLOBAL BACKGROUND
# ------------------------- */
# .stApp {
#     background: radial-gradient(circle at top left, #0b1220 0%, #0f172a 40%, #020617 100%);
#     color: #e5e7eb;
#     font-family: 'Inter', sans-serif;
# }

# /* -------------------------
#    TITLE
# ------------------------- */
# .main-title {
#     font-size: 36px;
#     font-weight: 900;
#     text-align: center;
#     background: linear-gradient(90deg, #38bdf8, #a78bfa, #34d399);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     margin-top: 10px;
#     margin-bottom: 5px;
# }

# .sub-title {
#     text-align: center;
#     color: #94a3b8;
#     font-size: 14px;
#     margin-bottom: 25px;
# }

# /* -------------------------
#    CHAT AREA
# ------------------------- */
# .chat-box {
#     max-width: 900px;
#     margin: auto;
#     padding: 15px;
# }

# /* -------------------------
#    USER MESSAGE
# ------------------------- */
# .user-msg {
#     background: linear-gradient(135deg, #3b82f6, #6366f1);
#     color: white;
#     padding: 12px 16px;
#     border-radius: 18px 18px 4px 18px;
#     margin: 10px 0;
#     max-width: 75%;
#     margin-left: auto;
#     box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);
#     font-size: 14px;
#     line-height: 1.5;
# }

# /* -------------------------
#    BOT MESSAGE (GLASS EFFECT)
# ------------------------- */
# .bot-msg {
#     background: rgba(15, 23, 42, 0.75);
#     backdrop-filter: blur(10px);
#     border: 1px solid rgba(148, 163, 184, 0.15);
#     color: #e5e7eb;
#     padding: 12px 16px;
#     border-radius: 18px 18px 18px 4px;
#     margin: 10px 0;
#     max-width: 75%;
#     box-shadow: 0 10px 25px rgba(0,0,0,0.35);
#     font-size: 14px;
#     line-height: 1.5;
# }

# /* -------------------------
#    SIDEBAR
# ------------------------- */
# section[data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0f172a, #020617);
#     border-right: 1px solid rgba(148, 163, 184, 0.1);
# }

# /* -------------------------
#    BUTTONS
# ------------------------- */
# .stButton > button {
#     background: linear-gradient(90deg, #6366f1, #3b82f6);
#     color: white;
#     border-radius: 12px;
#     border: none;
#     padding: 10px 16px;
#     font-weight: 600;
#     transition: all 0.2s ease-in-out;
#     box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
# }

# .stButton > button:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 12px 30px rgba(99, 102, 241, 0.35);
# }

# /* -------------------------
#    INPUT BOX
# ------------------------- */
# .stTextInput > div > div > input {
#     background-color: rgba(15, 23, 42, 0.6);
#     color: white;
#     border-radius: 12px;
#     border: 1px solid rgba(148, 163, 184, 0.2);
#     padding: 10px;
# }

# .stTextInput > div > div > input:focus {
#     border: 1px solid #60a5fa;
#     box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
# }

# /* -------------------------
#    REMOVE STREAMLIT CLUTTER
# ------------------------- */
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}

# </style>
# """, unsafe_allow_html=True)


# # =========================================================
# # INIT BACKEND
# # =========================================================
# if "chat_service" not in st.session_state:
#     st.session_state.chat_service = ChatService()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "documents_loaded" not in st.session_state:
#     st.session_state.documents_loaded = False


# # =========================================================
# # PDF LOADER
# # =========================================================
# def extract_pdf_text(path):
#     reader = PdfReader(path)
#     text = ""
#     for page in reader.pages:
#         text += (page.extract_text() or "") + "\n"
#     return text


# def chunk_text(text, chunk_size=400):
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size):
#         chunks.append(" ".join(words[i:i + chunk_size]))
#     return chunks


# # =========================================================
# # TITLE
# # =========================================================
# st.markdown('<div class="main-title">🧠 Policy Intelligence Assistant</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-title">Compare Legacy vs Modernized policies using AI</div>', unsafe_allow_html=True)


# # =========================================================
# # LOAD POLICIES
# # =========================================================
# if st.button("📄 Load Policies"):

#     try:
#         with st.spinner("Reading the Documents..."):

#             base_dir = os.path.dirname(__file__)
#             old_path = os.path.join(base_dir, "old.pdf")
#             new_path = os.path.join(base_dir, "new.pdf")

#             old_text = extract_pdf_text(old_path)
#             new_text = extract_pdf_text(new_path)

#             old_chunks = chunk_text(old_text)
#             new_chunks = chunk_text(new_text)

#             st.session_state.chat_service.load_documents(old_chunks, new_chunks)
#             st.session_state.documents_loaded = True

#         st.success("Documents loaded successfully!")

#     except Exception as e:
#         st.error(f"Error loading PDFs: {str(e)}")


# # =========================================================
# # CHAT SECTION
# # =========================================================
# st.markdown("## 💬 Chat")

# if not st.session_state.documents_loaded:
#     st.warning("Please load the policies first before chatting.")


# # =========================================================
# # CHAT HISTORY
# # =========================================================
# st.markdown('<div class="chat-box">', unsafe_allow_html=True)

# for msg in st.session_state.messages:

#     if msg["role"] == "user":
#         st.markdown(
#             f"<div class='user-msg'>🧑 {msg['content']}</div>",
#             unsafe_allow_html=True
#         )
#     else:
#         st.markdown(
#             f"<div class='bot-msg'>🤖 {msg['content']}</div>",
#             unsafe_allow_html=True
#         )

# st.markdown('</div>', unsafe_allow_html=True)


# # =========================================================
# # INPUT (UNCHANGED LOGIC)
# # =========================================================
# if "last_processed_input" not in st.session_state:
#     st.session_state.last_processed_input = None


# user_input = st.text_input("💬 Ask anything about policy differences:")


# # =========================================================
# # PROCESS (UNCHANGED LOGIC)
# # =========================================================
# if (
#     user_input
#     and st.session_state.documents_loaded
#     and user_input != st.session_state.last_processed_input
# ):

#     st.session_state.last_processed_input = user_input

#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     with st.spinner("Thinking..."):
#         response = st.session_state.chat_service.ask(user_input)

#     st.session_state.messages.append({
#         "role": "bot",
#         "content": response
#     })

#     st.rerun()

import streamlit as st
import os
from pypdf import PdfReader
from services.chat_service import ChatService

st.set_page_config(page_title="Policy Chatbot", layout="wide")

# =========================================================
# 🌟 LIGHT UI + CHAT BUBBLES ONLY
# =========================================================
st.markdown("""
<style>

/* Chat container */
.chat-box {
    max-width: 800px;
    margin: auto;
    padding: 10px;
}

/* User message */
.user-msg {
    background: #2563eb;
    color: white;
    padding: 10px 14px;
    border-radius: 12px 12px 4px 12px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
}

/* Bot message */
.bot-msg {
    background: #f1f5f9;
    color: black;
    padding: 10px 14px;
    border-radius: 12px 12px 12px 4px;
    margin: 8px 0;
    max-width: 75%;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# INIT SESSION
# =========================================================
if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "last_processed_input" not in st.session_state:
    st.session_state.last_processed_input = None

# =========================================================
# PDF HELPERS
# =========================================================
def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


# =========================================================
# HEADER
# =========================================================
st.title("🧠 Policy Chatbot")
st.caption("Ask questions about policy changes and differences")

# Back to main app (optional)
st.page_link("app2.py", label="⬅️ Back to Dashboard")

# =========================================================
# LOAD POLICIES
# =========================================================
st.markdown("### 📄 Load Documents")

if st.button("Load Policies"):

    try:
        with st.spinner("Reading documents..."):

            base_dir = os.path.dirname(__file__)
            old_path = os.path.join(base_dir, "old.pdf")
            new_path = os.path.join(base_dir, "new.pdf")

            old_text = extract_pdf_text(old_path)
            new_text = extract_pdf_text(new_path)

            old_chunks = chunk_text(old_text)
            new_chunks = chunk_text(new_text)

            st.session_state.chat_service.load_documents(
                old_chunks,
                new_chunks
            )

            st.session_state.documents_loaded = True

        st.success("✅ Documents loaded successfully")

    except Exception as e:
        st.error(f"Error loading PDFs: {str(e)}")


# =========================================================
# CHAT AREA
# =========================================================
st.markdown("## 💬 Chat")

if not st.session_state.documents_loaded:
    st.warning("Please load policies first")

# =========================================================
# CHAT HISTORY
# =========================================================
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.markdown(
            f"<div class='user-msg'>🧑 {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='bot-msg'>🤖 {msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# INPUT
# =========================================================
user_input = st.text_input("Ask about policy changes:")

# =========================================================
# PROCESS INPUT
# =========================================================
if (
    user_input
    and st.session_state.documents_loaded
    and user_input != st.session_state.last_processed_input
):

    st.session_state.last_processed_input = user_input

    # ✅ Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ✅ Get bot response
    with st.spinner("Thinking..."):
        response = st.session_state.chat_service.ask(user_input)

    # ✅ Save bot response
    st.session_state.messages.append({
        "role": "bot",
        "content": response
    })

    st.rerun()