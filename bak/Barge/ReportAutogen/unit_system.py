from docx import Document
from docx.shared import Inches
# import openpyxl as xl

table = document.add_table(rows=12, cols=4)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'MULTIPLY BY'
hdr_cells[1].text = 'TO CONVERT FROM'
hdr_cells[2].text = 'TO OBTAIN'
for qty, id, desc in records:
    row_cells = table.add_row().cells
    row_cells[0].text = str(qty)
    row_cells[1].text = id
    row_cells[2].text = desc


MILIMETERS
CENTIMETERS
METERS
KILOGRAMMES
KILOGRAMMES
METRIC TONS
(ie TONNES OF 1000) KILOS
METRIC TONS PER CENTIMETER (OF IMMERSION)
MOMENT TO CHANGE TRIM ONE CENTIMETER
(TONESS METER UNIT)
METER RADIANS
TO OBTAIN


INCHES
INCHES
FEET
POUNDS
TONS(2240 lbs)
TONS(2240 lbs)
TONS PER INCH
(IMMERSION)
MOMENT TO CHANGE
(FOOT TON UNITS)
FEET DEGREE
TO CONVERT FROM



25.400
2.540
0.3048
0.45359
1016.047
1.016
0.400
0.122
0.0053
MULTIPLY BY ABOVE
