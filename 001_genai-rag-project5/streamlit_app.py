import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = "http://localhost:8000"


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Investment Banking RAG",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       Application Background
       ======================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #f0fdf4 100%
        );
    }

    .main {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }


    /* ========================================================
       Metrics
       ======================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.90);

        border-radius: 14px;

        padding: 18px;

        border: 1px solid #e5e7eb;

        box-shadow:
            0 5px 15px rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
    }

    div[data-testid="stMetricValue"] {
        color: #312e81;
        font-weight: 800;
    }


    /* ========================================================
       Sidebar
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #eef2ff 0%,
            #f8fafc 60%,
            #ecfdf5 100%
        );

        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] h2 {
        color: #312e81;
    }

    section[data-testid="stSidebar"] h3 {
        color: #4338ca;
    }


    /* ========================================================
       Chat Messages
       ======================================================== */

    div[data-testid="stChatMessage"] {
        border-radius: 16px;

        margin-bottom: 14px;

        border: 1px solid #e5e7eb;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.04);
    }


    /* User message */

    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-user"]
    ) {
        background: #eef2ff;
        border-color: #c7d2fe;
    }


    /* Assistant message */

    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-assistant"]
    ) {
        background: white;
        border-color: #ddd6fe;
    }


    /* ========================================================
       Chat Input
       ======================================================== */

    div[data-testid="stChatInput"] {
        border-radius: 16px;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 14px;
    }


    /* ========================================================
       Buttons
       ======================================================== */

    .stButton button {
        border-radius: 10px;

        font-weight: 600;

        transition: all 0.2s ease;
    }

    .stButton button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 5px 12px rgba(0, 0, 0, 0.10);
    }


    /* ========================================================
       File Uploader
       ======================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        background: white;

        border: 2px dashed #818cf8;

        border-radius: 14px;
    }


    /* ========================================================
       Expander
       ======================================================== */

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.80);

        border-radius: 12px;

        border: 1px solid #e5e7eb;
    }


    /* ========================================================
       Source Badges
       ======================================================== */

    .source-badge {
        display: inline-block;

        background: #eef2ff;

        color: #4338ca;

        padding: 6px 10px;

        margin: 3px;

        border-radius: 8px;

        font-size: 12px;

        border: 1px solid #c7d2fe;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# API Functions
# ============================================================

def check_api_health():

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        if response.status_code == 200:

            return response.json()

        return None

    except requests.RequestException:

        return None


def get_documents():

    try:

        response = requests.get(
            f"{API_URL}/documents",
            timeout=10
        )

        if response.status_code == 200:

            return response.json()

        return []

    except requests.RequestException:

        return []


def upload_document(uploaded_file):

    try:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        return requests.post(
            f"{API_URL}/upload",
            files=files,
            timeout=300
        )

    except requests.RequestException as exc:

        st.error(
            f"Unable to connect to API: {exc}"
        )

        return None


def ask_question(question):

    try:

        return requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            },
            timeout=300
        )

    except requests.RequestException as exc:

        st.error(
            f"Unable to connect to API: {exc}"
        )

        return None


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🏦 Investment Banking"
    )

    st.caption(
        "AI-Powered RAG Document Assistant"
    )

    st.divider()


    # ========================================================
    # System Status
    # ========================================================

    st.markdown("### 🔌 System Status")

    health = check_api_health()

    if health:

        st.success("API Connected")

        if health.get(
            "vectorstore_loaded",
            False
        ):

            st.success("Vector Database Ready")

        else:

            st.warning("Vector Database Empty")

    else:

        st.error("API Offline")


    st.divider()


    # ========================================================
    # Upload Document
    # ========================================================

    st.markdown("### 📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        file_size = (
            len(uploaded_file.getvalue())
            / (1024 * 1024)
        )

        st.info(
            f"📄 {uploaded_file.name}\n\n"
            f"Size: {file_size:.2f} MB"
        )

        if st.button(
            "🚀 Upload & Index",
            use_container_width=True,
            type="primary"
        ):

            with st.spinner(
                "Processing document and creating embeddings..."
            ):

                response = upload_document(
                    uploaded_file
                )

            if response:

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Document indexed successfully!"
                    )

                    st.metric(
                        "Chunks Created",
                        result.get(
                            "chunks_created",
                            0
                        )
                    )

                    st.rerun()

                elif response.status_code == 409:

                    try:

                        detail = response.json().get(
                            "detail",
                            "Document already indexed."
                        )

                    except Exception:

                        detail = (
                            "Document already indexed."
                        )

                    st.warning(detail)

                else:

                    try:

                        detail = response.json().get(
                            "detail",
                            "Upload failed."
                        )

                    except Exception:

                        detail = "Upload failed."

                    st.error(detail)


    st.divider()


    # ========================================================
    # Documents
    # ========================================================

    st.markdown("### 📚 Indexed Documents")

    documents = get_documents()

    if documents:

        st.caption(
            f"{len(documents)} document(s) available"
        )

        for document in documents:

            with st.expander(
                f"📄 {document['filename']}"
            ):

                st.write(
                    f"**Chunks:** "
                    f"{document['chunks']}"
                )

                size_mb = (
                    document["size_bytes"]
                    / (1024 * 1024)
                )

                st.write(
                    f"**Size:** "
                    f"{size_mb:.2f} MB"
                )

    else:

        st.info(
            "No documents indexed yet."
        )


    st.divider()


    # ========================================================
    # New Chat
    # ========================================================

    if st.button(
        "🗑️ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# Get Documents
# ============================================================

documents = get_documents()


# ============================================================
# Metrics
# ============================================================

total_chunks = sum(
    document["chunks"]
    for document in documents
)

total_size = sum(
    document["size_bytes"]
    for document in documents
)

total_size_mb = (
    total_size / (1024 * 1024)
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Documents",
        len(documents)
    )

with col2:

    st.metric(
        "🧩 Indexed Chunks",
        total_chunks
    )

with col3:

    st.metric(
        "💾 Storage",
        f"{total_size_mb:.1f} MB"
    )

with col4:

    st.metric(
        "💬 Questions",
        len(st.session_state.messages)
    )


st.divider()


# ============================================================
# Conversation History
# ============================================================

for message in st.session_state.messages:

    question = message["question"]

    answer = message["answer"]

    sources = message.get(
        "sources",
        []
    )


    # ========================================================
    # User Message
    # ========================================================

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(question)


    # ========================================================
    # Assistant Message
    # ========================================================

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        st.write(answer)


        # ====================================================
        # Sources
        # ====================================================

        if sources:

            st.markdown(
                "**📚 Sources**"
            )

            source_html = ""

            for source in sources:

                source_html += (
                    f'<span class="source-badge">'
                    f'📄 {source}'
                    f'</span>'
                )

            st.markdown(
                source_html,
                unsafe_allow_html=True
            )


# ============================================================
# Question Input
# ============================================================

question = st.chat_input(
    "💬 Ask a question about your banking documents..."
)


# ============================================================
# Process Question
# ============================================================

if question:

    question = question.strip()


    # ========================================================
    # Validation
    # ========================================================

    if len(question) < 3:

        st.warning(
            "Please enter at least 3 characters."
        )

        st.stop()


    # ========================================================
    # API Request
    # ========================================================

    with st.spinner(
        "🔎 Searching documents and generating answer..."
    ):

        response = ask_question(
            question
        )


    # ========================================================
    # Response
    # ========================================================

    if response:

        if response.status_code == 200:

            result = response.json()

            st.session_state.messages.append(
                {
                    "question": question,

                    "answer": result.get(
                        "answer",
                        ""
                    ),

                    "sources": result.get(
                        "sources",
                        []
                    )
                }
            )

            st.rerun()


        else:

            try:

                detail = response.json().get(
                    "detail",
                    "Unable to answer the question."
                )

            except Exception:

                detail = (
                    "Unable to answer the question."
                )

            st.error(detail)