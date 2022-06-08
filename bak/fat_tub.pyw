import os
import wx
import string

if __name__ == "__main__":
    app = wx.PySimpleApp()

    dlg = wx.FileDialog(None, "Choose a file", "","","*.lst",wx.MULTIPLE)

    if dlg.ShowModal() == wx.ID_OK:
        fname = dlg.GetPaths()
    print fname[0]
    dlg.Destroy()

f = open(fname[0],'r')
fi = open('./fat_inplace/pr2_inplace_sac.inp','r')
fmem = open('pr2_inplace_sac.mem','w')
fjnt = open('pr2_inplace_sac.jnt','w')

fo = open('fat_tub.out','w')

kw = []
j1 = []
j2 = []
grp = []
while 1:
    line = fi.readline()
    if not line: break
    if string.find(line,'*') == -1:
        if string.find(line,'MEMBER') != -1:
            kw = line[0:6]
            j1 = line[7:11]
            j2 = line[11:15]
            grp = line[16:19]
            fmem.write('%10s %10s %10s %10s \n' %(kw,j1,j2,grp))
            if string.find(line,'MEMBER1') != -1:
                fi.readline()
        elif string.find(line,'JOINT') != -1:
            kw = line[0:5]
            jn = line[6:10]
            jx = line[10:18]
            jy = line[18:25]
            jz = line[25:32]

            fjnt.write('%10s %10s %10s %10s %10s \n' %(kw, jn, jx, jy, jz))
            
                   
#while 1:
#    line = f.readline()
#    if not line: break
#    data = str.split(line," ")
#    if str.find(data[0],'-') != -1:
#        fo.write(line)

f.close
fo.close
fmem.close
fjnt.close
