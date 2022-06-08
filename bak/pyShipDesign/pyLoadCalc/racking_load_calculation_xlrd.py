import math as mth
import xlrd
import xlsxwriter
#import ShipMotion
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
    
    a_roll = fp*mth.radians(theta)*pow(2* mth.pi/Ttheta,2)
    
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

ay = envelope_transverse_accelerations(8.72,2.03,11.78 ,14.4)
print(ay)
ay = envelope_transverse_accelerations(8.72,2.03,11.78 ,20.94)
print(ay)


ndk = 5
nlc = 11

wb = xlrd.open_workbook('Colorado_Summary.xlsx')
ws = wb.sheet_by_name("DeckLoading")

irow = 3
deck = []
zi = []
ms = []
for i in range(irow, irow+ndk, 1):
    deck.append(ws.cell(i,0).value)
    zi.append(ws.cell(i, 1).value)
    ms.append(ws.cell(i, 2).value)
print(deck)
print(zi)
print(ms)

irow += ndk+4

LCn = []
TLC =[]
GM = []
kr = []
for i in range(irow,irow+nlc):
    LCn.append(ws.cell(i, 0).value)
    TLC.append(ws.cell(i, 1).value)
    GM.append(ws.cell(i, 2).value)
    kr.append(ws.cell(i, 3).value)

print(LCn)
print(TLC)
print(GM)
print(kr)
print("-----------------")
irow += nlc + 3
mc = []
for i in range(0, nlc):
    mc.append([])
    for j in range(irow, irow+ndk, 1):
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

wbx = xlsxwriter.Workbook("racking_result.xlsx")
sht = wbx.add_worksheet("racking_moment")

cell_format = wbx.add_format()
cell_format.set_align('center')
cell_format.set_num_format('0.000')
sht.set_column(0, 12, 12, cell_format)

align_left = wbx.add_format()
align_left.set_align('left')

align_right = wbx.add_format()
align_right.set_align('right')
align_right.set_num_format('0.000')

irow = 0
sht.write(irow, 0, 'Main Dimension'       , align_left )
irow += 1
sht.write(irow, 0, 'Length for Scantling', align_left)
sht.write(irow, 2, '(Ls)')
sht.write(irow, 3, Ls, align_right)
sht.write(irow, 4, 'm' )

irow += 1
sht.write(irow, 0, 'Moulded Breadth' , align_left)
sht.write(irow, 2, '(B)')
sht.write(irow, 3, B, align_right)
sht.write(irow, 4, 'm' )

irow += 1
sht.write(irow, 0, 'Moulded Depth' , align_left)
sht.write(irow, 2, '(Ds)')
sht.write(irow, 3, D, align_right)
sht.write(irow, 4, 'm' )

irow += 1
sht.write(irow, 0, 'Scantling Draft', align_left)
sht.write(irow, 2, '(Ts)')
sht.write(irow, 3, Ts, align_right)
sht.write(irow, 4, 'm' )

irow += 1
sht.write(irow, 0, 'Block Coefficient' , align_left)
sht.write(irow, 2, '(Cb)')
sht.write(irow, 3, Cb, align_right)

irow += 1
sht.write(irow, 0, 'Service Speed' , align_left)
sht.write(irow, 2, '(Vs)')
sht.write(irow, 3, Vs, align_right)
sht.write(irow, 4, 'kNot' )

irow += 1
sht.write(irow, 0, 'Acceleration parameter', align_left)
sht.write(irow, 2, '(a0)')
sht.write(irow, 3, a0, align_right)

irow += 1
sht.write(irow, 0, 'Sway Acceleration', align_left)
sht.write(irow, 2, '(a_sway)')
asway = sway_acceleration()
sht.write(irow, 3, asway, align_right)
sht.write(irow, 4, 'm/s^2' )

head_format = wbx.add_format()
head_format.set_bg_color('#A6C2E6')
head_format.set_align('center')

dot0_format = wbx.add_format({'num_format' : '0.'})
dot0_format.set_align('center')
dot1_format = wbx.add_format({'num_format' : '0.0'})
dot1_format.set_align('center')
dot2_format = wbx.add_format({'num_format' : '0.00'})
dot2_format.set_align('center')
dot3_format = wbx.add_format({'num_format' : '0.000'})
dot3_format.set_align('center')

irow += 2
sht.write( irow, 0, "LC", head_format)
sht.write( irow+1, 0, "", head_format)
sht.write( irow, 1, "GM", head_format)
sht.write( irow+1, 1, "(m)", head_format)
sht.write( irow, 2, "kr", head_format)
sht.write( irow+1, 2, "(m)", head_format)
sht.write( irow, 3, u"Tθ", head_format)
sht.write( irow+1, 3, "(sec)", head_format)
sht.write( irow, 4, u'θ', head_format)
sht.write( irow+1, 4, "(deg.)", head_format)
sht.write( irow, 5, "a_roll", head_format)
sht.write( irow+1, 5, "(rad/s^2)", head_format)
sht.write( irow, 6, "MR", head_format)
sht.write( irow+1, 6, "(kN-m)", head_format)

for lc in range(0,nlc):
    GM[lc] = max(GM[lc], 0.05*B)

Ttheta=[]
theta=[]
aroll = []
for lc in range(0,nlc):
    Ttheta_i, theta_i = roll_motion(GM[lc], kr[lc])
    Ttheta.append(Ttheta_i)
    theta.append(theta_i)
    aroll.append(roll_acceleration(GM[lc], kr[lc]))

MR = []
ay_env = []
for lc in range(0,nlc):
    ay_env.append([])
    for dk in range(0, ndk ):
        ay_env[lc].append(envelope_transverse_accelerations(TLC[lc], GM[lc], kr[lc], zi[dk]))
    
    MR.append(racking_moment(5, z_main, zi, mc[lc], ms, ay_env[lc]))

irow += 2
for lc in range(0,nlc):
    sht.write(irow, 0, LCn[lc])
    sht.write(irow, 1, GM[lc])
    sht.write(irow, 2, kr[lc])
    sht.write(irow, 3, theta[lc])
    sht.write(irow, 4, Ttheta[lc])
    sht.write(irow, 5, aroll[lc])
    sht.write(irow, 6, MR[lc], dot0_format)
    irow += 1

irow += 1
sht.write(irow, 0, 'ms(ton)', head_format)
for i in range(0, ndk):
    sht.write(irow, i+1, deck[i], head_format)
irow += 1
for dk in range(0,ndk):
    sht.write(irow, dk+1, ms[dk], dot2_format)

irow += 1
sht.write(irow, 0, 'mc(ton)', head_format)
for i in range(0, ndk):
    sht.write(irow, i+1, deck[i], head_format)

irow += 1
for lc in range(0, nlc):
    sht.write(irow, 0, LCn[lc])
    for dk in range(0, ndk):
        sht.write(irow, dk+1, mc[lc][dk], dot1_format)
    irow += 1

irow += 1
sht.write(irow, 0, 'ay_env(m/s^2)', head_format)
for i in range(0, ndk):
    sht.write(irow, i+1, deck[i], head_format)
irow += 1    
for lc in range(0, nlc):
    sht.write(irow, 0, LCn[lc])
    for dk in range(0, ndk):
        sht.write(irow, dk+1, ay_env[lc][dk])
    irow += 1

int_format = wbx.add_format({'num_format' : '#.'})

sht.write(irow, 7, MR[lc], int_format)    
for dk in range(0,ndk):
    sht.write(irow, dk+8, ay_env[lc][dk])
irow += 1

number_format = wbx.add_format({'num_format' : '0.000'})

cell_format = wbx.add_format()
cell_format.set_align('center')
cell_format.set_num_format('#.000')

irow += 1
for nlc in range(0, 12):
    sht.write(irow, 0, LCn[nlc])
    sht.write(irow, 1, GM[nlc])
    sht.write(irow, 2, kr[nlc])
    sht.write(irow, 3, MR[nlc], int_format)    
    for idk in range(0,ndk):
        sht.write(irow, idk+4, ay_env[nlc][idk])
    irow += 1

sht.write(irow,0,"Maximum")
sht.write(irow,1,"=MAX(B11:B22)")
sht.write(irow,2,"=MAX(C11:C22)")
sht.write(irow,3,"=MAX(D11:D22)",int_format)

irow += 1

irow += 1
for nlc in range(0,12):
    for ndk in range(0,8):
        sht.write(irow, ndk, mc[nlc][ndk])
    irow += 1

wbx.close()

