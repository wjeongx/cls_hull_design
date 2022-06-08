from math import *
from string import *

def bow_area_ice_pressure_coefficient(PolarClass, col):
    PC = {'A5':[3.7,5.],
          'A4':[3.08,4.5],
          'A3':[2.26,4.],
          'A2':[1.54,3.],
          'A1':[0.905,2.5],
          'A0':[0.997,2.],
          'B0':[0.750,0.],
          'C0':[0.60,0.],
          'D0':[0.5,0.]}
    
    return PC[PolarClass][col]

def basic_ice_pressure(PolarClass, Displacement, Power):
    N = Power
    D = Displacement
    cof = bow_area_ice_pressure_coefficient(PolarClass,0)
    if PolarClass == 'A1' or PolarClass == 'A2' or PolarClass == 'A3' or PolarClass == 'A4' or PolarClass == 'A5':
        P0 = cof*pow(N/746.,0.2)*pow(D/1000.,0.15)
    elif PolarClass == 'A0' or PolarClass == 'B0' or PolarClass == 'C0' or PolarClass == 'D0':
        P0 = cof*pow(D/1000.,0.2)

    return P0           

def F_coefficient(PolarClass, Displacement):
    D = Displacement    
    i = bow_area_ice_pressure_coefficient(PolarClass,1)
    Fb1 = 1.25
    if Fb1 < 0.85:
        Fb1 = 0.85
    elif Fb1 > 1.25:
        Fb1 = 1.25
        
    Fb2 = 1+i*pow(1.3+0.001*D,-2.)
    result = Fb1*Fb2
    return result

def bow_design_ice_pressure(PolarClass, Displacement, Power):
    P0 = basic_ice_pressure(PolarClass, Displacement, Power)
    Fb = F_coefficient(PolarClass,Displacement)
    Pb=P0*Fb
    return Pb

def plating(sy, space, p, tk):
    t = 0.6*space*pow(p/sy, 0.5)+tk
    return t






