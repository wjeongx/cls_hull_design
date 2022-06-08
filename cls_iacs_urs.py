import math as mth
from scipy import interpolate

class constant:
    g0 = 9.81
    s0 = 1.025
    A = B = D = E = {'fy':235., 'fac':1.0, 'fu':400}
    AH = DH = EH = FH = {'fy':315., 'fac':0.78, 'fu':440}
    AH36 = DH36 = EH36 = FH36 = {'fy':355., 'fac':0.72, 'fu':490}
    AH40 = DH40 = EH40 = FH40 = {'fy':390., 'fac':0.68, 'fu':510}

class csrh:
    def __init__(self, Ls, B, D, Ts, Vs, Cb):
        self.Ls = Ls
        self.B = B
        self.D = D
        self.Ts = Ts
        self.Vs = Vs
        self.Cb = Cb

    # S11.2.2 Wave loads
    def Cw(self):
        L = self.Ls

        if L < 90:
            result = 0.0792 * L
        elif 90 <= L < 300:
            result = 10.75 - pow(((300 - L) / 100),1.5)
        elif 300 <= L < 350:
            result = 10.75
        elif 350 <= L <= 500:
            result = 10.75 - pow(((L - 350) / 150),1.5)
        else:
            result = -1

        return result

    def fm(self, x):
        
        Ls = self.Ls

        if x <=0:
            result = 0
        elif 0 < x < 0.4*Ls:
            result = interpolate.interp1d()
        elif 0.4 * Ls <= x <= 0.65 * Ls:
            result = 1.0
        elif 0.65*Ls < x < Ls:
            result = interpolate.interp1d()
        elif x >= Ls:
            result = 0
        
        return result

        # if 0 <= x and x < 0.4 * L:
        #     result = 2.5 * x / L
        # elif 0.4 * L <= x and x <= 0.65 * L :
        #     result = 1.0
        # elif 0.65 * L < x and x < L :
        #     result = 2.86 * (1 - x / L)
        # return result

    def Mwh(self, Beta, x):    # Wave Bending Moment for hogging (+)
        L = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()
        M = self.M(x)

        ReturnValue = 0.19 * Beta * M * Cw * pow(L,2) * B * Cb
        return ReturnValue

    def Mws(self, Beta, x):   # Wave Bending Moment for sagging (-)
        L = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()
        M = self.M(x)
        return -0.11 * Beta * M * Cw * pow(L,2) * B * (Cb + 0.7)

# S11.2.2.2 Wave shear force
    def F1(self, x):
        L = self.Ls
        Cb = self.Cb

        a = 190 * Cb / (110 * (Cb + 0.7))

        if 0 <= x and x < 0.2 * L:
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

    def F2(self, x ):
        L = self.Ls
        Cb = self.Cb        

        a = 190 * Cb / (110 * (Cb + 0.7))

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

    def Fwp(self, x): # For positive shear force, in kN
        L = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw(L)

        F1 = self.F1(x)

        return 0.3 * F1 * Cw * L * B * (Cb + 0.7)

    def Fwm(self, x): # For negative shear force, in kN
        L = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw(L)
        
        F2 = self.F2(x)

        return -0.3 * F2 * Cw * L * B * (Cb + 0.7)

# S11.3.1.2 Moment of inertia
# Moment of inertia of hull section at the midship point is not to be less than
    def Imin(self):
        L = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw(L)

        return 3*Cw*pow(L,3)*B*(Cb+0.7)

# etc
    def a0(self):
        L = self.Ls
        V = self.Vs

        Cv = mth.sqrt(L) / 60
        if Cv > 0.2 :
            Cv = 0.2

        Cv1 = V / mth.sqrt(L)
        if Cv1 < 0.8 :
            Cv1 = 0.8

        return 3 * self.Cw() / L + Cv * Cv1

    def av(self):
        L = self.Ls
        V = self.Vs
        Cb = self.Cb        
        a0 = self.a0()

        return 0.7 * 9.81 * a0 / Cb

    def kf(self):
        L = self.Ls
        D = self.D
        T = self.Ts
        Cw = self.Cw()

        if D - T < 0.8 * Cw :
            F = D - T
        else:
            F = 0.8 * Cw()

        if T > F :
            result = F
        else:
            result = T
        return result

    def Mss(self):
        L = self.Ls
        B = self.B
        Cb = self.Cb

        return -0.065*self.Cw()*pow(L,2)*B*(Cb + 0.7)

    def Msh(self):
        L = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()

        return Cw*pow(L,2)*B*(0.1225-0.015*Cb)

    def Mh(self, x):
        L = self.Ls
        B = self.B
        T = self.Ts
        Cb = self.Cb

        return 0.22 * pow(L,9./4.) * (T * 0.3 * B) * Cb * (1 - mth.cos(2 * mth.pi * x / L))
