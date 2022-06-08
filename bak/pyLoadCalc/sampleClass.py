import math as mth

class ShipMotion:
    __g0 = 9.81
    GM = 0
    kr = 0
    def __init__(self, Ls, Bs, D, Cb):
        self.Ls = Ls
        self.Bs = Bs
        self.D = D
        self.Cb = Cb

    # Roll period - Ttheta
    def roll_period(self):
        self.Ttheta = 2.3 * mth.pi * self.kr / mth.sqrt(self.__g0*self.GM)
        return self.Ttheta


sm = ShipMotion(170.4, 30.2, 28.8, 0.56)
sm._g0 = 50
sm.GM = 2.02
sm.kr = 11.788
print(sm.roll_period())
