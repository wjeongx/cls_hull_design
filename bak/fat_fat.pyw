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
fo = open('fat_summary.out','w')

while 1:
    line = f.readline()
    if not line: break
    data = str.split(line," ")
    if str.find(data[0],'-') != -1:
        fo.write(line)

f.close
fo.close
    
