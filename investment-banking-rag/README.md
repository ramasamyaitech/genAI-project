# Investment Banking RAG Chatbot

An AI-powered "Retrieval-Augmented Generation" (RAG) chatbot designed to answer technical Investment Banking questions. This application ingests financial PDFs (like the "400 Questions & Technicals" guide), creates a semantic search index, and uses a local Large Language Model (LLM) to provide accurate, context-aware answers with citations.

The project is fully modularized for production use and supports both **CPU** and **GPU** inference.

## 🚀 Features

* **RAG Architecture:** Retains context from your own PDF documents to answer domain-specific questions.
* **Local Inference:** Runs entirely offline using Quantized GGUF models (no OpenAI API keys required).
* **Modular Design:** Clean separation of concerns (Chunking, Embedding, Retrieval, LLM) for easy maintenance.
* **Dual Support:** Configurable to run on standard CPUs or accelerated NVIDIA GPUs.
* **Source Citations:** Returns the exact text snippet and source document used to generate the answer.

## 🛠️ Tech Stack

* **Orchestration:** [LangChain](https://www.langchain.com/)
* **LLM Runtime:** [CTransformers](https://github.com/marella/ctransformers) (Mistral/Llama support)
* **Vector Store:** [ChromaDB](https://www.trychroma.com/)
* **Embeddings:** [HuggingFace BGE-Large](https://huggingface.co/BAAI/bge-large-en)
* **Backend API:** [Flask](https://flask.palletsprojects.com/)
* **Frontend:** HTML/Bootstrap (Simple Chat UI)

---

## 📂 Project Structure

```text
investment-banking-rag/
├── data/                 # Folder to store your source PDF documents
├── stores/               # Auto-generated folder for the Vector Database
├── templates/
│   └── index.html        # Frontend Chat Interface
├── app.py                # Main Flask application (Server)
├── ingest.py             # Script to process PDFs and build the DB
├── config.py             # Central configuration (Paths, Model settings, GPU/CPU)
├── chunking.py           # Logic for loading and splitting documents
├── embeddings.py         # Logic for initializing the Embedding Model
├── vector_store.py       # Logic for saving/loading ChromaDB
├── llm.py                # Logic for initializing the LLM and QA Chain
├── retriever.py          # Logic for the retrieval mechanism
└── requirements.txt      # Python dependencies