from math import *
from Numeric import *

class IACS_URI_Polar_Ship:
    Ls,B,D,T,Cb,V,Delta = 0,0,0,0,0,0,0
    def Polar_Discription(self,pc_code):
        PCK=['']*8
        PCK[1]='PC1-모든 극지해역에서의 년중 운항'
        PCK[2]='PC2-중간정도의 다년생 빙 조건에서의 년중 운항'
        PCK[3]='PC3-다년생 빙의 개재(inclusions)가 포함될 수도 있는 2년생 빙 조건에서의 년중 운항'
        PCK[4]='PC4-오래된 빙의 개재가 포함될 수도 있는 두꺼운 1년생 빙 조건에서의 연중 운항'
        PCK[5]='PC5-오래된 빙의 개재가 포함될 수도 있는 중간정도 두께의 1년생 빙 조건에서의 연중 운항'
        PCK[6]='PC6-오래된 빙의 개재가 포함될 수도 있는 중간정도 두께의 1년생 빙 조건에서의 하기/추기 운항'
        PCK[7]='PC7-오래된 빙의 개재가 포함될 수도 있는 얇은 두께의 1년생 빙 조건에서의 하기/추기 운항'
        return PCK[pc_code]
    
    def CF(self, pc_code):
        if pc_code == 1:
            CFC,CFF,CFD,CFDIS,CFL = 17.69,68.6,2.01,250,7.46
        elif pc_code == 2:
            CFC,CFF,CFD,CFDIS,CFL = 9.89,46.8,1.75,210,5.46
        elif pc_code == 3:
            CFC,CFF,CFD,CFDIS,CFL = 6.06,21.17,1.53,180,4.17
        elif pc_code == 4:
            CFC,CFF,CFD,CFDIS,CFL = 4.5,13.48,1.42,130,3.15
        elif pc_code == 5:
            CFC,CFF,CFD,CFDIS,CFL = 3.1,9,1.31,70,2.5
        elif pc_code == 6:
            CFC,CFF,CFD,CFDIS,CFL = 2.4,5.49,1.17,40,2.37
        elif pc_code == 7:
            CFC,CFF,CFD,CFDIS,CFL = 1.8,4.06,1.11,22,1.81

        return CFC,CFF,CFD,CFDIS,CFL

    # IACS - 선수지역 하중특성을 위한 형상계수(fai)
    def fa(self, pc_code, x,alpha,beta):
        CFC,CFF,CFD,CFDIS,CFL = self.CF(pc_code)
        disp = max(self.Delta / 1000, 5)
        fai_1= (0.097 - 0.68 * (x / self.Ls - 0.15)**2) * alpha / sqrt(beta)
        fai_2 = 1.2 * CFF / (sin(radians(beta))* CFC * pow(disp,0.64))
        fai_3 = 0.6
        fai = min(fai_1, fai_2, fai_3)

        return round(fai,3)
                              
    # 힘(FORCE) - F
    def Bow_Force(self,pc_code,x,alpha,beta):
        CFC,CFF,CFD,CFDIS,CFL = self.CF(pc_code)
        fai = self.fa(pc_code, x, alpha, beta)
        disp = max(self.Delta / 1000., 5)

        return round(fai * CFC * pow(disp,0.64),3)
    
    def NonBow_Force(self, pc_code):
        CFC,CFF,CFD,CFDIS,CFL = self.CF(pc_code)
        disp = max(self.Delta / 1000, 10)
        if disp <= CFDIS:
            DF = pow(disp,0.64)
        else:
            DF = pow(CFDIS, 0.64) + 0.1 * (self.D - CFDIS)
                    
        return round(0.36 * CFC * DF,3)

    # 하중작용부분 종횡비(AR)                  
    def Aspect_Ratio(self,beta):
        return round(7.46 * sin(radians(beta)),3)

   # 선하중(Line Load : Q)
    def LineLoad(self,pc_code, hull_area, Force, beta):
        CFC,CFF,CFD,CFDIS,CFL = self.CF(pc_code)
        AR = self.Aspect_Ratio(beta)
        if hull_area == "Bow":
            return round(pow(Force,0.61) * CFD / pow(AR,0.35),3)
        else:
            return round(0.639 * pow(Force,0.61) * CFD,3)
    #압력(Pressure :  P)                      
    def Pressure(self,pc_code, force, beta):
        CFC,CFF,CFD,CFDIS,CFL = self.CF(pc_code)
        AR = self.Aspect_Ratio(beta)
        return round(pow(force,0.22) * pow(CFD,2) * pow(AR,0.3),3)

    # 설계하중 작용부                               
    def App_Area(self,hull_area, force, lload, press):
        if hull_area == "Bow":
            w = force/lload
            b = lload/press
        else:
            w = force/lload
            b = w/3.6

        return round(w,3), round(b,3)

    def bow_load(self, pc_code, x, alpha, beta):
        Fbow=[]; Qbow=[]; Pbow=[]
        for i in range(0, len(x)):
            Fbow.append(self.Bow_Force(pc_code, x[i],alpha[i],beta[i]))
            Ice.Aspect_Ratio(beta[i])
            Qbow.append(self.LineLoad(pc_code, "Bow", Fbow[i], beta[i]))
            Pbow.append(self.Pressure(pc_code, Fbow[i], beta[i]))

        return max(Fbow), max(Qbow), max(Pbow)

    def PPFp(self, stiff_system, S):

        if stiff_system == "TRANS" or stiff_system == 'trans':
            PPF = max((1.8 - S), 1.2)
        elif stiff_system == "LONG" or stiff_system == 'long':
            PPF = max((2.2 - 1.2 * S), 1.5)

        return PPF

    def PPFm(self, load_carried_stringer, s):
        if load_carried_stringer == 'yes' or load_carried_stringer == 'YES':
            PPF = max((1.6 - s),1.0)
        elif load_carried_stringer == 'no' or load_carried_stringer == 'NO':
            PPF = max((1.8 - s),1.2)

        return PPF

    def PPFs(self, Sw, w):
	if Sw >= 0.5 * w :
            PPF = 1.0
	elif Sw < 0.5 * w :
            PPF = max(1.96 - 1.92 * Sw / w, 1.0)

        return PPF

    def PPFw(self, Sw, w):
        if Sw >= 2 * Sw :
            PPF = PPFs(Sw, w)
        elif Sw < 2 * Sw :
            PPF = max(PPFs(Sw,w)*w / (2 * Sw), 1.0)

        return PPF
    
    def area_factor(self, pc_code, area_code):
        if area_code == 'B':
            PC=[1.00,   1.00,   1.00,   1.00,   1.00,   1.00,   1.00]
        elif area_code == 'BIi':
            PC=[0.90, 	0.85, 	0.85, 	0.80, 	0.80, 	1.00,	1.00]
        elif area_code == 'BIl':
            PC=[0.70, 	0.65,	0.65, 	0.60, 	0.55, 	0.55, 	0.50]
        elif area_code=='BIb':
            PC=[0.55, 	0.50, 	0.45, 	0.40, 	0.35, 	0.30, 	0.25]
        elif area_code=='Mi':
            PC=[0.70, 	0.65, 	0.55, 	0.55, 	0.50, 	0.45, 	0.45]
        elif area_code=='Ml':
            PC=[0.50, 	0.45,	0.40, 	0.35, 	0.30, 	0.25, 	0.25]
        elif area_code=='Mb':
            PC=[0.30, 	0.30, 	0.25, 	0.00,	0.00,	0.00,	0.00]
        elif area_code=='Si':
            PC=[0.75, 	0.70, 	0.65, 	0.60, 	0.50, 	0.40, 	0.35] 
        elif area_code=='Sl':
            PC=[0.45, 	0.40, 	0.35, 	0.30, 	0.25, 	0.25, 	0.25] 
        elif area_code=='Sb':
            PC=[0.35, 	0.30, 	0.30, 	0.25, 	0.15, 	0.00,	0.00]

        return PC[pc_code-1]

    def plt_thk(self, pc_code, area_code, stiff_system, Pavg, sy, s, a, b):

        PPF = self.PPFp(stiff_system, s)
        AF = self.area_factor(pc_code, area_code)
        
        if stiff_system == 'trans':
            tnet = 500 * s * ((AF * PPF * Pavg) / sy)**0.5 / (1 + s / (2 * b))

        elif stiff_system == 'long':
            if b >= S:
                tnet = 500 * s * ((AF * PPF * Pavg) / sy)**0.5 / (1 + s / (2 * a))
            elif b < S:
                tnet = 500 * s * ((AF * PPF * Pavg) / sy)**0.5 * (2 * b / s - (b / s)**2)**5 / (1 + s / (2 * a))
        return round(tnet,3)

    def actual_Zp(self, hw, tw, bf, tf, beff, tnet):

        AF = bf * tf
        Aw = hw * tw
        Ap = tnet * beff

        if Ap >= AF + Aw:
            ka1 = 1
        else:
            ka1 = 1 - (1 - (Ap - AF) / Aw)**2 / (2 * (1 + 2 * AF / Aw))

        return (AF * (hw + (tf + tnet) / 2) + Aw * (hw + tnet) / 2) * ka1

    def A_factor(self, stiff_system, stiff_size, Amin, a, b):

        stiff, att_plt = stiff_size.split(',')
        sbeff, stp = att_plt.split('x')
        beff = float(sbeff)/10; tnet = float(stp)/10
        
        if stiff.find('/') != 0:
            shw, sbf, thk = stiff.split('x')
            hw = float(shw)/10; bf = float(sbf)/10
            stw, stf = thk.split('/')
            tw = float(stw)/10; tf = float(stf)/10
            
        elif stiff.find('+') != 0:
            web, flng = stiff.split('+')
            shw, stw = web.split('x')
            sbf, stf = flng.split('x')
            hw = float(shw)/10; bf=float(sbf)/10; tw = float(stw)/10; tf=float(stf)/10
            
        Afit = hw * tw 
        Af = bf * tf 
        kw = 1 / (1 + 2 * Af / Afit)
        shear_area_ratio = Amin/Afit
        if shear_area_ratio == 0:
            return 0
        zp = bf*tf**2/4 + beff*tnet**2/4
        Zp = self.actual_Zp(hw,tw,bf,tf,beff,tnet)
        kz = zp / Zp
        LL = min(a, b)
        if stiff_system == "TRANS" or stiff_system == "trans":
            #print '알림 : 단순지지가 없다고 가정한다.(j = 2)'
            j = 2
            Y = 1 - 0.5 * (LL / a)
            a1 = shear_area_ratio
            A1A = 1 / (1 + j / 2 + kw * j / 2 * ((1 - a1**2)**0.5 - 1))
            A1B = (1 - 1 / (2 * a1 * Y)) / (0.275 + 1.44 * kz**0.7)
            result = max(A1A, A1B)
            print round(A1A,3), round(A1B,3), round(result,3)
        elif stiff_system == "LONG" or stiff_system == "long":
            a4 = shear_area_ratio
            result = 1 / (2 + kw * ((1 - a4**2)**0.5 - 1))

        return result

    def b1_factor(self, b, s):
        bf = b / s
        k0 = 1 - 0.3 / bf
                            
        if bf < 2:
            b2 = b * (1 - 0.25 * bf)
        elif bf >= 2:
            b2 = s
                          
        return k0 * b2

    
    def shear_area(self, pc_code, area_code, stiff_system, sy, PPF, s, a, b, c, Pavg):

        LL = min(a, b)
        AF = self.area_factor(pc_code, area_code)

        if stiff_system == "trans" or stiff_system == "TRANS":
            SA = 100**2 * 0.5 * LL * s * (AF * PPF * Pavg) / (0.577 * sy)

        elif stiff_system == "long" or stiff_system == "LONG":
            b1 = self.b1_factor(b, s)

            SA = 100**2 * 0.5 * b1 * c * LL * AF * PPF * Pavg / (0.577 * sy)

        return round(SA,1)

    def plastic_sec_modulus(self, pc_code, area_code, stiff_system, sy, s, a, b, c, PPF, Pavg, A14, theta):
        if theta <= 15:
            KA = 1.0
        else:
            KA = 1 /cos(radians(theta))

        AF = self.area_factor(pc_code, area_code)
        LL = min(a , b)

        if stiff_system == "TRANS" or stiff_system == "trans":
            Y = 1 - 0.5 * (LL / a) 
            Zp = 100**3 * LL * Y * s * (AF * PPF * Pavg) * a * A14 * KA / (4 * sy)
                    
        elif stiff_system == "LONG" or stiff_system == "long":
            b1 = self.b1_factor(b, s)
            Zp = 100**3 * b1 * c * LL * A14 * KA * (AF * PPF * Pavg) / (4 * sy)

        return round(Zp,1)

    def mround(self, x,base):
        return round(x/base)*base

    # 종강도
    # 선수에서의 설계 수직 빙하중
"""
    def Fram(self,bow_type, eb, alpha_s, psi_s, psi, Awp)
        CFC,CFF,CFD,CFDIS,CFL = self.CF(pc_code)
        C = 1/(2*(Lb/B)**eb)
        Disp = max(self.Delta, 10)
        if bow_type = 'spoon'
            Kf = (2*C*B**(1-eb)/(1+eb))**0.9*tan(psi_s)**((-0.9)*1+eb))
        elif bow_type = 'wedge'
            Kf = (tan(alpha_s)/(tan(psi_s)**2)**0.9
              
        Kh = 0.01*Awp
        Ki = Kf/Kh
        F1 = 0.534*Ki**0.15*sin(psi)**0.2*(Disp*Kh)**0.5**CFL
        F2 = 1.2*CFF
        return mix(F1, F2)
"""    
Ice = IACS_URI_Polar_Ship()

# user input : statr to end
# start =====================================================================================
Ice.Ls = 99.033
Ice.B = 19.000 
Ice.D = 9.900 
Ice.T = 7.220 
Ice.Cb = 0.600 
Ice.V = 12.000 
Ice.Delta = 8320 
polar_code = 4

x = [0.00,4.95,10.99,14.85,19.81]
alpha = [71.2,26.,22.6,16.,10.4]
beta = [53.5,36.1,33.6,30.6,27.7]

area_code = ['B',   'BIi',  'BIl',  'BIb',  'Mi',   'Ml',   'Mb',   'Si',   'Sl',   'Sb']
stiff_sys = ['trans','trans','trans','trans','trans','trans','trans','trans','trans','trans']
span =      [2.4,   2.4,    2.4,    2.4,    2.4,    2.4,    2.4,    2.4,    2.4,    2.4]
space =     [0.6,   0.6,    0.6,    0.6,    0.6,    0.6,    0.6,    0.6,    0.6,    0.6]
Syp =    [355,   355,    355,    315,    315,    315,    235,    315,    315,    315]
Sys =  [355,   355,    355,    315,    315,    315,    235,    315,    315,    315]
ts =        [2.5,   2.5,    2.0,    2.0,    2.0,    2.0,    2.0,    2.0,    2.0,    2.0]
# 하중 분배 스트링거가 있느냐 ? 있으면 YES, 없으면 NO
load_car_str=['yes','yes',  'yes',  'yes',  'yes',  'yes',  'yes',  'yes',  'yes',  'yes']
stiff_size = ['550x100x12/16','350x100x12/17','350x100x12/17','350x100x12/17','350x100x12/17','350x100x12/17','350x100x12/17','350x100x12/17','350x100x12/17','350x100x12/17']
# ============================================================================================ end 

print Ice.Polar_Discription(polar_code)

# 선수지역에 작용하는 하중
print '\n 선수지역에 작용하는 하중(힘, 선하중, 압력, 평균압력)'
Fbow, Qbow, Pbow = Ice.bow_load(polar_code, x, alpha, beta)
wbow,bbow = round(Ice.App_Area("Bow", Fbow, Qbow, Pbow),3)
Pb = Fbow/(bbow*wbow)
print Fbow, Qbow, Pbow, round(Pb,3)
                         
#선수지역 이외의 선체지역에 작용하는 하중
print '\n 선수지역 이외이 선체지역에 작용하는 하중 (힘, 선하중, 압력)'

Fnbow =Ice.NonBow_Force(polar_code)
Qnbow = Ice.LineLoad(polar_code, "NonBow", Fnbow, 0)
wnbow,bnbow = round(Ice.App_Area("NonBow", Fnbow, Qnbow, 0),3)
Pnb = Fnbow/(bnbow*wnbow)
print Fnbow, Qnbow, round(Pnb,3)
# f.write(str(Fnbow) + str(Qnbow) + str(wnbow) + str(bnbow) + str(Pnb) + line_skip)

# 각 지역별 설계하중 작용부분 폭과 높이 및 평균압력
print '\n 각 지역별 설계하중 작용부분 폭과 높이 및 평균압력'
Pavg=[]; b=[]; w=[]
for i in range(0, len(area_code)):
    if area_code[i] == 'B':
        Pavg.append(Pb); b.append(bbow); w.append(wbow)
    else:
        Pavg.append(Pnb); b.append(bnbow); w.append(bnbow)
    
    print area_code[i], w[i], b[i], round(Pavg[i],3)
    
# 각 지역별 판 두께
print '\n 각 지역별 판 요구 두께'
tnet = []; thk = []
for i in range(0, len(area_code)):
    tnet.append(Ice.plt_thk(polar_code, area_code[i], stiff_sys[i],Pavg[i], Syp[i], space[i], span[i], b[i]))
    thk.append(tnet[i]+ts[i])
    print area_code[i], Ice.mround(thk[i],0.5)
#    print area_code[i], stiff_sys[i], Sy[i], round(Pavg[i],3), space[i], span[i], round(thk,1)
#    f.write(str(area_code[i])+str(stiff_sys[i])+str(Sy[i])+str(round(Pavg[i],3))+str(space[i])+str(span[i])+str(round(thk,1))+ " \\\ \n")


# 각 지역별 늑골의 전단면적
print '\n 각 지역별 늑골의 요구 전단면적'
c = 1.0
SA=[]; PPF=[]
for i in range(0, len(area_code)):
    if stiff_sys[i] == 'trans':
        PPF.append(Ice.PPFm(load_car_str[i], space[i]))
    elif stiff_sys[i] == 'long':
        PPF.append(Ice.PPFs(span[i],space[i]))
        
    SA.append(Ice.shear_area(polar_code, area_code[i], stiff_sys[i], Sys[i], PPF[i], space[i], span[i], b[i], c, Pavg[i]))
    print area_code[i], stiff_size[i], str(space[i]*1000)+'x'+str(tnet[i]), Sys[i],space[i],PPF[i],round(SA[i],1)
 
# 각 지역별 늑골의 소성단면 계수
print '\n 각 지역별 늑골의 요구 소성단면 계수'
for i in range(0, len(area_code)):
    stiff = stiff_size[i] + "," + str(space[i]*1000) + 'x' + str(Ice.mround(tnet[i],0.5))
    A14 = Ice.A_factor(stiff_sys[i], stiff, SA[i], span[i], b[i])

    Zpr =Ice.plastic_sec_modulus(polar_code, area_code[i], stiff_sys[i], Sys[i], space[i], span[i], b[i], c, PPF[i], Pavg[i], A14, 0.)
    print area_code[i], stiff, str(space[i]*1000)+'x'+str(tnet[i]), Sys[i],space[i],PPF[i],round(SA[i],1)
    print round(A14,3), round(b[i],3), round(Zpr,1)
        
# 각 Polar Class에 따른 하중 및 판 두께
# f.write('Code '+'Force '+'Line Load '+'Press '+'load w '+'load b '+'plt thk' + line_skip)
print '\n Polar Class에 따른 하중 및 판 요구 두께'
Fb=[]; Qb=[]; Pb=[]; wb=[]; bb=[]
for pc in range(1,8):
    F, Q, P = Ice.bow_load(pc , x, alpha, beta)
    w,b = round(Ice.App_Area("Bow", F, Q, P),3)
    wb.append(w); bb.append(b);
    Fb.append(F); Qb.append(Q); Pb.append(F/(b*w))

    thk = Ice.plt_thk(pc, 'B','trans',Pb[pc-1], Syp[0], space[0], span[0], bb[pc-1])+ts[0]
    
    print 'PC-'+str(pc), Fb[pc-1], Qb[pc-1], round(Pb[pc-1],3), wb[pc-1],bb[pc-1], Ice.mround(thk,0.5)



# 보고서 작성

f = open("kordi-icebreaker.tex", 'w' )

line_skip = ' \\\ \n'

f.write("\\documentclass{scrartcl}\n")
f.write("\\usepackage{hangul}\n")
f.write("\\begin{document}\n")
f.write('1. 주요치수' + line_skip)
f.write('\\begin{tabular}{llllr} \n')
f.write('Length betw. perpendiculars & Lbp & = &' + str(95.000) + ' & M' + line_skip)
f.write('Rule length & L & = &' + str(Ice.Ls) + ' & M' + line_skip)
f.write('Breadth moulded & B & = &' + str(Ice.B) + ' & M' + line_skip)
f.write('Depth moulded & D & = &' + str(Ice.D) + ' & M' + line_skip)
f.write('Draught moulded & T & = &' + str(Ice.T) + ' & M' + line_skip)
f.write('Block coefficient & Cb & = &' + str(Ice.Cb) + ' & ' + line_skip)
f.write('Service Speed & V & = &' + str(Ice.V) + ' & kNot' + line_skip)
f.write('Displacement & $\Delta$ & = &' + str(Ice.Delta) + ' & TON' +line_skip)
f.write('\\end{tabular} \n')
f.write(line_skip)
f.write(line_skip)
f.write('극지등급' + line_skip)
f.write(Ice.Polar_Discription(polar_code) + line_skip)
f.write(line_skip)
f.write(line_skip)
f.write('등급계수'+ line_skip)
CFC,CFF,CFD,CFDIS,CFL = Ice.CF(polar_code)
f.write('\\begin{tabular}{|p{2cm}|p{2.2cm}|p{2.2cm}|p{2.2cm}|p{2.2cm}|p{2.2cm}|} \\hline \n')
f.write('Polar Class &CFC &CFF &CFD &CFDIS &CFL \\\ \\hline \n')
f.write('PC'+ str(polar_code) + ' & ' + str(CFC) + ' & ' + str(CFF) + ' & ' + str(CFD) + ' & ' + str(CFDIS) + ' & ' + str(CFL) + '\\\ \\hline \n')
f.write('\\end{tabular} \n')
f.write(line_skip)
f.write('각 지역별 늑골의 요구 전단면적 및 소성 단면 계수'+line_skip)
f.write('\\begin{tabular}{|p{1cm}|p{1.5cm}|p{3.0cm}|p{1.0cm}|p{1.0cm}|p{1.0cm}|p{1.5cm}|} \\hline \n')
f.write('Area &system &stiff. size &$\sigma$y &S &PPF &Am/Al \\\ \\hline \n')
f.write('\\end{tabular} \n')
f.write(line_skip)
for i in range(0,len(area_code)):
    f.write('\\begin{tabular}{|p{1cm}|p{1.5cm}|p{3.0cm}|p{1.0cm}|p{1.0cm}|p{1.0cm}|p{1.5cm}|} \\hline {|p{1cm}) \\hline \n')
    f.write(area_code[i] + ' & ' + stiff_sys[i] + ' & ' + stiff_size[i] + ' & ' + str(Sys[i]) + ' & ' + str(space[i]) + ' & ' + str(PPF[i])+ ' & ' + str(SA[i]) + ' \\\ \\hline \n')
    f.write('\\end{tabular} \n')
    f.write(line_skip)

f.write(line_skip)
f.write('각 지역별 늑골의 요구 소성 단면 계수'+line_skip)

#f.write('PC-'+str(pc) +str(Fb[pc-1])+str(Qb[pc-1])+str(round(Pb[pc-1],3)) +str(wb[pc-1]) + str(bb[pc-1]) +str(round(thk,1))+line_skip)
    
f.write('\\end{document}')
# cmmd = 'texify ' + 'kordi-icebreaker.tex'
# print cmmd
# os.system(cmmd)
f.close()

"""
    def Polar_Fib1(ystem , KI , D , Kh ) 
        Polar_Fib1 = 0.534 * KI ^ 0.15 * Sin(ystem * 3.1415 / 180) ^ 0.2 * (D * Kh) ^ 0.5 * CFL


    def Polar_Fib2() 
        Polar_Fib2 = 1.2 * CFF

    def Polar_Mi(Cm , ystem , FIB )
        Polar_Mi = 0.1 * Cm * Ls * Sin(ystem * PPI / 180) ^ -0.2 * FIB

"""



