import math as mth
from unittest import result

class hullStructure:
    g0 = 9.81
    Ls = 172.
    B = 32.
    D = 18.
    Ts = 11.
    V = 14.5
    Cb = 0.830
# x = L/2.
    def __init__(self, x) -> None:
        self.x = x
    

    def Cw(self):
        Ls = self.Ls
        if Ls < 100. :
            result = 0.0792 * Ls
        elif 100. <= Ls < 300.:
            result = 10.75 - pow((300. - Ls) / 100., 1.5)
        elif 300. <= Ls < 350:
            result = 10.75
        else:
            result = 10.75 - pow((Ls - 350.) / 150., 1.5)
        
        return result

    def kwm(self):
        x = self.x
        Ls = self.Ls
        if 0 <= x and x < 0.4 * Ls :
            result = 2.5 * x / Ls
        elif 0.4 * Ls <= x and x <= 0.65 * Ls:
            result = 1#
        elif 0.65 * Ls < x and x < Ls :
            result = 2.86 * (1 - x / Ls)
        
        return result


    def Mwvh(self):
        kwm = self.kwm()
        Ls = self.Ls
        Cw = self.Cw()
        B = self.B
        Cb = self.Cb

        result = 0.19 * kwm * Cw * pow(Ls, 2) * B * Cb
        
        return result

    def Mwvs(self):
        kwm = self.kwm()
        Cw = self.Cw()
        Ls = self.Ls
        B = self.B
        Cb = self.Cb

        result = -0.11 * kwm * Cw * pow(Ls, 2) * B * (Cb + 0.7)
        return result

    def Mh(self):
        x = self.x
        Ls = self.Ls
        B = self.B
        Ts = self.Ts
        Cb = self.Cb

        result = 0.22 * pow(Ls, 9 / 4) * (Ts * 0.3 * B) * Cb * (1 - mth.cos(2 * mth.pi * x / Ls))
        
        return result

    def kqp(self):
        
        x = self.x
        Ls = self.Ls
        B = self.B
        Ts = self.Ts
        Cb = self.Cb

        a = 190. * Cb / (110. * (Cb + 0.7))

        if 0 <= x and x < 0.2 * Ls :
            result = 4.6 * a * x / Ls
        elif 0.2 * Ls <= x and x <= 0.3 * Ls :
            result = 0.92 * a
        elif 0.3 * Ls < x and x < 0.4 * Ls :
            result = (9.2 * a - 7) * (0.4 - x / Ls) + 0.7
        elif 0.4 * Ls <= x and x <= 0.6 * Ls :
            result = 0.7
        elif 0.6 * Ls < x and x < 0.7 * Ls :
            result = 3 * (x / Ls - 0.6) + 0.7
        elif 0.7 * Ls <= x and x <= 0.85 * Ls :
            result = 1
        elif 0.85 * Ls < x and x < Ls :
            result = 6.67 * (1 - x / Ls)

        return result        
            
    def kqn(self):
        
        x = self.x
        Ls = self.Ls
        B = self.B
        Ts = self.Ts
        Cb = self.Cb

        a = 190. * Cb / (110. * (Cb + 0.7))

        if 0 <= x and x < 0.2 * Ls :
            result = -4.6 * x / Ls
        elif 0.2 * Ls <= x and x <= 0.3 * Ls :
            result = -0.92
        elif 0.3 * Ls < x and x < 0.4 * Ls :
            result = -2.2 * (0.4 - x / Ls) + 0.7
        elif 0.4 * Ls <= x and x <= 0.6 * Ls :
            result = -0.7
        elif 0.6 * Ls < x and x < 0.7 * Ls :
            result = -(10 * a - 7) * (x / Ls - 0.6) - 0.7
        elif 0.7 * Ls <= x and x <= 0.85 * Ls :
            result = -a
        elif 0.85 * Ls < x and x < s :
            result = 6.67 * a * (1 - x / Ls)

        return result

    def Qw(self, sign):
        Cw = self.Cw()
        Ls = self.Ls
        B = self.B
        Cb = self.Cb

        if sign == "+" :
            kq = self.kqp()
        elif sign == "-" :
            kq = self.kqn()

        result = 0.3 * kq * Cw * Ls * B * (Cb + 0.7)

        return result

    def a0(self):
        Ls = self.Ls
        V = self.V
        Cw = self.Cw()

        Cv = mth.sqrt(Ls) / 60
        if Cv > 0.2:
            Cv = 0.2

        Cv1 = V / mth.sqrt(Ls)
        if Cv1 < 0.8:
            Cv1 = 0.8

        result = 3 * Cw / Ls + Cv * Cv1

        return result

    def av(self):
        a0 = self.a0()
        Cb = self.Cb

        result = 0.7 * 9.81 * a0 / Cb

    def kf(self):
        Cw = self.Cw()
        Ls = self.Ls
        D = self.D
        Ts = self.Ts

        if D - Ts < 0.8 * Cw :
            F = D - Ts
        else:
            F = 0.8 * Cw

        if Ts > F :
            result = F
        else:
            result = Ts
        
        return result

    def Mss(self):
        Ls = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()

        result = -0.065 * Cw * pow(Ls,2) * B * (Cb + 0.7)
        return result

    def Msh(self):
        Ls = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()
        
        result = Cw*pow(Ls,2)*B*(0.1225-0.015*Cb)
        return result

    def Mwh(self, Beta):
        Ls = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()
        kwm = self.kwm()        

        result = 0.19 * Beta * kwm * Cw * pow(Ls,2) * B * Cb
        return result
        

    def Mws(self, Beta):
        Ls = self.Ls
        B = self.B
        Cb = self.Cb
        Cw = self.Cw()
        kwm = self.kwm()

        result = -0.11 * Beta * kwm * Cw * pow(Ls,2) * B * (Cb + 0.7)

        return result

    def Mh(self):
        x = self.x
        Ls = self.Ls
        B = self.B
        Ts = self.Ts
        Cb = self.Cb

        result = 0.22 * pow(Ls, 9./4.) * (Ts * 0.3 * B) * Cb * (1 - mth.cos(2 * mth.pi * x / Ls))
        return result

    def Zmin(self):
        Ls = self.Ls
        Cb = self.Cb
        Cw = self.Cw()

        result = Cw*pow(Ls,2)*(Cb+0.7)
        return result

    def Block_Coefficient(self, Delta):
        Ls = self.Ls
        B = self.B
        Ts = self.Ts

        result = Delta/(1.025*Ls*B*Ts)
        
        return result
    
    class ABSFPI:
        
        def __init__(self) -> None:
            pass

        def a0(self):
            Cb = hullStructure.Cb
            Ls = hullStructure.Ls

            ko = 1.34-0.47*Cb
            ReturnValue = ko*(2.4/mth.sqrt(Ls) + 34./Ls - 600./pow(Ls,2))

            return ReturnValue
        
        def Acceleration_Vertical(self):
            Ls = hullStructure.Ls
            kv = mth.sqrt(1+0.65*pow(5.3-45./Ls,2)*pow(XLOC/Ls-0.45, 2))
            Cv = mth.cos(mth.radians(mu))+(1+2.4*ZLOC/HULL.B)*mth.sin(mth.radians(mu))/kv
            
            av = Cv*VAC*kv*self.a0()*g0

            return av

        def Acceleration_Longitudinal(self):
            Ls = hullStructure.Ls
            g0 = hullStructure.g0

            kl = 0.5+8*YLOC/Ls
            Cl = 0.35-0.0005*(Ls-200)
            al = Cl*LAC*kl*a0()*g0

            return al

        def Acceleration_Transverse(self):
            Ls = hullStructure.Ls
            B = hullStructure.B
            g0 = hullStructure.g0

            kt = 0.35 + YLOC/B
            Ct = 1.27*mth.sqrt(1+1.52*pow(XLOC/Ls-0.45,2))
            at = Ct*TAC*kt*a0()*g0

            return at
        
        #[ExcelFunction(Description = "Pitch Amplitude - phi", Category = "ABS FPSO - Loads")]
        def Pitch_Amplitude(self):
            
            k1 = 1030.0
            phi = PMO*k1*pow(10/HULL.Cb,0.25)/HULL.Ls

            return phi

        #[ExcelFunction(Description = "Roll Amplitude - theta", Category = "ABS FPSO - Loads")]
        def Roll_Amplitude( self):
            CR = 1.05
            kq = 0.005
            Cdi = 1.06*(di/HULL.df)-0.06

            if Tr > 20:
                theta = CR*(35-kq*Cdi*delta/1000)

            elif Tr>=12.5 and Tr<=20.0:
                theta = CR*(35-kq*Cdi*delta/1000)*(1.5375-0.027*Tr)

            elif Tr<12.5:
                theta = CR*(35-kq*Cdi*delta/1000)*(0.8625+0.027*Tr)

            return theta

        # [ExcelFunction(Description = "Pitch Natural Period - Tp", Category = "ABS FPSO - Loads")]
        def Pitch_Period( self):
            k2 = 3.5
            Tp = k2*sqrt(HULL.Cb*di)
            
            return Tp

        def Roll_Period( kr,  GM):
            k4 = 2.0
            Tr = k4*kr/sqrt(GM)

            return Tr

        # [ExcelFunction(Description = "Added Pressure Head (Delta hi-1)", Category = "ABS FPSO - Loads")]
        def Delta_hi_i( Cru,  b,  phi,  theta,  Cphi,  Ctheta,  xi,  zeta,  eta):
            thetae = 0.71*Ctheta*theta
            phie = 0.71*Cphi*phi
            zetae = b - zeta
            etae = eta

            # print 'i=', thetae, phie, zetae, etae, zeta, eta, b
            dh = xi*sin(-radians(phie))+Cru*(zetae*sin(radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-zeta)

            return dh

        # [ExcelFunction(Description = "Added Pressure Head (Delta hi-2)", Category = "ABS FPSO - Loads")]
        def Delta_hi_ii( Cru,  l,  delta_b,  delta_h,  phi,  theta,  Cphi,  Ctheta,  xi,  zeta,  eta):

            thetae = 0.71*Ctheta*theta
            phie = 0.71*Cphi*phi
            zetae = zeta-delta_b
            etae = eta-delta_h

            # print 'ii =', thetae, phie, zetae, etae
            dh = (l-xi)*sin(radians(phie))+ Cru*(zetae*sin(-radians(thetae))*cos(radians(phie))+etae*cos(radians(thetae))*cos(radians(phie))-zeta)

            return dh

        def effective_ai(NLC, NTK, wlx, wtx, ZL, XL, YL):

            # For Rectangur Tank : Cdp = 1.0, Cru = 1.0
            Cdp = 1.0
            
            oooo=Acceleration_Vertical(BETA['VAC'],LC['mu'][NLC],XL, ZL)
            oooo=Acceleration_Longitudinal(BETA['LAC'],YL)
            oooo=Acceleration_Transverse(BETA['TAC'],XL, YLoooo
            oooo wlx == 0:
                wl = LC['wla'][NLC]
            ooooif wlx == 1:
                wl = LC['wlf'][NLC]

            if wtx == 0:
                wt = LC['wts'][NLC]
            elif wtx == 1:
                wt = LC['wtp'][NLC]
                
            ai = Acceleration_Effective(Cdp, LC['wv'][NLC], wl , wt, TANK.NO[NTK[0]][NTK[1]][3], TANK.NO[NTK[0]][NTK[1]][4],TANK.NO[NTK[0]][NTK[1]][5], LC['mu'][NLC] , av, al, at)

            return ai

        def Delta_h(NLC, NTK, phi, theta, ZL, XL, YL):

            # For Rectangur Tank : Cdp = 1.0, Cru = 1.0



    class DNV:

        def __init__(self) -> None:
            pass
    
    class ABS:

        def __init__(self) -> None:
            pass


    

hull = hullStructure(86)

print(hull.Cw())
