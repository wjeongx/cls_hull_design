import math as mth

g = 9.81
fnl = 1.0

lambda = g*Ttheta**2/(2*mth.pi)
P_BSR = fb*fnl*(-10*y*mth.sin(mth.radians(theta1))+0.88*fps*Cw*mth.sqrt((L0+lambda-125)/L0)*(fyB1+1))
