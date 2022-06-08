import math as mth
from cship_hull import ciacs_urs

class krs():
    def __init__(self, Ls, Ts):
        self.Ls = Ls
        self.Ts = Ts

    def Hw(self):
        Ls = self.Ls
        if Ls <= 150:
            result = 0.61*mth.sqrt(Ls)
        elif 150 < Ls <= 250:
            result = 1.41*pow(Ls, 1/3)
        elif 250 < Ls <= 300:
            result = 2.23*pow(Ls, 1/4)
        elif 300 < Ls:
            result = 9.28

        return result

    def Wave_head(self):
        H0 = 0.5 * self.Hw()
        H1 = 0.9 * self.Hw()
        H2 = 0.25 * self.Hw()

        return H0, H1, H2

