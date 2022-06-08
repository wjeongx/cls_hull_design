def BottomTransverse_SectionModulus(S_m, fy):
    print "Section Modulus of Bottom Transverse"
    print "===================================="

    fb = 0.7*S_m*fy
    print 'fb =', fb
    
    k = 1.0
    c = 1.4 # for wing tank
    lb = 8.995   # m
    p = 16.446*9.81 # kN/m^2
    print 'p = ', p
    s = 3.44    # m
    M = 10000*k*c*s*p*pow(lb,2) # kN-cm
    print 'M =', M

    SM = M/fb
    
    print 'SM =',SM
    print '0.85*SM =', 0.85*SM
    print
def BottomTransverse_SectionArea(S_m, fy):
    print "Web Area of Bottom Transverse"
    print "============================="

    k = 1.0
    Kb = 0.5
    p = 16.446*9.81 # kN/m^2
    ls = 12.9 # m
    he = 1.8 # m
    c = 0.15
    D = 18.2
    Bc = 12.9
    # Bc = 0.0
    fs = 0.45*S_m*fy
    print 'fs =',fs
    s = 3.44
    F = 1000*k*(p*s*(Kb*ls-he)+c*D*Bc*s)
    print 'F =', F
    A = F/fs
    print 'A =', A
    print '0.85A =', 0.85*A
    print

# S_m = 1.0 for mild steel
S_m = 1.0
fy = 23500.

BottomTransverse_SectionModulus(S_m, fy)

# S_m = 1.0
# fy = 23500.
BottomTransverse_SectionArea(S_m, fy)
