# 🤖 Build a Document AI Agent from Scratch
### A Step-by-Step Tutorial for Beginners

> **What you'll build:** A web app where you upload Word documents and ask the AI questions about them — powered by OpenAI and deployed free on Streamlit.

---

## 📋 Table of Contents

1. [What Are We Building?](#1-what-are-we-building)
2. [How It Works](#2-how-it-works)
3. [Prerequisites](#3-prerequisites)
4. [Project Setup](#4-project-setup)
5. [File 1 — loader.py](#5-file-1--loaderpy)
6. [File 2 — agent.py](#6-file-2--agentpy)
7. [File 3 — app.py](#7-file-3--apppy)
8. [File 4 — requirements.txt](#8-file-4--requirementstxt)
9. [Adding Your Documents](#9-adding-your-documents)
10. [Running Locally](#10-running-locally)
11. [Deploying to Streamlit Cloud](#11-deploying-to-streamlit-cloud)
12. [Testing Your App](#12-testing-your-app)
13. [Common Errors & Fixes](#13-common-errors--fixes)

---

## 1. What Are We Building?

Imagine having an assistant that has read all your documents and can instantly answer any question about them. That's exactly what this app does.

```
📂 Your Word Documents  →  🤖 AI Agent  →  💬 Answers Your Questions
```

**Real-world use cases:**
- 📄 Ask questions across multiple job descriptions
- 📚 Query a collection of research papers
- 📋 Search through policy or legal documents
- 🏢 Company knowledge base Q&A

This pattern is called **RAG (Retrieval Augmented Generation)** — it's the foundation of most AI document tools you see today like ChatPDF, NotebookLM, and enterprise search tools.

---

## 2. How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR APP FLOW                        │
│                                                         │
│  📁 docs/ folder                                        │
│     └── document1.docx  ──┐                            │
│     └── document2.docx  ──┤                            │
│     └── document3.docx  ──┘                            │
│              ↓                                          │
│         loader.py                                       │
│    (reads & extracts text)                              │
│              ↓                                          │
│  👤 User types a question                               │
│              ↓                                          │
│         agent.py                                        │
│  (sends docs + question to OpenAI)                      │
│              ↓                                          │
│       🤖 OpenAI GPT                                     │
│   (reads docs, finds answer)                            │
│              ↓                                          │
│         app.py                                          │
│    (displays answer in chat)                            │
└─────────────────────────────────────────────────────────┘
```

**Three key files, each with one job:**

| File | Job | Analogy |
|------|-----|---------|
| `loader.py` | Opens and reads Word files | A librarian who collects all books |
| `agent.py` | Asks OpenAI the question | A student who reads and answers |
| `app.py` | Shows the chat interface | The classroom where it all happens |

---

## 3. Prerequisites

Before starting, make sure you have:

### ✅ Required

- [ ] **Python 3.8+** installed → [python.org/downloads](https://python.org/downloads)
- [ ] **VS Code** (recommended editor) → [code.visualstudio.com](https://code.visualstudio.com)
- [ ] **OpenAI API Key** → [platform.openai.com](https://platform.openai.com) (requires billing setup)
- [ ] **GitHub account** → [github.com](https://github.com)
- [ ] **Streamlit account** → [share.streamlit.io](https://share.streamlit.io) (free, sign in with GitHub)

### 💡 Check Python is installed
Open your terminal and run:
```bash
python3 --version
```
You should see something like `Python 3.11.0`. If not, install Python first.

---

## 4. Project Setup

### Step 1 — Create your project folder

```bash
mkdir document-ai-agent
cd document-ai-agent
```

### Step 2 — Create the folder structure

```bash
mkdir docs
```

Your project should now look like this:
```
document-ai-agent/
└── docs/          ← your Word files go here
```

### Step 3 — Open in VS Code

```bash
code .
```

### Step 4 — Create a GitHub repository

1. Go to [github.com](https://github.com) → click **New Repository**
2. Name it `document-ai-agent`
3. Set it to **Public** (so it's open source)
4. Click **Create Repository**
5. Follow the instructions to connect your local folder to GitHub

---

## 5. File 1 — `loader.py`

> 📖 **What this file does:** Opens every `.docx` file in your `docs/` folder, extracts all the text (including tables), and returns it as one big string that the AI can read.

Create a new file called `loader.py` and paste this code:

```python
import os
from docx import Document
from docx.oxml.ns import qn

def get_outline_level(para):
    try:
        pPr = para._p.find(qn('w:pPr'))
        if pPr is not None:
            outlineLvl = pPr.find(qn('w:outlineLvl'))
            if outlineLvl is not None:
                return int(outlineLvl.get(qn('w:val')))
    except Exception:
        pass
    return None

def load_documents(folder="docs"):
    all_text = ""
    for filename in os.listdir(folder):
        if not filename.endswith(".docx"):
            continue
        path = os.path.join(folder, filename)
        try:
            doc = Document(path)
        except Exception as e:
            all_text += f"\n\n[Could not read {filename}: {e}]\n"
            continue

        all_text += f"\n\n{'='*50}\nDOCUMENT: {filename}\n{'='*50}\n"

        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            level = get_outline_level(para)
            if level is not None:
                all_text += f"\n[SECTION: {text}]\n"
            else:
                if "\n" in para.text:
                    for line in para.text.split("\n"):
                        line = line.strip()
                        if line:
                            all_text += f"- {line}\n"
                else:
                    all_text += f"- {text}\n"

    return all_text
```

### 🔍 Key Sections Explained

**`os.listdir(folder)`**
Loops through every file in the `docs/` folder. Only processes files ending in `.docx`.

**`Document(path)`**
This is from the `python-docx` library. It opens the Word file and gives us access to all its content.

**`get_outline_level(para)`**
Word documents use hidden XML to mark section headings like "Qualifications" or "Responsibilities". This function detects those and labels them clearly as `[SECTION: ...]` so the AI understands the document structure.

**`try/except`**
If a file is corrupted or not a valid Word file, the app skips it and moves on instead of crashing.

---

## 6. File 2 — `agent.py`

> 🧠 **What this file does:** Takes the document text and your question, sends both to OpenAI GPT, and returns the AI's answer. This is the "brain" of the app.

Create a new file called `agent.py`:

```python
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask(question, documents, chat_history):
    history_text = ""
    for msg in chat_history[:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are a helpful assistant that answers questions strictly 
from the job description documents provided below.

Rules:
- If multiple documents exist and the question is unclear about which job, 
  ask the user to clarify which role they mean.
- Search carefully through ALL sections (Qualifications, Responsibilities, 
  Job description, Benefits) to find relevant information.
- If the answer is truly not in the documents, say 
  "I could not find that in the documents."
- Always mention which company/role your answer is about.

Documents:
{documents}

Previous conversation:
{history_text}

Current question: {question}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### 🔍 Key Sections Explained

**`st.secrets["OPENAI_API_KEY"]`**
Reads your API key securely from Streamlit's secrets manager — no hardcoding keys in your code!

**`ask(question, documents, chat_history)`**
The main function takes 3 things:
- `question` — what the user typed
- `documents` — all the text extracted by `loader.py`
- `chat_history` — previous messages so the AI remembers context

**The prompt (most important part)**
This is the instruction set we give the AI. Notice we tell it to:
- Answer ONLY from the documents
- Ask which role if multiple documents exist
- Search through ALL sections, not just the first one it finds

> 💡 **This is called "prompt engineering"** — writing clear instructions for the AI is one of the most important skills in building AI apps.

---

## 7. File 3 — `app.py`

> 🖥️ **What this file does:** Creates the entire web interface — the chat window, the input box, the styling. This is what users see and interact with.

Create a new file called `app.py`:

```python
import streamlit as st
from loader import load_documents
from agent import ask

st.set_page_config(page_title="Document AI Agent", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; padding: 8px; margin-bottom: 8px; }
    h1 { color: #1a1a2e; font-family: 'Segoe UI', sans-serif; }
    .subtitle { color: #666; font-size: 16px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 📄 Document AI Agent")
st.markdown('<p class="subtitle">Ask questions and get instant answers from your documents.</p>',
            unsafe_allow_html=True)
st.divider()

documents = load_documents()

if not documents.strip():
    st.error("⚠️ No documents found. Please add .docx files to the 'docs' folder.")
else:
    st.success("✅ Documents loaded and ready! Start asking questions below.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.chat_message(msg["role"], avatar=icon).write(msg["content"])

    question = st.chat_input("💬 Ask a question about your documents...")
    if question:
        st.chat_message("user", avatar="🧑").write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        with st.spinner("🤖 Thinking..."):
            answer = ask(question, documents, st.session_state.messages)

        st.chat_message("assistant", avatar="🤖").write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
```

### 🔍 Key Sections Explained

**`st.set_page_config(...)`**
Sets the browser tab title, icon, and layout before anything else renders.

**`st.markdown("""<style>...</style>""")`**
Custom CSS styling injected directly into the page — changes background color, chat bubble shape, fonts.

**`st.session_state.messages`**
This is Streamlit's memory within one session. Every time the user sends a message, it's stored here. This is how the chat history stays on screen.

**`st.chat_input(...)`**
The input box at the bottom of the screen. When the user presses Enter, this triggers the AI call.

**`st.spinner("🤖 Thinking...")`**
Shows a loading animation while waiting for the AI to respond.

---

## 8. File 4 — `requirements.txt`

> 📦 **What this file does:** Tells Python (and Streamlit Cloud) which packages to install. Without this, the app won't know it needs OpenAI, Streamlit, etc.

Create a file called `requirements.txt`:

```
streamlit
openai
python-docx
```

---

## 9. Adding Your Documents

Place all your Word documents (`.docx`) inside the `docs/` folder:

```
document-ai-agent/
├── app.py
├── agent.py
├── loader.py
├── requirements.txt
└── docs/
    ├── document1.docx
    ├── document2.docx
    └── document3.docx
```

> ⚠️ **Important:** Only `.docx` format is supported. If you have `.doc` (older Word format), open it in Microsoft Word and save as `.docx` first.

---

## 10. Running Locally

### Step 1 — Install all packages

```bash
pip3 install streamlit openai python-docx
```

### Step 2 — Set your API key

Create a file called `.env` in your project root:
```
OPENAI_API_KEY=your-api-key-here
```

> 🔐 **Never share this file or commit it to GitHub.** Add `.env` to your `.gitignore` file.

Create `.gitignore`:
```
__pycache__/
*.pyc
.env
```

### Step 3 — Run the app

```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501` and you'll see your app!

---

## 11. Deploying to Streamlit Cloud

This gives your app a **free public URL** anyone can visit.

### Step 1 — Push to GitHub

Make sure all your files are committed and pushed:
```bash
git add .
git commit -m "Initial commit - Document AI Agent"
git push
```

> ⚠️ Do **NOT** push your `.env` file. Your `.gitignore` should prevent this.

### Step 2 — Connect to Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **Sign in with GitHub**
3. Click **New app**

### Step 3 — Configure your app

Fill in the form:
- **Repository:** select your `document-ai-agent` repo
- **Branch:** `main`
- **Main file path:** `app.py`

### Step 4 — Add your API key securely

Click **Advanced settings** → under **Secrets**, paste:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

> 💡 This replaces your `.env` file in the cloud. Streamlit encrypts and stores it securely.

### Step 5 — Deploy!

Click **Deploy** and wait ~2 minutes. You'll get a URL like:
```
https://your-name-document-ai-agent-app-xxxx.streamlit.app
```

Share this with anyone — they can use your app from any browser! 🎉

---

## 12. Testing Your App

Once deployed, try these types of questions to make sure everything works:

```
✅ Simple questions:
"What companies are in these documents?"
"What is the job title in document 1?"

✅ Specific questions:
"What qualifications are required for the Salesforce role?"
"What technical skills does Capital One require?"

✅ Comparison questions:
"Which role has the highest salary?"
"Which job requires the most years of experience?"

✅ Edge cases:
"What is the CEO's name?" ← should say "not found in documents"
```

---

## 13. Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Package not installed | Run `pip3 install -r requirements.txt` |
| `PackageNotFoundError` | Corrupted `.docx` file | Re-upload the Word file to the `docs/` folder |
| `openai.RateLimitError 429` | OpenAI quota exceeded | Add billing at platform.openai.com |
| `Invalid format: TOML` | Wrong secrets format on Streamlit | Use `KEY = "value"` format, not `Key: Value` |
| `File does not exist: app.py` | Wrong terminal directory | Run `cd your-project-folder` first |
| App says "No documents found" | `docs/` folder is empty | Add `.docx` files to the `docs/` folder |

---

## 🎓 What You Learned

By completing this tutorial, you've learned:

- ✅ **Python file structure** — how to split code across multiple files
- ✅ **Libraries** — using `python-docx`, `openai`, and `streamlit`
- ✅ **Prompt engineering** — writing instructions for an AI
- ✅ **RAG pattern** — how real AI document tools work
- ✅ **Streamlit** — building and deploying web apps with Python
- ✅ **API security** — keeping API keys safe with secrets management
- ✅ **GitHub** — version control and open source publishing

---

## 🚀 What's Next?

Now that you have a working app, here are some ideas to extend it:

- **Support PDF files** — add `PyPDF2` library to read `.pdf` files
- **File uploader** — let users upload documents directly in the browser instead of the `docs/` folder
- **Source highlighting** — show which document the answer came from
- **Multiple AI models** — let users choose between GPT-3.5 and GPT-4
- **Export answers** — add a button to download the chat as a PDF

---

*Built with ❤️ using Python, OpenAI, and Streamlit*

---

## ⭐ Enjoyed this tutorial?

If you learned something, it would mean a lot if you could:

- ⭐ **[Star the GitHub repository](https://github.com/adityasharmadotai-hash)** — helps others discover this project
- 💼 **[Follow on LinkedIn](https://www.linkedin.com/in/aditya-hicounselor/)** — daily AI news, tools, and updates
- 📺 **[Subscribe on YouTube](https://www.youtube.com/channel/UCPjQtVNUrf7EKrm8ZoqrCAQ)** — AI agents, tutorials, and the latest in AI

> 🚀 **Looking for a job at a top AI company in the USA?**
> Fill out your information here → **[Apply Now](https://docs.google.com/forms/d/e/1FAIpQLSc3gJssBV3B25EZ3sYA7Qcen9NbtOB_wgQaturfB7lTXuAdLQ/viewform)**

---
Now update the HTML blog post — adding a CTA banner right after the hero section:

Edited
blog-post.html
+28
-0
