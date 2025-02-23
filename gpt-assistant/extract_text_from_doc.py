from docx import Document

doc = Document("example.docx")
text = ""
for para in doc.paragraphs:
    text += para.text
print(text)
