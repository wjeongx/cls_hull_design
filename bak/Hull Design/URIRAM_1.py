from math import *
from string import *
import sys
import Polar_IACS
import IACS_URS

Ice = Polar_IACS
urs = IACS_URS

def run():
    fname = sys.argv[1]
    f = open(fname,'r')
    for i in range(16):
        Content, Value = split(f.readline(),"=")
        if strip(upper(Content)) == 'LS':
            Ls = float(Value)
        elif strip(upper(Content)) == 'B':
            B = float(Value)
        elif strip(upper(Content)) == 'D':
            D = float(Value)
        elif strip(upper(Content)) == 'T':
            T = float(Value)
        elif strip(upper(Content)) == 'CB':
            Cb = float(Value)
        elif strip(upper(Content)) == 'V':
            V = float(Value)
        elif strip(upper(Content)) == 'DELTA':
            Delta = float(Value)
        elif strip(upper(Content)) == 'SWBMH':
            SWBMH = float(Value)
        elif strip(upper(Content)) == 'SWBMS':            
            SWBMS = float(Value)
        elif strip(upper(Content)) == 'BOWTYPE':
            BowType = Value
        elif strip(upper(Content)) == 'LB':
            Lb = float(Value)
        elif strip(upper(Content)) == 'EB':
            eb = float(Value)
        elif strip(upper(Content)) == 'ALPHA':
            alpha = float(Value)
        elif strip(upper(Content)) == 'PSI':
            psi = float(Value)
        elif strip(upper(Content)) == 'AWP':
            Awp = float(Value)
        elif strip(upper(Content)) == 'POLARCODE':
            PolarCode = int(Value)

    f.close


    name_ext = split(fname,'.')
    name = name_ext[0]
    ext = name_ext[1]

    fname_out = name + '.lst'
    
    fout = open(fname_out, 'w')

    Discription = Ice.Polar_Discription(PolarCode)
    fout.write(Discription + '\n')
    fout.write('등급계수(Class Factor)\n')
    fout.write('%10s%10s%10s%10s%10s \n' % ('CFC','CFF','CFD','CFDIS','CFL'))
    CF_Val = Ice.CF(PolarCode)
    fout.write('%10.3f%10.3f%10.3f%10.3f%10.3f\n' % (CF_Val[0],CF_Val[1],CF_Val[2],CF_Val[3],CF_Val[4]))
    fout.write('\n')

    F1, F2, Fmin =Ice.ramming_force(PolarCode, B, Delta, BowType, Lb, eb, alpha, psi, Awp)
    fout.write('%10.3f%10.3f%10.3f\n' % (F1, F2, Fmin))

    x =[]; hgsfp = [0]*21; hgsfm =[0]*21; hgbm =[0]*21
    for i in range(21):
        x.append(float(i)/20.)
        hgsfp[i], hgsfm[i] = Ice.ice_shear_force(x[i], Fmin)
        hgbm[i] = Ice.ice_bending_modment(Ls, x[i], 33, Fmin)
        fout.write('%3d%10.3f%10.3f%10.3f%10.3f\n' % (i, round(x[i],3), round(hgsfp[i],3), round(hgsfm[i],3), round(hgbm[i],3)))

    fout.write('\n')
    
    for i in range(21):
        fout.write('%3d%10.3f%10.3f\n' % (i, x[i], round(hgbm[i])+round(SWBMH/1000,3)))

    fout.close

run()

# swbm_sag = urs.Mss(L, B, Cb)
# swbm_hog = urs.Msh(L, B, Cb)

# print round(swbm_sag,1)
# print round(swbm_hog,1)




    
    
    
