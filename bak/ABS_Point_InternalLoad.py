from math import *
from string import *
from Enviroment import *
from IACS import *
import json
from ABS_External_Pressure import *

g0 = 9.81

def run():

    Ls,B,D,df,Cb, C1 = 164.9, 32.4, 18.2, 12.6, 0.95, 9.18
    
    ku = 1.0

    LOC = [90.370, 0, 14.040]

    phi = 8.607
    theta = 19.53
    mu = 60

    k0 = 1.34-0.47*Cb
    a0 = k0*(2.4/sqrt(Ls) + 34./Ls - 600./pow(Ls,2)

    print k0, a0
       
#    kv = sqrt(1+0.65*pow(5.3-45./Ls,2)*pow(XLOC/Ls-0.45, 2))
#    Cv = cos(radians(mu))+(1+2.4*ZLOC/B)*sin(radians(mu))/kv
#    av = Cv*VAC*kv*a0()*g0

#    print k0, a0, kv, Cv, av

#    kl = 0.5+8*YLOC/Ls
#    Cl = 0.35-0.0005*(Ls-200)
#    al = Cl*LAC*kl*a0()*g0

#    kt = 0.35 + YLOC/HULL.B
#    Ct = 1.27*sqrt(1+1.52*pow(XLOC/Ls-0.45,2))
#    at = Ct*TAC*kt*a0()*g0

#    ai = 0.71*Cdp*(wv*av + wl*(tank_l/tank_h)*al+wt*(tank_b/tank_h)*at)

#    dh = Delta_h(NLC, [idx,idz], phi, theta, ZL,XL, YL)
#    eta = TANK.NO[idx][idz][1]- YL
    # hd = (eta*ai/g0 + dh)
#    hd = LC['kc_pi'][NLC]*(eta*ai/g0 + dh)
                            
#    ps = 1.025*9.81*eta
#    pd = 1.025*9.81*ku*hd
#    p0 = 48.4 # kN/m^2

#   ks = 1.0

#  pi = ks*(ps + pd) + p0

# if pi < 0:
#    pi = 0.0


#    print 'Process Complete'
        
run()

    








