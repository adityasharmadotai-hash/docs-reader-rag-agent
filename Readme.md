# 📄 Document AI Agent

An AI-powered chatbot that reads your Word documents and answers questions from them — built with Python, OpenAI, and Streamlit.

**👉 FIND THE STEP-BY-STEP TUTORIAL [HERE](https://github.com/adityasharmadotai-hash/docs-reader-rag-agent/blob/main/TUTORIAL.md)**

---

## Overview

Document AI Agent lets you upload any Word (`.docx`) files and instantly ask questions about their content. Instead of manually searching through documents, you simply type a question and the AI finds the answer for you.

Built as a beginner-friendly open source project to demonstrate how Retrieval Augmented Generation (RAG) works at its core — no complex frameworks, just clean Python.

---

## Features

- 💬 Chat interface — ask multiple questions in one session
- 📂 Multi-document support — reads all `.docx` files in the `docs/` folder
- 📊 Reads both paragraphs and tables from Word documents
- 🔍 Answers only from your documents — won't make things up
- 🤖 Asks clarifying questions when multiple documents are loaded
- 🧹 Clear chat button to reset the conversation

<img width="3024" height="1964" alt="image" src="https://github.com/user-attachments/assets/4eceb25e-122c-4681-9191-213956f4e6c9" />

---

## How It Works

```
User asks a question
        ↓
loader.py reads all .docx files from the docs/ folder
        ↓
agent.py sends the documents + question to OpenAI GPT
        ↓
GPT searches through the documents and returns an answer
        ↓
app.py displays the answer in the chat interface
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| OpenAI GPT-3.5 | AI model that reads and answers |
| Streamlit | Web interface |
| python-docx | Reads Word documents |

---

## File Structure

```
├── app.py            # Streamlit UI and chat interface
├── agent.py          # Sends questions + docs to OpenAI
├── loader.py         # Reads and parses .docx files
├── requirements.txt  # Python dependencies
└── docs/             # Put your Word documents here
    ├── document1.docx
    └── document2.docx
```
<img width="3024" height="1964" alt="image" src="https://github.com/user-attachments/assets/acc5f184-3d34-4d08-bd71-d5172f17fe58" />

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/adityasharmadotai-hash/docs-reader-rag-agent.git
cd docs-reader-rag-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your documents
Place your `.docx` files inside the `docs/` folder.

### 4. Set your OpenAI API key
Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your-api-key-here
```
Get your API key at [platform.openai.com](https://platform.openai.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub (do **not** commit your `.env` file)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set main file to `app.py`
4. Under **Advanced settings → Secrets**, add:
```toml
OPENAI_API_KEY = "your-api-key-here"
```
5. Click **Deploy** — you'll get a public URL in ~2 minutes

---

## Contributing

Pull requests are welcome! If you find a bug or want to suggest a feature, open an issue on GitHub.

---

## License

MIT License — free to use, modify, and share.

---

## ⭐ If you find this useful...

If you learned something from this project, it would mean a lot if you could:

- ⭐ **[Star this repository](https://github.com/adityasharmadotai-hash)** — it helps others discover this project
- 💼 **[Follow on LinkedIn](https://www.linkedin.com/in/aditya-hicounselor/)** — for daily AI news, tools, and updates
- 📺 **[Subscribe on YouTube](https://www.youtube.com/channel/UCPjQtVNUrf7EKrm8ZoqrCAQ)** — AI agents, tutorials, and the latest in the world of AI

> 🚀 **Looking for a job at a top AI company in the USA?**
> Fill out your information here → **[Apply Now](https://docs.google.com/forms/d/e/1FAIpQLSc3gJssBV3B25EZ3sYA7Qcen9NbtOB_wgQaturfB7lTXuAdLQ/viewform)**

---
