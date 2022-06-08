from docx import Document
from docx.shared import Inches

document = Document()
section = document.sections[0]
header = section.header
print(header)

paragraph = header.paragraphs[0]

paragraph.text = "Title of my document"

print(header.is_linked_to_previous)
document.save('demo.docx')