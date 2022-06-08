from math import *

class dnvShip:
    g0 = 9.81    
    fps = 1.0
    fbeta = 1.0

    def __init__(self,Ls,B,D,Ts,Cb,Vs, sn):
        self.Analysis_Type = 'Strength'   # Strength or fatigue
        self.Ls = Ls
        self.B = B
        self.D = D
        self.Ts = Ts
        self.Cb = Cb
        self.Vs = Vs
        self.service_notation = sn
        # ffa : Fatigue coefficient to be taken as:, HCSR

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

    #basic acceleration parameter - a0
    def acceleration_parameter(self):
        a0 = (1.58 - 0.47 * self.Cb) * (2.4 / sqrt(self.Ls) + 34 / self.Ls - 600 / pow(self.Ls,2))
        return a0

class sh(dnvShip):
	def show(self):
		print(self.Ls)