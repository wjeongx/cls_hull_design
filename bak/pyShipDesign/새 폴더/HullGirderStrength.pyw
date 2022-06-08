import math

L,B,D,T,V,CB = 172., 32., 18., 11., 14.5, 0.830
x = L/2.

def Cw():
    if L < 100. :
        result = 0.0792 * L
    elif 100. <= L and L < 300. :
        result = 10.75 - ((300. - L) / 100.) ^ 1.5
    elif 300. <= L and L < 350 :
        result = 10.75
    else:
        result = 10.75 - ((L - 350.) / 150.) ^ 1.5
    return result

def kwm():
    if 0 <= x and x < 0.4 * L :
        result = 2.5 * x / L
    elif 0.4 * L <= x and x <= 0.65 * L:
        result = 1#
    elif 0.65 * L < x and x < L :
        result = 2.86 * (1 - x / L)
    return result

def Mwvh():
    result = 0.19 * kwm(L, x) * Cw() * L ^ 2 * B * Cb
    return result

def Mwvs():
    result = -0.11 * kwm(L, x) * Cw() * L ^ 2 * B * (Cb + 0.7)
    return result

def Mh():
    result = 0.22 * L ^ (9 / 4) * (T * 0.3 * B) * Cb * (1 - Cos(2 * 3.14159265358979 * x / L))
    return result

def kqp():
    a = 190. * Cb / (110. * (Cb + 0.7))

    if 0 <= x and x < 0.2 * L :
        result = 4.6 * a * x / L
    elif 0.2 * L <= x and x <= 0.3 * L :
        result = 0.92 * a
    elif 0.3 * L < x and x < 0.4 * L :
        result = (9.2 * a - 7) * (0.4 - x / L) + 0.7
    elif 0.4 * L <= x and x <= 0.6 * L :
        result = 0.7
    elif 0.6 * L < x and x < 0.7 * L :
        result = 3 * (x / L - 0.6) + 0.7
    elif 0.7 * L <= x and x <= 0.85 * L :
        result = 1
    elif 0.85 * L < x and x < L :
        result = 6.67 * (1 - x / L)

    return result        
        
def kqn():
    a = 190. * Cb / (110. * (Cb + 0.7))

    if 0 <= x and x < 0.2 * L :
        result = -4.6 * x / L
    elif 0.2 * L <= x and x <= 0.3 * L :
        result = -0.92
    elif 0.3 * L < x and x < 0.4 * L :
        result = -2.2 * (0.4 - x / L) + 0.7
    elif 0.4 * L <= x and x <= 0.6 * L :
        result = -0.7
    elif 0.6 * L < x and x < 0.7 * L :
        result = -(10 * a - 7) * (x / L - 0.6) - 0.7
    elif 0.7 * L <= x and x <= 0.85 * L :
        result = -a
    elif 0.85 * L < x and x < L :
        result = 6.67 * a * (1 - x / L)

    return result

def Qw(sign):
    if sign == "+" :
        kq = kqp()
    elif sign == "-" :
        kq = kqn()

    result = 0.3 * kq * Cw() * L * B * (Cb + 0.7)

    return result

def a0():
    Cv = Sqr(L) / 60
    if Cv > 0.2:
        Cv = 0.2

    Cv1 = V / math.sqrt(L)
    if Cv1 < 0.8:
        Cv1 = 0.8

    result = 3 * Cw() / L + Cv * Cv1

    return result

def av():
    result = 0.7 * 9.81 * a0(L, V) / Cb

def kf():
    if D - T < 0.8 * Cw() :
        F = D - T
    else:
        F = 0.8 * result(L)

    if T > F :
        result = F
    else:
        result = T
    return result

def HGSR(SIGVR , SIGHR ):
    result = Sqr(SIGVR ^ 2 + SIGHR ^ 2 + 2 * 0.1 * SIGVR * SIGHR)
    return result

print 10.75 - math.pow((173.2 - 350) / 150,1.5)
