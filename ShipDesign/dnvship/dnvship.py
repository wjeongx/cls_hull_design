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


#HCSR
    def WaveCoefficient(self):
 
        if self.Ls < 90.0:
            Cw = 0.0856*self.Ls
        elif 90.0 <= self.Ls and self.Ls <= 300:
            Cw = 10.75 - pow(((300 - self.Ls) / 100), 1.5)
        elif 300 < self.Ls and self.Ls <= 350:
            Cw = 10.75
        elif 350 < self.Ls and self.Ls <= 500:
            Cw = 10.75 - pow(((self.Ls - 350) / 150), 1.5)

        return Cw

    def  distribution_factor_fp(self):

        if self.Analysis_Type == 'strength':
            fp = fps
        elif self.Analysis_Type == 'fatigue':
            fvib = self.hull_girder_vibrtion_factor_fvib()
            ffa = 0.85  #fatigue coefficient
            fp = ffa*fvib*(0.27-(6+4*ft)*self.Ls * 1E-5)
        return fp

    def reduction_factor_fr(self): # according service area
        if self.service_notation == 'R0':
            fr = 1.0
        elif self.service_notation == 'R1':
            fr = 0.9
        elif self.service_notation == 'R2':
            fr = 0.8
        elif self.service_notation == 'R3':
            fr = 0.7
        elif self.service_notation == 'R4':
            fr = 0.6                    
        else:
            fr = 0.5    
        
        return fr

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

    def distribution_factor_fnl_vh(self):
        fnl_vh = 1.0
        
        return fnl_vh

    def distribution_factor_fnl_vs(self):
        if self.Analysis_Type == 'Strength':
            fnl_vs = 0.58*((self.Cb + 0.7)/self.Cb)
        else:
            fnl_vs = 1.0
        
        return fnl_vs

    # HCSR    
    def distribution_factor_fsw(self, Lx):
        
        Xp = Lx / self.Ls

        if Xp <= 0:
            fsw = 0.0
        elif Xp >= 0 and Xp < 0.1:
            fsw = 1.5 * Xp
        elif Xp >= 0.1 and Xp < 0.3:
            fsw = 4.25 * Xp - 0.275
        elif Xp >= 0.3 and Xp <= 0.7:
            fsw = 1.0
        elif Xp > 0.7 and Xp <= 0.9:
            fsw = -4.25 * Xp + 3.975
        elif Xp > 0.9 and Xp <= 1.0:
            fsw = -1.5 * Xp + 1.5
        return fsw

    # HCSR        
    def distribution_factor_fm(self, Lx):

        Xp = Lx / self.Ls

        if Xp<= 0:
            fm = 0.0
        if Xp > 0 and Xp < 0.4:
            fm = 2.5 * Xp
        elif Xp >= 0.4 and Xp <= 0.65:
            fm = 1.0
        elif Xp >= 0.65 and Xp < 1.0:
            fm = -2.85714 * Xp + 2.85714
        else:
            fm = 0.0

        return fm

    # HCSR
    def vertical_wave_bending_moments_Mwvh(self, Lx):
        Cw = self.WaveCoefficient()        
        fnl_vh = self.distribution_factor_fnl_vh()
        fm = self.distribution_factor_fm(self.Ls/2)
        ft = 1.0
        if self.Analysis_Type == 'strength':
            fp = self.fps
        else:
            fp = 0.9*(0.27-(6+4*ft)*self.Ls * 1E-5)

        Mwvh = 0.19*self.fnl_vh*fm*fp*Cw*self.Ls**2*self.B*self.Cb

        return Mwvh
    
    def vertical_wave_bending_moments_Mwvs(self, Lx):
        Cw = self.WaveCoefficient()        
        fnl_vh = self.distribution_factor_fnl_vh()
        fm = self.distribution_factor_fm(Lx)
        ft = 1.0
        if self.Analysis_Type == 'strength':
            fp = self.fps
        else:
            fp = 0.9*(0.27-(6+4*ft)*self.Ls * 1E-5)

        Mwvs = -0.19*self.fnl_vs*self.fm*self.fp*Cw*self.Ls**2*self.B*self.Cb

        return Mwvs

    def min_swbm_for_hogging(self, Lx):
        
        fsw = self.distribution_factor_fsw(Lx)
        Cw = self.WaveCoefficient()
        Mwvhmid = self.vertical_wave_bending_moments_Mwvh(self.Ls/2)
        print(Mwvhmid)
        Mswhmin = fsw *(171*Cw*pow(self.Ls,2)*self.B*(self.Cb + 0.7))* 1E-3 - Mwvhmid

        return Mswhmin


    def min_swbm_for_sagging(self, Lx):
        
        fsw = self.distribution_factor_fsw(self, Lx)
        Cw = self.WaveCoefficient()
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

    # HCSR    
    def distribution_factor_fsw(self, Lx):
        
        Xp = Lx / self.Ls

        if Xp <= 0:
            fsw = 0.0
        elif Xp >= 0 and Xp < 0.1:
            fsw = 1.5 * Xp
        elif Xp >= 0.1 and Xp < 0.3:
            fsw = 4.25 * Xp - 0.275
        elif Xp >= 0.3 and Xp <= 0.7:
            fsw = 1.0
        elif Xp > 0.7 and Xp <= 0.9:
            fsw = -4.25 * Xp + 3.975
        elif Xp > 0.9 and Xp <= 1.0:
            fsw = -1.5 * Xp + 1.5
        return fsw

    # HCSR        
    def distribution_factor_fm(self, Lx):

        Xp = Lx / self.Ls

        if Xp<= 0:
            fm = 0.0
        if Xp > 0 and Xp < 0.4:
            fm = 2.5 * Xp
        elif Xp >= 0.4 and Xp <= 0.65:
            fm = 1.0
        elif Xp >= 0.65 and Xp < 1.0:
            fm = -2.85714 * Xp + 2.85714
        else:
            fm = 0.0

        return fm

    # HCSR
    def vertical_wave_bending_moments_Mwvh(self, Lx):
        Cw = self.WaveCoefficient()        
        fnl_vh = self.distribution_factor_fnl_vh()
        fm = self.distribution_factor_fm(self.Ls/2)
        ft = 1.0
        if self.Analysis_Type == 'strength':
            fp = self.fps
        else:
            fp = 0.9*(0.27-(6+4*ft)*self.Ls * 1E-5)

        Mwvh = 0.19*self.fnl_vh*fm*fp*Cw*self.Ls**2*self.B*self.Cb

        return Mwvh
    
    def vertical_wave_bending_moments_Mwvs(self, Lx):
        Cw = self.WaveCoefficient()        
        fnl_vh = self.distribution_factor_fnl_vh()
        fm = self.distribution_factor_fm(Lx)
        ft = 1.0
        if self.Analysis_Type == 'strength':
            fp = self.fps
        else:
            fp = 0.9*(0.27-(6+4*ft)*self.Ls * 1E-5)

        Mwvs = -0.19*self.fnl_vs*self.fm*self.fp*Cw*self.Ls**2*self.B*self.Cb

        return Mwvs

    def min_swbm_for_hogging(self, Lx):
        
        fsw = self.distribution_factor_fsw(Lx)
        Cw = self.WaveCoefficient()
        Mwvhmid = self.vertical_wave_bending_moments_Mwvh(self.Ls/2)
        print(Mwvhmid)
        Mswhmin = fsw *(171*Cw*pow(self.Ls,2)*self.B*(self.Cb + 0.7))* 1E-3 - Mwvhmid

        return Mswhmin


    def min_swbm_for_sagging(self, Lx):
        
        fsw = self.distribution_factor_fsw(self, Lx)
        Cw = self.WaveCoefficient()
        Mwvsmid = self.vertical_wave_bending_moments_Mwvs(self.Ls/2)
        print(Mwvsmid)
        Msws_min = -0.85*fsw *(171*Cw*pow(self.Ls,2)*self.B*(self.Cb + 0.7))* 1E-3 - Mwvsmid

        return Msws_min 

