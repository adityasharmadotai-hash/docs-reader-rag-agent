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
        if filename.endswith(".docx"):
            path = os.path.join(folder, filename)
            doc = Document(path)
            all_text += f"\n\n{'='*50}\nDOCUMENT: {filename}\n{'='*50}\n"

            current_section = ""
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                level = get_outline_level(para)
                if level is not None:
                    current_section = text
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
