from IACS import *
from math import *
from string import *
from Enviroment import *

g0 = 9.81

LC = SLC
BETA = SBETA

def LinearInterpolation(x1,x2,y1,y2,x):
    Value = y1 - (x1 - x) * (y1 - y2) / (x1 - x2)
    return Value

#[ExcelFunction(Description = "kf for load(5A-3-2, 5.5.3)", Category = "ABS FPSO - Loads")]
def factor_kf(Ls, kf0, mu, x0, lx):
    ReturnValue = kf0*(1-(1-cos(2*pi*(lx-x0)/Ls))*cos(mu*pi/180))
    return ReturnValue

#[ExcelFunction(Description = "Distribution Factor(kl) for External Pressure", Category = "ABS FPSO - Loads")]
def factor_kl(Ls, XLOC,  mu):
    Lx = XLOC / Ls

    if Lx >= 0 and Lx < 0.2:
        kl0 = -2.5 * Lx + 1.5
    elif Lx >= 0.2 and Lx <= 0.7:
        kl0 = 1.0
    elif Lx > 0.7 and Lx < 1.0:
        kl0 = 5 * Lx - 2.5
        
    ReturnValue = 1 + (kl0 - 1)* cos(radians(mu))

    return ReturnValue

def alpha_i(B, Ts, BR, mu, YL, ZL):
    a1 = 1.0 - 0.25 * cos(radians(mu))
    a2 = 0.4 - 0.10 * cos(radians(mu))
    a3 = 0.3 - 0.20 * sin(radians(mu))
    a4 = 2 * a3 - a2
    a5 = 0.75 - 1.25 * sin(radians(mu))

    hd1Y = Ts
    hd2Y = BR - sqrt(pow(BR,2)/2)
    hd2Z = B/2 - BR + sqrt(pow(BR,2)/2)
    hd3Z = 0.0
    hd4Z = -(B/2 - BR + sqrt(pow(BR,2)/2))
    hd4Y = BR - sqrt(pow(BR,2)/2)
    hd5Y = Ts

    # print 'hd1Y,  hd2Y, hd2Z, hd3Z, hd4Z, hd4Y, hd5Y'
    # print '%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % (hd1Y,  hd2Y, hd2Z, hd3Z, hd4Z, hd4Y, hd5Y)
    ai = 0.
    
    if YL >= hd2Y or YL >= hd4Y:
        if ZL >= hd2Z:
            ai = LinearInterpolation(hd1Y,hd2Y,a1,a2,YL)
        elif ZL <= hd4Z:
            ai = LinearInterpolation(hd4Y,hd5Y,a4,a5,YL)
    elif YL < hd2Y or YL < hd4Y:
        if ZL < hd2Z and ZL >= hd3Z:
            ai = LinearInterpolation(hd2Z,hd3Z,a2,a3,ZL)
        elif ZL < hd3Z and ZL > hd4Z:
            ai = LinearInterpolation(hd3Z,hd4Z,a3,a4,ZL)
            
    return ai

def dyna_pressure_head(Ls, B, di, BR, mu, XL, YL, ZL):
    kl = factor_kl(Ls, XL,  mu)
    ai = alpha_i(B, di, BR, mu, YL, ZL)
    hd0 = 1.36*Cw(Ls)
    hdi = kl*ai*hd0

    return hdi

def ExternalPressure(f, Ls, B, di, BR, NLC, XL0, XL, YL, ZL):

    # hydrostatic pressure
    hs = di - YL
    ps = 1.025 * g0 * hs

    if ZL >= 0:
        ESF = BETA['EPS']
    else:
        ESF = BETA['EPP']
             
    mu = LC['mu'][NLC]

    kf0 = LC['kf0'][NLC]
    kf = factor_kf(Ls, kf0, mu, XL0, XL)

    hdi = dyna_pressure_head(Ls, B, di, BR, mu, XL, YL, ZL)

    kc = LC['kc_pe'][NLC]
    hde = kc * hdi
    ku = 1.

    pd = 1.025*g0*ESF*kf*ku*hde
    pe = ps + pd

    #print 'di, hd0, kc, mu, kf0, kl'
    #print '%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % (di, hd0, kc, mu, kf0, kl)
    #print 'hs, ps, ai, ESF, hdi, hde, kf, pd, pe'
    # print '%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % (hs, ps, ai, ESF, hdi, hde, kf, pd, pe)
    f.write('%8.0f , %8.0f , %8.0f , %8.4f \n' % (YL*1000, ZL*1000, XL*1000, pe/1000))

#    if y == -Bmld/2:
#        if z <= Ts and z > 1.8:
#            ai =  a2-(a2-a1)*(1.8-z)/(1.8-Ts)
#    elif y 
    
#x1 = 164.9/2.

def run_ext_pressure(Ls, B, D):
    BR = 1.8;
    XL0 = 131.3
    XLOC = [83.14,90.02,100.34,110.66,120.98,131.3,151.94]
    #XLOC = [90.02]
    ZLOC = [-16.2, -15.673, 0, 15.673, 16.2]

    for idx in range(0,10):
        fcsv = 'ext_load_' + 'LC.%d' % (idx+1) + '.csv'
        f = open(fcsv, 'w')
        
        df = LC['df'][idx]
        mu = LC['mu'][idx]

        YLOC = [0, 0.527]
        YLOC.append(df)
        for XL in XLOC:
            kf0 = LC['kf0'][idx]
            kf = factor_kf(Ls, kf0, mu, XL0, XL)
            h1 = D - df
            hd1 = dyna_pressure_head(Ls, B, df, BR, LC['mu'][idx], XL, df, B/2)
            h2 = kf*hd1

            h0 = min(h1, h2)

            if h0 < 0.:
                YLOC.append(df + h0)

            for ZL in ZLOC:
                YLOC.sort()

        for XL in XLOC:
            for ZL in ZLOC:
                for YL in YLOC:
                    ExternalPressure(f, Ls, B, df, BR, idx, XL0, XL, YL, ZL)                

        f.close()












