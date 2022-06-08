from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.table import WD_ALIGN__HORIZONTAL

document = Document()
table = document.add_table(rows=5, cols =7)
table.cell.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
table.cell.horizontal_alignment = WD_TABLE_ALIGNMENT.CENTER.BOTTOM

#table.style = 'table_heading_style'
hdr_cells = table.rows[0].cells

# hdr_cells.
hdr_cells[0].text = 'REV'
hdr_cells[1].text = 'DATE'
hdr_cells[2].text = 'ISSUE PURPOSE / DESCRIPTION OF CHANGE'
hdr_cells[3].text = 'TOTAL PAGES'
hdr_cells[4].text = 'HYUNDAI-WISON PREP‟D/CHK‟/APR‟D BY'
hdr_cells[5].text = 'PDVSA CHECKED BY'
hdr_cells[6].text = 'PDVSA APPROVED BY'

document.save('demo.docx')