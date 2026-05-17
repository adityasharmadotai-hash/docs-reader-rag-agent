import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask(question, documents):
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the documents below.
If the answer is not in the documents, say "I could not find that in the documents."

Documents:
{documents}

Question: {question}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content