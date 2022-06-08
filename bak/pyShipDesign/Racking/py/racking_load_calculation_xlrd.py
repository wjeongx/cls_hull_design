import math as mth
import xlrd
import xlsxwriter

#basic acceleration parameter - a0
def acceleration_parameter():
    global Ls, Cb
    a0 = (1.58 - 0.47 * Cb) * (2.4 / mth.sqrt(Ls) + 34 / Ls - 600 / pow(Ls,2))

    return a0

# roll motion
def roll_motion(GM, kr):
    global B, g, fp, fBK
    # Roll period - Ttheta
    Ttheta = 2.3 * mth.pi * kr / mth.sqrt(g*GM)
    
    # Roll angle in deg. - theta
    theta = 9000 * (1.4 - 0.035 * Ttheta) * fp * fBK / ((1.15*B + 55)*mth.pi)

    return Ttheta, theta

# sway acceleration
def sway_acceleration():
    global Ls, g, a0, fp
    a_sway = 0.3*(2.25-20/mth.sqrt(g*Ls)) * fp * a0 * g

    return a_sway

# roll acceleration - aroll
# rad/sec^2
def roll_acceleration(GM, kr):
    global fp, fBK

    Ttheta, theta = roll_motion(GM, kr)
    
    a_roll = fp*theta* mth.pi/180*pow(2* mth.pi/Ttheta,2)
    
    return a_roll

# enveloped y acceleration
def envelope_transverse_accelerations(TLC, GM, kr, z):
    global Ls, D
    
    R = min(D/4+TLC/2, D/2)
    Ttheta, theta = roll_motion(GM, kr)
    asway = sway_acceleration()
    aroll = roll_acceleration(GM, kr)
    
    aroll_y = aroll*(z-R)
    
    ay_env = (1-mth.exp(-B*Ls/(215*GM)))*mth.sqrt(pow(asway,2)+pow(g*mth.sin(mth.radians(theta)) + aroll_y,2))
            
    return ay_env

def racking_moment(nDK, z_main, z, mc, ms, ay_env):
    MR = 0.0
    for i in range(0, nDK):
        MR = MR + (mc[i] + ms[i])*ay_env[i] *(z[i]-z_main)
    return MR

dki = 8
lci = 12

wb = xlrd.open_workbook('Colorado_Summary.xlsx')
ws = wb.sheet_by_name("DeckLoading")

zi = []
for i in range(10, 2, -1):
    zi.append(ws.cell(i, 1).value)

print(zi)

ms = []
for i in range(10, 2, -1):
    ms.append(ws.cell(i, 2).value)

print(ms)

LCn = []
for i in range(20,32):
    LCn.append(ws.cell(i, 0).value)

print(LCn)

TLC = []
for i in range(20,32):
    TLC.append(ws.cell(i, 1).value)

print(TLC)

GM = []
for i in range(20,32):
    GM.append(ws.cell(i, 2).value)
print(GM)

LWT = []
for i in range(20,32):
    LWT.append(ws.cell(i,3).value)
print(LWT)

DWT = []
for i in range(20,32):
    DWT.append(ws.cell(i,4).value)
print(DWT)

DSP = []
for i in range(20,32):
    DSP.append(ws.cell(i,5).value)
print(DSP)

print("--------------------------------------------------------")

mc = []
for i in range(0, 12):
    mc.append([])
    for j in range(59, 51, -1):
        mc[i].append(ws.cell(j, i+1).value)
    print(mc[i])

# Main dimension
Ls = 170.4
B = 30.2
D = 28.8
Ts = 8.7
Cb = 0.56
Vs = 20.0
g = 9.81
a0 = acceleration_parameter()
fp = 1.0
fBK = 1.0
z_main = 14.4

wbx = xlsxwriter.Workbook("racking_result1.xlsx")
sht = wbx.add_worksheet("racking_moment")

align_left_format = wbx.add_format()
align_left_format.set_align('left')

number_format = wbx.add_format({'num_format' : '0.000'})

irow = 0
sht.write(irow, 0, 'Main Dimension'       , align_left_format )
irow += 1
sht.write(irow, 0, 'Length for Scantling (Ls)', align_left_format)
sht.write_number(irow, 2, Ls,number_format  )
sht.write(irow, 3, 'm' )
irow += 1
sht.write(irow, 0, 'Moulded Breadth       (B)' , align_left_format)
sht.write_number(irow, 2, B,number_format )
sht.write(irow, 3, 'm' )
irow += 1
sht.write(irow, 0, 'Moulded Depth        (Ds)' , align_left_format)
sht.write(irow, 2, D,number_format )
sht.write(irow, 3, 'm' )
irow += 1
sht.write(irow, 0, 'Scantling Draft      (Ts)' , align_left_format)
sht.write(irow, 2, Ts,number_format  )
sht.write(irow, 3, 'm' )
irow += 1
sht.write(irow, 0, 'Block Coefficient    (Cb)' , align_left_format)
sht.write(irow, 2, Cb,number_format )
irow += 1
sht.write(irow, 0, 'Service Speed        (Vs)' , align_left_format)
sht.write(irow, 2, Vs,number_format )
sht.write(irow, 3, 'kNot' )
irow += 1
sht.write(irow, 0, 'Acceleration parameter(a0)', align_left_format)
sht.write(irow, 2, a0,number_format )
irow += 1
# print acceleration_parameter()
# print sway_acceleration()
# print roll_acceleration(GM[0], kr)
# print roll_motion(GM[0], kr)
# print zi[0]

#print zi
#print TLC
#print GM

for lci in range(0,12):
    GM[lci] = max(GM[lci], 0.05*B)

kr = []
for lci in range(0,12):
    kr.append(0.39*B)

MR = []
ay_env = []
for lci in range(0,12):
    ay_env.append([])
    for idk in range(0, 8):
        ay_env[lci].append(envelope_transverse_accelerations(TLC[lci], GM[lci], kr[lci], zi[idk]))
    
    MR.append(racking_moment(8, z_main, zi, mc[lci], ms, ay_env[lci]))

head_format = wbx.add_format()
head_format.set_bg_color('#A6C2E6')
head_format.set_align('center')

irow += 1

sht.write( irow, 0, "LC", head_format)
sht.write( irow, 1, "GM", head_format)
sht.write( irow, 2, "kr", head_format)
sht.write( irow, 3, "MR", head_format)

for i in range(0,dki):
    sht.write(irow, i+4, 'NO.'+str(i+6)+' DECK', head_format)

cell_format = wbx.add_format()
cell_format.set_align('center')
cell_format.set_num_format('#.000')
sht.set_column(0, 12, 12, cell_format)

int_format = wbx.add_format({'num_format' : '#.'})

irow += 1
for lci in range(0, 12):
    sht.write(irow, 0, LCn[lci])
    sht.write(irow, 1, GM[lci])
    sht.write(irow, 2, kr[lci])
    sht.write(irow, 3, MR[lci], int_format)    
    for idk in range(0,dki):
        sht.write(irow, idk+4, ay_env[lci][idk])
    irow += 1

sht.write(irow,0,"Maximum")
sht.write(irow,1,"=MAX(B11:B22)")
sht.write(irow,2,"=MAX(C11:C22)")
sht.write(irow,3,"=MAX(D11:D22)",int_format)

irow += 1

for dki in range(0,8):
    sht.write(irow, dki, ms[dki])

irow += 1
for lci in range(0,12):
    for dki in range(0,8):
        sht.write(irow, dki, mc[lci][dki])
    irow += 1



wbx.close()
