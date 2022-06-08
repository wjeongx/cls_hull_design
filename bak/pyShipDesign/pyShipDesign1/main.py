from dnvship import *
import xlrd
import xlsxwriter

# rie = ReadInputExcel('통합 문서1.xlsx', "Sheet1")

Bookname = '통합 문서1.xlsx'
Sheetname = 'Sheet1'
wb = xlrd.open_workbook(Bookname)
ws = wb.sheet_by_name(Sheetname)

# Analysis_Type = ws.cell(0,2).value
Analysis_Type = ws.cell(0,2).value
BilgeKeel = ws.cell(1,2).value
Ls = ws.cell(2,2).value
B = ws.cell(3,2).value
Ds = ws.cell(4,2).value
Ts = ws.cell(5,2).value
Cb = ws.cell(6,2).value
Vs = ws.cell(7,2).value
fps = ws.cell(8,2).value
fb = ws.cell(9,2).value
fR = ws.cell(10,2).value
if BilgeKeel == "with Bilge Keel":
    fBK = 1.0
elif BilgeKeel == "without Bilge Keel":
    fBK = 1.2

ffa = ws.cell(11,2).value

sm = shipMotion(Ls, B, Ds, Ts, Cb, Vs)

sm.fps = fps
sm.fbeta = fb
sm.fR = fR
sm.fBK = fBK
sm.ffa = ffa

print("Analysis_Type=",Analysis_Type)
print("Ls=",Ls)
print("B=",B)
print("Ds=", Ds)
print("Ts=", Ts)
print("Cb=", Cb)
print("Vs=", Vs)
print("fps=", sm.fps)
print("fbeta=", sm.fbeta)
print("fr=", sm.fr)
print("fBK=", sm.fBK)
print("ffa=", sm.ffa)


