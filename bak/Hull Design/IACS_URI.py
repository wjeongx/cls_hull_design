from math import *
from Numeric import *

def mround( x,base):
    return round(x/base)*base

def linear_interpolation(a, b, c, x, z):
    return x - (a - b) * (x - z) / (a - c)

def Polar_Discription(Polar_Code):
    PCK=['']*8
    PCK[1]='PC1-모든 극지해역에서의 년중 운항'
    PCK[2]='PC2-중간정도의 다년생 빙 조건에서의 년중 운항'
    PCK[3]='PC3-다년생 빙의 개재(inclusions)가 포함될 수도 있는 2년생 빙 조건에서의 년중 운항'
    PCK[4]='PC4-오래된 빙의 개재가 포함될 수도 있는 두꺼운 1년생 빙 조건에서의 연중 운항'
    PCK[5]='PC5-오래된 빙의 개재가 포함될 수도 있는 중간정도 두께의 1년생 빙 조건에서의 연중 운항'
    PCK[6]='PC6-오래된 빙의 개재가 포함될 수도 있는 중간정도 두께의 1년생 빙 조건에서의 하기/추기 운항'
    PCK[7]='PC7-오래된 빙의 개재가 포함될 수도 있는 얇은 두께의 1년생 빙 조건에서의 하기/추기 운항'

    return PCK[Polar_Code]
    
def CF( Polar_Code):
    if Polar_Code == 1:
        CFC,CFF,CFD,CFDIS,CFL = 17.69,68.6,2.01,250,7.46
    elif Polar_Code == 2:
        CFC,CFF,CFD,CFDIS,CFL = 9.89,46.8,1.75,210,5.46
    elif Polar_Code == 3:
        CFC,CFF,CFD,CFDIS,CFL = 6.06,21.17,1.53,180,4.17
    elif Polar_Code == 4:
        CFC,CFF,CFD,CFDIS,CFL = 4.5,13.48,1.42,130,3.15
    elif Polar_Code == 5:
        CFC,CFF,CFD,CFDIS,CFL = 3.1,9,1.31,70,2.5
    elif Polar_Code == 6:
        CFC,CFF,CFD,CFDIS,CFL = 2.4,5.49,1.17,40,2.37
    elif Polar_Code == 7:
        CFC,CFF,CFD,CFDIS,CFL = 1.8,4.06,1.11,22,1.81

    return CFC,CFF,CFD,CFDIS,CFL

# IACS - 선수지역 하중특성을 위한 형상계수(fai)
def fa( Polar_Code, Length, Delta, x,alpha,beta):
    CFC,CFF,CFD,CFDIS,CFL = CF(Polar_Code)
    disp = max(Delta / 1000, 5)
    fai_1= (0.097 - 0.68 * (x / Length - 0.15)**2) * alpha / sqrt(beta)
    fai_2 = 1.2 * CFF / (sin(radians(beta))* CFC * pow(disp,0.64))
    fai_3 = 0.6
    fai = min(fai_1, fai_2, fai_3)

    return round(fai,3)
                          
# 힘(FORCE) - F
def Bow_Force(Polar_Code,Length, Delta,x,alpha,beta):
    CFC,CFF,CFD,CFDIS,CFL = CF(Polar_Code)
    fai = fa(Polar_Code, Length, Delta,x, alpha, beta)
    disp = max(Delta / 1000., 5)

    return round(fai * CFC * pow(disp,0.64),3)

def NonBow_Force(Polar_Code, Depth, Delta):
    CFC,CFF,CFD,CFDIS,CFL = CF(Polar_Code)
    disp = max(Delta / 1000, 10)
    if disp <= CFDIS:
        DF = pow(disp,0.64)
    else:
        DF = pow(CFDIS, 0.64) + 0.1 * (Depth - CFDIS)
                
    return round(0.36 * CFC * DF,3)

# 하중작용부분 종횡비(AR)                  
def Aspect_Ratio(beta):
    return round(7.46 * sin(radians(beta)),3)

#선하중(Line Load : Q)
def Line_Load(Polar_Code, hull_area, Force, beta):
    CFC,CFF,CFD,CFDIS,CFL = CF(Polar_Code)
    AR = Aspect_Ratio(beta)
    if hull_area == "Bow":
        return round(pow(Force,0.61) * CFD / pow(AR,0.35),3)
    else:
        return round(0.639 * pow(Force,0.61) * CFD,3)
    
#압력(Pressure :  P)                      
def Pressure(Polar_Code, force, beta):
    CFC,CFF,CFD,CFDIS,CFL = CF(Polar_Code)
    AR = Aspect_Ratio(beta)
    return round(pow(force,0.22) * pow(CFD,2) * pow(AR,0.3),3)

# 설계하중 작용부                               
def Load_Area(area_code, force, lload, press):
    if area_code == 'B':
        w = force/lload
        b = lload/press
    else:
        w = force/lload
        b = w/3.6

    return round(w,3), round(b,3)

def Bow_Load( Polar_Code, Length, Delta, x, alpha, beta):
    Fbow=[]; Qbow=[]; Pbow=[]
    print '각 위치(x)에서 계산된 압력'
    for i in range(0, len(x)):
        Fbow.append(Bow_Force(Polar_Code, Length, Delta, x[i],alpha[i],beta[i]))
        Aspect_Ratio(beta[i])
        Qbow.append(Line_Load(Polar_Code, "Bow", Fbow[i], beta[i]))
        Pbow.append(Pressure(Polar_Code, Fbow[i], beta[i]))
#        print x[i], Fbow[i], Qbow[i], Pbow[i]

    return max(Fbow), max(Qbow), max(Pbow)

def Bow_Load_Area(polar_code, Ls, Delta, x, alpha, beta):
    # 선수지역에 작용하는 하중
    print '\n 선수지역에 작용하는 하중(힘, 선하중, 압력, 평균압력)'
    Fbow, Qbow, Pbow = Bow_Load(polar_code, Ls, Delta, x, alpha, beta)
    wbow,bbow = Load_Area('B', Fbow, Qbow, Pbow)
    Pb = Fbow/(bbow*wbow)
    print Fbow, Qbow, Pbow, round(Pb,3)

    return wbow, bbow, Pb

def NonBow_Load_Area(polar_code, D, Delta):
    #선수지역 이외의 선체지역에 작용하는 하중
    print '\n 선수지역 이외의 선체지역에 작용하는 하중 (힘, 선하중, 압력)'

    Fnbow =NonBow_Force(polar_code, D, Delta)
    Qnbow = Line_Load(polar_code, "NonBow", Fnbow, 0)
    wnbow,bnbow = Load_Area('Mi', Fnbow, Qnbow, 0)
    Pnb = Fnbow/(bnbow*wnbow)
    print Fnbow, Qnbow, round(Pnb,3)

    return wnbow, bnbow, Pnb

def Load_Area_Pavg(polar_code, area_code, Ls, D, Delta, x, alpha, beta):
    # 각 지역별 설계하중 작용부분 폭과 높이 및 평균압력
    
    wbow, bbow, Pb = Bow_Load_Area(polar_code, Ls, Delta, x, alpha, beta)
    wnbow, bnbow, Pnb = NonBow_Load_Area(polar_code, D, Delta)

    print '\n 각 지역별 설계하중 작용부분 폭과 높이 및 평균압력'
    Pavg=[]; b=[]; w=[]
    for i in range(0, len(area_code)):
        if area_code[i] == 'B':
            Pavg.append(Pb); b.append(bbow); w.append(wbow)
        else:
            Pavg.append(Pnb); b.append(bnbow); w.append(wnbow)

        Pavg[i] = round(Pavg[i],3)
        print area_code[i], area_list(area_code[i]),w[i], b[i], Pavg[i]

    return w, b, Pavg

def PPFp( stiff_system, S):

    if stiff_system == "TRANS" or stiff_system == 'trans':
        PPF = max((1.8 - S), 1.2)
    elif stiff_system == "LONG" or stiff_system == 'long':
        PPF = max((2.2 - 1.2 * S), 1.5)

    return PPF

def PPFm( load_carried_stringer, s):
    if load_carried_stringer == 'yes' or load_carried_stringer == 'YES':
        PPF = max((1.6 - s),1.0)
    elif load_carried_stringer == 'no' or load_carried_stringer == 'NO':
        PPF = max((1.8 - s),1.2)

    return PPF

def PPFs( Sw, w):
    if Sw >= 0.5 * w :
        PPF = 1.0
    elif Sw < 0.5 * w :
        PPF = max(1.96 - 1.92 * Sw / w, 1.0)

    return PPF

def PPFw( Sw, w):
    if Sw >= 2 * Sw :
        PPF = PPFs(Sw, w)
    elif Sw < 2 * Sw :
        PPF = max(PPFs(Sw,w)*w / (2 * Sw), 1.0)

    return PPF

def area_list(area_code):
    area_code_dic = {'B':'선수부-선수전체',
                     'BIi':'선수중간-빙벨트구역','BIl':'선수중간-하부구역','BIb':'선수중간-선저구역',
                     'Mi':'중앙부-빙벨트구역','Ml':'중앙부-하부구역','Mb':'중앙부-선저구역',
		     'Si':'선미부-빙벨트구역','Sl':'선미부-하부구역','Sb':'선미부-선저구역'}

    return area_code_dic[area_code]

def area_factor( Polar_Code, area_code):
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

    return PC[Polar_Code-1]

def plt_thk( Polar_Code, area_code, stiff_system, Pavg, sy, s, a, b):

    PPF = PPFp(stiff_system, s)
    AF = area_factor(Polar_Code, area_code)
    
    if stiff_system == 'trans':
        tnet = 500 * s * ((AF * PPF * Pavg) / sy)**0.5 / (1 + s / (2 * b))

    elif stiff_system == 'long':
        if b >= S:
            tnet = 500 * s * ((AF * PPF * Pavg) / sy)**0.5 / (1 + s / (2 * a))
        elif b < S:
            tnet = 500 * s * ((AF * PPF * Pavg) / sy)**0.5 * (2 * b / s - (b / s)**2)**5 / (1 + s / (2 * a))
    return round(tnet,3)

def stiff_dim(stiff_size):
    stiff, att_plt = stiff_size.split(',')
    sbeff, stp = att_plt.split('x')
    beff = float(sbeff)/10; tnet = float(stp)/10

    if stiff.find('/') != -1:
        shw, sbf, thk = stiff.split('x')
        hw = float(shw)/10; bf = float(sbf)/10
        stw, stf = thk.split('/')
        tw = float(stw)/10; tf = float(stf)/10
        hw = hw - tf
        
    elif stiff.find('+') != -1:
        web, flng = stiff.split('+')
        shw, stw = web.split('x')
        sbf, stf = flng.split('x')
        hw = float(shw)/10; bf=float(sbf)/10; tw = float(stw)/10; tf=float(stf)/10
        
    return hw, tw, bf, tf, beff, tnet

def actual_Zp2(stiff_size):

    hw, tw, bf, tf, beff, tnet = stiff_dim(stiff_size)
    
    Af = bf * tf
    Aw = hw * tw
    Ap = tnet * beff

    if Ap >= Af + Aw:
        ka1 = 1
    else:
        ka1 = 1 - (1 - (Ap - Af) / Aw)**2 / (2 * (1 + 2 * Af / Aw))

    return (Af * (hw + (tf + tnet) / 2) + Aw * (hw + tnet) / 2) * ka1

def actual_Zp(stiff_size):

    wh, wt, fh, ft, ah, at = stiff_dim(stiff_size)

    fa = fh*ft
    wa = wh*wt
    aa = ah*at
    
    half_area = (fa+wa+aa)/2

    if half_area > wa+fa:
        atp_area = (half_area - (wa+fa))
        atp_h = atp_area/ah
        zp = fa*(ft/2+wh+atp_h) + wa*(wh/2+atp_h)+(ah*atp_h)*atp_h/2 + ah*(at-atp_h)*(at-atp_h)/2
    else:
        web_h = (half_area-fa)/wt
        zp = fa*(ft/2+web_h)+(web_h*wt)*web_h/2 + (wh-web_h)*wt*(wh-web_h)/2+aa*(wh-web_h+at/2)

    return zp

def actual_Ze(stiff_size):

    wh, wt, fw, ft, aw, at = stiff_dim(stiff_size)

    wa=wt*wh
    wx = 0.
    wy = wh/2
    wax = wa*wx
    way = wa*wy
    wax2 = wa*wx**2
    way2 = wa*wy**2
    wixx = wt*wh**3/12
    wiyy = wh*wt**3/12
	
	# flange property
	
    fa = fw * ft
    fx = 0.0
    fy = wh+ft/2

    fax = fa*fx
    fay = fa*fy
    fax2 = fa*fx**2
    fay2 = fa*fy**2
    fixx = fw*ft**3/12
    fiyy = ft*fw**3/12

    # atached plate porperty

    aa = aw * at
    ax = 0.0
    ay = -at/2

    aax = aa*ax
    aay = aa*ay
    aax2 = aa*ax**2
    aay2 = aa*ay**2
    aixx = aw*at**3/12
    aiyy = at*aw**3/12


    # sum
    suma = wa + fa + aa
    sumax = wax + fax + aax 
    sumay = way + fay + aay
    sumax2 = wax2 + fax2 + aax2
    sumay2 = way2 + fay2 + aay2
    sumixx = wixx + fixx + aixx
    sumiyy = wiyy + fiyy + aiyy

    area = suma
    nx = sumax / suma
    ny = sumay / suma

    ixx = sumay2 + sumixx - ny * sumay
    iyy = sumax2 + sumiyy - nx * sumax

    return 	ixx/(wh+ft-ny)
	
	
def SA_act(stiff_size):
    hw, tw, bf, tf, beff, tnet = stiff_dim(stiff_size)

    return (hw+tf)*tw
    
def A_factor( stiff_system, stiff_size, Amin, a, b):

    hw, tw, bf, tf, beff, tnet = stiff_dim(stiff_size)
        
    Afit = hw * tw 
    Af = bf * tf 
    kw = 1 / (1 + 2 * Af / Afit)
    shear_area_ratio = Amin/Afit
    if shear_area_ratio == 0:
        return 0
    zp = bf*tf**2/4 + beff*tnet**2/4
    Zp = actual_Zp(stiff_size)
    kz = zp / Zp
    LL = min(a, b)

    if shear_area_ratio > 1:
        print "Shear Area를 만족하지 못합니다. 먼저 shear area를 만족시키기 바랍니다. \n"
        return 0, 0, 0, 0, 0, 0, 0, 0
        
    if stiff_system == "TRANS" or stiff_system == "trans":
        #print '알림 : 단순지지가 없다고 가정한다.(j = 2)'
        j = 2
        Y = 1 - 0.5 * (LL / a)
        a1 = shear_area_ratio
        A1A = 1 / (1 + j / 2 + kw * j / 2 * ((1 - a1**2)**0.5 - 1))
        A1B = (1 - 1 / (2 * a1 * Y)) / (0.275 + 1.44 * kz**0.7)
        result = max(A1A, A1B)
        print 'LL=',LL,'Y=',Y,'a=',a,'a1=',a1,'kz=',kz,'A1A =', round(A1A,3), 'A1B=',round(A1B,3), 'Max(A1A,A1B)',round(result,3)
    elif stiff_system == "LONG" or stiff_system == "long":
        a4 = shear_area_ratio
        result = 1 / (2 + kw * ((1 - a4**2)**0.5 - 1))

    return round(Afit,3), round(Af,3), round(kw,3), round(zp,3), round(Zp,3), round(kz,3), round(shear_area_ratio,3), round(result,3)

def b1_factor( b, s):
    bf = b / s
    k0 = 1 - 0.3 / bf
                        
    if bf < 2:
        b2 = b * (1 - 0.25 * bf)
    elif bf >= 2:
        b2 = s
                      
    return k0 * b2


def shear_area( Polar_Code, area_code, stiff_system, sy, PPF, s, a, b, c, Pavg):

    LL = min(a, b)
    AF = area_factor(Polar_Code, area_code)

    if stiff_system == "trans" or stiff_system == "TRANS":
        SA = 100**2 * 0.5 * LL * s * (AF * PPF * Pavg) / (0.577 * sy)

    elif stiff_system == "long" or stiff_system == "LONG":
        b1 = b1_factor(b, s)

        SA = 100**2 * 0.5 * b1 * c * LL * AF * PPF * Pavg / (0.577 * sy)

    return round(SA,1)

def plastic_sec_modulus( Polar_Code, area_code, stiff_system, sy, s, a, b, c, PPF, Pavg, A14, theta):
    if theta <= 15:
        KA = 1.0
    else:
        KA = 1 /cos(radians(theta))

    AF = area_factor(Polar_Code, area_code)
    LL = min(a , b)

    if stiff_system == "TRANS" or stiff_system == "trans":
        Y = 1 - 0.5 * (LL / a) 
        Zp = 100**3 * LL * Y * s * (AF * PPF * Pavg) * a * A14 * KA / (4 * sy)
                
    elif stiff_system == "LONG" or stiff_system == "long":
        b1 = b1_factor(b, s)
        Zp = 100**3 * b1 * c * LL * A14 * KA * (AF * PPF * Pavg) / (4 * sy)

    return round(Zp,1)

def ramming_force(Polar_Code, Breadth, Delta, bow_type, Lb, eb, alpha_s, psi_s, psi, Awp):
    CFC,CFF,CFD,CFDIS,CFL = CF(Polar_Code)
    C = 1/(2*(Lb/Breadth)**eb)
    Disp = max(Delta/1000, 10)

    if bow_type == 'spoon':
        Kf = (2 * C * Breadth**(1-eb) / (1+eb))**0.9 * tan(radinas(psi_s))**(-0.9 * (1 + eb))
    elif bow_type == 'wedge':
        Kf = (tan(radians(alpha_s)) / tan(radians(psi_s))**2)**0.9
              
    Kh = 0.01*Awp
    Ki = Kf/Kh
    F1 = 0.534*Ki**0.15*sin(radians(psi))**0.2 * (Disp * Kh)**0.5 * CFL
    F2 = 1.2*CFF
    print round(Kh,3), round(Kf,3), round(Ki,3),round(F1,3), round(F2,3)
    return min(F1, F2)

def ice_shear_force(x, Fram):
    if 0 <= x <= 0.6:
        Cfp = 0
    elif 0.6 < x < 0.9:
        Cfp = linear_interpolation(0.6, x, 0.9, 0.0, 1.0)
    elif 0.9 <= x <=1:
        Cfp = 1

    if x == 0:
        Cfm = 0
    elif 0 < x < 0.2:
        Cfm = linear_interpolation(0.0, x, 0.2, 0.0, -0.5)
    elif 0.2 <= x <= 0.6:
        Cfm = -0.5
    elif 0.6 < x < 0.8:
        Cfm = linear_interpolation(0.6, x, 0.8, -0.5, 0)
    elif 0.8 <= x <= 1:
        Cfm = 0
        
    Fip = Cfp*Fram
    Fim = Cfm*Fram

    return Fip, Fim

def ice_bending_modment(Length, x, psi, Fram):

    if x == 0:
        Cm = 0
    elif 0 < x < 0.5:
        Cm = linear_interpolation(0.0, x, 0.5, 0.0, 1.0)
    elif 0.5 <= x <= 0.7:
        Cm = 1
    elif 0.7 < x <= 0.95:
        Cm = linear_interpolation(0.7, x, 0.95, 1.0, 0.3)
    elif 0.95 < x <= 1.0:
        Cm = linear_interpolation(0.95, x, 1.0, 0.3, 0.0)
        
    Mi = 0.1*Cm*Length*sin(radians(psi))**(-0.2)*Fram
    
    return Mi



























