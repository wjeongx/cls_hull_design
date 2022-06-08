from math import *
from dnvship import dnvShip

class ShipMotion(dnvShip):
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
        
