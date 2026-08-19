# Setup

This guide takes you from a blank machine to running the notebooks.
Follow it top to bottom. It covers macOS, Windows, and Linux.

## 1. Install Python

You need Python 3.10 or newer.

Check what you have. Open a terminal (macOS: Terminal app, Windows:
PowerShell) and run:

```bash
python3 --version
```

On Windows use:

```powershell
python --version
```

If the version is 3.10 or higher, skip to step 2.

If not:

- macOS: install from https://www.python.org/downloads/ or with Homebrew:

  ```bash
  brew install python
  ```

- Windows: install from https://www.python.org/downloads/ and check the
  box "Add python.exe to PATH" in the installer.

- Linux (Debian/Ubuntu):

  ```bash
  sudo apt update && sudo apt install python3 python3-venv python3-pip
  ```

## 2. Get the code

If you have git:

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Crash-Course.git
cd RAG-Crash-Course
```

If you do not have git, download the repository as a ZIP from GitHub
(green "Code" button, then "Download ZIP"), extract it, and open a
terminal in the extracted folder.

## 3. Create a virtual environment

A virtual environment keeps this course's packages separate from the
rest of your system.

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Your prompt should now start with (.venv). You need to activate the
environment again in every new terminal you open.

## 4. Install the packages

```bash
pip install -r requirements.txt
```

This installs Jupyter, the OpenAI SDK, ChromaDB, and LangChain. It can
take a few minutes.

## 5. Get an OpenAI API key

1. Create an account at https://platform.openai.com
2. Add a small amount of credit (5 dollars is far more than enough).
3. Go to https://platform.openai.com/api-keys and create a new key.
4. Copy the key. It starts with sk-.

Now put the key into a file called .env in the project folder:

```bash
cp .env.example .env
```

Open .env in any editor and replace the placeholder with your real key:

```
OPENAI_API_KEY=sk-...your real key...
```

The .env file is listed in .gitignore, so your key will never be
committed to git.

## 6. Start Jupyter

```bash
jupyter lab
```

Your browser opens. In the left sidebar, go into the notebooks folder
and open 01-what-is-rag.ipynb. Run cells with Shift+Enter.

That is it. You are ready.

## Free alternative: Ollama instead of OpenAI

If you prefer not to use an API key, you can run models locally with
Ollama. This is free but needs a reasonably modern machine (8 GB RAM or
more) and the answers from small local models are weaker.

1. Install Ollama from https://ollama.com/download
2. Pull a chat model and an embedding model:

   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

3. In each notebook, look for the cell titled "Ollama alternative". It
   shows the one or two lines to change. The trick: Ollama exposes an
   OpenAI compatible API on your machine, so the same Python code works
   with a different base URL.

## About ChromaDB

ChromaDB is the vector database used in notebooks 05 to 07. The
notebooks use it in embedded mode: it is just a Python package
(installed in step 4) that stores its data in a local folder called
chroma_db. There is nothing to install or run separately.

Optional: ChromaDB can also run as a separate server in Docker, which
is how you would deploy it for a real application shared by many users:

```bash
docker run -d -p 8000:8000 chromadb/chroma
```

Then connect with chromadb.HttpClient(host="localhost", port=8000)
instead of chromadb.PersistentClient(...). For this course the embedded
mode is all you need, so Docker is entirely optional.

## Troubleshooting

- "command not found: python3" on Windows: use python instead of
  python3 everywhere.
- "Activate.ps1 cannot be loaded because running scripts is disabled":
  run this once in PowerShell:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- Jupyter opens but cells fail with "No module named openai": the
  notebook is not using your virtual environment. Close Jupyter,
  activate the venv (step 3), and start jupyter lab from that same
  terminal.
- OpenAI errors mentioning "insufficient_quota": your account has no
  credit. Add credit in the OpenAI billing page.
