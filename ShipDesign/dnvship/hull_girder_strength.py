from math import *
import dnvShip

class Hull_Girder_Strength(dnvShip):

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

dv = hull_girder_strength(216.25, 32.24, 20.65, 14.3, 0.87, 15.8)


"""
# dv.Analysis_Type = "Fatigue"
dv.Lx = dv.Ls/2
print(dv.Lx)
print(dv.WaveCoefficient())
print(dv.fnl_vs)
print(dv.fnl_vh)
print(dv.distribution_factor_fsw(100))
"""
#        heading_correction_f_beta(self):
"""
        • For strength assessment:
            fβ = 1.05 for HSM and FSM load cases for the extreme sea loads design load scenario.
            fβ= 0.8 for BSR and BSP load cases for the extreme sea loads design load scenario.
            fβ= 1.0 for HSA, OST and OSA load cases for the extreme sea loads design load scenario.
            fβ = 1.0 for ballast water exchange at sea, harbour/sheltered water and accidental flooded design load scenarios.
        • For fatigue assessment:
            fβ = 1.0.
       




 
    
    # HCSR    
    def distribution_factor_fnl_vs(self):
        if self.Analysis_Type == 'strength':
            fnl_vs = 0.58*((self.Cb + 0.7)/self.Cb)
        else:
            fnl_vs = 1.0

        return fnl_vs

    # HCSR    
    def  distribution_factor_fp(self):

        if self.Analysis_Type == 'strength':
            fp = fps
        else:
            fp = 0.9*(0.27-(6+4*ft)*self.Ls * 1E-5)

        return fp


    # HCSR    
    def distribution_factor_fqp(self, Lx):
        Xp = Lx / Ls

        if Xp > 0 and Xp < 0.2 * self.Ls:
            fqp = 4.6 * fnl_vh * Xp
        elif 0.2 <= Xp and Xp <= 0.3:
            fqp = 0.92*fnl_vh
        elif 0.3 < Xp and Xp < 0.4:
            fqp = -(9.2*fnl_vh-7)*Xp + (3.68*fnl_vh-2.8)
        elif 0.4 <= Xp and Xp <= 0.6:
            fqp = 0.7
        elif 0.6 < Xp and Xp < 0.7 :
            fqp = 3 * (x / L - 0.6) + 0.7
        elif 0.7 <= Xp and Xp <= 0.85:
            fqp = fnl_vs
        elif 0.85 < Xp and Xp <= 1.0:
            fqp = -6.67 *fnl_vs*Xp + 6.67
        else:
            fpq = 0.0
        return fqp

    # HCSR    
    def distribution_factor_fqn(self, Lx):
        
        Xp = Lx / self.Ls

        if 0 <= Xp and Xp < 0.2:
            fqn = -4.6 * Xp
        elif 0.2  <= Xp and Xp <= 0.3 :
            fqn = -0.92
        elif 0.3 < Xp and Xp < 0.4 :
            fqn = -2.2 * (0.4 - x / L) + 0.7
        elif 0.4 <= x and x <= 0.6:
            fqn = -0.7
        elif 0.6 * Xp and Xp < 0.7:
            fqn = -(10 * a - 7) * (x / L - 0.6) - 0.7
        elif 0.7 <= Xp and Xp <= 0.85 :
            fqn = -
        elif 0.85 < Xp and Xp < 1:
            fqn = 6.67 * fnl_vs + (1 - x / L)

        return fqn

# fT: Ratio between draught at a loading condition and scantling draught, to be taken as:    
# fT = TLC/ TSC but is not to be taken less than 0.5


2.2 Vertical still water bending moment
2.2.1 Still water bending moment in seagoing condition
As guidance values, at a preliminary design stage, the still water bending moments, in kNm, for hogging and
sagging respectively , in seagoing condition may be taken as:



    # 2.3 Still water torsion moment for container ships
    def min_swbm_for_sagging(self, Lx)

        fsw = distribution_factor_fsw(self, Lx)
        Cw = self.WaveCoefficient()
        
        # n = maximum number of 20 ft containers (TEU)
        # G = maximum mass in tonnes of each TEU the ship can carry        
        CC = n*G
        Mswt-min = 20*self.B*sqrt(CC)

        return Mswt-min
        
#    def swtm_for_containerships


#   [ExcelFunction(Description = "Distribution factor for vertical wave bending moment", Category = "Longitudinal Strength")]
    def distribution_factor_kwm(self, Lx):
        Xp = Lx / self.Ls

        if Xp >= 0 and Xp < 0.4:
            kwm = 2.5 * Lx
        elif Xp >= 0.4 and Xp < 0.65:
            kwm = 1.0
        elif Xp >= 0.65 and Xp < 1.0:
            kwm = -2.85714 * Lx + 2.85714
 
        return kwm



    def Msh(self):
        Cw = self.WaveCoefficient()
        Msh = Cw*pow(self.Ls,2) *self.B * (0.1225-0.015*self.Cb)
        return Msh

    def Mwh(self, Lx):
        Cw = self.WaveCoefficient()
        Mwh = 0.19 * kwm(Lx) * Cw * pow(self.Ls,2) * self.B * self.Cb
        return Mwh

    def Mws(self, Lx):
        Cw = self.WaveCoefficient()
        Mws = -0.11 * kwm(Lx) * Cw * pow(self.L,2) * self.B * (self.Cb + 0.7)
        return Mws

    def Mh(self, Lx):
        Mh = 0.22 * pow(L,9./4.) * (T * 0.3 * B) * Cb * (1 - cos(2 * pi * x / L))
        return Mh

    def Qw(self, Lx):
        Cw = self.WaveCoefficient()
        if sign == "+" :
            kq = kqp(Lx)
        elif sign == "-":
            kq = kqn(Lx)

        Qw = 0.3 * kq * Cw * L * B * (Cb + 0.7)
        return Qw

    def Zmin(self):
        Cw = self.WaveCoefficient()
        Zmin = Cw*pow(self.Ls,2)*(self.Cb+0.7)
        return Zmin


sm = bvShip(216.25, 32.24, 20.65, 14.3, 0.87, 15.8)
print(sm.Ls)
print(sm.WaveCoefficient())
print(sm.distribution_factor_fsw(100.))
sp = statix_p
print(sp.sta_pre())
print(sp.mro)
"""
