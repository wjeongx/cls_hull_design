from math import *

class ShipLoads:
    g0 = 9.81
  
    def __init__(self):
        self.Ls = 0.
        self.B = 0.
        self.D = 0.
        self.Ts = 0.
        self.Cb = 0.
        self.V = 0.

# ExcelFunction(Description = "Wave Coefficient (Cw)", Category = "Longitudinal Strength")]
    def WaveCoefficient(self):
        if 90.0 <= self.Ls and self.Ls < 300:
            Cw = 10.75 - pow(((300. - self.Ls) / 100.), 1.5)
        elif 300 <= Ls and Ls < 350:
            Cw = 10.75
        elif 350 < Ls and Ls <= 500:
            Cw = 10.75 - pow(((Ls - 350) / 150), 1.5)
        
        return Cw

ship = bvShip()
ship.Ls = 113
ship.Ts = 6.7
ship.g0 = 3.12
print(ship.g0)

