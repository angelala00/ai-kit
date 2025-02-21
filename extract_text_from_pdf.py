import pdfplumber

with pdfplumber.open("/Users/chijiang/Downloads/GNSS_V1.0.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
print(text)
