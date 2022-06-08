from math import *
from string import *

g0 = 9.81

Ls,B,D,df,Cb, C1 = 164.9, 32.4, 18.2, 12.6, 0.95, 9.18
tkl, tkb,tkh = 20.64, 12.96, 18.9
ku = 1.0
Cdp = 1.0
Cru = 1.0

phi = 8.607
theta = 19.53
    
VAC = 0.843
LAC = 0.699
TAC = 0.595

kc = [0.4,0.4,1.0,0.5,1.0,0.5,1.0,0.5,0.0,0.0]
wv = [0.75,-0.75,0.75,-0.75,0.25,-0.25,0.4,-0.4,0.0,0.0]
wlf = [0.25,-0.25,0.25,-0.25,0.0,0.0,0.2,-0.2,0.0,0.0]
wla = [-0.25,0.25,-0.25,0.25,0.0,0.0,-0.2,0.2,0.0,0.0]
wtp = [0.0,0.0,0.0,0.0,-0.75,0.75,-0.4,0.4,0.0,0.0]
wts = [0.0,0.0,0.0,0.0,0.75,-0.75,0.4,-0.4,0.0,0.0]
CP = [-1.0,1.0,-1.0,1.0,0.0,0.0,-0.7,0.7,0.0,0.0]
CR = [0.0,0.0,0.0,0.0,1.0,-1.0,0.7,-0.7,0.0,0.0]
mu = [0,0,0,0,90,90,60,60,0.0,0.0]
Heave = ['D','U','D','U','D','U','D','U','','']
Pitch = ['D','U','D','U','','','D','U','','']
Roll = ['','','','','D','U','D','U','','']

LOC = [91.89, 0, 0.405]
Ref = [0, 18.9, 16.2]
xi = 0.0
zeta = Ref[2] - LOC[2]
eta = Ref[1] - LOC[1]

def LinearInterpolation(x1,x2,y1,y2,x):
    Value = y1 - (x1 - x) * (y1 - y2) / (x1 - x2)
    return Value

def Eff_Acc():

    hd = []
    for idx in range(0,10):

        k0 = 1.34-0.47*Cb
        a0 = k0*(2.4/sqrt(Ls) + 34./Ls - 600./pow(Ls,2))

        kv = sqrt(1+0.65*pow(5.3-45./Ls,2)*pow(LOC[0]/Ls-0.45, 2))
        Cv = cos(radians(mu[idx]))+(1+2.4*LOC[2]/B)*sin(radians(mu[idx]))/kv
        av = Cv*VAC*kv*a0*g0

        kl = 0.5+8*LOC[1]/Ls
        Cl = 0.35-0.0005*(Ls-200)
        al = Cl*LAC*kl*a0*g0

        kt = 0.35 + LOC[1]/B
        Ct = 1.27*sqrt(1+1.52*pow(LOC[0]/Ls-0.45,2))
        at = Ct*TAC*kt*a0*g0

        wl = LinearInterpolation(0,tkl,wla[idx],wlf[idx],LOC[0]-90.02)

        if LOC[2] >= 0:
            wt = LinearInterpolation(0, 16.2,wtp[idx],wts[idx],LOC[2])
        elif LOC[2] < 0:
            wt = LinearInterpolation(-16.2,0,wts[idx],wtp[idx],LOC[2])

        ai = 0.71*Cdp*(wv[idx]*av + wl*(tkl/tkh)*al+wt*(tkb/tkh)*at)

        hd.append(kc[idx]*eta*ai/g0)
        
        print 'LC.%d' % (idx+1)
        print '==========================================================================='
        print '%10.3f %10.3f %10.3f %10.3f %10.3f' % (ai, av, al, at, hd[idx])

    return hd

def DeltaH():

    hd = []
    for idx in range(0,10):
        thetae = 0.71*CR[idx]*theta
        phie = 0.71*CP[idx]*phi

        if Pitch[idx] == 'D' and Roll[idx] == 'D':
            zetae = tkb - zeta
            etae = eta
            dh = xi*sin(radians(-phie)) + Cru*(zetae*sin(radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-eta)
            
        elif Pitch[idx] == 'U' and Roll[idx] == 'U':
            zetae = zeta - 0.0
            etae = eta - 0.7
            dh = (tkl-xi)*sin(radians(phie))+ Cru*(zetae*sin(-radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-eta)
        else:
            zetae = 0.0
            etae = 0.0
            dh = 0.0
            

        hd.append(kc[idx]*dh)

        print 'LC.%d' % (idx+1)
        print "theta, phi, zeta, eta, thetae, phie, zetae, etae  hd"
        print "%10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f " % (theta, phi, zeta, eta, thetae, phie, zetae, etae, hd[idx])

    return hd


hd1 = Eff_Acc()
hd2 = DeltaH()

for idx in range(0,10):
    print idx+1, 0.878*1.025*9.81*(hd1[idx]+hd2[idx]+eta)

    
