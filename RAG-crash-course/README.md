# RAG Crash Course

Learn Retrieval Augmented Generation (RAG) from absolute basics by building
one, piece by piece, in plain Python. No prior AI or machine learning
knowledge is needed. If you can read simple Python, you can follow along.

## What you will build

A question answering system over a small set of documents (a fictional
company called Aurora Dynamics). You will type questions like
"How many days of annual leave do employees get?" and get answers backed
by the actual documents, with sources.

You build every part yourself first: calling an LLM, creating embeddings,
chunking text, searching a vector database. Only at the very end do you
see how a framework (LangChain) wraps the same steps.

## Course structure

Work through the notebooks in order. Each one builds on the previous.

| # | Notebook | What you learn |
|---|----------|----------------|
| 1 | [01-what-is-rag.ipynb](notebooks/01-what-is-rag.ipynb) | Why LLMs fail on private data, and how RAG fixes it |
| 2 | [02-calling-an-llm.ipynb](notebooks/02-calling-an-llm.ipynb) | Your first API call, prompts, roles, temperature |
| 3 | [03-embeddings.ipynb](notebooks/03-embeddings.ipynb) | Turning text into numbers, measuring similarity |
| 4 | [04-chunking.ipynb](notebooks/04-chunking.ipynb) | Splitting documents into pieces an LLM can use |
| 5 | [05-vector-search.ipynb](notebooks/05-vector-search.ipynb) | Storing and searching chunks with ChromaDB |
| 6 | [06-build-a-rag-pipeline.ipynb](notebooks/06-build-a-rag-pipeline.ipynb) | Wiring everything into a working RAG system |
| 7 | [07-rag-with-langchain.ipynb](notebooks/07-rag-with-langchain.ipynb) | The same pipeline with LangChain, in far fewer lines |

## Getting started

Follow [SETUP.md](SETUP.md). It covers everything from installing Python
to getting an OpenAI API key. Total setup time is about 15 minutes.

Short version, if you already have Python 3.10 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste your OpenAI API key into .env
jupyter lab
```

## Cost

The notebooks use gpt-4o-mini and text-embedding-3-small, the cheapest
OpenAI models. Running the whole course typically costs a few cents.
A free alternative using Ollama (local models, no API key) is described
in [SETUP.md](SETUP.md).

## The sample data

The [data/](data/) folder contains six short documents about Aurora
Dynamics, a made up robotics company. The data is fictional on purpose:
the LLM has never seen it during training, so you can clearly watch RAG
make the difference between "I don't know" and a correct, sourced answer.

## What is not covered

This course sticks to the core RAG loop. Once you finish, natural next
topics to explore on your own are: hybrid search, reranking, query
rewriting, RAG evaluation (for example RAGAS), and agentic RAG.

## License

MIT. See [LICENSE](LICENSE).
