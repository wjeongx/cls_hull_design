from docx import Document
from docx.shared import Inches

document = Document()

document.add_picture('monty-truth.png', width=Inches(2.5))

document.save('demo.docx')