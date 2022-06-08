from IACS import *
from math import *
from nvs_math import *
from FPI_Factors import *

def aceleration_a0:
    a0 = k0*(2.4/math.pow(L,0.5)+34/L-600.0/math.pow(L,0.5))

def Eff_Acceleration():
    ks = 1.0
    ku = 1.0
    kc = 1.0
    Cdp = 0.7
    
    ai = 0.71*Cdp*(wv[1]*av+Wl_FBHD[1]*(l/h)*al+Wt_PBHD[1]*(b/h)*at)


def InternalPressure():
    cargo_density = 1.025
    gravity = 9.81
    
    
    
    #a = 18.2
    #kc = 1.0
    
    #hd = kc*(a*ai/gravity + delta_hi)

    pvp = 6.9
    pn = 2.06
    p0 = (pvp - pn)*10
    
    if(p0 < 0):
        p0= 0.0

    print p0
    
    eta = 18.9
    pi = ks*cargo_density*gravity*(eta + ku*hd) + p0
    
InternalPressure()
