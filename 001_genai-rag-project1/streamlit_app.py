import requests
import streamlit as st

# -----------------------------
# Configuration
# -----------------------------

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("📚 Enterprise RAG")

    st.markdown("---")

    st.subheader("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX or CSV",
        type=["pdf", "docx", "csv"]
    )

    if uploaded_file is not None:

        if st.button("Upload"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }

            with st.spinner("Uploading document..."):

                try:

                    response = requests.post(
                        f"{FASTAPI_URL}/upload",
                        files=files,
                        timeout=300
                    )

                    if response.status_code == 200:

                        st.success("✅ Upload Successful")

                    else:

                        st.error(response.text)

                except Exception as e:

                    st.error(str(e))

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# -----------------------------
# Title
# -----------------------------

st.title("🤖 Enterprise RAG Chatbot")

st.write(
    "Upload documents and ask questions."
)

# -----------------------------
# Health Check
# -----------------------------

try:

    health = requests.get(
        f"{FASTAPI_URL}/health",
        timeout=5
    )

    if health.status_code == 200:

        st.success("Backend Connected")

    else:

        st.error("Backend Not Healthy")

except:

    st.error("Cannot connect to FastAPI")

# -----------------------------
# Display Chat History
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------

question = st.chat_input(
    "Ask your question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(

                    f"{FASTAPI_URL}/ask",

                    json={
                        "question": question
                    },

                    timeout=300
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                else:

                    answer = response.text

            except Exception as e:

                answer = str(e)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )