import math as mth
import xlrd
import xlsxwriter
from cShipMotion import ShipMotion

class ReadInputExcel:
    def __init__(self, BookName, SheetName):
        self.BookName = BookName
        self.SheetName = SheetName
        self.wb = xlrd.open_workbook(self.BookName)
        self.ws = self.wb.sheet_by_name(self.SheetName)
   
    def read_input_column(self, nrow, row_start, i_col):
        self.data = []
        for i in range(0, nrow):
            self.data.append(self.ws.cell(i+row_start-1,i_col-1).value)
        return self.data

    def read_input_row(self, ncol, col_start, i_row):
        self.data = []
        for i in range(0, ncol):
            self.data.append(self.ws.cell(i_row-1,i+col_start-1).value)
        return self.data

    def read_input_col_row(self, ncol, nrow, col_start, row_start):
        self.data = []
        for i in range(0, ncol):
            self.data.append([])
            for j in range(row_start, row_start + nrow):
                self.data[i].append(self.ws.cell(j-1, i + col_start-1).value)
        return self.data

def racking_moment(nDK, z_main, z, mc, ms, ay_env):
    MR = 0.0
    for i in range(0, nDK):
        MR = MR + (mc[i] + ms[i])*ay_env[i] *(z[i]-z_main)
    return MR

in_wb = xlrd.open_workbook('Racking_Input.xlsx')
ws_main = in_wb.sheet_by_name('MainDimension')
LBP = ws_main.cell(1,7).value
Ls = ws_main.cell(2,7).value
B = ws_main.cell(3,7).value
D = ws_main.cell(4,7).value
Ts = ws_main.cell(5,7).value
Cb = ws_main.cell(6,7).value
Vs = ws_main.cell(7,7).value
zBHD = ws_main.cell(8,7).value

wbx = xlsxwriter.Workbook("motion_result.xlsx")
shx = wbx.add_worksheet("result")

print(LBP)
print(Ls)
print(B)
print(D)
print(Ts)
print(Cb)
print(Vs)
print('zBHD = ', zBHD)

sm = ShipMotion(Ls,B,D,Cb)
a0 = sm.acceleration_parameter()

print('a0 = ', a0)

wbInput1 = ReadInputExcel('Racking_Input.xlsx', 'MainDimension')

dki = wbInput1.read_input_column(13,14,1)
print(dki)
zi = wbInput1.read_input_column(13,14,2)
print(zi)

wbInput2 = ReadInputExcel('Racking_Input.xlsx', 'CargoLoading')

LCi = wbInput2.read_input_row(3,5,3)
print(LCi)
TLCi = wbInput2.read_input_row(3,5,5)
print(TLCi)
GMi = wbInput2.read_input_row(3,5,6)
print(GMi)
kri = wbInput2.read_input_row(3,5,7)
print(kri)

Ttheta = []
theta = []
aroll = []
idx = 0
for idx in range(3):
    sm.GM = GMi[idx]
    sm.kr = kri[idx]
    Ttheta.append(sm.roll_period())
    theta.append(sm.roll_angle(1.0, 1.0))
    aroll.append(sm.roll_acceleration(1.0, 1.0))
#    idx += 1

print(u"Tθ =", Ttheta)
print(u"θ = ", theta)
print(aroll)

ndk = 13
MR = []
ay_env = []
for lc in range(3):
    ay_env.append([])
    sm.GM = GMi[lc]
    sm.kr = kri[lc]    
    for dk in range(13):
        ay_env[lc].append(sm.envelope_transverse_accelerations(TLCi[lc], zi[dk]))

    print(ay_env[lc])

global_format = wbx.add_format()
global_format.set_align('center')
global_format.set_num_format('#.000')
shx.set_column(0, 12, 12, global_format)

shx.write(1, 0, "LCi")
shx.write(1, 0, "GM(mm)")
shx.write(2, 0, "kr(mm)")
shx.write(3, 0, u"Tθ")
shx.write(4, 0, u"θ")

for idx in range(3):
    shx.write(0, idx + 2, LCi[idx])
    shx.write(1, idx + 2, GMi[idx])
    shx.write(2, idx + 2, kri[idx])
    shx.write(3, idx + 2, Ttheta[idx])    
    shx.write(4, idx + 2, theta[idx])    

for idx in range(3):
    shx.write(0, idx + 2, LCi[idx])
    shx.write(1, idx + 2, GMi[idx])
    shx.write(2, idx + 2, kri[idx])
    shx.write(3, idx + 2, Ttheta[idx])    

i_row = 6
shx.write(i_row, 0, "DKi")
shx.write(i_row, 1, "zi(mm)")

i_row += 1
for i in range(3):
    shx.write(i_row-1, i+3, LCi[i])
    for j in range(13):
        shx.write(i_row+j, 0, dki[j])
        shx.write(i_row+j, 1, zi[j])
        shx.write(i_row+j, i+3, ay_env[i][j])

wbx.close()

#    MR.append(racking_moment(5, zmain, zi, mc[lc], ms, ay_env[lc]))

"""
deck_name = rie.read_input_column(5, 4, 1)
zi = rie.read_input_column(5, 4, 2)
ms = rie.read_input_column(5, 4, 3)
lc_name = rie.read_input_column(11, 13, 1)
TLC = rie.read_input_column(11,13,2)
GM = rie.read_input_column(11,13,3)
kr = rie.read_input_column(11,13,4)
mc = rie.read_input_col_row(11, 5, 2, 35)

sm = ShipMotion(Ls, B, D, Cb)
a0 = sm.acceleration_parameter()

Ttheta = []
theta = []
aroll = []
idx = 0
for i in lc_name:
    sm.GM = GM[idx]
    sm.kr = kr[idx]
    Ttheta.append(sm.roll_period())
    theta.append(sm.roll_angle(1.0, 1.0))
    aroll.append(sm.roll_acceleration(1.0, 1.0))
    idx += 1

nlc = 11
ndk = 5
MR = []
ay_env = []
for lc in range(0,nlc):
    ay_env.append([])
    sm.GM = GM[lc]
    sm.kr = kr[lc]    
    for dk in range(0, ndk ):
        ay_env[lc].append(sm.envelope_transverse_accelerations(TLC[lc], zi[dk]))

    MR.append(racking_moment(5, zmain, zi, mc[lc], ms, ay_env[lc]))
"""