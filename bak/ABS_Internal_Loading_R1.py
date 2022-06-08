from math import *
from string import *
from Enviroment import *

g0 = 9.81

class PRINCIPAL_DATA:
    Ls,B,df,Cb, C1 = 164.9, 32.4, 12.6, 0.95, 9.18

class TANK_DATA:

    NO = []

    NO.append([[90.02, 18.341, 16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0]])
    NO[0].append([90.02, 18.9, 12.96, 20.64, 12.96, 18.9, 0., 0.559, 0.878 ])
    NO[0].append([90.02, 18.9, -12.96,  20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[0].append([90.02, 18.341, -16.2,  20.64, 3.24, 18.341, 0., 0.141, 1.0])
    
    NO.append([[110.66, 18.341, 16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0]])
    NO[1].append([110.66, 18.9, 12.96, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[1].append([110.66, 18.9, -12.96, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[1].append([110.66, 18.341, -16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0])
    
    NO.append([[131.31, 18.341, 16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0]])
    NO[2].append([131.31, 18.9, 12.96, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[2].append([131.31, 18.9, -12.96, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[2].append([131.31, 18.341, -16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0])


HULL = PRINCIPAL_DATA
TANK = TANK_DATA
LC = SLC
BETA = SBETA

#[ExcelFunction(Description = "kf for load(5A-3-2, 5.5.3)", Category = "ABS FPSO - Loads")]
def kf(kf0, mu, x0, lx):
    ReturnValue = kf0*(1-(1-cos(2*PI*(lx-x0)/HULL.Ls))*Cos(mu*PI/180))
    return ReturnValue

#[ExcelFunction(Description = "Distribution Factor(kl) for External Pressure", Category = "ABS FPSO - Loads")]
def kl(XLOC,  mu):
    Lx = XLOC / HULL.Ls

    if Lx >= 0 and Lx < 0.2:
        kl0 = -2.5 * Lx + 1.5
    elif Lx >= 0.2 and Lx <= 0.7:
        kl0 = 1.0
    elif Lx > 0.7 and Lx < 1.0:
        kl0 = 5 * Lx - 2.5
        
    ReturnValue = 1 + (kl0 - 1)* cos(radians(mu))

    return ReturnValue

#[ExcelFunction(Description = "Pitch Amplitude - phi", Category = "ABS FPSO - Loads")]
def Pitch_Amplitude(PMO):
    k1 = 1030.0
    phi = PMO*k1*pow(10/HULL.Cb,0.25)/HULL.Ls

    return phi

#[ExcelFunction(Description = "Roll Amplitude - theta", Category = "ABS FPSO - Loads")]
def Roll_Amplitude( Tr,  delta, di):
    CR = 1.05
    kq = 0.005
    Cdi = 1.06*(di/HULL.df)-0.06

    if Tr > 20:
        theta = CR*(35-kq*Cdi*delta/1000)

    elif Tr>=12.5 and Tr<=20.0:
        theta = CR*(35-kq*Cdi*delta/1000)*(1.5375-0.027*Tr)

    elif Tr<12.5:
        theta = CR*(35-kq*Cdi*delta/1000)*(0.8625+0.027*Tr)

    return theta

# [ExcelFunction(Description = "Pitch Natural Period - Tp", Category = "ABS FPSO - Loads")]
def Pitch_Period( di):
    k2 = 3.5
    Tp = k2*sqrt(HULL.Cb*di)
	
    return Tp

# [ExcelFunction(Description = "Roll Natural Period - Tr", Category = "ABS FPSO - Loads")]
def Roll_Period( kr,  GM):
    k4 = 2.0
    Tr = k4*kr/sqrt(GM)

    return Tr

def a0():
    ko = 1.34-0.47*HULL.Cb
    ReturnValue = ko*(2.4/sqrt(HULL.Ls) + 34./HULL.Ls - 600./pow(HULL.Ls,2))
    return ReturnValue

def Acceleration_Vertical(VAC, mu, XLOC, ZLOC):
    kv = sqrt(1+0.65*pow(5.3-45./HULL.Ls,2)*pow(XLOC/HULL.Ls-0.45, 2))
    Cv = cos(radians(mu))+(1+2.4*ZLOC/HULL.B)*sin(radians(mu))/kv
    av = Cv*VAC*kv*a0()*g0

    return av

def Acceleration_Longitudinal(LAC, YLOC):
    kl = 0.5+8*YLOC/HULL.Ls
    Cl = 0.35-0.0005*(HULL.Ls-200)
    al = Cl*LAC*kl*a0()*g0

    return al

def Acceleration_Transverse(TAC, XLOC, YLOC):

    kt = 0.35 + YLOC/HULL.B
    Ct = 1.27*sqrt(1+1.52*pow(XLOC/HULL.Ls-0.45,2))
    at = Ct*TAC*kt*a0()*g0

    return at

def Acceleration_Effective(Cdp, wv, wl, wt, tank_l, tank_b, tank_h, mu, av, al, at):
    ReturnValue = 0.71*Cdp*(wv*av + wl*(tank_l/tank_h)*al+wt*(tank_b/tank_h)*at)
    return ReturnValue

# [ExcelFunction(Description = "Added Pressure Head (Delta hi-1)", Category = "ABS FPSO - Loads")]
def Delta_hi_i( Cru,  b,  phi,  theta,  Cphi,  Ctheta,  xi,  zeta,  eta):
    thetae = 0.71*Ctheta*theta
    phie = 0.71*Cphi*phi
    zetae = b - zeta
    etae = eta

    # print 'i=', thetae, phie, zetae, etae, zeta, eta, b
    dh = xi*sin(-radians(phie))+Cru*(zetae*sin(radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-zeta)

    return dh

# [ExcelFunction(Description = "Added Pressure Head (Delta hi-2)", Category = "ABS FPSO - Loads")]
def Delta_hi_ii( Cru,  l,  delta_b,  delta_h,  phi,  theta,  Cphi,  Ctheta,  xi,  zeta,  eta):

    thetae = 0.71*Ctheta*theta
    phie = 0.71*Cphi*phi
    zetae = zeta-delta_b
    etae = eta-delta_h

    # print 'ii =', thetae, phie, zetae, etae
    dh = (l-xi)*sin(radians(phie))+Cru*(zetae*sin(-radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-zeta)

    return dh

def effective_ai(NLC, NTK, wlx, wtx, ZL, XL, YL):

    # For Rectangur Tank : Cdp = 1.0, Cru = 1.0
    Cdp = 1.0
    
    av=Acceleration_Vertical(BETA['VAC'],LC['mu'][NLC],XL, ZL)
    al=Acceleration_Longitudinal(BETA['LAC'],YL)
    at=Acceleration_Transverse(BETA['TAC'],XL, YL)

    if wlx == 0:
        wl = LC['wla'][NLC]
    elif wlx == 1:
        wl = LC['wlf'][NLC]

    if wtx == 0:
        wt = LC['wts'][NLC]
    elif wtx == 1:
        wt = LC['wtp'][NLC]
        
    ai = Acceleration_Effective(Cdp, LC['wv'][NLC], wl , wt, TANK.NO[NTK[0]][NTK[1]][3], TANK.NO[NTK[0]][NTK[1]][4],TANK.NO[NTK[0]][NTK[1]][5], LC['mu'][NLC] , av, al, at)

    return ai

def Delta_h(NLC, NTK, phi, theta, ZL, XL, YL):

    # For Rectangur Tank : Cdp = 1.0, Cru = 1.0
    Cru = 1.0

    # print XL, NTK[0], NTK[1], TANK.NO[NTK[0]][NTK[1]][0], TANK.NO[0][0][0]
    
    xi = XL - TANK.NO[NTK[0]][NTK[1]][0]
    zeta = TANK.NO[NTK[0]][NTK[1]][2]-ZL
    eta = TANK.NO[NTK[0]][NTK[1]][1]- YL

    # print xi, zeta, eta
    
    if LC['Pitch'][NLC] == 'D' or LC['Roll'][NLC] == 'D':
        DH = Delta_hi_i( Cru,  TANK.NO[NTK[0]][NTK[1]][4],  phi,  theta,  LC['Cpitch'][NLC],  LC['Croll'][NLC],  xi,  zeta,  eta)
    elif LC['Pitch'][NLC] == 'U' or LC['Roll'][NLC] == 'U':
        DH = Delta_hi_ii( Cru, TANK.NO[NTK[0]][NTK[1]][3],  TANK.NO[NTK[0]][NTK[1]][6],  TANK.NO[NTK[0]][NTK[1]][7],  phi,  theta,  LC['Cpitch'][NLC],  LC['Croll'][NLC],  xi,  zeta,  eta)
    else:
        DH = 0

    return DH
        
def run():

    ku = 1.0
    
    ZLOC = [[16.2, 12.96],[12.96, 0],[0, -12.96],[-12.96, -16.2]]
    XLOC = [[90.02, 110.66],[110.66, 131.3],[131.3, 151.94]]
    YLOC = [0, 1.8, 18.2]

    phi = Pitch_Amplitude(BETA['PMO'])
    theta = 19.53

    fout = open('load.res', 'w')
    fses = open('load.ses', 'w')
    for NLC in range(0,10):
        LCN = NLC + 1
        print LCN
        fout.write('%d \n' % LCN)
        pix = '['
        for idz in range(0, 4):
            wtx = 0
            pix = '['
            for ZL in ZLOC[idz]:
                for idx in range(0,3):
                    wlx = 0
                    pix = pix + '['
                    for XL in XLOC[idx]:
                        pix = pix + '['
                        for YL in YLOC:
                            ai = effective_ai(NLC, [idx,idz], wlx, wtx, ZL,XL, YL)
                            dh = Delta_h(NLC, [idx,idz], phi, theta, ZL,XL, YL)
                            eta = TANK.NO[idx][idz][1]- YL
                            hd = (eta*ai/g0 + dh)
                            # hd = LC['kc_pi'][NLC]*(eta*ai/g0 + dh)
                            
                            ps = 1.025*9.81*eta
                            pd = 1.025*9.81*ku*hd
                            p0 = 48.4 # kN/m^2

                            ks = TANK.NO[idx][idz][8]

                            pi = ks*(ps + pd) + p0

                            pix = pix + ' %8.1f ' % pi

                            # print ZL, XL, YL, ai, dh, hd, ps, pd, pi

                            fout.write('%8.3f %8.3f %8.3f %8.1f %8.1f %8.1f \n' % (ZL, XL, YL, ps, pd, pi))
                        wlx += 1
                        pix = pix + ']'
                    pix = pix + ']'
                wtx += 1
            pix = pix + ']'
            print pix

            field_name = '"LC.%d_TANK_%d%d"' % (LCN, idx, idz)
            p3_field = 'fields_create( ' + field_name + ', "Spatial", 1, "Scalar", "Real", "Coord 10", "", "Table", 3, "X", "Y", "Z", "", "", "", FALSE,'
            XTable = '[ %f,%f ]' % (XLOC[idx][0],XLOC[idx][1])
            ZTable = '[ %f,%f ]' % (ZLOC[idz][0],ZLOC[idz][1])
            YTable = '[ %f,%f,%f ]' % (YLOC[0],YLOC[1],YLOC[2])
            
            p3_field = p3_field + XTable + ',' + ZTable +','+ YTable +',' + pix + ') \n'

            fses.write(p3_field)

    fses.close()
    fout.close()        
    
# fields_create( "I_EX_LC31", "Spatial", 1, "Scalar", "Real", "Coord 4", "", "Table", 3, "X", "Y", "Z", "", "", "", FALSE,
# [-16200., 0., 16200.], [0., 1273., 11340., 13786.], [83140., 115430., 164900.],
#[[[0.117294, 0.103734, 0.114027][0.104517, 0.090859003, 0.101226][0.0082280003, 0., 0.][0., 0., 0.]][[0.117263, 0.103833, 0.114027][0.10449, 0.090945996, 0.101226][0.0081590004, 0., 0.]
#[0., 0., 0.]][[0.117232, 0.103932, 0.114027][0.104462, 0.091032997, 0.101226][0.0080899997, 0., 0.][0., 0., 0.]]] )

def table_to_patran():

    f = open('load.res', 'r')

    loadcase = []
    XDAT = []
    XL, ZL, YL, ps, pd, pi = [], [], [], [],[], []
    while 1:
        readline = f.readline()
        if len(readline) <=0: break
        
        loadcase.append(readline)
        for idx in range(0, 6):
            XL.append([])
            ZL.append([])
            YL.append([])
            ps.append([])
            pd.append([])
            pi.append([])
            
            for idz in range(0, 24):
                readline = f.readline()
                XDAT = split(readline)
                XL[idx].append(XDAT[0])
                ZL[idx].append(XDAT[1])
                YL[idx].append(XDAT[2])
                ps[idx].append(XDAT[3])
                pd[idx].append(XDAT[4])
                pi[idx].append(XDAT[5])

        
    for idx in range(0,6):
        XTable = '[ %f,%f ]' % (atof(XL[idx][0]),atof(XL[idx+1][0]))
        print XTable
#        for idz in range(0,6):

run()


    








