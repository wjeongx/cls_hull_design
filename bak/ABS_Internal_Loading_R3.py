from math import *
from string import *
from Enviroment import *
from IACS import *
import json
# from ABS_External_Pressure import *

g0 = 9.81

class PRINCIPAL_DATA:
    Ls,B,D,df,Cb, C1 = 164.9, 32.4, 18.2, 12.6, 0.95, 9.18

class TANK_DATA:

    NO = []

    NO.append([[90.02, 18.341, 16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0]])
    NO[0].append([90.02, 18.9, 16.2, 20.64, 12.96, 18.9, 0., 0.559, 0.878 ])
    NO[0].append([90.02, 18.9, -16.2,  20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[0].append([90.02, 18.341, -16.2,  20.64, 3.24, 18.341, 0., 0.141, 1.0])
    
    NO.append([[110.66, 18.341, 16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0]])
    NO[1].append([110.66, 18.9, 16.2, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[1].append([110.66, 18.9, -16.2, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[1].append([110.66, 18.341, -16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0])
    
    NO.append([[131.31, 18.341, 16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0]])
    NO[2].append([131.31, 18.9, 16.2, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[2].append([131.31, 18.9, -16.2, 20.64, 12.96, 18.9, 0., 0.559, 0.878])
    NO[2].append([131.31, 18.341, -16.2, 20.64, 3.24, 18.341, 0., 0.141, 1.0])

HULL = PRINCIPAL_DATA
TANK = TANK_DATA
LC = SLC
BETA = SBETA

def LinearInterpolation(x1,x2,y1,y2,x):
    Value = y1 - (x1 - x) * (y1 - y2) / (x1 - x2)
    return Value

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
    dh = (l-xi)*sin(radians(phie))+ Cru*(zetae*sin(-radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-zeta)

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
        wt = LC['wtp'][NLC]
    elif wtx == 1:
        wt = LC['wts'][NLC]

    ai = Acceleration_Effective(Cdp, LC['wv'][NLC], wl , wt, TANK.NO[NTK[0]][NTK[1]][3], TANK.NO[NTK[0]][NTK[1]][4],TANK.NO[NTK[0]][NTK[1]][5], LC['mu'][NLC] , av, al, at)

    return ai

def Delta_h(NLC, NTK, phi, theta, ZL, XL, YL):

    # For Rectangur Tank : Cdp = 1.0, Cru = 1.0
    Cru = 1.0

    # print XL, NTK[0], NTK[1], TANK.NO[NTK[0]][NTK[1]][0], TANK.NO[0][0][0]
    
    xi = XL - TANK.NO[NTK[0]][NTK[1]][0]
    zeta = abs(TANK.NO[NTK[0]][NTK[1]][2]-ZL)
    eta = TANK.NO[NTK[0]][NTK[1]][1]- YL

    # print xi, zeta, eta, '\n'
    
    if LC['Pitch'][NLC] == 'D' and LC['Roll'][NLC] == 'D':
        DH = Delta_hi_i( Cru,  TANK.NO[NTK[0]][NTK[1]][4],  phi,  theta,  LC['Cpitch'][NLC],  LC['Croll'][NLC],  xi,  zeta,  eta)
    elif LC['Pitch'][NLC] == 'U' and LC['Roll'][NLC] == 'U':
        DH = Delta_hi_ii( Cru, TANK.NO[NTK[0]][NTK[1]][3],  TANK.NO[NTK[0]][NTK[1]][6],  TANK.NO[NTK[0]][NTK[1]][7],  phi,  theta,  LC['Cpitch'][NLC],  LC['Croll'][NLC],  xi,  zeta,  eta)
    else:
        DH = 0

    return DH
        
def ABSFPI_InternalPressure():

    ku = 1.0

    ZLOC = [[12.96, 16.2],[0.0, 12.96],[-12.96, 0.0],[-16.2, -12.96]]
    XLOC = [[90.02, 110.66],[110.66, 131.3],[131.3, 151.94]]
    YLOC = [0.0, 1.8, 18.2]

    phi = Pitch_Amplitude(BETA['PMO'])
    theta = 19.53

    fout = open('pi2_std.res', 'w')

    for NLC in range(0,2):
        LCN = NLC + 1
        print LCN
        fout.write('LCS.1%d \n' % LCN)
        for idz in range(0,4):
            for idx in range(0,3):
                wlx = 0
                for XL in XLOC[idx]:
                    for YL in YLOC:
                        wtx = 0
                        for ZL in ZLOC[idz]:
                            ai = effective_ai(NLC, [idx,idz], wlx, wtx, ZL,XL, YL)
                            dh = Delta_h(NLC, [idx,idz], phi, theta, ZL,XL, YL)
                            eta = TANK.NO[idx][idz][1]- YL
                            # hd = (eta*ai/g0 + dh)
                            hd = LC['kc_pi'][NLC]*(eta*ai/g0 + dh)
                            
                            ps = 1.025*9.81*eta
                            pd = 1.025*9.81*ku*hd
                            p0 = 48.4 # kN/m^2

                            ks = TANK.NO[idx][idz][8]

                            pi = ks*(ps + pd) + p0

                            if pi < 0:
                                pi = 0.0
                                eta0 = -(hd + 4.813/ks)
                                YL = TANK.NO[idx][idz][1] - eta0 

                            # print XL, ZL, YL  #, ai, dh, hd, ps, pd, pi

                            fout.write('%8.3f %8.3f %8.3f %8.1f %8.1f %8.1f\n' % (XL, YL, ZL, ps, pd, pi))
                            wtx += 1
                    wlx += 1

    fout.close()

    print 'Process Complete'
    
def table_to_field():

    ZLOC = [[12960., 16200.],[0., 12960.],[-12960., 0.],[-16200., -12960.]]
    XLOC = [[0., 20640.],[20640, 41280.],[41280., 61920]]
    YLOC = [0., 1800., 18200.]
    
    f = open('pi2_std.res', 'r')
    fw = open('pi2_std.ses', 'w')

    lcname = []
    while 1:
        readline = f.readline()
        if len(readline) <=0: break

        lcname = strip(readline[:-1])

        idx = 0
        for i in range(0,3):
            for j in range(0,4):
                idx += 1
                field_name = '"%s_TANK_%d"' % (lcname, idx )
                p3_field = 'fields_create( ' + field_name + ', "Spatial", 1, "Scalar", "Real", "Coord 5", "", "Table", 3, "X", "Y", "Z", "", "", "", FALSE, '

                pix = []
                pdx = []
                a = []
                for idu in range(0,2):
                    pix.append([])
                    pdx.append([])
                    for idv in range(0, 3):
                        pix[idu].append([])
                        pdx[idu].append([])
                        for idw in range(0, 2):
                            readline = f.readline()
                            a_dat = split(readline)

                            XL,ZL,YL, ps, pd, pdi = atof(a_dat[0]),atof(a_dat[1]),atof(a_dat[2]),atof(a_dat[3]),atof(a_dat[4]), atof(a_dat[5])
                            
                            pix[idu][idv].append(pdi/1000.)
                            pdx[idu][idv].append(pd/1000.)

                # p3_field = p3_field + json.dumps(XLOC[i]) + ',' + json.dumps(YLOC) + ',' + json.dumps(ZLOC[j]) + ',' + json.dumps(pix)
                p3_field = p3_field + json.dumps(XLOC[i]) + ',' + json.dumps(YLOC) + ',' + json.dumps(ZLOC[j]) + ', @ \n' + json.dumps(pdx)
                fw.write(p3_field + ')' '\n')
                #print p3_field

    fw.close()
    f.close()

    print 'Process Complete'

                    
def Hull_Girder_Loads():

    XDIST = { 0:0, 0.3:49.47,0.5:82.45,0.7:115.43,1:164.9} 
#    SWBMH = { 0:0, 0.3:1422450, 0.5:1422450, 0.7:1422450, 1:0.}
#    SWBMS = { 0:0, 0.3:-1304730, 0.5:-1304730, 0.7:-1304730, 1:0.}

    SWBMH = { 0:0, 0.3:990810, 0.5:990810, 0.7:990810, 1:0.}
    SWBMS = { 0:0, 0.3:-2256300, 0.5:-2256300, 0.7:-2256300, 1:0.}

    f = open('RHullGirder.res', 'w')
    
    XLOC = [82.45, 110.66]
    print BETA['VBM']

    for idx in range(0, 10):
        if LC['VBM'][idx] < 0:
            for x in XLOC:
                if x > XDIST[0] and x < XDIST[0.3]:
                    SWBM = LinearInterpolation(XDIST[0],XDIST[0.3],SWBMS[0],SWBMS[0.3],x)
                elif x > XDIST[0.3] and x < XDIST[0.7]:
                    SWBM = SWBMS[0.5]
                elif x > XDIST[0.7] and x < XDIST[1]:
                    SWBM = LinearInterpolation(XDIST[0.7],XDIST[1],SWBMS[0.7],SWBMS[1],x)
                
                VBM = Mws(BETA['VBM'], HULL.Ls, HULL.B, HULL.Cb, x)
                XVBM = LC['kc_vbm'][idx]*VBM
                TBM = XVBM + SWBM
                f.write('%10.3f  %15.0f  %15.0f  %15.0f \n' % (x, SWBM, XVBM, TBM))
                
        elif LC['VBM'][idx] > 0:
            for x in XLOC:
                if x > XDIST[0] and x < XDIST[0.3]:
                    SWBM = LinearInterpolation(XDIST[0],XDIST[0.3],SWBMH[0],SWBMH[0.3],x)
                elif x > XDIST[0.3] and x < XDIST[0.7]:
                    SWBM = SWBMH[0.5]
                elif x > XDIST[0.7] and x < XDIST[1]:
                    SWBM = LinearInterpolation(XDIST[0.7],XDIST[1],SWBMH[0.7],SWBMH[1],x)
                    
                VBM = Mwh(BETA['VBM'], HULL.Ls, HULL.B, HULL.Cb, x)
                XVBM = LC['kc_vbm'][idx]*VBM
                TBM = XVBM + SWBM

                f.write('%10.3f  %15.0f %15.0f %15.0f \n' % (x, SWBM, XVBM, TBM))
        print LC['kc_vbm'][idx]
        
    f.close()
    print 'Process Complete'
    
def run_external():
    run_ext_pressure(HULL.Ls, HULL.B, HULL.D)
    
def run():

    print '========================================================================'
    print '    1 - Internal Pressure (ABS, FPI)'
    print '    2 - Hull Girder Loads'
    print '    3 - Internal Pressure Table to Patran Field'
    print '    4 - Considered Point Load'
    print '    5 - External Pressure'
    print '========================================================================'
    
    ExecKey = raw_input('key number for exec. : ')
    print ExecKey

    if atoi(ExecKey) == 1:
        ABSFPI_InternalPressure()

    if atoi(ExecKey) == 2:
        Hull_Girder_Loads()

    if atoi(ExecKey) == 3:
        table_to_field()

    if atoi(ExecKey) == 4:
        ConsideredPointLoad()

    if atoi(ExecKey) == 5:
        run_external()
        
run()

    








