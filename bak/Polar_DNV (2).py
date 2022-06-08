from math import *
from string import *

def ice_strength(Polar_Class):
    PC = {'ICE-05':4.2,
          'ICE-10':5.6,
          'ICE-15':7.0,
          'POLAR-10':7.0,
          'POLAR-20':8.5,
          'POLAR-30':10.0}

    return PC[Polar_Class]
    
def ice_thickness(Polar_Class):
    # PolarClass:[sy_ice, hice]
    PC = {'ICE-05':0.5,
          'ICE-10':1.0,
          'ICE-15':1.5,
          'POLAR-10':1.0,
          'POLAR-20':2.0,
          'POLAR-30':3.0}

    return PC[Polar_Class]

def ramming_speed(Polar_Class):
    PC = {'ICE-05':0.,
          'ICE-10':0.,
          'ICE-15':0.,
          'POLAR-10':2.0,
          'POLAR-20':3.0,
          'POLAR-30':4.0}

    return PC[Polar_Class]
    
# D100 Ice Impact forces on the Bow
def Kinetic_Energy(PolarClass, delta):
    VRAM = ramming_speed(PolarClass)

    return 0.5*delta*pow(VRAM, 2)
    
def Impact_Energy(PolarClass, delta, gamma):
    EKE = Kinetic_Energy(PolarClass, delta)
    tang = tan(radians(gamma))
    EIMP = EKE*pow(tang,2)/(pow(tang,2)+2.5)
    return EIMP

def tan_alpha(bow_shape, alpha):
    if bow_shape == 'spoon':
        tana = 1.2*pow(B,0.1)/sqrt(cos(radians(gamma)))
    else:
        tana = tan(radians(alpha))

    return tana

def ramming_force(PolarClass, L, B, delta, Iv, bow_shape, alpha, gamma):
    
    sy_ice = ice_strength(PolarClass)
    h = ice_thickness(PolarClass)
    tana = tan_alpha(bow_shape, alpha)
    tang = tan(radians(gamma))
    
    EKE = Kinetic_Energy(PolarClass, delta)
    EIMP = Impact_Energy(PolarClass, delta, gamma)
    
    CR = 1.0 
    PR = 28.*pow(CR*EIMP/tang, 0.6)*pow(sy_ice*tana,0.4)
    CL = pow(L,3)/(3*pow(10,10)*Iv)
    FEL = sqrt(EIMP/(EIMP+CL*pow(PR,2)))
                                                           
    PZR = PR*FEL
    return PZR

def oblique_ramming_force(PolarClass, L, B, delta, Iv, bow_shape, alpha, gamma):
    sy_ice = ice_strength(PolarClass)
    PZR = ramming_force(PolarClass, L, B, delta, Iv, bow_shape,gamma, alpha)
    EKE = Kinetic_Energy(PolarClass, delta)

    tana = tan_alpha(bow_shape, alpha)
        
    FSIDE = 1.9/pow(tana,0.4)*pow(sy_ice/EKE,0.05)

    POI = PZR*FSIDE/cos(radians(gamma))

    return POI
 
def beaching_force(PolarClass, L, B, delta, CWL):
    EKE = Kinetic_Energy(PolarClass, delta)
    rfw = 0.3
    kb = 2*9.81*(1-rfw)
    GB = sqrt(CWL*(CWL-0.5)/(CWL+1))
    PZB = GB*sqrt(kb*EKE*L*B)

    return PZB

def Ice_compression_loads(PolarClass, beta):
    hice = ice_thickness(PolarClass)    
    q = 165.*pow(hice, 1.5)/sin(radians(beta))
    return q
    
def basic_ice_pressure(PolarClass,FA):
    sy_ice = ice_strength(PolarClass)
    return 1000*FA*sy_ice

def contact_area_eff_height(PolarClass, bow_shape, region, P, alpha, gamma):
    sy_ice = ice_strength(PolarClass)
    hice = ice_thickness(PolarClass)        
    tana = tan_alpha(bow_shape, alpha)
    tang = tan(radians(gamma))

    hstem = pow(P/(645.*sy_ice),0.6)*pow((pow(tang,2)+pow(tana,2))/tana,0.5)    
    if region == 'stem':
        if find(upper(PolarClass),'POLAR') != -1:
            h = hstem
        else:
            h =0.8*hice
    elif region == 'bow':
        h = 0.8*hstem
    else:
        h = 0.4*hice

    return h        

def design_pressure(PolarClass, L, B, delta, CWL, Iv, bow_shape, region, members, FA, alpha, gamma, max_h0, w):
    p0 = basic_ice_pressure(PolarClass,FA)
    PZR = ramming_force(PolarClass, L, B, delta, Iv, bow_shape, gamma, alpha)
    PZB = beaching_force(PolarClass, L, B, delta, CWL)
    P = max(PZR, PZB)
    h = contact_area_eff_height(PolarClass, bow_shape, region, P, alpha, gamma)
    h0 = min(h, max_h0)
    AC = h0*w
    if AC <= 1.0:
        FB = 0.58/pow(AC,0.5)
    else:
        FB = 0.58/pow(AC,1.0)
    
    return FB*p0
                              
def plating(sy, stiff_system, span, space, tk, p0, h0, mp):
    
    ka = 1.1 - 0.25*space/span
    if ka <= 0.85:
        ka = 0.85
    elif ka >= 1.0:
        ka = 1.0
       
    if stiff_system == 'trans':
        a, b = h0, space
    else:
        a, b = space, h0
        
    kw=min(1.3-4.2/pow(a/space+1.8,2),1.0)
    t= 23.*ka*(pow(space,0.75)/pow(h0,0.25))*sqrt(kw*p0/(mp*sy))+ tk
       
    return round(t,3)






