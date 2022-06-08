from IACS import *
from math import *
from Enviroment import *
from nvs_math import *

Ls = 164.9
Bmld = 32.4
Ts = 12.6

def ExternalPressure(xp, yp, zp):
    sea_density = 1.025
    gravity = 9.81

    # hydrostatic pressure
    hs = Ts - zp

    ps = sea_density * gravity * hs
    
    # ============================
    
    # beta = BETA1['EPP'] # for EPP
    beta = BETA1['EPS'] # for EPS
    ku = 1.  # for load factor

    # hydrodynamic pressure head induced by the wave
    k = 1.0
    C1 = Cw(164.9)
    hdo = 1.36*k*C1
    

    heading_angle = [0.,30.,60.,90.]
    xr = xp/Ls
    for wave_angle in heading_angle:
        alpha = 0.3-0.20* sin(wave_angle*pi/180.)
        if(xr < 0.2):
            kl0 = LinearInterpolation(0.0,0.2,1.5,1.0,xr)
        elif(xr >= 0.2 and xr <= 0.7):
            kl0 = 1.0
        elif(xr > 0.7):
            kl0 = LinearInterpolation(0.7,1.0,1.0,2.5,xr)

        kl = 1+(kl0-1)*cos(wave_angle*pi/180.)

        hdi = kl*alpha*hdo

        kc = 1.0
        hde = kc*hdi

        print "====================================================="
        print "wave heading angle :", wave_angle ,"deg", wave_angle*pi/180., "radian"
        # parameter
        
        print " ===== parameter ========"
        print "kc = ", kc
        print "hde = ", hde
        print "hdo = ", hdo
        print "ai = ", alpha
        print "kl = ", kl
        print "kl0 = ", kl0
        print "C1 = ", C1
        
        print " ==== External Pressure ====="
        print "hydrostatic pressure = ", ps, " kN/m^2"
        pd = sea_density*gravity*beta*ku*hde
        print "hydrodynamic pressure = ", pd , " kN/m^2" 
        pe = ps + pd
        print "Total External Pressure =", pe , " kN/m^2"

#def kl0(x)
#    if(x < 0.3 * 
#def alpha_i(y, z, wangle):
#    a1 = 1.0 - 0.25 * cos(wangle)mod
#    a2 = 0.4 - 0.10 * cos(wangle)
#    a3 = 0.3 - 0.20 * sin(wangle)
#    a4 = 2 * a3 - a2
#    a5 = 0.75 - 1.25 * sin(wangle)

#    if y == -Bmld/2:
#        if z <= Ts and z > 1.8:
#            ai =  a2-(a2-a1)*(1.8-z)/(1.8-Ts)
#    elif y 
    
#x1 = 164.9/2.

x1 = 10.
y1 = 16.2
z1 = 0.

ExternalPressure(x1, y1, z1)
print BETA1['VBM']
