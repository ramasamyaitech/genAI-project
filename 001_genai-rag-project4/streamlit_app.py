import requests
import streamlit as st


API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="Investment Banking RAG",
    page_icon="🏦",
    layout="wide"
)


st.title("🏦 Investment Banking RAG Assistant")

st.write(
    "Upload banking documents and ask questions "
    "using Retrieval-Augmented Generation."
)


# --------------------------------------------------
# PDF Upload
# --------------------------------------------------

st.header("1. Upload Investment Banking Document")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.button("Upload and Index"):

        try:

            response = requests.post(
                f"{API_URL}/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                },
                timeout=300
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    data["message"]
                )

                st.info(
                    f"Chunks created: "
                    f"{data['chunks_created']}"
                )

            else:

                st.error(
                    response.text
                )

        except Exception as e:

            st.error(
                f"API connection error: {e}"
            )


# --------------------------------------------------
# Question
# --------------------------------------------------

st.header("2. Ask a Question")

question = st.text_area(
    "Enter your investment banking question",
    placeholder=(
        "Example: What are the key risks "
        "associated with an M&A transaction?"
    ),
    height=120
)


if st.button("Ask Question"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Searching documents and generating answer..."
            ):

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=300
                )

            if response.status_code == 200:

                data = response.json()

                st.subheader("Answer")

                st.write(
                    data["answer"]
                )

                st.subheader("Sources")

                for source in data["sources"]:

                    st.write(
                        f"- {source}"
                    )

            else:

                st.error(
                    response.text
                )

        except Exception as e:

            st.error(
                f"API connection error: {e}"
            )