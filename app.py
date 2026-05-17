import streamlit as st
from loader import load_documents
from agent import ask

st.title("📄 Document AI Agent")
st.write("Ask any question and the AI will answer from your Word documents.")

documents = load_documents()

if not documents.strip():
    st.warning("No documents found. Please add .docx files to the 'docs' folder in your GitHub repo.")
else:
    st.success("Documents loaded and ready!")
    question = st.text_input("Ask a question about your documents:")
    if st.button("Ask"):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask(question, documents)
            st.subheader("Answer:")
            st.write(answer)
        else:
            st.warning("Please type a question first.")