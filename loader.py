import os
from docx import Document

def load_documents(folder="docs"):
    all_text = ""
    for filename in os.listdir(folder):
        if filename.endswith(".docx"):
            path = os.path.join(folder, filename)
            doc = Document(path)

            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

            table_texts = []
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                    if row_text:
                        table_texts.append(row_text)

            combined = "\n".join(paragraphs)
            if table_texts:
                combined += "\n\nTable Data:\n" + "\n".join(table_texts)

            all_text += f"\n\n--- {filename} ---\n{combined}"
    return all_text