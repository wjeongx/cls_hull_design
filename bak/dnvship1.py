from math import *

class dnvShip:
    g0 = 9.81
    fps = 1.0
    fbeta = 1.0
######################## factors  ########################
    fR = 1.0
    fT = 1.0
    fBK = 1.0 # with bilge keel , 1.2 for without bilge keel
    ffa = 0.85  # #fatigue coefficient

    def __init__(self,Ls,B,D,Ts,Cb,Vs):
        self.Analysis_Type = 'Strength'   # Strength or fatigue
        self.Ls = Ls
        self.B = B
        self.D = D
        self.Ts = Ts
        self.Cb = Cb
        self.Vs = Vs
        # ffa : Fatigue coefficient to be taken as:, HCSR

    def WaveCoefficient_Cw(self):
 
        if self.Ls < 90.0:
            Cw = 0.0856*self.Ls
        elif 90.0 <= self.Ls and self.Ls <= 300:
            Cw = 10.75 - pow(((300 - self.Ls) / 100), 1.5)
        elif 300 < self.Ls and self.Ls <= 350:
            Cw = 10.75
        elif 350 < self.Ls and self.Ls <= 500:
            Cw = 10.75 - pow(((self.Ls - 350) / 150), 1.5)

        return Cw

    def acceleration_parameter_a0(self):
        a0 = (1.58 - 0.47 * self.Cb) * (2.4 / sqrt(self.Ls) + 34 / self.Ls - 600 / pow(self.Ls,2))
        return a0

    def service_restrictions_reduction_factor(self, sa):
        fr = {'R0':1.0,'R1':0.9,'R2':0.8,'R3':0.7,'R4':0.6,'RE':0.5}

        return fr[sa]

class hull_girder_strength(dnvShip):
    def  distribution_factor_fp(self):

        if self.Analysis_Type == 'strength':
            fp = dnvShip.fps
        elif self.Analysis_Type == 'fatigue':
            fvib = self.hull_girder_vibrtion_factor_fvib()
            fp = self.ffa * fvib * (0.27-(6+4*self.fT)*self.Ls * 1E-5)
        return fp



    def hull_girder_vibrtion_factor_fvib(self):
        
        if self.B <= 28.0:
            fvib = 1.10
        elif self.B > 40.0:
            fvib = 1.20
        elif self.B > 28.0 and self.B <= 40.0:
            fvib = 1.1+0.008333*self.B+0.2333
        else:
            fvib = 1.15
        
        return fvib
    # HCSR    
    def distribution_factor_fsw(self, Lx):
        
        f_Lx = Lx / self.Ls

        if f_Lx <= 0:
            fsw = 0.0
        elif f_Lx >= 0 and f_Lx < 0.1:
            fsw = 1.5 * f_Lx
        elif f_Lx >= 0.1 and f_Lx < 0.3:
            fsw = 4.25 * f_Lx - 0.275
        elif f_Lx >= 0.3 and f_Lx <= 0.7:
            fsw = 1.0
        elif f_Lx > 0.7 and f_Lx <= 0.9:
            fsw = -4.25 * f_Lx + 3.975
        elif f_Lx > 0.9 and f_Lx <= 1.0:
            fsw = -1.5 * f_Lx + 1.5
        return fsw

    # HCSR        
    def distribution_factor_fm(self, Lx):

        f_Lx = Lx / self.Ls

        if f_Lx<= 0:
            fm = 0.0
        if f_Lx > 0 and f_Lx < 0.4:
            fm = 2.5 * f_Lx
        elif f_Lx >= 0.4 and f_Lx <= 0.65:
            fm = 1.0
        elif f_Lx >= 0.65 and f_Lx < 1.0:
            fm = -2.85714 * f_Lx + 2.85714
        else:
            fm = 0.0

        return fm

    # HCSR
    def vertical_wave_bending_moments_Mwvh(self, Lx):
        Cw = self.WaveCoefficient_Cw()        
        fnl_vh = self.distribution_factor_fnl_vh()
        fm = self.distribution_factor_fm(self.Ls/2)

        if self.Analysis_Type == 'strength':
            fp = dnvShip.fps
        else:
            fp = 0.9*(0.27-(6+4*self.fT)*self.Ls * 1E-5)

        Mwvh = 0.19*fnl_vh*fm*fp*Cw*self.Ls**2*self.B*self.Cb

        return Mwvh
    
    def vertical_wave_bending_moments_Mwvs(self, Lx):
        Cw = self.WaveCoefficient_Cw()        
        fnl_vs = self.distribution_factor_fnl_vs()
        fm = self.distribution_factor_fm(Lx)

        if self.Analysis_Type == 'strength':
            fp = self.fps
        else:
            fp = 0.9*(0.27-(6+4*self.fT)*self.Ls * 1E-5)

        Mwvs = -0.19* fnl_vs *fm*fp*Cw*self.Ls**2*self.B*self.Cb

        return Mwvs

    def min_swbm_for_hogging(self, Lx):
        
        fsw = self.distribution_factor_fsw(Lx)
        Cw = self.WaveCoefficient_Cw()
        Mwvhmid = self.vertical_wave_bending_moments_Mwvh(self.Ls/2)
        print(Mwvhmid)
        Mswhmin = fsw *(171*Cw*pow(self.Ls,2)*self.B*(self.Cb + 0.7))* 1E-3 - Mwvhmid

        return Mswhmin


    def min_swbm_for_sagging(self, Lx):
        
        print(self.Ls)
        print(self.B)
        print(self.Analysis_Type)
        print(self.WaveCoefficient_Cw())


        fsw = self.distribution_factor_fsw(Lx)
        Cw = self.WaveCoefficient_Cw()

        Mwvsmid = self.vertical_wave_bending_moments_Mwvs(self.Ls/2)
        print(Mwvsmid)
        Msws_min = -0.85*fsw *(171*Cw*pow(self.Ls,2)*self.B*(self.Cb + 0.7))* 1E-3 - Mwvsmid

        return Msws_min 

    def distribution_factor_fnl_vh(self):
        fnl_vh = 1.0
        
        return fnl_vh

    def distribution_factor_fnl_vs(self):
        if self.Analysis_Type == 'Strength':
            fnl_vs = 0.58*((self.Cb + 0.7)/self.Cb)
        else:
            fnl_vs = 1.0
        
        return fnl_vs


# 2 Ship motions and accelerations
class shipMotion(dnvShip):
    GM = 0
    kr = 0

# 2.1 Ship motions
# 2.1.1 Roll motion
# The roll period, in s, shall be taken as:

# Roll period - Ttheta
    def roll_period(self):
        self.Ttheta = 2.3 * pi * self.kr / sqrt(self.g0*self.GM)
        return self.Ttheta

# The roll angle, in deg, shall be taken as:
    def roll_angle(self):

        self.theta = 9000 * (1.4 - 0.035 * self.Ttheta) * self.fp * self.fBK / ((1.15*self.B + 55)*pi)
        return self.theta

# 2.1.2 Pitch motion
    def pitch_period(self):
        
        lambda_phi = 0.6* ( 1 + self.fT)*self.Ls

        Tphi = sqrt(2*pi*lambda_phi / self.g0)

        return lambda_phi

    def pitch_angle(self):
        if self.Analysis_Type == "strength":
            fp = self.fps
        else:
            fp = self.fr * (0.27-0.02*self.fT)-(13-5*self.fT)*self.Ls * 1E-5

        phi = 920*fp*pow(self.Ls, -0.84)*(1.0+pow(2.57/sqrt(self.g0*self.Ls),1.2))

# 2.2 Ship accelerations at the centre of gravity
# 2.2.1 Surge acceleration
# The longitudinal acceleration due to surge, in m/s2, shall be taken as:
    def surge_acceleration_asurge(self):
        if self.Analysis_Type == "strength":
            fp = self.fps
        else:
            fp = self.fr * (0.27-(15+4*self.fT)*self.Ls * 1E-5)

        a0 = self.acceleration_parameter_a0()
        asurge = 0.2*(1.6 + 1.5/sqrt(self.g0*self.Ls))*fp*a0*self.g0

    
 # 2.2.2 Sway acceleration
# The transverse acceleration due to sway , in m/s2, shall be taken as:
    def sway_acceleration_asway(self):
        a0 = self.acceleration_parameter_a0()
        if self.Analysis_Type == "strength":
            fp = self.fps
        else:
            fp = self.fr * (0.24-( 6 - 2*self.fT)*self.B * 1E-4)

            asway = 0.3*(2.25-20/sqrt(self.g0*self.Ls)) * fp * a0 * self.g0
  
        return asway

# 2.2.3 Heave acceleration
# The vertical acceleration due to heave, in m/s2, shall be taken as:
    def heave_aceceleration_aheave():
        
        if self.Analysis_Type == "strength":
            fp = self.fps
        else:
            fp = self.fr * (0.27-0.02*self.fT)-17*self.Ls * 1E-5
        
        a0 = self.acceleration_parameter_a0()

        if self.Ls < 100:
            v = 0
        elif self.Ls >= 150:
            v = 5.0
        else:
            v = 0.1*self.Ls - 10

        if self.Ls < 100:
            aheave = 0.8*(1+0.03*v)*(0.72+2*self.Ls/700)*(1.15-6.5/sqrt(self.g0*self.Ls))*fp*a0*self.g0
        
        elif self.Ls >= 100 and self.Ls < 150:
            aheave = (0.4 + self.Ls/250)*(1+0.03*v*(3-self.Ls/50))*(1.15-6.5/sqrt(self.g0*self.Ls))*fp*a0*self.g0
        
        else:
            aheave = (1.15-6.5/sqrt(self.g0*self.Ls))*fp*a0*self.g0

        return aheave


# # 2.2.4 Roll acceleration
# The roll acceleration, aroll, in rad/s2, shall be taken as:
    def roll_acceleration_aroll(self):

        Ttheta = self.roll_period()
        theta = self.roll_angle(self.fp, self.fBK)
        self.aroll = self.fp*radians(theta)*pow(2* pi/Ttheta,2)
        return self.aroll

# 2.2.5 Pitch acceleration
# The pitch acceleration, in rad/s2, shall be taken as:
    def pitch_acceleration_apitch():
        
        phi = self.pitch_angle()
        Tphi = self.pitch_period()

        if self.Ls < 100:
            v = 0
        elif self.Ls >= 150:
            v = 5.0
        else:
            v = 0.1*self.Ls - 10

        if self.Analysis_Type == "strength":
            fp = self.fps
        else: ## 수정 ##
            fp = self.fr * (0.27-0.02*self.fT)-17*self.Ls * 1E-5

        if self.Ls < 100:
            apitch = 0.8*(1+0.05*v)*fp*(0.72+2*self.Ls/700)*(1.75-22/(self.g0*self.Ls))*phi*pi/180*(2*pi/Tphi)**2
        elif self.Ls >= 100 and self.Ls <150:
            apitch = (0.4+self.Ls/250)*(1+0.05*v*(3-self.Ls/50))*fp*(1.75-22/(self.g0*self.Ls))*phi*pi/180*(2*pi/Tphi)**2
        else:
            apitch = fp*(1.75-22/(self.g0*self.Ls))*phi*pi/180*(2*pi/Tphi)**2
        

# 3 Accelerations at any position
# 3.2 Accelerations for dynamic load cases
# 3.2.1 Longitudinal acceleration
# The longitudinal acceleration at any position for each dynamic load case, in m/s2, shall be taken as:
    def longitudinal_acceleration_ax():
        ax = 0.0

        return ax
# 3.2.2 Transverse acceleration
# The transverse acceleration at any position for each dynamic load case, in m/s2, shall be taken as:
    def transverse_acceleration_ay():
        ay = 0.0

        return ay
    
# 3.2.3 Vertical acceleration
# The vertical acceleration at any position for each dynamic load case, in m/s2, shall be taken as:
    def vertical_accelration_az():
        az = 0.0

        return az

# 3.3 Envelope accelerations
# 3.3.1 Longitudinal acceleration
# The envelope longitudinal acceleration in m/s2, at any position, shall be taken as:
    def envelope_longitudinal_accelerations(self, z):
        R = min(self.D/4+TLC/2, self.D/2)
        theta = self.roll_angle(self.fp, self.fBK)
        asway = self.sway_acceleration(1.0)
        
        aroll = self.roll_acceleration(1.0, 1.0)
        apitch_x = apitch*(z-R)

        if self.Ls < 90:
            fL = 1.0
        elif self.Ls >= 90 and self.Ls < 150:
            fL = 1.3-self.Ls/300
        elif self.Ls >= 150:
            fL = 0.8 

        ax_env = 0.7*fL*(0.65+2*z/(7*TSC))*sqrt(pow(asurge,2)+pow(self.g0*sin(radians(theta)) + aroll_y,2))
                
        return self.ax_env    

# 3.3.2 Transverse acceleration
# The envelope transverse acceleration in m/s2, at any position, shall be taken as:
    # enveloped y acceleration
    def envelope_transverse_accelerations(self, z):
        R = min(self.D/4+TLC/2, self.D/2)
        theta = self.roll_angle(self.fp, self.fBK)
        asway = self.sway_acceleration(1.0)
        aroll = self.roll_acceleration(1.0, 1.0)
        aroll_y = aroll*(z-R)
        self.ay_env = (1-exp(-self.B*self.Ls/(215*self.GM)))*sqrt(pow(asway,2)+pow(self.g0*sin(radians(theta)) + aroll_y,2))
                
        return self.ay_env    

# 3.3.3 Vertical acceleration
# The envelope vertical acceleration for all headings in m/s2, at any position, shall be taken as:
    def envelope_vertical_acceration_az_env():
# The envelope vertical acceleration for all headings in m/s2, at any position, shall be taken as:
        
        az_env = sqrt(aheave**2 + pow((0.95 + exp(-self.Ls/15)))*apitch_z, 2)+(1.2*aroll_z)**2

        return az_env
# 3.3.4 Application of envelope accelerations for deck cargo units and heavy equipment