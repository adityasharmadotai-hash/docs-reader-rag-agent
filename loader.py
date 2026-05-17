import os
from docx import Document

def load_documents(folder="docs"):
    all_text = ""
    for filename in os.listdir(folder):
        if filename.endswith(".docx"):
            path = os.path.join(folder, filename)
            doc = Document(path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            all_text += f"\n\n--- {filename} ---\n{text}"
    return all_text
