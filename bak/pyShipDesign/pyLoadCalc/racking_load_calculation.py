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

rie = ReadInputExcel('Colorado_Summary.xlsx', "DeckLoading")

deck_name = rie.read_input_column(5, 4, 1)
zi = rie.read_input_column(5, 4, 2)
ms = rie.read_input_column(5, 4, 3)
lc_name = rie.read_input_column(11, 13, 1)
TLC = rie.read_input_column(11,13,2)
GM = rie.read_input_column(11,13,3)
kr = rie.read_input_column(11,13,4)
mc = rie.read_input_col_row(11, 5, 2, 35)

Ls = 170.4
B = 30.2
D = 28.8
Ts = 8.7
Cb = 0.56
zmain = 14.4

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