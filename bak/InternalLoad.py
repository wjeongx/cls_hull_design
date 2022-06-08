from math import *
from string import *

g0 = 9.81

def InternalLoad():

    Ls,B,D,df,Cb, C1 = 164.9, 32.4, 18.2, 12.6, 0.95, 9.18
    
    ku = 1.0
    
    LOC = [90.37, 0, 14.040]

    phi = 8.607
    theta = 19.53
    mu = 60
    VAC = 0.843
    LAC = 0.699
    TAC = 0.595

    CP, CR = -0.7, 0.7
    xi = 0.35
    zeta = 2.16
    eta = 18.341
    wl, wt, wv = -0.2, 0.0, 0.4
    tkl, tkb,tkh = 20.64, 3.24, 18.341

    Cdp = 1.0
    Cru = 1

    
    k0 = 1.34-0.47*Cb
    a0 = k0*(2.4/sqrt(Ls) + 34./Ls - 600./pow(Ls,2))

    kv = sqrt(1+0.65*pow(5.3-45./Ls,2)*pow(LOC[0]/Ls-0.45, 2))
    Cv = cos(radians(mu))+(1+2.4*LOC[2]/B)*sin(radians(mu))/kv
    av = Cv*VAC*kv*a0*g0

    print "k0, a0, kv, Cv, av"
    print "%10.3f %10.3f %10.3f %10.3f %10.3f " % (k0, a0, kv, Cv, av)

    kl = 0.5+8*LOC[1]/Ls
    Cl = 0.35-0.0005*(Ls-200)
    al = Cl*LAC*kl*a0*g0

    print "kl, Cl, al"
    print "%10.3f %10.3f %10.3f " % (kl, Cl, al)

    kt = 0.35 + LOC[1]/B
    Ct = 1.27*sqrt(1+1.52*pow(LOC[0]/Ls-0.45,2))
    at = Ct*TAC*kt*a0*g0

    ai = 0.71*Cdp*(wv*av + wl*(tkl/tkh)*al+wt*(tkb/tkh)*at)
    print "kt, Ct, at, ai"
    print "%10.3f %10.3f %10.3f %10.3f" % (kt, Ct, at, ai)


    thetae = 0.71*CR*theta
    phie = 0.71*CP*phi
    zetae = tkb - zeta
    etae = eta
    
    dh = xi*sin(-phie) + Cru*(zetae*sin(thetae)*cos(phie)+etae*cos(thetae)*cos(phie)-zeta)

    print "theta, phi, zeta, eta, thetae, phie, zetae, etae, dh"
    print "%10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f" % (theta, phi, zeta, eta, thetae, phie, zetae, etae, dh)

    
    hd = 1.0*(eta*ai/g0 + dh)
    ks = 1.0
    pi = ks*0.1025*9.81*(eta + ku*hd) + 4.84

    print "hd, ks, pi"
    print "%10.3f %10.3f %10.3f" % (hd, ks, pi)
        
        

InternalLoad()


    
