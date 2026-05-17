import streamlit as st
from loader import load_documents
from agent import ask

st.set_page_config(page_title="Document AI Agent", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; padding: 8px; margin-bottom: 8px; }
    .stChatInputContainer { border-top: 2px solid #e0e0e0; padding-top: 10px; }
    h1 { color: #1a1a2e; font-family: 'Segoe UI', sans-serif; }
    .subtitle { color: #666; font-size: 16px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 📄 Document AI Agent")
st.markdown('<p class="subtitle">Ask questions and get instant answers from your documents.</p>', unsafe_allow_html=True)
st.divider()

documents = load_documents()

if not documents.strip():
    st.error("⚠️ No documents found. Please add .docx files to the 'docs' folder in your GitHub repo.")
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
            answer = ask(question, documents)

        st.chat_message("assistant", avatar="🤖").write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})