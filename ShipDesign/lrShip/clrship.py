from math import *

class bvShip:
    g0 = 9.81
    
    def __init__(self,Ls,B,D,Ts,Cb,Vs):
        self.Ls = Ls
        self.B = B
        self.D = D
        self.Ts = Ts
        self.Cb = Cb
        self.Vs = Vs
    
#   [ExcelFunction(Description = "Wave Coefficient (Cw)", Category = "Longitudinal Strength")]
    def WaveCoefficient(self):
 
        if self.Ls < 90:
            Cw = 0.0856*self.Ls
        elif 90.0 <= self.Ls and self.Ls <= 300:
            Cw = 10.75 - pow(((300 - self.Ls) / 100), 1.5)
        elif 300 < self.Ls and self.Ls <= 350:
            Cw = 10.75
        elif 350 < self.Ls and self.Ls <= 500:
            Cw = 10.75 - pow(((self.Ls - 350) / 150), 1.5)

        return Cw

#   [ExcelFunction(Description = "Distribution Factor for still water bending Moment", Category = "Longitudinal Strength")]
    def distribution_factor_fsw(self, Lx):
        
        Xs = Lx / self.Ls

        if Xs <= 0:
            fsw = 0.0
        elif Xs >= 0 and Xs < 0.1:
                    fsw = 1.5 * Xs
        elif Xs >= 0.1 and Xs < 0.3:
            fsw = 4.25 * Xs - 0.275
        elif Xs >= 0.3 and Xs <= 0.7:
            fsw = 1.0
        elif Xs > 0.7 and Xs <= 0.9:
            fsw = -4.25 * Xs + 3.975
        elif Xs > 0.9 and Xs <= 1.0:
            fsw = -1.5 * Xs + 1.5
        return fsw

#   [ExcelFunction(Description = "Distribution factor for vertical wave bending moment", Category = "Longitudinal Strength")]
    def distribution_factor_kwm(Lx):
        Lx = Xs / Ls

        if Lx >= 0 and Lx < 0.4:
            kwm = 2.5 * Lx
        elif Lx >= 0.4 and Lx < 0.65:
            kwm = 1.0
        elif Lx >= 0.65 and Lx < 1.0:
            kwm = -2.85714 * Lx + 2.85714
 
        return kwm

def distribution_factor_kqp(Lx):
    a = 190 * Cb / (110 * (Cb + 0.7))

    if 0 <= x and x < 0.2 * L:
        kqp = 4.6 * a * x / L
    elif 0.2 * Lx <= x and x <= 0.3 * L :
        kqp = 0.92 * a
    elif 0.3 * Lx < x and x < 0.4 * L :
        kqp = (9.2 * a - 7) * (0.4 - x / L) + 0.7
    elif 0.4 * Lx <= x and x <= 0.6 * L :
        kqp = 0.7
    elif 0.6 * Lx < x and x < 0.7 * L :
        kqp = 3 * (x / L - 0.6) + 0.7
    elif 0.7 * Lx <= x and x <= 0.85 * L :
        kqp = 1
    elif 0.85 * Lx < x and x < L :
        kqp = 6.67 * (1 - x / L)
    return kqp

def kqn(Lx):
    a = 190 * Cb / (110 * (Cb + 0.7))

    if 0 <= x and x < 0.2 * L :
        kqn = -4.6 * x / L
    elif 0.2 * L <= x and x <= 0.3 * L :
        kqn = -0.92
    elif 0.3 * L < x and x < 0.4 * L :
        kqn = -2.2 * (0.4 - x / L) + 0.7
    elif 0.4 * L <= x and x <= 0.6 * L :
        kqn = -0.7
    elif 0.6 * L < x and x < 0.7 * L :
        kqn = -(10 * a - 7) * (x / L - 0.6) - 0.7
    elif 0.7 * L <= x and x <= 0.85 * L :
        kqn = -a
    elif 0.85 * L < x and x < L :
        kqn = 6.67 * a * (1 - x / L)

    return kqn

def Msh():
    Msh = Cw(L)*pow(L,2)*B*(0.1225-0.015*Cb)
    return Msh`

def Mwh(Lx):
    Mwh = 0.19 * kwm(L, x) * Cw(L) * pow(L,2) * B * Cb
    return Mwh

def Mws(Lx):
    Mws = -0.11 * kwm(L, x) * Cw(L) * pow(L,2) * B * (Cb + 0.7)
    return Mws

def Mh(Lx ):
    Mh = 0.22 * pow(L,9./4.) * (T * 0.3 * B) * Cb * (1 - cos(2 * pi * x / L))
    return Mh

def Qw(Lx ):

    if sign == "+" :
        kq = kqp(L, Cb, x)
    elif sign == "-" :
        kq = kqn(L, Cb, x)

    Qw = 0.3 * kq * Cw(L) * L * B * (Cb + 0.7)
    return Qw

def Zmin():
    Zmin = Cw(L)*pow(L,2)*(Cb+0.7)
    return Zmin

sm = bvShip(216.25, 32.24, 20.65, 14.3, 0.87, 15.8)
print(sm.Ls)
print(sm.WaveCoefficient())
print(sm.distribution_factor_fsw(100.))
sp = statix_p
print(sp.sta_pre())
print(sp.mro)