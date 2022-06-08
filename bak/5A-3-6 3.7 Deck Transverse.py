def DeckTransverse_SectionModulus(S_m, fy):
    print "Section Modulus of Bottom Transverse"
    print "===================================="

    fb = 0.7*S_m*fy
    print 'fb =', fb

    c2 = 0.4 # no closs tie
    s = 3.44
    ps = 0.0
    ls = 
    Ms = 10000*c2*ps*s*pow(ls,2)
    
    k = 
    k = 1.0
    c = 1.4 # for wing tank
    lb = 9.475   # m
    p = 16.446*9.81 # kN/m^2
    print 'p = ', p
    s = 3.44    # m

    
    Mo = 10000*k*c2*pb*s*pow(lb,2)

    M = k*(10000*c1*phi*p*s*pow(lt,2)+Beta*Ms) # kN-cm
    print 'M =', M

    SM = M/fb
    
    print 'SM =',SM
    print '0.85*SM =', 0.85*SM
    print
    
def DeckTransverse_SectionArea(S_m, fy):
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

DeckTransverse_SectionModulus(S_m, fy)

# S_m = 1.0
# fy = 23500.
# BottomTransverse_SectionArea(S_m, fy)
