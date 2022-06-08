import math as mth

class ship_motion:
    __g0 = 9.81
    GM = 0.
    kr = 0.
    fp = 1.0
    def __init__(self, Ls, Bs, D, Cb):
        self.Ls = Ls
        self.Bs = Bs
        self.D = D
        self.Cb = Cb

    #basic acceleration parameter - a0
    def a0(self):
        return (1.58 - 0.47 * self.Cb) * (2.4 / mth.sqrt(self.Ls) + 34 / self.Ls - 600 / pow(self.Ls,2))

    # Roll period - Ttheta
    def roll_period(self):
        return 2.3 * mth.pi * self.kr / mth.sqrt(9.81*self.GM)


    # Roll angle in deg. - theta
    def roll_angle(self, fp, fBK):
        self.fp = fp
        self.fBK = fBK
        return 9000 * (1.4 - 0.035 * self.Ttheta) * self.fp * self.fBK / ((1.15*self.Bs + 55)*mth.pi)
        

    # sway acceleration (m/s^2)
    def a_sway(self):        # sway_acceleration(self, fp):
        fp = ship_motion.fp
        g0 = ship_motion.g0
        return 0.3*(2.25-20/mth.sqrt(g0*self.Ls)) * fp * self.a0() * g0

    
    # roll acceleration - aroll (rad/s^2)
    def roll_acceleration(self, fp, fBK):
        self.fp = fp
        self.fBK = fBK
        Ttheta = self.roll_period()
        theta = self.roll_angle(self.fp, self.fBK)
        self.a_roll = self.fp*mth.radians(theta)*pow(2* mth.pi/Ttheta,2)
        return self.a_roll

    # enveloped y acceleration
    def envelope_transverse_accelerations(self, TLC, z):
        R = min(self.D/4+TLC/2, self.D/2)
        theta = self.roll_angle(self.fp, self.fBK)
        asway = self.sway_acceleration(1.0)
        aroll = self.roll_acceleration(1.0, 1.0)
        aroll_y = aroll*(z-R)
        self.ay_env = (1-mth.exp(-self.Bs*self.Ls/(215*self.GM)))*mth.sqrt(pow(asway,2)+pow(self.__g0*mth.sin(mth.radians(theta)) + aroll_y,2))
                
        return self.ay_env